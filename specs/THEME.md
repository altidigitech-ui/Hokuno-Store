# specs/THEME.md — Design system CSS

> Contrat pour Claude Code. Chaque valeur CSS du site est définie ici.
> Ce fichier est la source de vérité pour `assets/hokuno.css`.
> En cas de conflit entre ce fichier et les valeurs dans d'autres specs, ce fichier fait autorité.

---

## 1. PALETTE DE COULEURS

### Fonds

| Nom | Valeur | Usage |
|-----|--------|-------|
| Body | `#000000` | Fond principal — tout le site, TOUJOURS |
| Footer | `#050505` | Fond footer (légèrement plus clair que body) |
| Cartes | `#111` ou `#111111` | Fond des collection-cards |
| Surface 1 | `rgba(255,255,255,0.02)` | Fond product-cards |
| Surface 2 | `rgba(255,255,255,0.03)` | Fond trust-cards |
| Surface 3 | `rgba(255,255,255,0.04)` | Fond navbar glassmorphism, inputs formulaires, hero-products |
| Surface 4 | `rgba(255,255,255,0.08)` | Fond inputs au focus (si besoin) |
| Overlay | `rgba(0,0,0,0.75)` | Fond info collection-cards (avec blur) |
| Image fallback | `#111` | Background des images pendant le chargement |

### Texte

| Nom | Valeur | Usage |
|-----|--------|-------|
| Primaire | `#FFFFFF` | Titres, texte principal |
| Secondaire 90 | `rgba(255,255,255,0.9)` | Labels trust bar |
| Secondaire 85 | `rgba(255,255,255,0.85)` | Liens navbar, titres product-cards |
| Secondaire 75 | `rgba(255,255,255,0.75)` | Actions navbar droite |
| Secondaire 70 | `rgba(255,255,255,0.7)` | Titre section feat, breadcrumb current, contenu article |
| Secondaire 60 | `rgba(255,255,255,0.6)` | Description produit, FAQ réponses, options labels |
| Secondaire 50 | `rgba(255,255,255,0.5)` | Sous-texte trust, prix variant, liens inactifs, bottom nav |
| Secondaire 45 | `rgba(255,255,255,0.45)` | Sous-titre collections, descriptions collection-cards, footer h5 |
| Secondaire 40 | `rgba(255,255,255,0.4)` | Liens footer, breadcrumbs, collection tag produit, trust sub |
| Secondaire 35 | `rgba(255,255,255,0.35)` | Compteur filtre, dates blog, prix barré |
| Secondaire 30 | `rgba(255,255,255,0.3)` | Placeholder inputs |
| Secondaire 25 | `rgba(255,255,255,0.25)` | Textes verticaux hero, copyright footer, bordure btn-outline |
| Secondaire 20 | `rgba(255,255,255,0.2)` | Coordonnées hero, séparateur langue |

### Accent

| Nom | Valeur | Usage |
|-----|--------|-------|
| Doré | `#D4A853` | Couleur principale d'accent — boutons CTA, hover, prix, liens actifs, katakana |
| Doré hover | `#c49a3d` | Bouton .btn-gold au hover (légèrement plus foncé) |
| Doré faible | `rgba(212,168,83,0.5)` | Bordure .col-btn |
| Doré glow | `rgba(212,168,83,0.35)` | Bordure hover product-cards |
| Doré shadow | `rgba(212,168,83,0.08)` | Box-shadow hover collection-cards |

### Fonctionnels

| Nom | Valeur | Usage |
|-----|--------|-------|
| Erreur | `#ff6b6b` | Messages d'erreur, icône supprimer |
| Erreur fond | `rgba(255,0,0,0.08)` | Background messages d'erreur |
| Sale | `#ff4444` | Prix en solde, badge remise, coeur favoris |
| Sale fond | `rgba(255,68,68,0.15)` | Background badge remise |
| Succès | `#22c55e` | Bouton copier lien (après copie) |
| Succès fond | `rgba(212,168,83,0.1)` | Background message succès formulaire |
| Sélection | `::selection { background: #D4A853; color: #000000; }` | Texte sélectionné |

### Bordures

