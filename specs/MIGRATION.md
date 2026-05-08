# specs/MIGRATION.md — Migration storemdtesttt → My Store 5

> Plan d'exécution complet. Chaque étape, qui la fait, dans quel ordre, avec quelles vérifications.
> Ce fichier est le séquenceur — il référence les autres specs pour le détail de chaque action.

---

## RÉSUMÉ

| Élément | Source | Cible |
|---------|--------|-------|
| Store | storemdtesttt (store dev, limitations) | My Store 5 (vrai store) |
| Produits | 430 sur Printify → publiés sur storemdtesttt | 430 à republier sur My Store 5 |
| Thème | theme.liquid v1 (497 lignes, monolithique) | Thème Hokuno modulaire (specs) |
| Collections | Aucune (les produits sont en vrac) | 4 collections automatiques |
| Pages | Aucune | about, faq, contact, mentions-legales, blog |
| Configuration | Aucune | Paiements, livraison, promo, devises, SEO, legal |

**L'ancien store storemdtesttt reste actif comme backup/test. On ne supprime rien.**

---

## DÉPENDANCES ET PRÉREQUIS

Avant de commencer la migration, ces éléments doivent être prêts :

| Prérequis | Statut | Responsable |
|-----------|--------|-------------|
| 18 specs rédigées et validées | ⏳ En cours | Toi + Claude (chat) |
| Thème Hokuno codé selon les specs | ⏳ À faire | Claude Code |
| Mockups réordonnés (Phase 4) | ⏳ À faire | Claude Chrome / toi |
| Coque "The End Brique" renommée sur Printify | ⏳ À faire | Toi (manuellement) |
| 68 titres Wanted /17→/46 corrigés | ⏳ À faire | Claude Code (API) |
| Accès admin à My Store 5 | ⏳ À vérifier | Toi |

---

## PHASE 1 — ACTIONS MANUELLES PRÉ-MIGRATION (toi)

Ces actions nécessitent un accès humain au dashboard. Claude Code ne peut pas les faire.

### Étape 1.1 — Créer l'app développeur sur My Store 5

1. Aller sur le Dev Dashboard Shopify Partners
2. Settings → Apps → Develop apps → Create an app
3. Nom de l'app : `Hokuno Admin`
4. Configurer les Admin API scopes :

```
read_products, write_products
read_themes, write_themes
read_content, write_content
read_customers
read_orders
read_inventory
read_script_tags, write_script_tags
read_locales, write_locales
read_publications, write_publications
```

5. Install app
6. Copier le token `atkn_xxxxxxxxxx`
7. **Ne jamais partager ce token ni le commit dans le repo**

### Étape 1.2 — Connecter Printify à My Store 5

1. Aller sur `printify.com/app/stores`
2. "Add store" → Shopify
3. Entrer l'URL : `s6btxa-q0.myshopify.com`
4. Autoriser la connexion
5. Vérifier que le shop apparaît dans Printify avec le bon nom

> Note : Printify peut être connecté à PLUSIEURS stores Shopify simultanément. storemdtesttt reste connecté.

### Étape 1.3 — Renommer la coque sur Printify

Ouvrir le produit `69f61d909110dda91005e89b` dans le dashboard Printify.
Renommer : "Coque de téléphone The End sur Brique Saga 1" → "Coque Wanted The End Brique Saga 1"
Sauvegarder.

Raison : la condition auto de la collection Wanted est `titre contient "wanted"`. Sans le renommage, cette coque ne sera pas dans Wanted (voir `specs/COLLECTIONS.md` §2).

---

## PHASE 2 — CONFIGURER LE CODESPACE (Claude Code)

### Étape 2.1 — Variables d'environnement

```bash
export PRINTIFY_API_TOKEN=ton_token_printify
export SHOPIFY_ACCESS_TOKEN=atkn_xxxxxxxxxx
export SHOPIFY_STORE=s6btxa-q0.myshopify.com
```

Vérification :
```bash
# Test connexion Printify
curl -s -H "Authorization: Bearer $PRINTIFY_API_TOKEN" \
  https://api.printify.com/v1/shops.json | python3 -m json.tool

# Test connexion Shopify
curl -s -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN" \
  "https://$SHOPIFY_STORE/admin/api/2024-01/shop.json" | python3 -m json.tool
```

Les deux doivent retourner un JSON valide. Si erreur → vérifier les tokens.

### Étape 2.2 — Installer les outils

