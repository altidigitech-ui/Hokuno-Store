# specs/NAVIGATION.md — Navigation complète

> Contrat pour Claude Code. Chaque lien, chaque icône, chaque comportement est défini ici.
> La navigation doit être fluide, instantanée et sans friction sur desktop comme mobile.

---

## 1. NAVBAR DESKTOP

### Position et style

- Position : `fixed`, flottante, centrée horizontalement
- Top : `20px` du haut de la page
- Largeur : `calc(100% - 48px)`, max `1440px`
- Z-index : `9999`
- Style : glassmorphism — `background: rgba(255,255,255,0.04); backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px`
- Padding : `16px 32px`
- Transition : `all 0.3s ease`
- Toujours visible (pas de hide-on-scroll)

### Structure : 3 zones

```
[LOGO]          [LIENS PRINCIPAUX]          [ACTIONS DROITE]
```

### Zone gauche — Logo

| Élément | Détail |
|---------|--------|
| Image | `logo-hokuno-transparent.png` via `{{ 'logo-hokuno-transparent.png' | asset_url }}` |
| Hauteur desktop | `65px` |
| Hauteur mobile | `30px` |
| Style image | `mix-blend-mode: screen; filter: brightness(1.2); background: transparent` |
| Lien | `/` (retour accueil) |
| Alt | `HOKUNO` |

### Zone centre — Liens principaux

| Texte affiché | href | Comportement |
|---------------|------|-------------|
| COLLECTIONS | `/collections` | Page grille des 4 collections |
| NOUVEAUTÉS | `/collections/all?sort_by=created-descending` | Tous les produits triés par date |
| À PROPOS | `/pages/about` | Page statique about |
| JOURNAL | `/blogs/journal` | Page blog |

Style des liens :
- Font-size : `12.5px`
- Font-weight : `500`
- Letter-spacing : `2px`
- Text-transform : `uppercase`
- Couleur : `rgba(255,255,255,0.85)`
- Hover : couleur `#D4A853`, transition `0.3s`

### Zone droite — Actions

| Élément | href | Détail |
|---------|------|--------|
| FR \| EN | — | Sélecteur de langue (voir section 6) |
| Icône loupe (SVG inline) | `/search` | Ouvre la page recherche |
| Icône compte (SVG inline) | `/account` | Page connexion/compte |
| Icône panier (SVG inline) + compteur | `/cart` | Compteur = `{{ cart.item_count }}`, mis à jour en AJAX |