| Nom | Valeur | Usage |
|-----|--------|-------|
| Subtile | `rgba(255,255,255,0.05)` | Bordure collection-cards, séparateurs footer |
| Légère | `rgba(255,255,255,0.06)` | Bordure product-cards, séparateur cart items, bottom nav top, FAQ |
| Moyenne | `rgba(255,255,255,0.07)` | Bordure trust-cards |
| Standard | `rgba(255,255,255,0.08)` | Bordure navbar glassmorphism, hero-products |
| Input | `rgba(255,255,255,0.1)` | Bordure inputs, miniatures produit, boutons taille |
| Input hover | `rgba(255,255,255,0.15)` | Bordure boutons taille, boutons quantité, boutons nav hero |

---

## 2. TYPOGRAPHIE

### Police

```css
font-family: 'Inter', sans-serif;
```

Chargement : `https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap`

### Poids utilisés

| Poids | Nom CSS | Usage |
|-------|---------|-------|
| 900 | Black | H1 hero (76px), page titles (42px), product name (36px), error code (120px) |
| 800 | Extra Bold | Article h2 (24px) |
| 700 | Bold | H2 hero katakana, prix, boutons CTA, nav links actifs, trust labels, card h3, FAQ questions |
| 600 | Semi Bold | Nav links, section titles, product info h4, boutons taille, badges, FAQ |
| 500 | Medium | Nav actions, textes verticaux, cols label, bottom nav, breadcrumbs current |
| 400 | Regular | Body text, descriptions, footer links, inputs |
| 300 | Light | Katakana hero, sous-titres collections, descriptions collection-cards, footer kata |

### Échelle typographique

| Élément | Taille desktop | Taille mobile | Poids | Letter-spacing | Transform |
|---------|:--------------:|:-------------:|:-----:|:--------------:|:---------:|
| H1 hero | `76px` | `38px` | 900 | `-1px` | uppercase |
| Katakana hero | `52px` | `30px` | 300 | `8px` | — |
| H2 cols title | `52px` | `30px` | 900 | `-1px` | — |
| H1 page title | `42px` | `32px` | 900 | `1px` | uppercase |
| H1 product name | `36px` | `28px` | 900 | — | uppercase |
| H2 article title | `36px` | `28px` | 900 | — | uppercase |
| H3 page content | `18px` | `18px` | 700 | — | — |
| H3 card collection | `17px` | `17px` | 700 | `1.5px` | uppercase |
| Prix produit | `28px` | `24px` | 700 | — | — |
| Prix product-card | `17px` | `17px` | 700 | — | — |
| Body / descriptions | `14px` | `14px` | 400 | — | — |
| Article body | `16px` | `16px` | 400 | — | — |
| Boutons CTA | `13px` | `13px` | 700 | `1.5px` | uppercase |
| Nav links | `12.5px` | — | 500 | `2px` | uppercase |
| Labels options | `13px` | `13px` | 600 | `1.5px` | uppercase |
| Cols label "COLLECTIONS" | `13px` | `13px` | 500 | `4px` | uppercase |
| Small / trust sub | `11px` | `11px` | 400 | — | — |
| Trust label | `11.5px` | `11.5px` | 700 | `1.2px` | uppercase |
| Texte vertical gauche | `10px` | — | 500 | `5px` | uppercase |
| Copyright footer | `11px` | `11px` | 400 | `1px` | — |
| Mini (hp-card title) | `9px` | — | 600 | `0.5px` | uppercase |
| Coordonnées hero | `9px` | — | 400 | `2px` | — |

### Line-height

| Contexte | Valeur |
|----------|--------|
| Titres (h1, h2) | `1.02` à `1.15` |
| Cards info | `1.3` |
| Description collection | `1.6` |
| Body text | `1.7` |
| Page content / article | `1.8` à `1.9` |
| FAQ réponses | `1.8` |
| Footer links | implicite (via margin-bottom `12px`) |

### Anti-aliasing

