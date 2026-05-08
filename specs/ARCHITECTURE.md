# specs/ARCHITECTURE.md — Architecture globale

> Contrat pour Claude Code. Aucune improvisation. Chaque décision est documentée ici.

---

## 1. STORES SHOPIFY

### Store de production — My Store 5

| Clé | Valeur |
|-----|--------|
| Nom interne Shopify | My Store 5 |
| URL admin | `s6btxa-q0.myshopify.com/admin` |
| Variable d'env | `SHOPIFY_STORE=s6btxa-q0.myshopify.com` |
| Token API | `SHOPIFY_ACCESS_TOKEN=atkn_xxxxxxxxxx` |
| Statut | À configurer — app dev à créer |

C'est le store final. Tout le travail de thème et de configuration se fait dessus.

### Store de développement — storemdtesttt

| Clé | Valeur |
|-----|--------|
| Nom interne Shopify | storemdtesttt |
| Statut | Store dev avec limitations, 430 produits publiés via Printify |
| Usage futur | Backup / test uniquement — ne plus développer dessus |

### Store Printify

| Clé | Valeur |
|-----|--------|
| Shop ID | `22774508` |
| Nom | "My new store" |
| Connexion actuelle | storemdtesttt via app Printify |
| Action requise | Connecter aussi à My Store 5 via Printify → Add store → Shopify |

---

## 2. STACK TECHNIQUE

| Couche | Technologie | Note |
|--------|-------------|------|
| Boutique | Shopify (plan à définir) | Héberge le thème, gère les paiements, commandes, clients |
| Production | Printify (POD) | Fabrication et expédition, connecté via app Shopify |
| Thème | Liquid + CSS + JS vanilla | Pas de framework (pas de React, pas de Next.js, pas de Tailwind) |
| Polices | Google Fonts — Inter (300-900) | Chargée via `<link>` dans `<head>` |
| Images | PNG dans `assets/` du thème | Uploadées via Shopify CLI ou API |
| Analytics | GA4, Meta Pixel, TikTok Pixel | Injectés dans theme.liquid, conditionnés par consentement cookies |
| SEO | JSON-LD natif dans le Liquid | Pas d'app tierce pour le schema — codé en dur dans le thème |

### Ce qu'on n'utilise PAS

- **Dawn** : on ne part pas du thème Dawn, on construit from scratch
- **Sections/blocs Shopify** : pas de `{% section %}` dans cette v1 — tout est dans theme.liquid et les templates
- **Online Store 2.0 JSON templates** : on utilise les templates `.liquid` classiques
- **JavaScript frameworks** : pas de React, Vue, Svelte, Alpine, jQuery
- **CSS frameworks** : pas de Tailwind, Bootstrap — CSS vanilla uniquement
- **Bundlers** : pas de Webpack, Vite, esbuild — les assets sont servis directement

---

## 3. ARCHITECTURE DU THÈME

### Principe central

Le thème Hokuno est **modulaire et organisé**. Le fichier `layout/theme.liquid` contient le layout global (head, navbar, footer, bottom nav mobile). Chaque template gère le contenu de sa page. Le CSS et le JS sont dans des fichiers séparés dans `assets/`, cachés par le CDN Shopify.

### Structure des fichiers du thème

```
shopify-theme/
├── layout/
│   └── theme.liquid              # Layout global : <head>, navbar, {{ content_for_layout }}, footer, bottom nav
│
├── templates/
│   ├── index.liquid              # Page d'accueil (hero, trust bar, collections, produits phares)
│   ├── collection.liquid         # Page collection (filtres, grille produits, pagination)
│   ├── list-collections.liquid   # Page /collections (grille des 4 collections)
│   ├── product.liquid            # Page produit (galerie, variantes, panier, backstory, similaires)
│   ├── cart.liquid               # Page panier (liste, quantités, sous-total, checkout)
│   ├── search.liquid             # Page recherche
│   ├── page.liquid               # Pages statiques (about, FAQ, mentions légales)
│   ├── page.contact.liquid       # Page contact (formulaire Liquid dédié)
│   ├── blog.liquid               # Liste des articles
│   ├── article.liquid            # Article unique
│   ├── 404.liquid                # Page 404
│   ├── password.liquid           # Page mot de passe (store protégé)
│   ├── gift_card.liquid          # Carte cadeau
│   └── customers/
│       ├── login.liquid          # Connexion
│       ├── register.liquid       # Inscription
│       ├── account.liquid        # Mon compte
│       └── order.liquid          # Détail commande
│
├── snippets/                     # Fragments réutilisables
│   ├── product-card.liquid       # Card produit (utilisée dans grilles collection + produits phares)
│   ├── collection-card.liquid    # Card collection (utilisée sur accueil + /collections)
│   ├── breadcrumbs.liquid        # Fil d'Ariane
│   ├── seo-jsonld.liquid         # Schema JSON-LD (Product, Organization, BreadcrumbList, CollectionPage)
│   ├── pagination.liquid         # Navigation pages
│   └── newsletter-form.liquid    # Formulaire newsletter footer
│
├── assets/
│   ├── hokuno.css                # CSS global unique — tout le style du site
│   ├── hokuno.js                 # JS global unique — navigation, cart AJAX, animations
│   ├── boussole-gold.png
│   ├── card-wanted.png
│   ├── card-direction.png
│   ├── card-mythologie.png
│   ├── card-design-hokuno.png
│   ├── hero-tshirt.png
│   ├── logo-hokuno-nav.png
│   └── logo-hokuno-transparent.png
│
├── config/
│   └── settings_schema.json      # Métadonnées du thème
│
└── locales/
    ├── fr.json                   # Traductions FR
    └── en.json                   # Traductions EN
```