```bash
# Shopify CLI
npm install -g @shopify/cli @shopify/theme

# ImageMagick (traitement d'images)
sudo apt-get install -y imagemagick

# Plugins Claude Code (si disponibles dans l'environnement)
# claude install-plugin shopify  # Shopify AI Toolkit
```

> Note : les plugins Claude Code (Shopify AI Toolkit, dylanreed, mrgoonie, jezweb) sont listés dans le plan mais leur disponibilité dépend de l'environnement. Claude Code doit tenter de les installer et continuer sans eux s'ils ne sont pas disponibles — l'API REST/GraphQL Shopify couvre tous les besoins.

### Étape 2.3 — Tester la connexion

```bash
# Lister les thèmes existants sur My Store 5
shopify theme list --store=$SHOPIFY_STORE

# Vérifier le nombre de produits (devrait être 0 avant publication)
curl -s -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN" \
  "https://$SHOPIFY_STORE/admin/api/2024-01/products/count.json"
```

---

## PHASE 3 — PUBLIER LES PRODUITS (Claude Code)

### Étape 3.1 — Republier les 430 produits via Printify

Printify gère la publication vers Shopify via son API. Pour chaque produit :

```bash
# Publier un produit vers My Store 5
curl -s -X POST "https://api.printify.com/v1/shops/{shop_id_my_store_5}/products/{product_id}/publish.json" \
  -H "Authorization: Bearer $PRINTIFY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": true,
    "description": true,
    "images": true,
    "variants": true,
    "tags": true
  }'
```

> ⚠️ **Shop ID** : le shop_id de My Store 5 dans Printify est DIFFÉRENT de celui de storemdtesttt (22774508). Après l'étape 1.2, récupérer le nouveau shop_id via `GET /v1/shops.json`.

**Script batch :**

```python
import os, requests, json, time

TOKEN = os.environ["PRINTIFY_API_TOKEN"]
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# 1. Récupérer le shop_id de My Store 5
shops = requests.get("https://api.printify.com/v1/shops.json", headers=HEADERS).json()
new_shop = next(s for s in shops if "my store 5" in s["title"].lower() or "s6btxa" in s.get("sales_channel_url", "").lower())
NEW_SHOP_ID = str(new_shop["id"])
print(f"My Store 5 shop ID: {NEW_SHOP_ID}")

# 2. Récupérer tous les produits du shop Printify principal (22774508)
OLD_SHOP_ID = "22774508"
all_products = []
for page in range(1, 25):
    r = requests.get(f"https://api.printify.com/v1/shops/{OLD_SHOP_ID}/products.json",
                     headers=HEADERS, params={"page": page})
    data = r.json()
    all_products.extend(data["data"])
    if page >= data["last_page"]:
        break
    time.sleep(0.3)
print(f"{len(all_products)} produits à publier")

# 3. Publier chaque produit vers My Store 5
success, errors = 0, []
for p in all_products:
    try:
        r = requests.post(
            f"https://api.printify.com/v1/shops/{NEW_SHOP_ID}/products/{p['id']}/publish.json",
            headers=HEADERS,
            json={"title": True, "description": True, "images": True, "variants": True, "tags": True}
        )
        if r.status_code in (200, 201):
            success += 1
        else:
            errors.append({"id": p["id"], "title": p["title"], "status": r.status_code, "body": r.text[:200]})
    except Exception as e:
        errors.append({"id": p["id"], "title": p["title"], "error": str(e)})
    time.sleep(0.5)  # Rate limit

print(f"Publiés: {success}/{len(all_products)}")
if errors:
    print(f"Erreurs: {len(errors)}")
    for e in errors[:10]:
        print(f"  - {e}")
```

> ⚠️ **Attention** : ce script publie les produits DEPUIS le shop Printify 22774508 VERS My Store 5. Si Printify ne permet pas de publier un même produit vers deux stores avec le même shop_id, il faudra peut-être dupliquer les produits ou utiliser un autre workflow. Tester avec 1-2 produits d'abord.

### Étape 3.2 — Vérification publication

```bash
# Compter les produits sur My Store 5
curl -s -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN" \
  "https://$SHOPIFY_STORE/admin/api/2024-01/products/count.json"
# Attendu : {"count": 430}
```

Si le count est < 430, identifier les produits manquants et les republier manuellement.

### Étape 3.3 — Corriger les 68 titres /17→/46