```css
body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

---

## 3. ESPACEMENTS

### Padding des sections (desktop → mobile)

| Section | Desktop | Mobile |
|---------|---------|--------|
| Hero | `0 64px`, padding-top `90px` | `100px 24px 40px` |
| Trust bar | `32px 64px` | `20px 24px` |
| Section collections | `100px 64px 80px` | `60px 24px` |
| Produits phares | `80px 64px 100px` | `60px 24px` |
| Page wrap | `120px 64px 80px` | `100px 24px 100px` |
| Product wrap | `120px 64px 60px` | `100px 24px 40px` |
| Footer | `64px` | `40px 24px` |
| Produits similaires | `0 64px 80px` | `0 24px 80px` |

### Gaps

| Élément | Valeur |
|---------|--------|
| Grilles (collections, produits) | `18px` desktop, `12px` mobile |
| Boutons hero | `16px` |
| Nav links | `36px` |
| Nav actions droite | `28px` |
| Trust cards | `20px` desktop, `10px` mobile |
| Footer colonnes | `48px` desktop, `32px` mobile |
| Cart items | `24px` (entre image et infos) |
| Color swatches | `10px` |
| Size buttons | `10px` |
| Product-card info padding | `18px 20px` |
| Collection-card info padding | `28px` desktop, `18px` mobile |

### Max-width

| Élément | Valeur |
|---------|--------|
| Navbar | `1440px` |
| Sous-titre collections | `580px` |
| Page content / descriptions | `700px` |
| Article body | `760px` |
| Auth forms | `420px` |
| Accordéons produit | `900px` |

---

## 4. BORDER-RADIUS

| Élément | Valeur |
|---------|--------|
| Navbar desktop | `14px` |
| Navbar mobile | `10px` |
| Collection-cards | `14px` |
| Trust-cards | `12px` |
| Product-cards | `12px` |
| Images produit | `12px` |
| Article hero image | `12px` |
| Hero-product cards | `10px` |
| Blog-cards | `12px` |
| Miniatures produit | `6px` |
| Boutons CTA (.btn-gold) | `4px` |
| Boutons outline (.btn-outline) | `4px` |
| Boutons taille (.size-btn) | `4px` |
| Boutons collection (.col-btn) | `4px` |
| Bouton ajouter au panier | `6px` |
| Inputs formulaires | `6px` |
| Boutons quantité | `6px` (gauche ou droite arrondi) |
| Badge remise | `4px` |
| Message erreur/succès | `6px` |
| Barre progression livraison | `2px` |
| Cart item image | `8px` |
| Partage social boutons | `50%` (rond) |
| Color swatches | `50%` (rond) |
| Boutons nav hero | `50%` (rond) |

---

## 5. GLASSMORPHISM

### Navbar

```css
background: rgba(255,255,255,0.04);
backdrop-filter: blur(24px);
-webkit-backdrop-filter: blur(24px);
border: 1px solid rgba(255,255,255,0.08);
```

### Trust-cards

```css
background: rgba(255,255,255,0.03);
backdrop-filter: blur(12px);
-webkit-backdrop-filter: blur(12px);
border: 1px solid rgba(255,255,255,0.07);
```

### Bottom nav mobile

```css
background: rgba(10,10,10,0.92);
backdrop-filter: blur(20px);
-webkit-backdrop-filter: blur(20px);
border-top: 1px solid rgba(255,255,255,0.06);
```

### Collection-card info overlay

```css
background: rgba(0,0,0,0.75);
backdrop-filter: blur(10px);
```

### Bouton panier sticky mobile

```css
background: rgba(0,0,0,0.95);
backdrop-filter: blur(12px);
-webkit-backdrop-filter: blur(12px);
border-top: 1px solid rgba(255,255,255,0.06);
```

> **Toujours** inclure le préfixe `-webkit-backdrop-filter` pour la compatibilité Safari.

---

## 6. Z-INDEX

| Couche | Valeur | Éléments |
|--------|:------:|----------|
| Navbar | `9999` | `.nav` |
| Bottom nav mobile | `9999` | `.mobile-nav` |
| Mobile menu overlay | `9998` | `.mobile-menu` |
| Cart notification | `9998` | `.cart-notif` |
| Bouton panier sticky mobile | `9998` | `.product-actions` (mobile) |
| Hero products | `5` | `.hero-products` |
| Trust bar | `4` | `.trust` |
| Hero texte gauche | `3` | `.hero-left` |
| Hero fondu image | `3` | `.hero-img-wrap::after` |
| Hero image droite | `2` | `.hero-right` |
| Textes verticaux | `1` | `.v-left`, `.v-right` |

---

## 7. BREAKPOINTS

| Nom | Media query | Usage |
|-----|-------------|-------|
| Desktop | `> 1024px` | Layout par défaut (pas de media query) |
| Tablette | `max-width: 1024px` | Grilles 2 colonnes, hero titre réduit |
| Mobile | `max-width: 768px` | Layout mobile complet, bottom nav, hamburger |
| Desktop only (bottom nav) | `min-width: 769px` | `.mobile-nav { display: none }` |

### Ordre des media queries dans hokuno.css

```css
/* 1. Styles desktop par défaut (pas de media query) */