Les icônes sont en SVG inline (pas d'emoji) pour un rendu net et cohérent. Taille : `18×18px`, stroke `1.5px`, couleur `currentColor`.

Style des actions :
- Font-size : `12.5px`
- Font-weight : `500`
- Letter-spacing : `1px`
- Couleur : `rgba(255,255,255,0.75)`
- Hover : couleur `#D4A853`
- Gap entre les actions : `28px`

### Détection page active

Le lien correspondant à la page en cours a la couleur `#D4A853` et le font-weight `600`.

```liquid
{%- assign nav_links = "collections,nouveautes,about,journal" | split: "," -%}

<!-- Dans chaque lien : -->
<a href="/collections" {% if template == 'list-collections' or template == 'collection' %}class="nav-active"{% endif %}>COLLECTIONS</a>
<a href="/collections/all?sort_by=created-descending" {% if canonical_url contains 'sort_by=created' %}class="nav-active"{% endif %}>NOUVEAUTÉS</a>
<a href="/pages/about" {% if page.handle == 'about' %}class="nav-active"{% endif %}>À PROPOS</a>
<a href="/blogs/journal" {% if template == 'blog' or template == 'article' %}class="nav-active"{% endif %}>JOURNAL</a>
```

CSS :
```css
.nav-active { color: #D4A853 !important; font-weight: 600; }
```

---

## 2. NAVBAR MOBILE (<768px)

### Header mobile sticky

- Position : `fixed`, en haut de l'écran
- Top : `12px`
- Largeur : `calc(100% - 24px)`, centré
- Style : glassmorphism (même que desktop, border-radius `10px`)
- Padding : `12px 20px`
- Contenu visible : logo à gauche (height `30px`), hamburger à droite
- Les liens principaux (`.nav-links`) et les actions (`.nav-right`) sont `display: none`

### Bouton hamburger

- 3 barres horizontales : largeur `22px`, épaisseur `1.5px`, couleur `#FFFFFF`, gap `5px`
- Padding tactile : `8px` (zone de touch effective > 44×44px)
- Transition : `all 0.3s ease`

**Animation hamburger → X quand le menu est ouvert :**
```css
/* Menu ouvert : classe .menu-open sur <body> */
.menu-open .nav-hamburger span:nth-child(1) {
  transform: rotate(45deg) translate(4.5px, 4.5px);
}
.menu-open .nav-hamburger span:nth-child(2) {
  opacity: 0;
}
.menu-open .nav-hamburger span:nth-child(3) {
  transform: rotate(-45deg) translate(4.5px, -4.5px);
}
```

### Menu overlay fullscreen

- Élément : `<div class="mobile-menu">` — frère de `<nav class="nav">`
- Fond : `#000000` opaque (pas de glassmorphism — fond plein pour lisibilité)
- Position : `fixed`, couvre tout le viewport (`inset: 0`)
- Z-index : `9998` (sous la navbar à 9999, le hamburger/X reste accessible par dessus)
- État fermé : `transform: translateX(100%); visibility: hidden; opacity: 0`
- État ouvert : `transform: translateX(0); visibility: visible; opacity: 1`
- Transition : `transform 0.3s ease, opacity 0.3s ease, visibility 0.3s`
- Ouverture/fermeture : toggle classe `.menu-open` sur `<body>`

**Scroll lock quand le menu est ouvert :**
```css
body.menu-open {
  overflow: hidden;
  position: fixed;
  width: 100%;
}
```

```javascript
// Dans hokuno.js
const hamburger = document.querySelector('.nav-hamburger');
const body = document.body;
let scrollPos = 0;

hamburger.addEventListener('click', () => {
  if (body.classList.contains('menu-open')) {
    // Fermer
    body.classList.remove('menu-open');
    body.style.top = '';
    window.scrollTo(0, scrollPos);
  } else {
    // Ouvrir
    scrollPos = window.scrollY;
    body.style.top = `-${scrollPos}px`;
    body.classList.add('menu-open');
  }
});
```

**Fermer le menu au clic sur un lien :**
```javascript
document.querySelectorAll('.mobile-menu a').forEach(link => {
  link.addEventListener('click', () => {
    body.classList.remove('menu-open');
    body.style.top = '';
    window.scrollTo(0, 0);
  });
});
```

**Fermer le menu avec la touche Escape :**
```javascript
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && body.classList.contains('menu-open')) {
    body.classList.remove('menu-open');
    body.style.top = '';
    window.scrollTo(0, scrollPos);
  }
});
```

**Liens dans le menu mobile (ordre du haut en bas) :**

| Texte | href |
|-------|------|
| COLLECTIONS | `/collections` |
| NOUVEAUTÉS | `/collections/all?sort_by=created-descending` |
| À PROPOS | `/pages/about` |
| JOURNAL | `/blogs/journal` |
| RECHERCHE | `/search` |
| COMPTE | `/account` |

Style des liens :
- Disposition : flex column, centré verticalement et horizontalement dans le viewport
- Font-size : `28px`
- Font-weight : `700`
- Letter-spacing : `3px`
- Text-transform : `uppercase`
- Couleur : `#FFFFFF`
- Espacement vertical : `24px` entre chaque lien
- Tap : couleur `#D4A853`
- Lien actif : couleur `#D4A853` (même logique de détection que desktop)

**Sélecteur de langue** en bas du menu mobile : `FR | EN` (voir section 6)

---

## 3. BOTTOM NAV MOBILE (<768px)

### Position et style

- Position : `fixed` en bas de l'écran
- Largeur : `100%`
- Z-index : `9999`
- Style : `background: rgba(10,10,10,0.92); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border-top: 1px solid rgba(255,255,255,0.06)`
- Padding : `10px 0 max(10px, env(safe-area-inset-bottom))` — safe area pour iPhone avec barre home
- Affiché UNIQUEMENT sous 768px (`display: none` au-dessus)
- Caché quand le menu hamburger est ouvert (`.menu-open .mobile-nav { display: none }`)
- Disposition : `display: flex; justify-content: space-around; align-items: center`

### 4 icônes

| Icône | Texte | href |
|-------|-------|------|
| 🏠 | ACCUEIL | `/` |
| 📦 | COLLECTIONS | `/collections` |
| 🛒 | PANIER | `/cart` |
| 👤 | COMPTE | `/account` |

Style de chaque item :
- Disposition : flex column, centré
- Icône : font-size `18px`
- Texte : font-size `10px`, font-weight `500`, letter-spacing `0.5px`, text-transform `uppercase`
- Couleur par défaut : `rgba(255,255,255,0.5)`
- Couleur page active : `#D4A853`
- Les 4 items occupent chacun 25% de la largeur
- Padding : `6px 12px`
- Touch target : minimum `44×44px` (garanti par le padding)

### Détection page active bottom nav

```liquid
<a href="/" {% if template == 'index' %}class="active"{% endif %}>
  <span class="mobile-nav-icon">🏠</span>ACCUEIL
</a>
<a href="/collections" {% if template == 'collection' or template == 'list-collections' %}class="active"{% endif %}>
  <span class="mobile-nav-icon">📦</span>COLLECTIONS
</a>
<a href="/cart" {% if template == 'cart' %}class="active"{% endif %}>
  <span class="mobile-nav-icon">🛒</span>PANIER
  {% if cart.item_count > 0 %}<span class="cart-badge">{{ cart.item_count }}</span>{% endif %}
</a>
<a href="/account" {% if template contains 'customers' %}class="active"{% endif %}>
  <span class="mobile-nav-icon">👤</span>COMPTE
</a>
```

### Badge panier

L'icône panier 🛒 affiche un badge rond avec le nombre d'articles. Si le panier est vide (0), pas de badge.

- Position : `absolute`, en haut à droite de l'icône panier (l'élément `<a>` du panier est `position: relative`)
- Fond : `#D4A853`
- Texte : `#000000`, font-size `10px`, font-weight `700`
- Taille : `16×16px`, border-radius `50%`, `display: flex; align-items: center; justify-content: center`
- Offset : `top: -4px; right: 8px`
- Mise à jour en AJAX en même temps que le compteur navbar desktop

