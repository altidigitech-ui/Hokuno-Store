#!/usr/bin/env bash
# Resumable Printify republish script
# Usage: nohup bash /workspaces/Hokuno-Store/republish.sh &
# Resume: same command — skips IDs already in done_ids.txt

SHOP_ID="22774508"
TOKEN="${PRINTIFY_API_TOKEN:-}"
DIR="/workspaces/Hokuno-Store"
ALL_IDS="$DIR/all_ids.txt"
DONE_IDS="$DIR/done_ids.txt"
LOG="$DIR/republish.log"

PUBLISH_BODY='{"title":true,"description":false,"images":false,"variants":false,"tags":false,"keyFeatures":false,"shipping_template":false}'

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG"; }

if [ -z "$TOKEN" ]; then
  log "ERROR: PRINTIFY_API_TOKEN non défini"
  exit 1
fi

touch "$DONE_IDS"

# ── Step 1 : fetch all product IDs via Node.js (correct JSON parsing) ────────
if [ ! -s "$ALL_IDS" ]; then
  log "Récupération de la liste des produits..."
  > "$ALL_IDS"

  node - <<NODEEOF >> "$ALL_IDS"
const https = require('https');
const TOKEN = process.env.PRINTIFY_API_TOKEN;
const SHOP_ID = '22774508';

function get(path) {
  return new Promise((resolve, reject) => {
    https.get({ hostname: 'api.printify.com', path, headers: {
      'Authorization': 'Bearer ' + TOKEN,
      'User-Agent': 'ClaudeCode-Hokuno/1.0'
    }}, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => resolve({ status: res.statusCode, body: d }));
    }).on('error', reject);
  });
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

(async () => {
  let page = 1;
  while (true) {
    const r = await get('/v1/shops/' + SHOP_ID + '/products.json?page=' + page + '&limit=50');
    if (r.status !== 200) { process.stderr.write('Page ' + page + ' failed: ' + r.status + '\n'); break; }
    const data = JSON.parse(r.body);
    for (const p of data.data) process.stdout.write(p.id + '\n');
    process.stderr.write('Page ' + page + '/' + data.last_page + ' — ' + data.data.length + ' IDs\n');
    if (page >= data.last_page) break;
    page++;
    await sleep(500);
  }
})();
NODEEOF

  total=$(wc -l < "$ALL_IDS" | tr -d ' ')
  log "Total : $total IDs sauvegardés dans $ALL_IDS"
else
  total=$(wc -l < "$ALL_IDS" | tr -d ' ')
  log "all_ids.txt existe ($total IDs) — récupération ignorée"
fi

# ── Step 2 : republish each ID ───────────────────────────────────────────────
done_count=$(wc -l < "$DONE_IDS" | tr -d ' ')
total=$(wc -l < "$ALL_IDS" | tr -d ' ')
log "Début republish — $done_count/$total déjà traités"

i=0
while IFS= read -r product_id; do
  [ -z "$product_id" ] && continue
  i=$((i + 1))

  # skip if already done
  if grep -qxF "$product_id" "$DONE_IDS"; then
    log "[SKIP $i/$total] $product_id"
    continue
  fi

  retries=0
  while true; do
    http_code=$(curl -s -o /dev/null -w "%{http_code}" \
      -X POST \
      -H "Authorization: Bearer $TOKEN" \
      -H "User-Agent: ClaudeCode-Hokuno/1.0" \
      -H "Content-Type: application/json" \
      -d "$PUBLISH_BODY" \
      "https://api.printify.com/v1/shops/${SHOP_ID}/products/${product_id}/publish.json")

    if [ "$http_code" = "200" ] || [ "$http_code" = "204" ]; then
      echo "$product_id" >> "$DONE_IDS"
      done_now=$(wc -l < "$DONE_IDS" | tr -d ' ')
      log "[OK $i/$total] $product_id (done: $done_now)"
      break
    elif [ "$http_code" = "429" ]; then
      retries=$((retries + 1))
      log "[429] Rate limit — pause 300s (retry $retries) — $product_id"
      sleep 300
    else
      log "[FAIL $i/$total] HTTP $http_code — $product_id"
      break
    fi
  done

  sleep 2
done < "$ALL_IDS"

done_final=$(wc -l < "$DONE_IDS" | tr -d ' ')
log "=== TERMINÉ === $done_final/$total publiés"