Après publication, corriger les titres sur My Store 5 (ou sur Printify puis republier) :

```python
# Script de correction des titres Wanted /17 → /46
# Cibler les produits dont le titre contient "/17"
import re

products = []  # Récupérer via API Shopify
for p in products:
    if "/17" in p["title"]:
        new_title = p["title"].replace("/17", "/46")
        requests.put(
            f"https://{SHOPIFY_STORE}/admin/api/2024-01/products/{p['id']}.json",
            headers={"X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN, "Content-Type": "application/json"},
            json={"product": {"id": p["id"], "title": new_title}}
        )
        time.sleep(0.3)
```

---

## PHASE 4 — MOCKUPS (Claude Chrome / toi)

**Doit être fait AVANT le push du thème.**

Voir `specs/MOCKUPS.md` pour le détail complet.

| Action | Produits | Méthode |
|--------|----------|---------|
| T-shirts : Back 2 en featured | 257 | Claude Chrome ou API |
| Mugs : Left/Right design en featured | 142 | Claude Chrome ou API |
| Coques : vérifier Front en featured | 14 | Vérification manuelle |
| Accessoires : design/logo en featured | 17 | Vérification manuelle |

Après réordonnement : republier les produits modifiés vers Shopify.

---

## PHASE 5 — COLLECTIONS ET TAGS (Claude Code)

### Étape 5.1 — Créer les 4 collections automatiques

Via l'API Shopify Admin :

```bash
# Collection Wanted (auto, titre contient "wanted")
curl -s -X POST "https://$SHOPIFY_STORE/admin/api/2024-01/smart_collections.json" \
  -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "smart_collection": {
      "title": "WANTED",
      "rules": [{"column": "title", "relation": "contains", "condition": "wanted"}],
      "disjunctive": false,
      "published": true
    }
  }'
```

Répéter pour Direction (`"condition": "direction"`), Mythologie (`"condition": "mythologie"`).

Design Hokuno : collection basée sur tag :
```json
{
  "smart_collection": {
    "title": "DESIGN HOKUNO",
    "rules": [{"column": "tag", "relation": "equals", "condition": "design-hokuno"}],
    "disjunctive": false,
    "published": true
  }
}
```

Détail des conditions : voir `specs/COLLECTIONS.md` §2.

### Étape 5.2 — Ajouter les tags

**Tag `design-hokuno` sur les 33 produits Design Hokuno :**

```python
design_hokuno_ids = [...]  # 33 IDs depuis INVENTAIRE.md section Design Hokuno
for pid in design_hokuno_ids:
    r = requests.get(f"https://{STORE}/admin/api/2024-01/products/{pid}.json", headers=HEADERS)
    product = r.json()["product"]
    tags = product.get("tags", "")
    if "design-hokuno" not in tags:
        new_tags = f"{tags}, design-hokuno" if tags else "design-hokuno"
        requests.put(f"https://{STORE}/admin/api/2024-01/products/{pid}.json",
                     headers=HEADERS, json={"product": {"id": pid, "tags": new_tags}})
    time.sleep(0.3)
```

**Tags `lang-fr` et `lang-en` sur les produits Wanted et Direction :**

Logique : si le titre contient " EN " ou se termine par " EN" → tag `lang-en`, sinon → tag `lang-fr`.

### Étape 5.3 — Configurer les images et descriptions des collections

Pour chaque collection :
1. Upload de l'image de couverture (card PNG)
2. Rédaction de la description FR (textes dans `specs/COLLECTIONS.md` §1)
3. Configuration de l'ordre de tri par défaut

### Étape 5.4 — Vérification collections

| Check | Attendu | Commande |
|-------|---------|----------|
| Wanted | 277 produits | `GET /admin/api/2024-01/smart_collections/{id}/products/count.json` |
| Direction | 80 produits | idem |
| Mythologie | 40 produits | idem |
| Design Hokuno | 33 produits | idem |
| Total | 430 | Somme = total Printify |
| Orphelins | 0 | Produits sans collection |

---

## PHASE 6 — THÈME (Claude Code)

### Étape 6.1 — Coder le thème

Claude Code crée le thème complet dans `shopify-theme/` en suivant les specs :
- `specs/ARCHITECTURE.md` — structure, fichiers, conventions
- `specs/NAVIGATION.md` — navbar, footer, breadcrumbs, cart AJAX
- `specs/COLLECTIONS.md` — pages collection, filtres, pagination
- `specs/PAGES.md` — toutes les pages
- `specs/PRODUIT.md` — page produit
- `specs/THEME.md` — design system CSS
- `specs/MOBILE.md` — comportements mobile
- `specs/SEO.md` — meta tags, JSON-LD
- `specs/MULTILINGUE.md` — FR/EN