---

## 4. ESPACEMENT POUR ÉLÉMENTS FIXED

### Problème

La navbar est `position: fixed` en haut, le bottom nav est `position: fixed` en bas. Sans padding compensatoire, le contenu des pages est caché derrière.

### Solution : padding sur les conteneurs de page

**Desktop :**
```css
/* Le contenu de chaque template doit commencer sous la navbar */
.page-wrap { padding-top: 120px; }  /* navbar height ~90px + marge */
```

**Mobile (<768px) :**
```css
.page-wrap {
  padding-top: 100px;   /* navbar mobile plus petite */
  padding-bottom: 80px; /* bottom nav ~60px + marge */
}
```

**Page d'accueil (index) :**
Le hero est plein écran (`min-height: 100vh`) avec son propre `padding-top: 90px` pour la navbar. Pas besoin de `.page-wrap`.

**Footer mobile :**
```css
@media (max-width: 768px) {
  .foot { margin-bottom: 70px; } /* ne pas être caché par le bottom nav */
}
```

### Classe `.page-wrap`

Chaque template (sauf index.liquid) entoure son contenu dans un `<div class="page-wrap">` :

```liquid
<!-- Dans collection.liquid, product.liquid, cart.liquid, etc. -->
<div class="page-wrap">
  {% render 'breadcrumbs' %}
  <!-- contenu de la page -->
</div>
```

Le hero de la page d'accueil (index.liquid) gère son propre padding — pas de `.page-wrap`.

---

## 5. FOOTER

### Style global

- Fond : `#050505`
- Padding desktop : `80px 64px 40px`
- Padding mobile : `40px 24px`
- Border-top : `1px solid rgba(255,255,255,0.06)`
- Mobile : `margin-bottom: 70px` (compense le bottom nav)

### Structure : grille 4 colonnes desktop → 1 colonne mobile

```
[LOGO + TAGLINE + RÉSEAUX]    [COLLECTIONS]    [INFORMATION]    [LÉGAL]
```

### Colonne 1 — Marque

