# SETUP-CLAUDE-CODE.md — Guide d'installation complet

> Ce fichier détaille TOUT ce qu'il faut installer et configurer dans le Codespace / environnement Claude Code
> AVANT de commencer à coder le thème et migrer vers My Store 5.
> À exécuter une seule fois, dans l'ordre.

---

## SOMMAIRE

1. [Outils système](#1-outils-système)
2. [Plugins Claude Code (marketplace)](#2-plugins-claude-code-marketplace)
3. [Skills à cloner (repos GitHub)](#3-skills-à-cloner-repos-github)
4. [Fichier de référence — CLAUDE.md Shopify Best Practices](#4-fichier-de-référence)
5. [Skill custom Printify (déjà dans le repo)](#5-skill-printify-déjà-dans-le-repo)
6. [Variables d'environnement](#6-variables-denvironnement)
7. [Scopes API Shopify](#7-scopes-api-shopify)
8. [Vérification post-installation](#8-vérification-post-installation)
9. [Ordre d'exécution](#9-ordre-dexécution)

---

## 1. OUTILS SYSTÈME

### 1.1 Shopify CLI

Le CLI officiel de Shopify pour interagir avec les thèmes et le store.

```bash
npm install -g @shopify/cli @shopify/theme
```

**Ce que ça permet :**
- `shopify theme dev` — lancer un serveur de preview local du thème
- `shopify theme push` — pousser le thème sur le store (mode dev ou production)
- `shopify theme pull` — récupérer le thème actuel du store
- `shopify theme list` — lister les thèmes du store
- `shopify theme publish` — publier un thème en production

**Vérification :**
```bash
shopify version
# Doit afficher la version (ex: 3.x.x)
```

### 1.2 ImageMagick

Pour traiter les images (favicon, redimensionnement, conversion).

```bash
sudo apt-get update && sudo apt-get install -y imagemagick
```

**Ce que ça permet :**
- Générer les favicons (32x32, 16x16, 180x180) depuis `boussole-gold.png`
- Convertir/redimensionner des images
- Voir `specs/SOCIAL.md` §5 pour les commandes exactes

**Vérification :**
```bash
convert --version
# Doit afficher ImageMagick + version
```

---

## 2. PLUGINS CLAUDE CODE (marketplace)

Les plugins s'installent directement dans Claude Code via les commandes `/plugin`.
Claude Code doit tenter chaque installation. Si une commande échoue (plugin non trouvé, marketplace indisponible), il continue avec les suivants.

### 2.1 Shopify AI Toolkit — Plugin officiel Shopify

```
claude install-plugin shopify
```

**Source :** https://shopify.dev/docs/apps/build/ai-toolkit

**Ce que ça apporte :**
- MCP server Shopify intégré
- Accès direct à la GraphQL Admin API depuis Claude Code
- Gestion des thèmes, produits, collections, pages
- Auto-complétion et validation Liquid

**⚠️ Note :** ce plugin est documenté par Shopify mais son installation exacte peut varier selon la version de Claude Code. Si `claude install-plugin shopify` échoue, essayer :
```
/plugin install shopify
```
ou chercher dans la marketplace :
```
/plugin search shopify
```

### 2.2 jezweb/claude-skills → Plugin Shopify

```
/plugin marketplace add jezweb/claude-skills
/plugin install shopify@jezweb-skills
```

**Source :** https://github.com/jezweb/claude-skills

**Ce que ça apporte — 3 skills :**

| Skill | Ce qu'il fait |
|-------|--------------|
| `shopify-setup` | Configure le token API, teste la connexion, vérifie les scopes |
| `shopify-products` | CRUD produits via GraphQL Admin API (single + bulk CSV) |
| `shopify-content` | Crée des pages, articles de blog, SEO metadata, navigation |

**Pourquoi c'est utile pour Hokuno :**
- Créer les 4 collections automatiques via API
- Créer les pages statiques (about, FAQ, contact, mentions-legales)
- Créer le blog "Journal"
- Gérer les tags produits (design-hokuno, lang-fr, lang-en) en batch
- Corriger les 68 titres Wanted /17→/46

### 2.3 mrgoonie/claudekit-skills → Plugin Shopify

```
/plugin marketplace add mrgoonie/claudekit-skills
/plugin install shopify@claudekit-skills
```

**Source :** https://github.com/mrgoonie/claudekit-skills

**Ce que ça apporte :**
- Skills pour apps Shopify, extensions, thèmes Liquid
- Patterns GraphQL optimisés
- Guardrails pour éviter les erreurs courantes Liquid

### 2.4 freshtechbro/claudedesignskills → Plugin Design 3D/Animation

```
/plugin marketplace add freshtechbro/claudedesignskills
/plugin install core-3d-animation
```

**Source :** https://github.com/freshtechbro/claudedesignskills

**Ce que ça apporte — 23 skills de design :**
- Three.js, WebGL
- GSAP, ScrollTrigger
- React Three Fiber
- Framer Motion
- Glassmorphism, effets visuels
- Scroll effects, parallax

**Pourquoi c'est utile pour Hokuno :**
- Le thème utilise du glassmorphism sur la navbar, trust bar, bottom nav
- Les animations fadeUp, hover effects
- Si en v2 on ajoute des effets 3D (boussole animée, etc.)

**⚠️ Note :** Ce plugin est optionnel au lancement. Le thème v1 utilise du CSS vanilla (pas de Three.js). Mais il sera utile pour les itérations futures.

---

## 3. SKILLS À CLONER (repos GitHub)

Les skills se clonent dans le répertoire des skills locaux de Claude Code.

### 3.1 dylanreed/shopify-theme-design

```bash
# Créer le dossier si nécessaire
mkdir -p ~/.claude/skills/local 2>/dev/null || mkdir -p ~/.claude/plugins/local 2>/dev/null

# Cloner
cd ~/.claude/skills/local 2>/dev/null || cd ~/.claude/plugins/local
git clone https://github.com/dylanreed/shopify-theme-design.git
```

**Source :** https://github.com/dylanreed/shopify-theme-design

**Ce que ça apporte :**
- Workflow structuré pour créer des thèmes Shopify de qualité marketplace
- **Étape 1 — Vibe Discovery** : 7 questions pour définir la direction esthétique
- **Étape 2 — HTML Preview** : coder le thème en HTML/CSS statique d'abord
- **Étape 3 — Liquid Conversion** : convertir le HTML en templates Liquid
- Évite les "Dawn clones" (thèmes génériques)
- Conventions de qualité marketplace

**Pourquoi c'est critique pour Hokuno :**
Le workflow HTML → Liquid est exactement ce que prescrit le plan (Phase 5, étape 16). On code le thème en HTML d'abord pour valider le visuel, PUIS on convertit en Liquid.

### 3.2 Microck/ordinary-claude-skills

```bash
cd ~/.claude/skills/local 2>/dev/null || cd ~/.claude/plugins/local
git clone https://github.com/Microck/ordinary-claude-skills.git
```

**Source :** https://github.com/Microck/ordinary-claude-skills

**Ce que ça apporte :**
- Skill `shopify-api` complet
- OAuth flow
- GraphQL + REST API patterns
- Rate limiting et gestion d'erreurs
- Webhooks
- Référence technique pour l'API Shopify Admin

---

## 4. FICHIER DE RÉFÉRENCE

### Karim Tarek — CLAUDE.md Shopify Best Practices

**Source :** https://gist.github.com/karimmtarek/3a8a636a05ae1c349ad0bba9d10425f0

**Ce que c'est :**
Un fichier `CLAUDE.md` complet avec toutes les conventions Shopify pour Claude Code :
- Structure Liquid (layout, templates, sections, snippets, locales)
- Performance (lazy loading, critical CSS, JS defer)
- Cart API (AJAX cart, notifications)
- SEO (meta tags, JSON-LD, canonical)
- Accessibilité (aria labels, focus management)
- Conventions de nommage

**Comment l'utiliser :**
1. Télécharger le gist manuellement (ouvrir l'URL dans un navigateur)
2. Extraire les best practices pertinentes
3. Les merger dans le `CLAUDE.md` du repo Hokuno (déjà existant)

**⚠️ Note :** Le gist peut être inaccessible par API (erreur 403). Le télécharger manuellement via le navigateur si besoin. Notre `CLAUDE.md` contient déjà les conventions Hokuno — les best practices de Karim Tarek viendraient compléter la section Liquid/Shopify.

---

## 5. SKILL PRINTIFY (déjà dans le repo)

**Emplacement :** `.claude/skills/printify/SKILLS.md` (265 lignes)

**Ce qu'il contient :**
- Authentification Printify API (`PRINTIFY_API_TOKEN`)
- Endpoints : shops, products, images, publishing
- Workflow : créer un produit, upload image, publier vers Shopify
- Structure de données : product JSON, variants, print_areas
- Shop ID actuel : `22774508` (storemdtesttt)

**Déjà prêt** — pas besoin de l'installer, il est dans le repo.

---

## 6. VARIABLES D'ENVIRONNEMENT

### 6.1 Token Printify

```bash
export PRINTIFY_API_TOKEN=ton_token_printify
```

**Où le trouver :** Printify → Settings → Connections → Personal access token → Generate

**Statut :** Tu l'as déjà.

### 6.2 Token Shopify Admin API (My Store 5)

```bash
export SHOPIFY_ACCESS_TOKEN=shpat_xxxxxxxxxx
export SHOPIFY_STORE=mystore5.myshopify.com
```

**Où le trouver :**
1. Aller sur `mystore5.myshopify.com/admin`
2. Settings → Apps → Develop apps
3. "Create an app" → nom : `Hokuno Admin`
4. Configurer les Admin API scopes (voir section 7)
5. "Install app"
6. Copier le token `shpat_xxxxxxxxxx` qui apparaît

**⚠️ IMPORTANT :**
- Le token n'est affiché qu'UNE SEULE FOIS. Le copier immédiatement.
- Ne JAMAIS commiter le token dans le repo. Toujours en variable d'environnement.
- Si perdu, il faut supprimer l'app et en recréer une.

### 6.3 Configuration dans le Codespace

Ajouter dans `~/.bashrc` ou `~/.zshrc` (ou dans les secrets du Codespace) :

```bash
# Hokuno — API tokens
export PRINTIFY_API_TOKEN="eyJhbGci..."
export SHOPIFY_ACCESS_TOKEN="shpat_..."
export SHOPIFY_STORE="mystore5.myshopify.com"
```

Puis recharger :
```bash
source ~/.bashrc
```

---

## 7. SCOPES API SHOPIFY

Lors de la création de l'app dev (étape 6.2), sélectionner ces scopes :

| Scope | Pourquoi |
|-------|----------|
| `read_products` | Lire les produits publiés par Printify |
| `write_products` | Modifier les titres (68 corrections /17→/46), ajouter des tags |
| `read_themes` | Lister les thèmes existants |
| `write_themes` | Pousser le thème Hokuno |
| `read_content` | Lire les pages et le blog |
| `write_content` | Créer les pages (about, FAQ, contact, mentions-legales) et le blog |
| `read_customers` | Lire les comptes clients |
| `read_orders` | Lire les commandes (dashboard, analytics) |
| `read_inventory` | Lire le stock (affiché sur les fiches produit) |
| `read_script_tags` | Lire les scripts injectés |
| `write_script_tags` | Injecter les scripts analytics (GA4, Meta Pixel) |
| `read_locales` | Lire les traductions du thème |
| `write_locales` | Uploader fr.json et en.json |
| `read_publications` | Lire les canaux de publication |
| `write_publications` | Publier les produits sur le canal Online Store |

**Sélectionner TOUS ces scopes.** Si un scope est oublié, certaines commandes API échoueront avec une erreur 403.

---

## 8. VÉRIFICATION POST-INSTALLATION

Après avoir tout installé, exécuter ces vérifications :

```bash
echo "=== 1. Shopify CLI ===" 
shopify version

echo "=== 2. ImageMagick ===" 
convert --version | head -1

echo "=== 3. Printify API ===" 
curl -s -H "Authorization: Bearer $PRINTIFY_API_TOKEN" \
  https://api.printify.com/v1/shops.json | python3 -m json.tool | head -5

echo "=== 4. Shopify API ===" 
curl -s -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN" \
  "https://$SHOPIFY_STORE/admin/api/2024-01/shop.json" | python3 -m json.tool | head -5

echo "=== 5. Thèmes sur le store ===" 
shopify theme list --store=$SHOPIFY_STORE

echo "=== 6. Nombre de produits ===" 
curl -s -H "X-Shopify-Access-Token: $SHOPIFY_ACCESS_TOKEN" \
  "https://$SHOPIFY_STORE/admin/api/2024-01/products/count.json"
```

**Résultats attendus :**
- (1) Version Shopify CLI affichée
- (2) Version ImageMagick affichée
- (3) JSON avec la liste des shops Printify (dont shop_id 22774508)
- (4) JSON avec les infos du store My Store 5
- (5) Liste des thèmes (au moins le thème par défaut Dawn)
- (6) `{"count": 0}` (aucun produit avant la migration) ou `{"count": 430}` (après)

**Si (3) ou (4) échoue** → vérifier le token correspondant.
**Si (5) échoue** → vérifier que `SHOPIFY_STORE` est correct et que le Shopify CLI est authentifié.

---

## 9. ORDRE D'EXÉCUTION

```
ÉTAPE 1 — Toi (manuel, avant Claude Code)
  ├── Créer l'app dev sur My Store 5 (section 6.2)
  ├── Copier le token shpat_
  ├── Connecter Printify à My Store 5 (Printify → Add store)
  └── Renommer la coque "The End Brique" sur Printify

ÉTAPE 2 — Claude Code (automatique)
  ├── Configurer les env vars (section 6)
  ├── Installer Shopify CLI + ImageMagick (section 1)
  ├── Installer les plugins marketplace (section 2)
  │   ├── Shopify AI Toolkit
  │   ├── jezweb/claude-skills → shopify
  │   ├── mrgoonie/claudekit-skills → shopify
  │   └── freshtechbro/claudedesignskills → core-3d-animation
  ├── Cloner les skills GitHub (section 3)
  │   ├── dylanreed/shopify-theme-design
  │   └── Microck/ordinary-claude-skills
  ├── Vérifier les connexions API (section 8)
  └── Commit les 18 specs dans specs/

ÉTAPE 3 — Claude Code (thème + migration)
  └── Suivre specs/MIGRATION.md phases 3-9
```

---

## RÉCAPITULATIF — TOUT CE QUI DOIT ÊTRE INSTALLÉ

| # | Quoi | Type | Commande | Critique ? |
|---|------|------|----------|:----------:|
| 1 | Shopify CLI | npm global | `npm install -g @shopify/cli @shopify/theme` | 🔴 Oui |
| 2 | ImageMagick | apt | `sudo apt-get install -y imagemagick` | 🟡 Non (favicon seulement) |
| 3 | Shopify AI Toolkit | plugin Claude Code | `claude install-plugin shopify` | 🟡 Tenter, continuer si échoue |
| 4 | jezweb → Shopify skills | plugin Claude Code | `/plugin marketplace add jezweb/claude-skills` | 🟡 Tenter, continuer si échoue |
| 5 | mrgoonie → Shopify skills | plugin Claude Code | `/plugin marketplace add mrgoonie/claudekit-skills` | 🟡 Tenter, continuer si échoue |
| 6 | freshtechbro → Design skills | plugin Claude Code | `/plugin marketplace add freshtechbro/claudedesignskills` | 🟢 Optionnel v1 |
| 7 | dylanreed/shopify-theme-design | git clone skill | `git clone` dans `~/.claude/skills/local/` | 🔴 Oui (workflow thème) |
| 8 | Microck/ordinary-claude-skills | git clone skill | `git clone` dans `~/.claude/skills/local/` | 🟡 Référence API |
| 9 | Karim Tarek CLAUDE.md | gist à télécharger | Manuel via navigateur | 🟡 Best practices Liquid |
| 10 | Printify skill | déjà dans le repo | `.claude/skills/printify/SKILLS.md` | ✅ Déjà prêt |
| 11 | PRINTIFY_API_TOKEN | env var | `export PRINTIFY_API_TOKEN=...` | 🔴 Oui |
| 12 | SHOPIFY_ACCESS_TOKEN | env var | `export SHOPIFY_ACCESS_TOKEN=shpat_...` | 🔴 Oui |
| 13 | SHOPIFY_STORE | env var | `export SHOPIFY_STORE=mystore5.myshopify.com` | 🔴 Oui |

**🔴 Critique** = le projet ne peut pas avancer sans.
**🟡 Important** = tenter l'installation, continuer sans si échoue. L'API REST/GraphQL Shopify couvre tous les besoins même sans plugins.
**🟢 Optionnel** = utile pour les versions futures, pas nécessaire pour le lancement v1.
