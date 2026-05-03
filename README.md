# ホクノ — HOKUNO

**Toujours aller de l'avant.**

Hokuno (北の) est une marque streetwear manga française. Designs générés par IA, imprimés en Print on Demand via Printify, vendus sur Shopify + TikTok Shop.

---

## Collections

**WANTED** — Avis de recherche parodiques. Des personnages de manga vieillis par 30 ans de publication, épuisés, éreintés. Ils veulent juste que ça se termine. 46 personnages FR+EN.

**MYTHOLOGIE** — Silhouettes divines en toge grecque. Chaque personnage dans sa couleur signature, auréole lumineuse. Épique et mystique. 10 personnages, design universel (sans texte).

**DIRECTION** — Silhouettes encrées avec citations motivationnelles. Toujours aller de l'avant. Le cœur de l'identité Hokuno. 10 personnages FR+EN.

## Produits (382 sur Printify)

Chaque design est décliné en t-shirt (light + dark), mug et coque de téléphone. Wanted + Direction disponibles en français et en anglais. Mythologie est universelle (sans texte).

## Stack

- **Production** : Printify (POD)
- **Vente** : Shopify (principal) + TikTok Shop + Etsy (phase 2) + Amazon (phase 3)
- **Boutique** : Custom Shopify theme (Next.js, 3D, glassmorphisme) via Claude Code
- **App** : StoreMD — app Shopify développée par la même équipe

## Structure du repo

```
├── CONTEXT.md                        # Brand bible — source de vérité pour Claude Code
├── CLAUDE.md                         # Instructions Claude Code + état du projet
├── INVENTAIRE.md                     # Inventaire complet Printify (342 produits + IDs)
├── TODO.md                           # Feuille de route par phase
├── .claude/
│   └── skills/
│       └── printify/
│           └── SKILLS.md             # Skill API Printify pour Claude Code
├── collections/
│   ├── wanted.json                   # 46 personnages Wanted (FR+EN, tous IDs Printify)
│   ├── direction.json                # 10 personnages Direction (FR+EN, IDs Printify)
│   └── mythologie.json               # 10 personnages Mythologie (IDs Printify)
├── exports/
│   ├── wanted-fr/                    # Designs Wanted FR (posters 1198×1690)
│   ├── wanted-en/                    # Designs Wanted EN
│   ├── direction-fr-dark/            # 10 PNG Direction FR — fond transparent (t-shirts noirs)
│   ├── direction-fr-light/           # 10 PNG Direction FR — fond transparent (t-shirts clairs)
│   ├── direction-en-dark/            # 10 PNG Direction EN — fond transparent (t-shirts noirs)
│   └── direction-en-light/           # 10 PNG Direction EN — fond transparent (t-shirts clairs)
└── scripts/
    ├── update_direction_backs.py     # Met à jour le dos des t-shirts Direction FR
    ├── create_direction_en.py        # Crée les t-shirts Direction EN depuis templates FR
    ├── restore_front_logo.py         # Restaure le logo front sur les produits Direction
    ├── fix_front_logo_scale.py       # Corrige le scale du logo front
    └── create_direction_mugs.py      # Crée les 40 mugs Direction (FR+EN, light+dark)
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