| Élément | Détail |
|---------|--------|
| Logo | `logo-hokuno-transparent.png`, même rendu que la navbar |
| Tagline | `ホクノ — Toujours aller de l'avant` |
| Réseaux sociaux | Icônes SVG TikTok + Instagram — liens vers les comptes @hokuno (à créer, voir `specs/SOCIAL.md`) |

Style réseaux sociaux :
- Icônes SVG : `24×24px`, couleur `rgba(255,255,255,0.4)`
- Hover : couleur `#D4A853`
- Gap : `16px`
- Margin-top : `20px`

### Colonne 2 — Collections

| Texte | href |
|-------|------|
| **Collections** (titre h5) | — |
| Wanted | `/collections/wanted` |
| Direction | `/collections/direction` |
| Mythologie | `/collections/mythologie` |
| Design Hokuno | `/collections/design-hokuno` |

### Colonne 3 — Information

| Texte | href |
|-------|------|
| **Information** (titre h5) | — |
| À propos | `/pages/about` |
| FAQ | `/pages/faq` |
| Contact | `/pages/contact` |
| Blog | `/blogs/journal` |

### Colonne 4 — Légal

| Texte | href |
|-------|------|
| **Légal** (titre h5) | — |
| Conditions générales | `/policies/terms-of-service` |
| Politique de confidentialité | `/policies/privacy-policy` |
| Retours & remboursements | `/policies/refund-policy` |
| Mentions légales | `/pages/mentions-legales` |

### Style des colonnes

- Titres h5 : font-size `12px`, font-weight `700`, letter-spacing `2px`, text-transform `uppercase`, couleur `rgba(255,255,255,0.5)`, margin-bottom `16px`
- Liens : font-size `14px`, font-weight `400`, couleur `rgba(255,255,255,0.4)`, line-height `2.2`
- Liens hover : couleur `#D4A853`
- Grid desktop : `grid-template-columns: 1.5fr 1fr 1fr 1fr`, gap `40px`
- Grid mobile : `grid-template-columns: 1fr`, gap `32px`, texte centré

### Newsletter (sous la grille, séparée visuellement)

- Séparateur : `border-top: 1px solid rgba(255,255,255,0.06)`, margin-top `48px`, padding-top `48px`
- Texte d'accroche : `Rejoignez l'équipage — 15% sur votre première commande`
- Style texte : font-size `14px`, couleur `rgba(255,255,255,0.6)`, margin-bottom `16px`
- Formulaire : champ email + bouton côte à côte
  - Input email : fond `rgba(255,255,255,0.04)`, bordure `1px solid rgba(255,255,255,0.1)`, border-radius `4px`, padding `14px 16px`, couleur `#FFFFFF`, placeholder `Votre adresse email`, largeur `300px` desktop / `100%` mobile
  - Bouton : style `.btn-gold`, texte `S'INSCRIRE`
- Intégration : Shopify Customer API ou Shopify Email (natif)
- Snippet : `{% render 'newsletter-form' %}`

### Copyright (tout en bas)

```
© 2026 HOKUNO. Tous droits réservés.
```

Style : font-size `12px`, couleur `rgba(255,255,255,0.25)`, text-align `center`, margin-top `40px`

---

## 6. FIL D'ARIANE (BREADCRUMBS)

### Affiché sur

- Pages collection : `Accueil › Collections › Wanted`
- Pages produit : `Accueil › Wanted › T-Shirt Lufi Wanted`
- Pages statiques : `Accueil › À propos`
- Articles blog : `Accueil › Journal › [Titre de l'article]`

### PAS affiché sur

- Page d'accueil (index)
- Page panier
- Page recherche
- Page 404
- Page mot de passe
- Page /collections (liste des collections)

### Logique Liquid