### Étape 6.2 — Preview et itérations

```bash
cd shopify-theme/
shopify theme dev --store=$SHOPIFY_STORE
# Ouvre une URL de preview temporaire
```

Itérer jusqu'à validation visuelle sur desktop ET mobile.

### Étape 6.3 — Push en mode dev

```bash
shopify theme push --store=$SHOPIFY_STORE --unpublished
# Le thème est sur le store mais pas encore publié (mode preview)
```

---

## PHASE 7 — CONFIGURATION SHOPIFY (Claude Code + toi)

### Étape 7.1 — Créer les pages statiques

Via API Shopify Admin ou manuellement dans le dashboard :

| Page | Handle | Template | Contenu |
|------|--------|----------|---------|
| À propos | `about` | `page` | `specs/PAGES.md` §3 |
| FAQ | `faq` | `page` | `specs/PAGES.md` §4 |
| Contact | `contact` | `page.contact` | `specs/PAGES.md` §5 |
| Mentions légales | `mentions-legales` | `page` | `specs/LEGAL.md` |

### Étape 7.2 — Créer le blog

Créer le blog "Journal" (handle : `journal`) dans Shopify Admin → Blog posts → Manage blogs.

### Étape 7.3 — Configuration paiements, livraison, promo

Détail dans `specs/CONFIG-SHOPIFY.md`. Résumé :

| Config | Action |
|--------|--------|
| Paiements | Activer Shopify Payments (CB, Apple Pay, Google Pay, Shop Pay) |
| Livraison | Gratuite dès 60€, sinon tarifs Printify par zone |
| Code promo | HOKUNO15 = -15%, tous produits SAUF coques, durée 2 semaines |
| Devises | EUR (principal) + USD, GBP, CAD, AUD |
| Checkout | Logo Hokuno + couleur #D4A853 |
| Emails | Template branded noir + doré — `specs/EMAILS.md` |
| Marchés | France/EU (EUR, FR) + International (USD, EN) |

### Étape 7.4 — SEO & Analytics

Détail dans `specs/SEO.md` et `specs/ANALYTICS.md`. Résumé :

| Config | Action |
|--------|--------|
| Meta tags | Inclus dans le thème (theme.liquid + templates) |
| JSON-LD | Inclus dans le thème (snippet seo-jsonld.liquid) |
| robots.txt | Configuré — GPTBot, ClaudeBot, PerplexityBot autorisés |
| llms.txt | Fichier à la racine — description du site pour les LLMs |
| GA4 | Installer le Measurement ID dans le thème |
| Meta Pixel | Installer le Pixel ID dans le thème |
| TikTok Pixel | Optionnel — installer si TikTok Shop prévu |

### Étape 7.5 — Legal

Détail dans `specs/LEGAL.md`. Résumé :

| Config | Action |
|--------|--------|
| CGV | Rédiger dans Shopify → Settings → Policies → Terms of service |
| Confidentialité | Rédiger dans Settings → Policies → Privacy policy |
| Retours | Rédiger dans Settings → Policies → Refund policy |
| Mentions légales | Créer la page `/pages/mentions-legales` |
| Bannière cookies | Intégrer dans le thème (JS conditionnel analytics) |

---

## PHASE 8 — VÉRIFICATION (toi + Claude Code)

Passer la checklist complète définie dans `specs/CHECKLIST.md`.

### Tests obligatoires avant lancement

| Test | Méthode | Critère |
|------|---------|---------|
| Navigation desktop | Cliquer chaque lien navbar + footer | Tous fonctionnent, aucun 404 |
| Navigation mobile | Hamburger, overlay, bottom nav, liens | Fluide, pas de bug |
| Collections | Ouvrir chaque collection | Bon nombre de produits, filtres marchent |
| Produit | Ouvrir 5 produits (1 par collection) | Image correcte, variantes, panier, prix |
| Panier | Ajouter/supprimer/modifier quantité | Calculs corrects, checkout accessible |
| Responsive | iPhone SE, iPhone 14, iPad, desktop 1440px | Pas de cassure, lisible |
| Performance | PageSpeed Insights sur / et /collections/wanted | LCP < 2.5s, CLS < 0.1 |
| SEO | Google Rich Results Test sur une page produit | Schema Product valide |
| Commande test | Commander un produit → payer → annuler | Tout le flow fonctionne |

