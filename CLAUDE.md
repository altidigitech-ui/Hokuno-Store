# CLAUDE.md — Instructions pour Claude Code

## Contexte du projet

Ce repo est la source de vérité pour **Hokuno** (ホクノ), une marque streetwear manga en Print on Demand.
Lis `CONTEXT.md` en premier — il contient toute la brand bible : identité, collections, produits, SEO/GEO, stratégie multi-canal.

## Structure

```
├── CONTEXT.md                        # Brand bible complète
├── .claude/skills/printify/SKILL.md  # Référence API Printify
├── collections/
│   ├── wanted.json                   # Personnages collection Wanted (46 — tous sur Printify FR+EN)
│   ├── direction.json                # Personnages collection Direction (10)
│   └── mythologie.json               # Personnages collection Mythologie (10)
```

## État actuel (2026-05-03)

- **Shop Printify** : ID `22774508`, nom "My new store", **sales channel : disconnected** (à connecter Shopify + TikTok Shop)
- **Total produits** : 320 (voir détail ci-dessous)
- **Wanted** : 46/46 personnages complets FR+EN — 46 t-shirts FR light, 46 FR dark, 46 EN light, 46 EN dark, 46 mugs FR, 46 mugs EN = 276 produits
  - ⚠️ wanted-018 Bartolomiou Kouma : produits EN nommés "TEST-..." à renommer
- **Direction** : 10/10 personnages FR (light+dark = 20 t-shirts), 1 mug (Luffy seulement) — versions EN non créées (ChatGPT/DALL-E requis)
- **Mythologie** : 10/10 version noir, 8/10 version light (Choper et Robin manquent), 1 mug, 1 coque = 20 produits
- **Hors collections** : 3 produits non référencés dans les JSONs (maillot de bain AOP, étuis kanji otaku, étuis mur brique × THE END)

### Produits restants à créer
- [ ] **Direction EN** : 10 personnages × 2 versions = 20 t-shirts (régénération complète ChatGPT)
- [ ] **Direction Mugs** : 9 mugs manquants (tous sauf Luffy)
- [ ] **Mythologie light** : 2 t-shirts manquants (Choper, Robin)
- [ ] **Renommer** : 2 produits TEST Bartolomiou Kouma EN → format standard
- [ ] **Intégrer dans JSON** : 3 produits hors collections (maillot, 2 coques)

## Projets Canva

- **"THE END"** : Wanted FR — 92 pages (tous les personnages Wanted en français)
- **"Copie de THE END"** : Wanted EN — 49 designs traduits automatiquement via l'outil de traduction intégré Canva
- **"FRUIT"** : Direction FR — 24 pages (10 personnages × variantes couleur)

## Contraintes importantes

- **Punchline Wanted** : identique pour TOUS les personnages — `"ÇA NE FINIRA JAMAIS..."` (FR) / `"IT WILL NEVER END..."` (EN). Ne jamais créer de punchlines personnalisées.
- **Texte secondaire Wanted** : identique pour tous — `"CETTE PRIME TRAINE DEPUIS 12 ANS. HONNETEMENT, SI VOUS LE TROUVEZ DEMANDEZ-LUI SIL EST TOUJOURS PARTANT"` (FR) / `"THIS BOUNTY HAS BEEN RUNNING FOR 12 YEARS. HONESTLY, IF YOU FIND HIM ASK HIM IF HE'S STILL UP FOR IT"` (EN)
- **Quote Direction** : identique pour TOUS — `"JE N'AI PAS BESOIN D'UN PLAN.. JUSTE D'UNE DIRECTION."` (FR) / `"I DON'T NEED A PLAN.. JUST A DIRECTION."` (EN)
- **Direction EN** : le texte est intégré dans l'image IA, non modifiable dans Canva. Les versions EN doivent être régénérées entièrement avec ChatGPT / DALL-E (même silhouette, texte EN intégré).

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
