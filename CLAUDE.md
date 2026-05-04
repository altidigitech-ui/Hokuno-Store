# CLAUDE.md — Instructions pour Claude Code

## Contexte du projet

Ce repo est la source de vérité pour **Hokuno** (ホクノ), une marque streetwear manga en Print on Demand.
Lis `CONTEXT.md` en premier — il contient toute la brand bible : identité, collections, produits, SEO/GEO, stratégie multi-canal.

## Structure

```
├── CONTEXT.md                        # Brand bible complète
├── INVENTAIRE.md                     # Inventaire complet Printify (tous IDs)
├── .claude/skills/printify/SKILLS.md # Référence API Printify
├── collections/
│   ├── wanted.json                   # Personnages collection Wanted (46 — tous sur Printify FR+EN)
│   ├── direction.json                # Personnages collection Direction (10)
│   └── mythologie.json               # Personnages collection Mythologie (10)
├── exports/
│   ├── wanted-fr/                    # Designs Wanted FR (posters 1198×1690)
│   ├── wanted-en/                    # Designs Wanted EN
│   ├── direction-fr-dark/            # 10 PNG Direction FR — silhouette blanche, fond transparent (t-shirts noirs)
│   ├── direction-fr-light/           # 10 PNG Direction FR — silhouette noire, fond transparent (t-shirts clairs)
│   ├── direction-en-dark/            # 10 PNG Direction EN — silhouette blanche, fond transparent (t-shirts noirs)
│   └── direction-en-light/           # 10 PNG Direction EN — silhouette noire, fond transparent (t-shirts clairs)
└── scripts/
    ├── update_direction_backs.py     # Met à jour le dos des 20 t-shirts Direction FR
    ├── create_direction_en.py        # Crée les 20 t-shirts Direction EN depuis templates FR
    ├── restore_front_logo.py         # Restaure le logo front sur N produits Direction
    └── fix_front_logo_scale.py       # Corrige le scale du logo front (59.53 UI = 0.14076 API)
```

## État actuel (2026-05-03)

- **Shop Printify** : ID `22774508`, nom "My new store", **sales channel : disconnected** (à connecter Shopify + TikTok Shop)
- **Total produits** : 391 (382 + 9 mugs Mythologie créés le 2026-05-04)
- **Wanted** : 46/46 personnages complets FR+EN — 46 t-shirts FR light, 46 FR dark, 46 EN light, 46 EN dark, 46 mugs FR, 46 mugs EN = 276 produits
  - ⚠️ 4 produits EN à renommer (Lufi ×2 + Bartolomiou Kouma ×2 — titres incorrects, contenu OK)
- **Direction FR** : 10/10 personnages — 20 t-shirts (light+dark) + 21 mugs (10 light + 10 dark + 1 ancien Luffy) ✅
  - Dos mis à jour avec nouvelles images (exports/direction-fr-dark/ et direction-fr-light/)
  - Logo front restauré (ID `69f79f1270e1b9ced794f3ab`, scale 59.53)
  - Mugs : blueprint 478 (white) + 479 (black), kanji ID `6846fd1c1a6d958e91819b36`
- **Direction EN** : 10/10 personnages — 20 t-shirts (light+dark) + 20 mugs (10 light + 10 dark) ✅
  - Dos : exports/direction-en-dark/ et direction-en-light/
  - Logo front identique FR (ID `69f79f1270e1b9ced794f3ab`, scale 59.53)
- **Mythologie** : 10/10 light, 10/10 dark, 10/10 mugs ✅, 1 coque (Zoro) = 31 produits
- **Hors collections** : 3 produits (maillot de bain AOP, étuis kanji otaku, étuis mur brique × THE END)

### Produits restants à créer
- [ ] **Direction Coques FR+EN** : 20 coques (10 FR + 10 EN)
- [x] **Mythologie Mugs** : 10/10 créés (2026-05-04)
- [ ] **Mythologie Coques** : 9 coques manquantes (toutes sauf Zoro)
- [ ] **Renommer** : 4 produits Wanted EN → format standard (cosmétique)

## Projets Canva

- **"THE END"** : Wanted FR — 92 pages (tous les personnages Wanted en français)
- **"Copie de THE END"** : Wanted EN — 49 designs traduits automatiquement via l'outil de traduction intégré Canva
- **"FRUIT"** : Direction FR — 24 pages (10 personnages × variantes couleur) — exports dans `exports/direction-fr-dark/` et `direction-fr-light/`
- **Direction EN** : images régénérées manuellement (texte EN intégré dans l'IA) — exports dans `exports/direction-en-dark/` et `direction-en-light/`

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

## Ne jamais faire

- Ne jamais commit de tokens ou secrets dans le repo
- Ne jamais utiliser les noms originaux des personnages One Piece dans le code ou le contenu public
- Ne jamais générer de contenu qui reproduit directement des designs protégés par copyright