---

## PHASE 9 — LANCEMENT

### Étape 9.1 — Domaine (optionnel au lancement)

Détail dans `specs/DOMAINE.md`. Résumé :
- Acheter hokuno.com / .fr / .store
- Configurer DNS (A Record + CNAME)
- Shopify génère le SSL automatiquement
- **Timing** : acheter APRÈS validation du thème, AVANT le lancement public

### Étape 9.2 — Publication

```bash
# 1. Publier le thème en production
shopify theme publish --store=$SHOPIFY_STORE

# 2. Désactiver le mot de passe
# Shopify Admin → Online Store → Preferences → Password protection → Décocher
```

### Étape 9.3 — Post-lancement immédiat

| Action | Détail |
|--------|--------|
| Vérifier le site live | Naviguer sur toutes les pages, tester l'achat |
| Vérifier GA4 | Temps réel dans Google Analytics — le trafic apparaît |
| Vérifier Meta Pixel | Facebook Pixel Helper (extension Chrome) — événements OK |
| Annoncer | Poster sur TikTok + Instagram (`specs/SOCIAL.md`) |
| Monitorer | 24h de surveillance — erreurs console, erreurs checkout |

---

## SÉQUENCE COMPLÈTE — RÉSUMÉ VISUEL

```
PHASE 1 — Pré-migration (toi, manuel)
  1.1 Créer app dev My Store 5 → token atkn_
  1.2 Connecter Printify → My Store 5
  1.3 Renommer coque The End Brique
  ✓ CHECKPOINT : token OK, Printify connecté

PHASE 2 — Codespace (Claude Code)
  2.1 Variables d'environnement
  2.2 Installer outils (Shopify CLI)
  2.3 Tester connexions API
  ✓ CHECKPOINT : API Shopify + Printify répondent

PHASE 3 — Produits (Claude Code)
  3.1 Publier 430 produits vers My Store 5
  3.2 Vérifier count = 430
  3.3 Corriger 68 titres /17→/46
  ✓ CHECKPOINT : 430 produits sur My Store 5, titres OK

PHASE 4 — Mockups (Claude Chrome / toi)
  Réordonner images : Back 2 pour t-shirts, Left/Right pour mugs
  Republier les produits modifiés
  ✓ CHECKPOINT : images featured montrent le design

PHASE 5 — Collections + Tags (Claude Code)
  5.1 Créer 4 collections auto
  5.2 Ajouter tags (design-hokuno, lang-fr, lang-en)
  5.3 Images + descriptions collections
  5.4 Vérifier 277 + 80 + 40 + 33 = 430
  ✓ CHECKPOINT : chaque produit dans 1 collection exactement

PHASE 6 — Thème (Claude Code)
  6.1 Coder le thème (toutes les specs)
  6.2 Preview + itérations
  6.3 Push unpublished
  ✓ CHECKPOINT : validation visuelle desktop + mobile

PHASE 7 — Configuration (Claude Code + toi)
  7.1 Pages statiques (about, faq, contact, mentions légales)
  7.2 Blog journal
  7.3 Paiements, livraison, promo HOKUNO15, devises
  7.4 SEO, analytics (GA4, Meta Pixel)
  7.5 Legal (CGV, confidentialité, retours, cookies)
  ✓ CHECKPOINT : config complète, promo fonctionne

PHASE 8 — Vérification
  Checklist complète (specs/CHECKLIST.md)
  Tests mobile + desktop + commande réelle
  ✓ CHECKPOINT : zéro bug, zéro lien cassé

PHASE 9 — Lancement
  9.1 Domaine custom (si prêt)
  9.2 Publier thème + désactiver mot de passe
  9.3 Vérifier live, annoncer, monitorer

🚀 LIVE
```

---

## ROLLBACK

Si un problème critique est détecté après lancement :

1. **Remettre le mot de passe** : Shopify Admin → Online Store → Preferences → Password protection
2. **Revenir au thème précédent** : Shopify Admin → Online Store → Themes → Actions → Publish (le thème précédent)
3. **L'ancien store storemdtesttt reste fonctionnel** comme backup pendant toute la migration

Aucune donnée n'est perdue — les produits sont sur Printify, les commandes dans Shopify, le code dans le repo Git.