### Répartition des fichiers

**`layout/theme.liquid` contient (~200 lignes) :**
- `<head>` complet (meta, fonts, lien vers hokuno.css)
- Snippet SEO JSON-LD (`{% render 'seo-jsonld' %}`)
- Navbar (desktop + hamburger mobile)
- `{{ content_for_layout }}` — injecte le contenu du template actif
- Footer
- Bottom nav mobile
- Lien vers hokuno.js avant `</body>`

**`assets/hokuno.css` contient :**
- Reset
- Variables couleurs/tailles (via custom properties CSS si besoin)
- Styles navbar, hero, trust bar, collections, produits, footer, bottom nav
- Media queries mobile/tablette/desktop
- Animations (fadeUp, hover effects)

**`assets/hokuno.js` contient :**
- Navigation mobile (hamburger toggle)
- Cart AJAX (add to cart sans rechargement)
- Galerie produit (changement d'image au clic sur miniature)
- Sélecteur de variantes (couleur → image, taille → variant ID)
- Animations au scroll (IntersectionObserver)
- Cookies RGPD (consentement → chargement analytics)

**Les templates contiennent :**
- Le contenu HTML/Liquid spécifique à chaque page
- Appels aux snippets : `{% render 'product-card', product: product %}`
- Pas de `<head>`, `<nav>`, `<footer>` — c'est dans theme.liquid

**Chargement CSS/JS dans theme.liquid :**
```liquid
<!-- Dans <head> -->
<link rel="stylesheet" href="{{ 'hokuno.css' | asset_url }}">

<!-- Avant </body> -->
<script src="{{ 'hokuno.js' | asset_url }}" defer></script>
```

### État actuel vs cible

Le thème actuel a tout dans theme.liquid (497 lignes, CSS inline, templates vides). La migration :
1. Extraire le CSS du `<style>` vers `assets/hokuno.css`
2. Extraire le JS (à écrire) vers `assets/hokuno.js`
3. Extraire le contenu de chaque `{% if template == 'xxx' %}` vers son template
4. Créer les snippets pour le code réutilisé
5. Ajouter les locales FR/EN
6. Theme.liquid ne garde que le layout (~200 lignes)

---

## 4. ORGANISATION DU REPO

```
hokuno-store/
├── CONTEXT.md                    # Brand bible — NE PAS MODIFIER sans validation
├── CLAUDE.md                     # Instructions Claude Code + état du projet
├── INVENTAIRE.md                 # Inventaire Printify 430 produits
├── PRICING.md                    # Coûts, prix, marges
├── TODO.md                       # Roadmap
├── PLAN-RECONSTRUCTION-HOKUNO-v2.md  # Plan des 18 specs + phases
│
├── specs/                        # 18 fichiers de spécification (contrats)
│   ├── ARCHITECTURE.md           # Ce fichier
│   ├── NAVIGATION.md
│   ├── COLLECTIONS.md
│   ├── PAGES.md
│   ├── PRODUIT.md
│   ├── MOCKUPS.md
│   ├── MIGRATION.md
│   ├── THEME.md
│   ├── SEO.md
│   ├── CONFIG-SHOPIFY.md
│   ├── MOBILE.md
│   ├── CHECKLIST.md
│   ├── ANALYTICS.md
│   ├── EMAILS.md
│   ├── LEGAL.md
│   ├── MULTILINGUE.md
│   ├── DOMAINE.md
│   └── SOCIAL.md
│
├── collections/                  # JSON personnages + IDs Printify
│   ├── wanted.json               # 46 personnages
│   ├── direction.json            # 10 personnages
│   └── mythologie.json           # 10 personnages
│
├── shopify-theme/                # Thème Shopify complet (push via Shopify CLI)
│   ├── layout/
│   ├── templates/
│   ├── snippets/
│   ├── assets/
│   ├── config/
│   └── locales/
│
├── assets/
│   ├── theme/                    # 8 images source (originaux renommés)
│   ├── originals/                # 7 images source (noms lisibles)
│   └── design-reference/         # 4 mockups ChatGPT de référence
│
└── archive/
    └── scripts/                  # Scripts Python Printify (usage historique)
```

---

## 5. PRINCIPES DE DÉVELOPPEMENT

### Design

- Fond body : `#000000` — toujours, partout, sans exception
- Couleur accent : `#D4A853` (doré) — boutons CTA, liens hover, highlights
- Texte principal : `#FFFFFF`
- Texte secondaire : `rgba(255,255,255,0.5)` à `rgba(255,255,255,0.85)`
- Glassmorphism : `background: rgba(255,255,255,0.04); backdrop-filter: blur(24px); border: 1px solid rgba(255,255,255,0.08)`
- Toutes les valeurs CSS exactes sont dans `specs/THEME.md`

### Code

- **CSS** : un seul fichier `assets/hokuno.css` — tout le style du site
- **JS** : un seul fichier `assets/hokuno.js` — toute l'interactivité du site
- **Liquid** : utiliser les filtres natifs (`| money`, `| image_url`, `| asset_url`, `| t`)
- **Classes CSS** : nommage court et descriptif (`.nav`, `.hero`, `.prod-card`, `.btn-gold`) — pas de BEM, pas de utility classes
- **IDs** : réservés aux ancres et aux hooks JS — jamais pour le style
- **Inline styles** : interdits — tout dans hokuno.css
- **Commentaires** : en français dans le Liquid, en anglais dans le CSS/JS
- **Images** : toujours utiliser `{{ 'filename.png' | asset_url }}` — jamais de chemins en dur

### Performance

- Images : lazy loading via `loading="lazy"` sur tout sauf le hero
- Fonts : `display=swap` sur Google Fonts
- CSS : un seul fichier, caché par le CDN Shopify après la première visite
- JS : un seul fichier, chargé avec `defer`
- Pas d'app Shopify inutile — chaque app ajoute du JS et ralentit le site

### Accessibilité minimum

- Alt text sur toutes les images : `alt="{{ product.title }}"` ou `alt="HOKUNO — [description]"`
- Touch targets mobile : minimum 44×44px
- Contraste texte/fond : respecté par défaut (blanc sur noir)
- Formulaires : `<label>` associé à chaque `<input>`

---

## 6. DÉPLOIEMENT DU THÈME

### Via Shopify CLI

```bash
# Depuis le dossier shopify-theme/
shopify theme dev --store=s6btxa-q0.myshopify.com    # Preview local
shopify theme push --store=s6btxa-q0.myshopify.com   # Push en mode dev
shopify theme publish                                # Publier en production
```

### Via API Admin (alternative)

Upload des fichiers du thème via l'API REST/GraphQL Shopify Admin si le CLI n'est pas disponible dans le Codespace.

### Workflow

1. Modifier les fichiers dans `shopify-theme/`
2. Preview avec `shopify theme dev` (preview URL temporaire)
3. Valider visuellement (desktop + mobile)
4. Push en mode dev pour tester sur le vrai store
5. Itérer jusqu'à validation
6. Publish en production

---

## 7. CONVENTIONS DE NOMMAGE

| Élément | Convention | Exemple |
|---------|------------|---------|
| Fichiers Liquid | kebab-case | `product-card.liquid` |
| Classes CSS | kebab-case court | `.prod-card`, `.col-btn`, `.nav-logo` |
| Variables JS | camelCase | `cartCount`, `mobileNav` |
| Fichiers images | kebab-case | `card-wanted.png`, `hero-tshirt.png` |
| Clés de traduction | dot-notation groupées | `hero.title`, `nav.collections`, `product.add_to_cart` |
| Handles Shopify (collections) | kebab-case | `wanted`, `direction`, `mythologie`, `design-hokuno` |

---

## 8. DÉPENDANCES EXTERNES

| Dépendance | URL | Usage |
|------------|-----|-------|
| Google Fonts — Inter | `fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900` | Typographie unique du site |

Aucune autre dépendance externe. Pas de CDN JS, pas de librairie CSS, pas d'icônes externes (les icônes sont en emoji Unicode ou en SVG inline).

---

## 9. CE QUE CLAUDE CODE NE DOIT JAMAIS FAIRE

- Installer Dawn ou un starter theme et le modifier
- Ajouter un framework CSS ou JS
- Créer plusieurs fichiers CSS ou JS (un seul de chaque : hokuno.css + hokuno.js)
- Utiliser des sections Shopify (`{% section 'xxx' %}`)
- Utiliser des JSON templates (Online Store 2.0)
- Modifier les fichiers dans `collections/`, `CONTEXT.md`, `PRICING.md` sans validation explicite
- Utiliser des inline styles (`style="..."`) dans le HTML
- Hardcoder des URLs de produits ou d'images
- Utiliser les noms originaux des personnages One Piece
- Commit des tokens ou secrets