```liquid
<!-- snippets/breadcrumbs.liquid -->
<nav class="breadcrumbs" aria-label="Fil d'Ariane">
  <a href="/">{{ 'breadcrumbs.home' | t }}</a>

  {% if template == 'collection' %}
    <span class="breadcrumb-sep">›</span>
    <span class="breadcrumb-current">{{ collection.title }}</span>

  {% elsif template == 'product' %}
    {% if product.collections.size > 0 %}
      <span class="breadcrumb-sep">›</span>
      <a href="{{ product.collections.first.url }}">{{ product.collections.first.title }}</a>
    {% endif %}
    <span class="breadcrumb-sep">›</span>
    <span class="breadcrumb-current">{{ product.title }}</span>

  {% elsif template == 'page' %}
    <span class="breadcrumb-sep">›</span>
    <span class="breadcrumb-current">{{ page.title }}</span>

  {% elsif template == 'article' %}
    <span class="breadcrumb-sep">›</span>
    <a href="{{ blog.url }}">{{ blog.title }}</a>
    <span class="breadcrumb-sep">›</span>
    <span class="breadcrumb-current">{{ article.title | truncate: 50 }}</span>
  {% endif %}
</nav>
```

### Style

- Margin-bottom : `24px`
- Font-size : `12px`
- Letter-spacing : `0.5px`
- Couleur liens : `rgba(255,255,255,0.4)`
- Couleur séparateur `›` : `rgba(255,255,255,0.2)`, padding `0 8px`
- Couleur page courante : `rgba(255,255,255,0.7)`, font-weight `500`
- Hover liens : `#D4A853`

### Schema JSON-LD BreadcrumbList

Chaque breadcrumb génère le schema JSON-LD correspondant — détaillé dans `specs/SEO.md`.

---

## 7. SÉLECTEUR DE LANGUE FR/EN

### Desktop

Position : dans `.nav-right`, premier élément (avant les icônes).

### Mobile

Position : en bas du menu overlay fullscreen, centré.

### Rendu visuel

```
FR | EN
```

- Langue active : couleur `#D4A853`, font-weight `700`
- Langue inactive : couleur `rgba(255,255,255,0.5)`, font-weight `400`
- Séparateur `|` : couleur `rgba(255,255,255,0.2)`, padding `0 6px`
- Font-size : `12px`, letter-spacing `1px`

### Implémentation Liquid

```liquid
{% if request.locale.iso_code == 'fr' %}
  <span class="lang-active">FR</span>
  <span class="lang-sep">|</span>
  <a href="{{ canonical_url | replace: request.locale.root_url, '/en' }}" class="lang-link">EN</a>
{% else %}
  <a href="{{ canonical_url | replace: request.locale.root_url, '/fr' }}" class="lang-link">FR</a>
  <span class="lang-sep">|</span>
  <span class="lang-active">EN</span>
{% endif %}
```

> Note : l'implémentation exacte dépend de la configuration Shopify Markets (voir `specs/MULTILINGUE.md`). Le code ci-dessus est l'intention — Claude Code doit adapter selon le système de localisation actif sur le store.

---

## 8. BARRE DE RECHERCHE

### Accès

- Desktop : icône loupe SVG dans la navbar → lien vers `/search`
- Mobile : lien RECHERCHE dans le menu hamburger → `/search`

### Page /search

- URL : `/search?q=...`
- Template : `search.liquid`
- Champ de recherche : pleine largeur en haut de la page
  - Fond : `rgba(255,255,255,0.04)`
  - Bordure : `1px solid rgba(255,255,255,0.1)`
  - Border-radius : `8px`
  - Padding : `16px 20px`
  - Font-size : `16px` (empêche le zoom auto sur iOS)
  - Couleur texte : `#FFFFFF`
  - Placeholder : `Rechercher un produit, une collection...` — couleur `rgba(255,255,255,0.3)`
  - Focus : `border-color: #D4A853; outline: none`
  - Autofocus au chargement de la page
- Bouton : icône loupe SVG ou texte "RECHERCHER", style `.btn-gold`
- Soumission : form GET vers `/search`

### Résultats

- Affichage : grille de product-cards identique aux pages collection (snippet `{% render 'product-card', product: item %}`)
- Titre : `{{ search.results_count }} résultats pour "{{ search.terms }}"`
- Grid : 4 colonnes desktop, 2 colonnes mobile
- Tri : par pertinence (défaut Shopify)

### Pas de résultats

```liquid
{% if search.results_count == 0 %}
<div class="search-empty">
  <p>Aucun résultat pour "{{ search.terms }}".</p>
  <p>Essayez un autre mot-clé ou explorez nos collections.</p>
  <a href="/collections" class="btn-gold">DÉCOUVRIR NOS COLLECTIONS</a>
</div>
{% endif %}
```

### Recherche prédictive

