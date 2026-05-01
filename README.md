# ホクノ — HOKUNO

**Toujours aller de l'avant.**

Hokuno (北の) est une marque streetwear manga française. Designs générés par IA, imprimés en Print on Demand via Printify, vendus sur Shopify + TikTok Shop.

---

## Collections

**WANTED** — Avis de recherche parodiques. Des personnages de manga vieillis par 30 ans de publication, épuisés, éreintés. Ils veulent juste que ça se termine. (~15 designs)

**MYTHOLOGIE** — Silhouettes divines en toge grecque. Chaque personnage dans sa couleur signature, auréole lumineuse. Épique et mystique. (8-10 designs)

**DIRECTION** — Silhouettes encrées avec citations motivationnelles. Toujours aller de l'avant. Le cœur de l'identité Hokuno. (8-10 designs)

## Produits

Chaque design est décliné en t-shirt, mug et coque de téléphone. Designs disponibles en français et en anglais (Wanted + Direction). Mythologie est universelle (pas de texte).

## Stack

- **Production** : Printify (POD)
- **Vente** : Shopify (principal) + TikTok Shop + Etsy (phase 2) + Amazon (phase 3)
- **Boutique** : Custom Shopify theme (Next.js, 3D, glassmorphisme) via Claude Code
- **App** : StoreMD — app Shopify développée par la même équipe

## Structure du repo

```
├── CONTEXT.md                        # Brand bible — source de vérité pour Claude Code
├── .claude/
│   └── skills/
│       └── printify/
│           └── SKILL.md              # Skill API Printify pour Claude Code
├── collections/
│   ├── wanted.json                   # Personnages collection Wanted
│   ├── direction.json                # Personnages collection Direction
│   └── mythologie.json               # Personnages collection Mythologie
├── assets/
│   └── logos/                        # Logpose + ホクノ typographie
├── seo/
│   ├── llms.txt                      # Fichier descriptif pour LLMs (GEO)
│   └── schemas/                      # Templates JSON-LD
└── config/
    └── products.json                 # Specs produits Printify
```

## Setup Claude Code

```bash
# 1. Cloner le repo
git clone https://github.com/ton-org/hokuno-store.git
cd hokuno-store

# 2. Configurer les API tokens (ne jamais commit)
export PRINTIFY_API_TOKEN=ton_token_printify
export SHOPIFY_ACCESS_TOKEN=ton_token_shopify
export SHOPIFY_STORE=hokuno.myshopify.com

# 3. Installer les skills externes
claude plugin marketplace add jezweb/claude-skills
claude plugin install shopify@jezweb-skills
claude plugin marketplace add freshtechbro/claudedesignskills

# 4. Lancer Claude Code
claude
```

Claude Code aura accès au `CONTEXT.md` (brand bible), au skill Printify, aux skills Shopify, et aux skills 3D/design pour construire la boutique.

## Environnement

| Variable | Description |
|----------|-------------|
| `PRINTIFY_API_TOKEN` | Token API Printify (Connections → Generate) |
| `SHOPIFY_ACCESS_TOKEN` | Token Admin API Shopify |
| `SHOPIFY_STORE` | URL du store (hokuno.myshopify.com) |

> ⚠️ Ne jamais commit les tokens. Utiliser des variables d'environnement ou un `.env` dans le `.gitignore`.

## Licence

Propriétaire — Tous droits réservés.