/* 2. Tablette */
@media (max-width: 1024px) { ... }

/* 3. Mobile */
@media (max-width: 768px) { ... }

/* 4. Desktop only (masquer les éléments mobile) */
@media (min-width: 769px) { .mobile-nav { display: none; } }
```

---

## 8. ANIMATIONS ET TRANSITIONS

### Transitions globales

Toutes les transitions du site utilisent `0.3s ease` sauf indication contraire.

```css
/* Appliqué via les propriétés transition sur chaque élément */
transition: all 0.3s ease;      /* boutons, cartes */
transition: color 0.3s ease;    /* liens texte */
transition: transform 0.3s ease; /* cartes au hover */
transition: transform 0.5s ease; /* images dans les cartes */
```

### Animation fadeUp (chargement page)

```css
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.hero-left { animation: fadeUp 0.8s ease-out; }
.hero-right { animation: fadeUp 0.8s ease-out 0.15s both; }
```

### Hover effects

| Élément | Effet | Valeurs |
|---------|-------|---------|
| Liens texte | Couleur → doré | `color: #D4A853` |
| `.btn-gold` | Légère montée | `transform: translateY(-1px); background: #c49a3d` |
| `.col-card` | Scale + ombre | `transform: scale(1.015); box-shadow: 0 8px 40px rgba(212,168,83,0.08)` |
| `.col-card img` | Zoom interne | `transform: scale(1.03)` |
| `.prod-card` | Montée + bordure | `transform: translateY(-4px); border-color: rgba(212,168,83,0.35); box-shadow: 0 12px 40px rgba(0,0,0,0.3)` |
| `.prod-card img` | Zoom interne | `transform: scale(1.04)` |
| `.col-btn` | Fond doré | `background: #D4A853; color: #000000` |
| `.hp-card` | Bordure dorée | `border-color: rgba(212,168,83,0.4)` |
| `.hp-nav button` | Bordure + texte doré | `border-color: #D4A853; color: #D4A853` |

### Accordéon

```css
.accord-body, .faq-answer {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.4s ease;
}
.accord-item.open .accord-body,
.faq-item.open .faq-answer {
  max-height: 1000px; /* suffisamment grand pour le contenu */
}
```

### Menu mobile slide-in

```css
.mobile-menu {
  transform: translateX(100%);
  visibility: hidden;
  opacity: 0;
  transition: transform 0.3s ease, opacity 0.3s ease, visibility 0.3s;
}
body.menu-open .mobile-menu {
  transform: translateX(0);
  visibility: visible;
  opacity: 1;
}
```

### Cart notification fade

```css
.cart-notif {
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s, visibility 0.3s;
}
.cart-notif.show {
  opacity: 1;
  visibility: visible;
}
```

---

## 9. BOUTONS

### .btn-gold (CTA principal)

```css
.btn-gold {
  display: inline-flex; align-items: center; gap: 8px;
  background: #D4A853; color: #000000;
  padding: 18px 36px;
  font-weight: 700; font-size: 13px; letter-spacing: 1.5px;
  text-transform: uppercase; border: none; border-radius: 4px;
  cursor: pointer; transition: all 0.3s;
  text-decoration: none;
}
.btn-gold:hover {
  background: #c49a3d; color: #000000;
  transform: translateY(-1px);
}
.btn-gold:disabled {
  background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.3);
  cursor: not-allowed; transform: none;
}
```

