# CLAUDE.md — Instructions pour Claude Code

## Contexte du projet

Ce repo est la source de vérité pour **Hokuno** (ホクノ), une marque streetwear manga en Print on Demand.
Lis `CONTEXT.md` en premier — il contient toute la brand bible : identité, collections, produits, SEO/GEO, stratégie multi-canal.

## Structure

```
├── CONTEXT.md                        # Brand bible complète
├── INVENTAIRE.md                     # Inventaire complet Printify (tous IDs)
├── PRICING.md                        # Prix de vente, coûts, marges par produit
├── .claude/skills/printify/SKILLS.md # Référence API Printify
├── collections/
│   ├── wanted.json                   # Personnages collection Wanted (46 — tous sur Printify FR+EN)
│   ├── direction.json                # Personnages collection Direction (10)
│   └── mythologie.json               # Personnages collection Mythologie (10 + coques)
├── assets/
│   └── design-reference/             # Captures UI de référence (landing, collections, produits, mobile)
└── archive/
    └── scripts/                      # Scripts Python Printify (archivés — usage historique)
```

## État actuel (2026-05-05)

- **Shop Printify** : ID `22774508`, nom "My new store", **sales channel : disconnected** (à connecter Shopify + TikTok Shop)
- **Total produits** : 430 — voir INVENTAIRE.md pour le détail complet (audité 2026-05-05)
- **Prix Printify** : mis à jour sur 413/430 produits — 17 bloqués API 500 (à faire manuellement, listés dans TODO.md)
- **Descriptions HTML** : injectées sur 413/430 produits via API (2026-05-05) — 17 bloqués API 500 (mêmes produits que prix)
- **Tailles t-shirts** : XL max — 2XL/3XL/4XL/5XL désactivées sur 44/48 t-shirts (4 bloqués API 500)
- **Collection Wanted** : 46/46 personnages × FR+EN × light+dark + mugs = 276 produits
  - ⚠️ 68 titres avec suffix `/17` au lieu de `/46` (cosmétique — correction via API planifiée)
  - ✅ Variante 15oz activée sur 142 mugs (Wanted FR+EN, Direction FR+EN, Mythologie)
  - ✅ Logo front 74.png correct sur tous les t-shirts dark Wanted (92/92)
- **Collection Direction FR** : 10/10 — 20 t-shirts + 10 mugs light (bp 478) + 10 mugs dark (bp 479)
  - Logo front DARK (74.png) : ID `6849b65d8ee17a5b00c03855`, scale 53.59 UI / 0.21105 API
  - Logo front LIGHT (silhouette) : ID `69f79f1270e1b9ced794f3ab`, scale 59.53 UI / 0.14076 API
  - Kanji mug : ID `6846fd1c1a6d958e91819b36`
- **Collection Direction EN** : 10/10 — 20 t-shirts + 10 mugs light (bp 478) + 10 mugs dark (bp 479)
  - ✅ Doublon `684d56c509bce0c2370d3254` supprimé (2026-05-05)
  - ✅ Logo front 74.png correct sur tous les t-shirts dark Direction (20/20)
- **Collection Mythologie** : 10/10 t-shirts light + 10/10 dark + 10/10 mugs + **10/10 coques** = 40 produits ✅ COMPLET
  - ✅ Variante 15oz activée sur tous les mugs Mythologie
  - Coques Mythologie : BP 268 / SPOKE (PP 1) — image réutilisée depuis t-shirt back, x=0.5, y=0.605, scale=0.7216, 26 variantes actives (iPhone 11 → iPhone 17)
- **Collection Design Hokuno** : 13 t-shirts (bp 6+145) + 21 accessoires = 34 produits
  - ⚠️ 4 t-shirts avec XXL non désactivé (API 500 — faire manuellement)
  - ⚠️ 1 doublon Target Dark à supprimer : `69f9e82ec12ffe54490a4e8d`
  - ⚠️ Target Light `69f8c86f09f3b73024023a0e` : 1 seule variante active (White/L $25.96) — à reconfigurer
  - ℹ️ 7 t-shirts dark ont un design front custom (pas le logo 74.png) — à valider si intentionnel

### Logos Design Hokuno (référence)
- **Logo front DARK (74.png)** : `6849b65d8ee17a5b00c03855` — scale 53.59 UI / 0.21105 API (t-shirts NOIR)
- **Logo front LIGHT (silhouette Direction)** : `69f79f1270e1b9ced794f3ab` — scale 59.53 UI / 0.14076 API
- **Kanji mug Direction** : `6846fd1c1a6d958e91819b36`

## Projets Canva