Pas dans la v1. À implémenter plus tard avec l'API Predictive Search de Shopify.

---

## 9. CART AJAX — COMPORTEMENT GLOBAL

### Ajout au panier sans rechargement

Tous les boutons "AJOUTER AU PANIER" sur le site fonctionnent en AJAX :

```javascript
// Dans hokuno.js
async function addToCart(variantId, quantity = 1) {
  const res = await fetch('/cart/add.js', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: variantId, quantity: quantity })
  });

  if (res.ok) {
    // Mettre à jour les compteurs
    const cartRes = await fetch('/cart.js');
    const cart = await cartRes.json();
    updateCartCounters(cart.item_count);
    showCartNotification();
  }
}

function updateCartCounters(count) {
  // Compteur navbar desktop
  document.querySelectorAll('.cart-count').forEach(el => {
    el.textContent = count;
  });
  // Badge bottom nav mobile
  const badge = document.querySelector('.cart-badge');
  if (badge) {
    badge.textContent = count;
    badge.style.display = count > 0 ? 'flex' : 'none';
  }
}
```

### Notification "Ajouté au panier"

- Apparaît pendant 2.5 secondes après un ajout réussi
- Position : fixe, sous la navbar, centré horizontalement
- Style : `background: #D4A853; color: #000000; padding: 14px 28px; border-radius: 6px; font-weight: 600; font-size: 13px; letter-spacing: 1px`
- Texte : `✓ Ajouté au panier`
- Animation : fade in → pause 2.5s → fade out
- Z-index : `9998` (sous la navbar)

```javascript
function showCartNotification() {
  const notif = document.querySelector('.cart-notif');
  notif.classList.add('show');
  setTimeout(() => notif.classList.remove('show'), 2500);
}
```

```css
.cart-notif {
  position: fixed;
  top: 100px;
  left: 50%;
  transform: translateX(-50%);
  /* ... styles ci-dessus ... */
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s, visibility 0.3s;
  z-index: 9998;
}
.cart-notif.show {
  opacity: 1;
  visibility: visible;
}
```

L'élément `<div class="cart-notif">✓ Ajouté au panier</div>` est dans `theme.liquid`, après la navbar.

### Pas de redirection

L'ajout au panier ne redirige JAMAIS vers `/cart`. Le client reste sur la page en cours.

---

## 10. TRANSITIONS ET ANIMATIONS NAVIGATION

### Animations au chargement

- Hero (page accueil) : `fadeUp` — `opacity: 0 → 1`, `translateY(30px) → 0`, durée `0.8s ease-out`
- Hero droite (image) : même animation avec `0.15s` de délai

```css
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### Transitions hover

- Tous les liens : `transition: color 0.3s ease`
- Cards produit : `transition: transform 0.3s ease, border-color 0.3s ease` — hover : `transform: scale(1.015); border-color: rgba(212,168,83,0.3)`
- Boutons : `transition: all 0.3s ease` — hover : `transform: translateY(-1px)` sur `.btn-gold`

### Pas de transitions de page

V1 : rechargement classique Shopify. Pas de SPA, pas de barba.js, pas de transition entre pages.

---

## 11. RÉCAPITULATIF DES ÉLÉMENTS HTML DANS THEME.LIQUID

Ordre exact des éléments dans `layout/theme.liquid` :

```html
<!DOCTYPE html>
<html lang="{{ request.locale.iso_code }}">
<head>
  <!-- meta, title, fonts, hokuno.css -->
  {% render 'seo-jsonld' %}
  {{ content_for_header }}
</head>
<body>

  <!-- 1. Navbar -->
  <nav class="nav"> ... </nav>

  <!-- 2. Menu mobile overlay -->
  <div class="mobile-menu"> ... </div>

  <!-- 3. Notification cart -->
  <div class="cart-notif">✓ Ajouté au panier</div>

  <!-- 4. Contenu de la page (injecté par le template actif) -->
  {{ content_for_layout }}

  <!-- 5. Footer -->
  <footer class="foot"> ... </footer>

  <!-- 6. Bottom nav mobile -->
  <nav class="mobile-nav"> ... </nav>

  <!-- 7. JS -->
  <script src="{{ 'hokuno.js' | asset_url }}" defer></script>
</body>
</html>
```