### .btn-outline (CTA secondaire)

```css
.btn-outline {
  display: inline-flex; align-items: center;
  background: transparent; color: #fff;
  padding: 18px 36px;
  font-weight: 600; font-size: 13px; letter-spacing: 1.5px;
  text-transform: uppercase;
  border: 1px solid rgba(255,255,255,0.25); border-radius: 4px;
  cursor: pointer; transition: all 0.3s;
  text-decoration: none;
}
.btn-outline:hover {
  border-color: #D4A853; color: #D4A853;
}
```

### .col-btn (bouton collection-card)

```css
.col-btn {
  display: inline-block; margin-top: 18px;
  padding: 10px 22px;
  border: 1px solid rgba(212,168,83,0.5); color: #D4A853;
  font-size: 11px; font-weight: 600; letter-spacing: 1.5px;
  text-transform: uppercase; border-radius: 4px;
  transition: all 0.3s;
}
.col-btn:hover { background: #D4A853; color: #000000; }
```

### .add-cart (bouton panier)

```css
.add-cart {
  width: 100%; padding: 18px;
  background: #D4A853; color: #000000;
  border: none; font-size: 15px; font-weight: 700;
  letter-spacing: 1.5px; text-transform: uppercase;
  border-radius: 6px; cursor: pointer;
  transition: all 0.3s;
  display: flex; align-items: center; justify-content: center; gap: 10px;
}
.add-cart:hover { background: #c49a3d; transform: translateY(-1px); }
.add-cart:disabled {
  background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.3);
  cursor: not-allowed; transform: none;
}
```

### Mobile boutons

```css
@media (max-width: 768px) {
  .btn-gold, .btn-outline {
    width: 100%; justify-content: center;
    padding: 16px 24px;
  }
}
```

---

## 10. IMAGES

### Règles globales

```css
img { max-width: 100%; display: block; }
```

### Logo navbar

```css
.nav-logo img {
  height: 65px;           /* desktop */
  mix-blend-mode: screen;
  filter: brightness(1.2);
  background: transparent;
}
/* mobile */
@media (max-width: 768px) {
  .nav-logo img { height: 30px; }
}
```

### Hero image

```css
.hero-img {
  max-height: 90vh;      /* desktop */
  margin-top: -40px;
  width: auto;
  object-fit: contain;
}
/* Fondu radial vers le fond noir */
.hero-img-wrap::after {
  content: '';
  position: absolute; inset: -4px;
  background: radial-gradient(ellipse at center, transparent 55%, #000000 100%);
  pointer-events: none; z-index: 3;
}
/* mobile */
@media (max-width: 768px) {
  .hero-img { max-height: 50vh; }
}
```

### Images dans les cards

| Card | Hauteur desktop | Hauteur mobile | Object-fit |
|------|:--------------:|:-------------:|:----------:|
| Collection-card | `420px` | `260px` | `cover` |
| Product-card | `320px` | `220px` | `cover` |
| Hero-product card | `60px` | — | `cover` |
| Blog-card | `200px` | `200px` | `cover` |
| Cart item | `100px` | `80px` | `cover` |
| Product thumbs | `80×80px` | `80×80px` | `cover` |

### Lazy loading

```html
loading="lazy"  <!-- sur TOUTES les images sauf le hero -->
```

---

## 11. GRILLES

### Colonnes par breakpoint

| Grille | Desktop | Tablette | Mobile |
|--------|:-------:|:--------:|:------:|
| Collections (`.cols-grid`) | 4 | 2 | 2 |
| Produits (`.products-grid`, `.feat-grid`) | 4 | 2 | 2 |
| Produits similaires (`.related-grid`) | 4 | 2 | 2 |
| Blog (`.blog-grid`) | 3 | 2 | 1 |
| Footer (`.foot-grid`) | `2fr 1fr 1fr 1.5fr` | 1 | 1 |
| Contact form (`.contact-wrap`) | `1fr 1.5fr` | 1 | 1 |
| Product page (`.product-wrap`) | `55% / 45%` (flex) | — | column |