- **"THE END"** : Wanted FR — 92 pages (tous les personnages Wanted en français)
- **"Copie de THE END"** : Wanted EN — 49 designs traduits automatiquement via l'outil de traduction intégré Canva
- **"FRUIT"** : Direction FR — 24 pages (10 personnages × variantes couleur)
- **Direction EN** : images régénérées manuellement (texte EN intégré dans l'IA)

## Contraintes importantes

- **Punchline Wanted** : identique pour TOUS les personnages — `"ÇA NE FINIRA JAMAIS..."` (FR) / `"IT WILL NEVER END..."` (EN). Ne jamais créer de punchlines personnalisées.
- **Texte secondaire Wanted** : identique pour tous — `"CETTE PRIME TRAINE DEPUIS 12 ANS. HONNETEMENT, SI VOUS LE TROUVEZ DEMANDEZ-LUI SIL EST TOUJOURS PARTANT"` (FR) / `"THIS BOUNTY HAS BEEN RUNNING FOR 12 YEARS. HONESTLY, IF YOU FIND HIM ASK HIM IF HE'S STILL UP FOR IT"` (EN)
- **Quote Direction** : identique pour TOUS — `"JE N'AI PAS BESOIN D'UN PLAN.. JUSTE D'UNE DIRECTION."` (FR) / `"I DON'T NEED A PLAN.. JUST A DIRECTION."` (EN)
- **Direction EN** : le texte est intégré dans l'image IA — les 20 t-shirts (light+dark) sont créés sur Printify. Pour les prochaines collections similaires, utiliser le script `scripts/create_direction_en.py` comme référence.

## Convention de titrage Printify

Format standard : `T-SHIRT [NOM] [COLLECTION] [VERSION]` en MAJUSCULES

- `VERSION` = vide pour light standard, `NOIR` pour dark (Black+Navy), `NOIR XL` pour Black uniquement 8 tailles, `XL` pour palette étendue 56 variantes
- Mugs : `tasse en céramique [collection] [nom] (11oz, 15oz)` en minuscules
- Coques : `[type] [NOM] [COLLECTION]`

## API Printify

Le token API est dans la variable d'environnement `PRINTIFY_API_TOKEN`.
Avant tout appel API, vérifie que le token est disponible :

```bash
if [ -z "$PRINTIFY_API_TOKEN" ]; then
  echo "⚠️ PRINTIFY_API_TOKEN non défini — mode hors-ligne, remplissage manuel des JSON"
fi
```

Si le token est disponible :
1. Lis `.claude/skills/printify/SKILL.md` pour les endpoints et le workflow
2. Récupère le shop ID via `GET /v1/shops.json`
3. Liste tous les produits via `GET /v1/shops/{shop_id}/products.json`
4. Mappe chaque produit à sa collection (Wanted/Direction/Mythologie) selon le titre
5. Remplis les `printify_product_ids` dans les JSON de collection

Si le token n'est PAS disponible :
- Remplis quand même les JSON avec toutes les infos possibles (noms, backstories, descriptions, punchlines)
- Laisse les `printify_product_ids` vides — ils seront remplis manuellement

## Tâches courantes

### Remplir les JSON de collection

Pour chaque personnage dans chaque collection :
- `nom` : nom parodique du personnage Hokuno (jamais le nom original)
- `backstory_fr` / `backstory_en` : 2-3 phrases max, ton décalé/nostalgique (Wanted = humour noir, Mythologie = épique, Direction = motivationnel)
- `description_visuelle` : description précise du design tel qu'il apparaît sur le t-shirt
- `punchline_fr` / `punchline_en` (Wanted) ou `quote_fr` / `quote_en` (Direction) : texte imprimé sur le t-shirt
- `tags` : mots-clés pour le SEO et le filtrage

Respecte le ton et le style décrits dans `CONTEXT.md` pour chaque collection.

### Construire la boutique Shopify

- Landing page immersive avec Three.js (3D), glassmorphisme, animations GSAP
- Navigation par collection avec storytelling
- Pages produit riches avec backstory du personnage
- Schema JSON-LD sur chaque page (Product, Organization, CollectionPage, BreadcrumbList)
- SSR obligatoire — le contenu doit être dans le HTML initial
- Fichier `llms.txt` à la racine du site
- `robots.txt` : ne pas bloquer GPTBot, ChatGPT-User, ClaudeBot, PerplexityBot
- Bilingue FR/EN

### SEO/GEO

Consulte la section SEO & GEO dans `CONTEXT.md` pour toutes les directives.

## Conventions de code

- TypeScript strict pour le frontend
- Tailwind CSS pour le styling
- Composants React fonctionnels avec hooks
- Noms de variables et commentaires en anglais, contenu utilisateur en FR/EN
- Pas de `console.log` en production
- Gestion d'erreurs systématique

## Règle obligatoire — mise à jour systématique

**À chaque fin de session ou après toute action sur Printify (création, modification, suppression de produits) :**

1. **Mettre à jour `INVENTAIRE.md`** — régénérer depuis l'API (script ci-dessous) ou mettre à jour manuellement les sections concernées, avec le bon total et la bonne date
2. **Mettre à jour `CLAUDE.md` section "État actuel"** — total produits, état par collection, anomalies connues
3. **Mettre à jour la liste "Produits restants à créer"** — cocher ce qui est fait, ajouter ce qui est découvert
4. **Mettre à jour les JSON de collection** (`wanted.json`, `direction.json`, `mythologie.json`) — tous les `printify_product_ids` doivent refléter l'état réel

Pour régénérer l'inventaire complet depuis l'API :
```bash
python3 - <<'EOF'
import os, requests, json, time
TOKEN = os.environ["PRINTIFY_API_TOKEN"]
SHOP_ID = "22774508"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "User-Agent": "ClaudeCode-Hokuno/1.0"}
all_products = []
for page in range(1, 20):
    r = requests.get(f"https://api.printify.com/v1/shops/{SHOP_ID}/products.json",
                     headers=HEADERS, params={"page": page})
    r.raise_for_status()
    data = r.json()
    all_products.extend(data["data"])
    if page >= data["last_page"]: break
    time.sleep(0.3)
with open("/tmp/printify_all_products.json", "w") as f:
    json.dump(all_products, f)
print(f"{len(all_products)} produits récupérés")
EOF
```

## Ne jamais faire

- Ne jamais commit de tokens ou secrets dans le repo
- Ne jamais utiliser les noms originaux des personnages One Piece dans le code ou le contenu public
- Ne jamais générer de contenu qui reproduit directement des designs protégés par copyright
