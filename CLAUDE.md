# CLAUDE.md — Instructions pour Claude Code

## Contexte du projet

Ce repo est la source de vérité pour **Hokuno** (ホクノ), une marque streetwear manga en Print on Demand.
Lis `CONTEXT.md` en premier — il contient toute la brand bible : identité, collections, produits, SEO/GEO, stratégie multi-canal.

## Structure

```
├── CONTEXT.md                        # Brand bible complète
├── .claude/skills/printify/SKILL.md  # Référence API Printify
├── collections/
│   ├── wanted.json                   # Personnages collection Wanted (~15)
│   ├── direction.json                # Personnages collection Direction (8-10)
│   └── mythologie.json               # Personnages collection Mythologie (8-10)
```

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