---

## 12. RESET ET BASE

```css
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  background: #000000; color: #fff;
  font-family: 'Inter', sans-serif;
  overflow-x: hidden;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
a { color: #fff; text-decoration: none; transition: color 0.3s ease; }
a:hover { color: #D4A853; }
img { max-width: 100%; display: block; }
::selection { background: #D4A853; color: #000000; }
button { font-family: 'Inter', sans-serif; cursor: pointer; border: none; background: none; }
```

---

## 13. STRUCTURE DE `hokuno.css`

Ordre des sections dans le fichier CSS :

```
/* ═══ 1. RESET & BASE ═══ */
/* ═══ 2. NAVBAR ═══ */
/* ═══ 3. MOBILE MENU OVERLAY ═══ */
/* ═══ 4. HERO ═══ */
/* ═══ 5. TEXTES VERTICAUX ═══ */
/* ═══ 6. TRUST BAR ═══ */
/* ═══ 7. HERO PRODUCTS ═══ */
/* ═══ 8. SECTION COLLECTIONS ═══ */
/* ═══ 9. COLLECTION-CARDS ═══ */
/* ═══ 10. PRODUCT-CARDS ═══ */
/* ═══ 11. PRODUITS VEDETTES ═══ */
/* ═══ 12. PAGE WRAP ═══ */
/* ═══ 13. COLLECTION PAGE (filtres, tri) ═══ */
/* ═══ 14. PRODUCT PAGE ═══ */
/* ═══ 15. GALERIE PRODUIT ═══ */
/* ═══ 16. SWATCHES & TAILLES ═══ */
/* ═══ 17. QUANTITÉ & ACTIONS ═══ */
/* ═══ 18. ACCORDÉONS ═══ */
/* ═══ 19. GUIDE DES TAILLES ═══ */
/* ═══ 20. PRODUITS SIMILAIRES ═══ */
/* ═══ 21. PARTAGE SOCIAL ═══ */
/* ═══ 22. PANIER ═══ */
/* ═══ 23. PAGES STATIQUES (about, content) ═══ */
/* ═══ 24. FAQ ═══ */
/* ═══ 25. CONTACT ═══ */
/* ═══ 26. BLOG & ARTICLE ═══ */
/* ═══ 27. COMPTE CLIENT ═══ */
/* ═══ 28. 404 ═══ */
/* ═══ 29. BREADCRUMBS ═══ */
/* ═══ 30. PAGINATION ═══ */
/* ═══ 31. CART NOTIFICATION ═══ */
/* ═══ 32. NEWSLETTER ═══ */
/* ═══ 33. FOOTER ═══ */
/* ═══ 34. MOBILE BOTTOM NAV ═══ */
/* ═══ 35. BOUTONS GLOBAUX ═══ */
/* ═══ 36. PRIX ═══ */
/* ═══ 37. BADGES ═══ */
/* ═══ 38. FORMULAIRES ═══ */
/* ═══ 39. ANIMATIONS ═══ */
/* ═══ 40. TABLETTE (max-width: 1024px) ═══ */
/* ═══ 41. MOBILE (max-width: 768px) ═══ */
/* ═══ 42. DESKTOP ONLY (min-width: 769px) ═══ */
```

---

## 14. RÈGLES STRICTES

- **Jamais d'inline styles** (`style="..."`) dans le HTML — tout dans hokuno.css
- **Un seul fichier CSS** : `assets/hokuno.css` — pas de fichier par composant
- **Pas de CSS custom properties** (`:root { --color: ... }`) en v1 — valeurs en dur pour simplicité
- **Pas de `!important`** sauf `.nav-active` (nécessaire car les liens ont des styles de spécificité identique)
- **Pas de préprocesseur** (pas de SASS, LESS) — CSS vanilla
- **Commentaires** : séparateurs en anglais (`/* ═══ SECTION NAME ═══ */`)
- **Mobile-first : non** — desktop-first, les media queries ajustent pour le mobile (cohérent avec le thème actuel)
