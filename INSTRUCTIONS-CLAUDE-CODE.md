# INSTRUCTIONS — Pipeline Mockup Custom Hokuno

> **Pour Claude Code.** Lis le fichier en entier avant toute action. Exécute phase par phase. À chaque `🛑 STOP`, attends explicitement la validation de l'utilisateur avant de continuer.

---

## 0. OBJECTIF

Remplacer les 430 images principales des produits Shopify Hokuno par des mockups custom (t-shirt/mug/casquette détouré sur background stylé par collection).

- 100 % gratuit (rembg local + PIL + Shopify Admin API)
- Réversible (les images Printify d'origine ne sont jamais modifiées)
- Anti-écrasement Printify (passe par un metafield Shopify, pas par les images produit)
- 4 collections, 4 backgrounds :
  - `WANTED` → `bg-wanted.png`
  - `DIRECTION` → `bg-direction.png`
  - `MYTHOLOGIE` → `bg-mythologie.png`
  - `DESIGN HOKUNO` → `bg-design.png`

---

## 1. ORDRE D'EXÉCUTION

```
PHASE 1 — Setup
PHASE 2 — POC sur 4 produits (1 par collection)
🛑 STOP : validation visuelle utilisateur de la grille preview
PHASE 3 — Upload Shopify + patch thème pour les 4 POC
🛑 STOP : validation utilisateur sur le site live
PHASE 4 — Scale aux 426 restants
🛑 STOP : récap final
```

**Tu ne passes jamais à la phase suivante sans validation explicite.**

---

## 2. PHASE 1 — SETUP

### 2.1 Variables d'environnement
Affiche en console (sans révéler les valeurs complètes) :

```bash
echo "PRINTIFY_TOKEN: ${PRINTIFY_TOKEN:0:8}..."
echo "SHOPIFY_STORE: $SHOPIFY_STORE"
echo "SHOPIFY_ADMIN_TOKEN: ${SHOPIFY_ADMIN_TOKEN:0:8}..."
```

- Si `PRINTIFY_TOKEN` est vide → **🛑 STOP**, demande à l'utilisateur de la setter.
- Si `SHOPIFY_STORE` est vide → tente de le lire depuis `shopify.theme.toml` ou `.shopify-cli.yml` à la racine. Sinon **🛑 STOP**.
- Si `SHOPIFY_ADMIN_TOKEN` est vide → tente dans l'ordre :
  1. Lecture d'un `.env` à la racine
  2. `shopify auth print-token` (si la version CLI le supporte)
  3. Si rien ne marche → **🛑 STOP** et dis exactement à l'utilisateur :
     > "Je ne trouve pas de token Admin API Shopify utilisable. Options : (1) tu m'en fournis un via `export SHOPIFY_ADMIN_TOKEN=shpat_xxx`, (2) on bascule en mode 'préparation locale uniquement' : je génère les images, tu les uploades manuellement via le dashboard Shopify Files. Que préfères-tu ?"

### 2.2 Déplacement des backgrounds
L'utilisateur a posé 4 fichiers à la racine :
- `bg-wanted.png`
- `bg-direction.png`
- `bg-mythologie.png`
- `bg-design.png`

Crée `assets/mockup-backgrounds/` et déplace-les dedans.
Si un fichier manque → **🛑 STOP** et liste les fichiers manquants.

### 2.3 Structure de dossiers à créer

```
scripts/mockup-pipeline/
  __init__.py
  config.py
  printify_client.py
  shopify_client.py
  detourage.py
  compositing.py
  collection_detector.py
  mockup_selector.py
  01_run_poc.py
  02_upload_poc.py
  03_patch_theme.py
  04_scale_full.py
output/mockup-pipeline/
  01-raw/
  02-detoured/
  03-final/
  logs/
```

### 2.4 .gitignore (append, ne pas écraser)

```
output/
*.pyc
__pycache__/
.env
```

### 2.5 Dépendances

```bash
pip install "rembg[cpu]" pillow requests python-dotenv tenacity
```

Pré-télécharge le modèle rembg pour éviter une latence au premier produit :

```bash
python -c "from rembg import new_session; new_session('u2netp')"
```

### 2.6 config.py (modèle)

```python
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = REPO_ROOT / "output" / "mockup-pipeline"
BG_DIR = REPO_ROOT / "assets" / "mockup-backgrounds"
LOG_DIR = OUTPUT_DIR / "logs"

PRINTIFY_TOKEN = os.environ["PRINTIFY_TOKEN"]
PRINTIFY_SHOP_ID = "22774508"

SHOPIFY_STORE = os.environ["SHOPIFY_STORE"]            # ex: storemdtesttt.myshopify.com
SHOPIFY_ADMIN_TOKEN = os.environ.get("SHOPIFY_ADMIN_TOKEN", "")
SHOPIFY_API_VERSION = "2024-10"

# Mapping collection → background
BG_BY_COLLECTION = {
    "WANTED":         BG_DIR / "bg-wanted.png",
    "DIRECTION":      BG_DIR / "bg-direction.png",
    "MYTHOLOGIE":     BG_DIR / "bg-mythologie.png",
    "DESIGN HOKUNO":  BG_DIR / "bg-design.png",
}

# Compositing
FINAL_SIZE = (1500, 1500)
PRODUCT_RELATIVE_WIDTH = {
    "tshirt":    0.62,
    "mug":       0.52,
    "casquette": 0.58,
    "phonecase": 0.42,
    "default":   0.55,
}
WEBP_QUALITY = 88

# Rate limits
PRINTIFY_DELAY_S = 0.4
SHOPIFY_DELAY_S = 0.6   # Shopify Admin API : ~2 req/s
```

---

## 3. PHASE 2 — POC SUR 4 PRODUITS

### 3.1 Sélection automatique des 4 cobayes

Dans `01_run_poc.py` :

1. Récupère tous les produits Printify via `GET /v1/shops/{shop_id}/products.json?limit=100` (paginer).
2. Pour chaque produit, détecte sa collection via `collection_detector.detect_collection(product)` :
   - Regarde le `title` du produit (uppercase) :
     - Contient `WANTED` → `WANTED`
     - Contient `DIRECTION` → `DIRECTION`
     - Contient `MYTHOLOGIE` ou `MYTHOLOGY` → `MYTHOLOGIE`
     - Sinon → `DESIGN HOKUNO`
3. Sélectionne **1 produit par collection** (le premier disponible). Préfère un t-shirt si la collection en contient.
4. **🛑 STOP intermédiaire (court)** : affiche les 4 produits choisis (ID, titre, collection détectée) et demande "OK pour ces 4 cobayes ?" avant de continuer.

### 3.2 Détection du type de produit (`mockup_selector.py`)

Approche : matche par **mots-clés dans le titre** (rapide et fiable sur ce store), fallback sur `blueprint_id`.

| Type        | Mots-clés title              |
|-------------|------------------------------|
| tshirt      | "T-SHIRT", "TSHIRT", "TEE"   |
| mug         | "MUG", "TASSE"               |
| casquette   | "CASQUETTE", "BOB", "HAT"    |
| phonecase   | "COQUE", "CASE"              |

### 3.3 Sélection du mockup source

Parmi `product["images"]`, choisis intelligemment :

```python
def pick_source_mockup(product, ptype):
    imgs = product.get("images", [])
    if not imgs:
        raise ValueError("Aucun mockup")

    pub_imgs = [i for i in imgs if i.get("is_selected_for_publishing")]
    pool = pub_imgs or imgs

    needles_by_type = {
        "tshirt":    ["back-2", "back_2", "back-1", "back"],
        "mug":       ["front", "default"],
        "casquette": ["front"],
        "phonecase": ["front", "default"],
    }
    needles = needles_by_type.get(ptype, [])

    for needle in needles:
        for i in pool:
            pos = (i.get("position") or "").lower()
            if needle in pos:
                return i

    for i in pool:
        if i.get("is_default"):
            return i
    return pool[0]
```

**Log** la `position` du mockup sélectionné pour chaque produit. Si l'utilisateur dit plus tard "le design n'apparaît pas", c'est ce log qu'on inspectera.

### 3.4 Détourage (`detourage.py`)

```python
from rembg import remove, new_session
from PIL import Image
import io
import numpy as np

SESSION = new_session("u2netp")

def detoure(input_bytes: bytes) -> Image.Image:
    """Retourne une PIL Image RGBA détourée, cropée à la bbox."""
    output = remove(input_bytes, session=SESSION)
    img = Image.open(io.BytesIO(output)).convert("RGBA")

    # Seuil alpha : élimine le halo des bords (typique sur fond blanc Printify)
    arr = np.array(img)
    arr[..., 3] = np.where(arr[..., 3] < 30, 0, arr[..., 3])
    img = Image.fromarray(arr)

    # Crop sur la bbox réelle pour bien centrer ensuite
    bbox = img.getbbox()
    if bbox:
        img = img.crop(bbox)
    return img
```

### 3.5 Compositing (`compositing.py`)

```python
from PIL import Image
from .config import FINAL_SIZE, PRODUCT_RELATIVE_WIDTH, WEBP_QUALITY

def compose(detoured: Image.Image, bg_path, product_type: str, output_path):
    bg = Image.open(bg_path).convert("RGB").resize(FINAL_SIZE, Image.LANCZOS)

    rel_w = PRODUCT_RELATIVE_WIDTH.get(product_type, PRODUCT_RELATIVE_WIDTH["default"])
    target_w = int(FINAL_SIZE[0] * rel_w)
    ratio = target_w / detoured.width
    target_h = int(detoured.height * ratio)
    resized = detoured.resize((target_w, target_h), Image.LANCZOS)

    x = (FINAL_SIZE[0] - target_w) // 2
    y = (FINAL_SIZE[1] - target_h) // 2

    bg_rgba = bg.convert("RGBA")
    bg_rgba.alpha_composite(resized, dest=(x, y))
    final = bg_rgba.convert("RGB")
    final.save(output_path, "WEBP", quality=WEBP_QUALITY, method=6)
```

### 3.6 Grille de preview

À la fin de `01_run_poc.py`, génère `output/mockup-pipeline/03-final/_PREVIEW_grid.png` (2×2) avec les 4 mockups composés et leur titre en légende. Affiche le path absolu en console.

### 3.7 🛑 STOP — Validation visuelle utilisateur

Affiche en console :

```
======================================================================
🛑 PHASE 2 TERMINÉE — POC sur 4 produits
======================================================================
Ouvre cette image et regarde le rendu :
  → output/mockup-pipeline/03-final/_PREVIEW_grid.png

Détail par produit :
  [WANTED]        65xxx — T-SHIRT LUFI WANTED 1/46     → 03-final/65xxx.webp
  [DIRECTION]     65yyy — T-SHIRT DIRECTION ...        → 03-final/65yyy.webp
  [MYTHOLOGIE]    65zzz — T-SHIRT POSEIDON ...         → 03-final/65zzz.webp
  [DESIGN HOKUNO] 65www — CASQUETTE HOKUNO DARK        → 03-final/65www.webp

Réponses possibles :
  - "OK, continue" → passe à PHASE 3
  - "Le t-shirt est trop petit/grand" → ajuste PRODUCT_RELATIVE_WIDTH et relance
  - "Le détourage est moche sur X" → bascule sur isnet-general-use et relance
  - "Le mockup choisi n'est pas le bon" → corrige mockup_selector.py
======================================================================
```

**N'enchaîne PAS sur la phase 3 sans validation explicite.**

---

## 4. PHASE 3 — UPLOAD SHOPIFY POC + PATCH THÈME

### 4.1 Mapping Printify → Shopify

Le champ `external.id` du produit Printify contient le Shopify product numeric id quand publié :

```json
{ "id": "65abc...", "external": { "id": "8123456789", "handle": "..." } }
```

→ Shopify GID = `gid://shopify/Product/8123456789`.

Si `external` est `null` → produit non publié sur Shopify. Skip, log l'erreur, continue.

### 4.2 Création (idempotente) du metafield definition

```graphql
mutation {
  metafieldDefinitionCreate(definition: {
    name: "Featured Image Override"
    namespace: "custom"
    key: "featured_image_override"
    type: "file_reference"
    ownerType: PRODUCT
    validations: [{name: "file_type_options", value: "[\"Image\"]"}]
  }) {
    createdDefinition { id }
    userErrors { field message }
  }
}
```

Si l'erreur dit "already exists" / "has been taken" → OK, continue. Toute autre erreur → **🛑 STOP**.

### 4.3 Upload des fichiers (Shopify Files via GraphQL)

**Étape 1 — staged upload** :
```graphql
mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
  stagedUploadsCreate(input: $input) {
    stagedTargets { url resourceUrl parameters { name value } }
    userErrors { field message }
  }
}
```
Input :
```json
{
  "filename": "hokuno-{product_id}.webp",
  "mimeType": "image/webp",
  "httpMethod": "POST",
  "resource": "FILE"
}
```

**Étape 2 — POST multipart** vers `stagedTargets[0].url` :
- Tous les `parameters` en form fields
- Le fichier en dernier champ `file`

**Étape 3 — fileCreate** :
```graphql
mutation fileCreate($files: [FileCreateInput!]!) {
  fileCreate(files: $files) {
    files {
      id
      fileStatus
      ... on MediaImage { image { url } }
    }
    userErrors { field message }
  }
}
```
Input :
```json
{
  "alt": "Hokuno custom mockup",
  "contentType": "IMAGE",
  "originalSource": "<resourceUrl de l'étape 1>"
}
```

**Étape 4 — Poll fileStatus jusqu'à READY** (timeout 30s, sleep 1.5s entre polls) avant d'enchaîner sur le metafield.

### 4.4 Set le metafield sur le produit

```graphql
mutation metafieldsSet($metafields: [MetafieldsSetInput!]!) {
  metafieldsSet(metafields: $metafields) {
    metafields { id key value }
    userErrors { field message }
  }
}
```
Input :
```json
{
  "ownerId": "gid://shopify/Product/8123456789",
  "namespace": "custom",
  "key": "featured_image_override",
  "type": "file_reference",
  "value": "gid://shopify/MediaImage/xxxxx"
}
```

### 4.5 Patch `shopify-theme/snippets/product-card.liquid`

**Backup obligatoire avant patch** : copie l'original en `product-card.liquid.bak`.

**Avant** :
```liquid
<div class="prod-card-img">
  {% if product.featured_image %}
    <img src="{{ product.featured_image | image_url: width: 600 }}" ...>
  {% endif %}
```

**Après** :
```liquid
<div class="prod-card-img">
  {%- assign override = product.metafields.custom.featured_image_override -%}
  {%- if override.value != blank -%}
    <img
      src="{{ override.value | image_url: width: 600 }}"
      alt="{{ product.title }}"
      width="600" height="600" loading="lazy">
  {%- elsif product.featured_image -%}
    <img
      src="{{ product.featured_image | image_url: width: 600 }}"
      alt="{{ product.title }}"
      width="600" height="600" loading="lazy">
  {%- endif -%}
```

Ne touche RIEN d'autre dans le fichier (badges, infos prix, etc.).

### 4.6 Push du thème via CLI

```bash
cd shopify-theme
shopify theme push --live --allow-live --json
cd ..
```

Si la commande échoue :
- Auth manquante → propose `shopify login --store=$SHOPIFY_STORE`
- Theme ID non set → propose `shopify theme list` puis demande à l'utilisateur quel theme cibler
- **🛑 STOP** en affichant le message d'erreur brut

### 4.7 🛑 STOP — Validation live

```
======================================================================
🛑 PHASE 3 TERMINÉE — POC uploadé sur Shopify
======================================================================
Va voir les 4 produits sur ta boutique live :
  https://$SHOPIFY_STORE/products/<handle-1>
  https://$SHOPIFY_STORE/products/<handle-2>
  https://$SHOPIFY_STORE/products/<handle-3>
  https://$SHOPIFY_STORE/products/<handle-4>

Vérifie que :
  ✓ L'image principale est ton mockup custom (pas le fond blanc Printify)
  ✓ Les autres images du produit (front, folded) restent normales
  ✓ Pas de glitch sur mobile

Réponses possibles :
  - "OK, scale les 426 restants" → PHASE 4
  - "Problème X" → décris, on rectifie avant scale
  - "Annule tout" → reset (voir section 6)
======================================================================
```

---

## 5. PHASE 4 — SCALE AUX 426 RESTANTS

Dans `04_scale_full.py` :

1. Récupère TOUS les produits Printify (pagination, `limit=100`).
2. Exclus les 4 déjà traités (`output/mockup-pipeline/logs/poc_results.json`).
3. Pour chaque produit restant, exécute le pipeline complet :
   - detection collection → mockup source → download → detourage → compositing → upload Shopify → set metafield
4. Stocke un log JSON par produit dans `output/mockup-pipeline/logs/{product_id}.json` :
   ```json
   {
     "product_id": "65abc...",
     "shopify_id": "gid://shopify/Product/8123...",
     "collection": "WANTED",
     "type": "tshirt",
     "mockup_position_used": "back-2",
     "shopify_file_gid": "gid://shopify/MediaImage/xxx",
     "metafield_set": true,
     "duration_s": 12.4,
     "error": null
   }
   ```
5. **Rate limits stricts** :
   - Printify : `time.sleep(0.4)` entre appels
   - Shopify : `time.sleep(0.6)` entre mutations (2 req/s Admin GraphQL)
   - Erreur `THROTTLED` Shopify → sleep 5s + retry
6. **Retries tenacity** sur tous les appels HTTP : 3 essais, backoff exponentiel (2s, 4s, 8s).
7. **Continue on error** : un produit qui échoue ne casse PAS le batch. Log + skip.
8. **Progress console** : `[i/total] {title} → OK` ou `→ ERROR: {msg}`.

### 5.1 Récap final

À la fin, génère `output/mockup-pipeline/logs/_SUMMARY.md` :

```markdown
# Récap pipeline mockup — {date ISO}

- Total produits traités : 430
- Succès : XXX
- Échecs : YY
- Durée totale : Z h

## Échecs détaillés
| Product ID | Title | Erreur |
|---|---|---|
| 65abc | ... | external.id manquant |

## Stats par collection
| Collection | OK | Erreur |
|---|---|---|
| WANTED | 184 | 0 |
| ...
```

Affiche le path du summary en console.

### 5.2 🛑 STOP final

```
======================================================================
🛑 PHASE 4 TERMINÉE
======================================================================
Récap : output/mockup-pipeline/logs/_SUMMARY.md

Actions utilisateur :
  1. Inspecter le récap (notamment les échecs)
  2. Vérifier 5-10 produits aléatoires sur la boutique live
  3. Vider le cache CDN Shopify si les images ne s'affichent pas

Pour retry uniquement les échecs :
  python scripts/mockup-pipeline/04_scale_full.py --retry-failed-only
======================================================================
```

---

## 6. RESET / ROLLBACK

Si l'utilisateur dit "annule tout" :

1. Restore `shopify-theme/snippets/product-card.liquid` depuis le `.bak` créé en 4.5.
2. `shopify theme push` pour pousser la restauration.
3. Pour chaque produit traité (lis les logs), exécute `metafieldsDelete` GraphQL.
4. (Optionnel) `fileDelete` GraphQL sur les MediaImage uploadés pour libérer les Files Shopify.
5. `rm -rf output/mockup-pipeline/` pour nettoyer le local.

---

## 7. EDGE CASES

| Cas | Comportement |
|---|---|
| `external.id` Printify absent | Skip + log, continue |
| Mockup source absent | Skip + log |
| rembg crash sur une image | Retry session fraîche, sinon skip + log |
| Shopify throttle (429 / THROTTLED) | sleep 5s + retry tenacity |
| Shopify `fileStatus: FAILED` | Re-upload une fois, sinon skip |
| Collection non détectée | Fallback `bg-design.png` + warning |
| Metafield déjà set | Skip set (sauf flag `--force`) |
| CLI Shopify pas authentifiée | 🛑 STOP, demande `shopify login` |

---

## 8. LOG VERBEUX (obligatoire)

Pour chaque produit, console :
```
[3/430] [WANTED] 65abc12... T-SHIRT LUFI WANTED 1/46
  ├─ Type: tshirt
  ├─ Mockup source: back-2
  ├─ Détourage: OK (1245x1300 → 1180x1295 après crop)
  ├─ Compositing: OK → 03-final/65abc12.webp (412 KB)
  ├─ Upload Shopify: OK (gid://shopify/MediaImage/xxxxx)
  ├─ Metafield set: OK
  └─ Durée: 8.2s
```

---

## 9. COMMENT L'UTILISATEUR LANCE LE PIPELINE

```bash
# Phase 2 — POC
python scripts/mockup-pipeline/01_run_poc.py

# Phase 3 — Upload POC (après validation)
python scripts/mockup-pipeline/02_upload_poc.py
python scripts/mockup-pipeline/03_patch_theme.py

# Phase 4 — Scale (après validation live)
python scripts/mockup-pipeline/04_scale_full.py
```

**Toi (Claude Code) ne lances PAS les scripts toi-même. Tu écris le code, tu affiches la commande, l'utilisateur la lance.** À chaque fin de phase, dis-lui précisément quelle commande lancer ensuite.

---

## FIN — DÉMARRAGE

Commence par **PHASE 1 (Setup)** uniquement. N'écris pas le code des phases 3 et 4 tant que la phase 2 n'est pas validée. Inutile et risqué.

Une fois la phase 1 setup terminée, écris les scripts de la phase 2 (`config.py`, `printify_client.py`, `collection_detector.py`, `mockup_selector.py`, `detourage.py`, `compositing.py`, `01_run_poc.py`), puis demande à l'utilisateur de lancer `python scripts/mockup-pipeline/01_run_poc.py`.

**Reste défensif. Mieux vaut un 🛑 STOP en trop qu'un scale aux 430 dans le mur.**
