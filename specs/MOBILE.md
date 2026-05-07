# specs/MOBILE.md — Comportement mobile

> Contrat pour Claude Code. Tout le comportement spécifique mobile (<768px) est défini ici.
> Ce fichier consolide et complète les règles mobile dispersées dans les autres specs.
> En cas de doute, ce fichier fait autorité pour le mobile.

---

## 1. RÈGLES FONDAMENTALES

### Breakpoint

```css
@media (max-width: 768px) { /* tout le mobile */ }
@media (max-width: 1024px) { /* tablette + mobile */ }
```

### Viewport meta

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

**PAS de `maximum-scale=1` ni `user-scalable=no`** — laisser le pinch-to-zoom natif. C'est une exigence d'accessibilité et un signal SEO négatif si désactivé.

### Touch targets

**Minimum 44×44px** pour tous les éléments interactifs. Sans exception.

| Élément | Taille actuelle | Conforme ? | Action si non conforme |
|---------|:--------------:|:----------:|----------------------|
| Nav links mobile | 28px font + 24px gap | ✅ via padding | — |
| Hamburger | 22px barres + 8px padding | ✅ 38px total | — |
| Bottom nav items | 18px icon + 10px text + 6px padding | ✅ ~48px total | — |
| Boutons taille (.size-btn) | 12px padding + 14px font | ✅ ~44px | — |
| Color swatches | 32px + 2px outline + 2px offset | ✅ ~40px | Ajouter `min-height: 44px; min-width: 44px` au conteneur |
| Boutons quantité | 44×44px | ✅ | — |
| Bouton panier | Pleine largeur × 56px | ✅ | — |
| Wishlist | 56×56px | ✅ | — |
| FAQ question | Pleine largeur × ~60px | ✅ | — |
| Footer liens | 13.5px font, line-height 2.2 | ✅ ~30px hauteur, mais tappable via area | — |
| Miniatures produit | 80×80px | ✅ | — |
| Pagination boutons | 40×40px | ⚠️ Juste sous 44px | Augmenter à `44×44px` en mobile |
| Breadcrumbs liens | 12px font | ⚠️ Petits | Augmenter padding vertical à `8px` |

### Font-size minimum

**14px minimum partout en mobile** — les textes plus petits sont illisibles sur un écran 5-6 pouces.

Éléments à ajuster en mobile :

```css
@media (max-width: 768px) {
  /* Textes qui sont < 14px en desktop */
  .trust-label { font-size: 14px; }    /* desktop: 11.5px */
  .trust-sub { font-size: 14px; }      /* desktop: 11px */
  .cols-label { font-size: 14px; }     /* desktop: 13px → OK mais harmoniser */
  .col-card-info p { font-size: 14px; } /* desktop: 13px */
  .prod-info h4 { font-size: 14px; }   /* desktop: 13px */
  .product-badge { font-size: 14px; }  /* desktop: 12px */
  .breadcrumbs { font-size: 14px; }    /* desktop: 12px */
  .foot-col a { font-size: 14px; }     /* desktop: 13.5px → OK */
  .foot-copy { font-size: 12px; }      /* exception : copyright peut rester petit */
  .bottom-nav a { font-size: 10px; }   /* exception : bottom nav labels restent petits */
}
```

> Les 2 exceptions (copyright footer et labels bottom nav) sont acceptables car non critiques pour la lecture.

### Pas de hover sur mobile

Les effets hover ne s'appliquent pas en mobile (pas de souris). Utiliser `@media (hover: hover)` pour les hovers :

```css
/* Au lieu de : */
.prod-card:hover { transform: translateY(-4px); }

/* Utiliser : */
@media (hover: hover) {
  .prod-card:hover { transform: translateY(-4px); }
}
```

Ceci empêche les "sticky hovers" sur mobile (l'effet reste après un tap, ce qui est visuellement buggé).

**Appliquer sur :** `.prod-card:hover`, `.col-card:hover`, `.btn-gold:hover`, `.btn-outline:hover`, `.col-btn:hover`, `.hp-card:hover`, tous les liens `:hover` avec des effets visuels (pas juste un changement de couleur — le changement de couleur au tap est OK).

### Tap highlight

Supprimer le highlight bleu/gris par défaut sur iOS/Android :

```css
* { -webkit-tap-highlight-color: transparent; }
```

### iOS input zoom

iOS zoom automatiquement quand un input a un font-size < 16px. Pour éviter :

```css
@media (max-width: 768px) {
  input, select, textarea { font-size: 16px !important; }
}
```

Appliqué dans `hokuno.css`. Ceci surcharge le 14px desktop des inputs pour éviter le zoom involontaire.

---

## 2. NAVIGATION MOBILE

Détail complet dans `specs/NAVIGATION.md` §2-3. Résumé :

### Header sticky

```css
.nav {
  padding: 12px 20px;
  top: 12px;
  width: calc(100% - 24px);
  border-radius: 10px;
}
.nav-logo img { height: 30px; }
.nav-links { display: none; }
.nav-right { display: none; }
.nav-hamburger { display: flex; }
```

### Menu overlay

- Slide-in depuis la droite (`translateX(100%)` → `translateX(0)`)
- Fond `#000000` opaque
- Liens en `28px`, font-weight `700`, centrés
- Scroll lock sur body (`.menu-open { overflow: hidden; position: fixed; }`)
- Fermeture : tap lien, tap X, touche Escape
- Sélecteur langue FR/EN en bas
- Bottom nav caché quand menu ouvert

### Bottom nav

- Position fixed en bas, z-index 9999
- `padding-bottom: max(10px, env(safe-area-inset-bottom))` pour iPhone
- 4 icônes : Accueil, Collections, Panier, Compte
- Badge panier avec compteur AJAX
- Page active en doré

---

## 3. PAGE D'ACCUEIL MOBILE

### Hero

```css
.hero {
  flex-direction: column;   /* texte au-dessus, image en dessous */
  padding: 100px 24px 40px;
  min-height: auto;          /* pas 100vh en mobile */
  gap: 32px;
}
.hero-left { flex: 1; padding-right: 0; text-align: left; }
.hero-right { flex: 1; width: 100%; }
.hero-img { max-height: 50vh; }
.hero-title { font-size: 38px; letter-spacing: 0; }
.hero-katakana { font-size: 30px; }
```

### Boutons hero

```css
.hero-buttons { flex-direction: column; gap: 12px; }
.btn-gold, .btn-outline { width: 100%; justify-content: center; padding: 16px 24px; }
```

### Éléments cachés

```css
.v-left, .v-right { display: none; }     /* textes verticaux */
.hero-products { display: none; }          /* carrousel produits hero */
```

### Trust bar

```css
.trust { flex-direction: column; padding: 20px 24px; gap: 10px; }
.trust-card { max-width: 100%; }
```

### Section collections

```css
.cols { padding: 60px 24px; }
.cols-title { font-size: 30px; }
.cols-grid { grid-template-columns: 1fr 1fr; gap: 12px; }
.col-card img { height: 260px; }
.col-card-info { padding: 18px; }
```

### Produits phares

```css
.feat { padding: 60px 24px; }
.feat-grid { grid-template-columns: 1fr 1fr; gap: 12px; }
.prod-card img { height: 220px; }
```

---

## 4. PAGE COLLECTION MOBILE

### Grille produits

```css
.products-grid { grid-template-columns: 1fr 1fr; gap: 12px; }
```

### Filtres mobile

Détail dans `specs/COLLECTIONS.md` §6.

- Bouton "FILTRES" en haut de la grille (visible uniquement en mobile)
- Au tap : drawer slide-up depuis le bas
- Fond drawer : `#000000`
- Bordure top : `1px solid rgba(255,255,255,0.08)`
- Contenu : filtres empilés verticalement
- Bouton "APPLIQUER" (`.btn-gold`) en bas
- Bouton "RÉINITIALISER" en texte simple
- Fermeture : tap sur "APPLIQUER" ou tap hors du drawer

```css
@media (max-width: 768px) {
  .filter-bar { display: none; }  /* masquer la barre de filtres desktop */
  .filter-mobile-btn { display: flex; }  /* afficher le bouton FILTRES */
  
  .filter-drawer {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    max-height: 70vh;
    background: #000000;
    border-top: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px 16px 0 0;
    padding: 24px;
    transform: translateY(100%);
    transition: transform 0.3s ease;
    z-index: 9998;
    overflow-y: auto;
  }
  .filter-drawer.open { transform: translateY(0); }
}
```

### Tri mobile

Le select de tri passe en pleine largeur sous le bouton filtres.

---

## 5. PAGE PRODUIT MOBILE

Détail dans `specs/PRODUIT.md` §15.

### Layout

```css
.product-wrap {
  flex-direction: column;
  padding: 100px 24px 40px;
  gap: 24px;
}
.product-name { font-size: 28px; }
```

Image full width en haut, infos produit en dessous.

### Swipe galerie

Touch swipe gauche/droite sur l'image principale pour naviguer entre les images.
Seuil : 50px de déplacement minimum. Code JS dans `specs/PRODUIT.md` §15.

### Miniatures

Scroll horizontal (pas de wrap) :

```css
@media (max-width: 768px) {
  .product-thumbs {
    overflow-x: auto;
    flex-wrap: nowrap;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none; /* masquer scrollbar Firefox */
  }
  .product-thumbs::-webkit-scrollbar { display: none; } /* masquer scrollbar Chrome/Safari */
}
```

### Bouton "AJOUTER AU PANIER" sticky

Le bouton panier est fixé en bas de l'écran, au-dessus du bottom nav :

```css
@media (max-width: 768px) {
  .product-actions {
    position: fixed;
    bottom: 60px;  /* au-dessus du bottom nav */
    left: 0; right: 0;
    padding: 12px 20px;
    background: rgba(0,0,0,0.95);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-top: 1px solid rgba(255,255,255,0.06);
    z-index: 9998;
  }
  .product-wrap { padding-bottom: 140px; } /* espace pour sticky + bottom nav */
}
```

### Accordéons produit

```css
@media (max-width: 768px) {
  .product-accordions { margin: 32px 0 0; max-width: 100%; }
}
```

### Produits similaires

```css
@media (max-width: 768px) {
  .related { padding: 0 24px 80px; }
  .related-grid { grid-template-columns: 1fr 1fr; gap: 12px; }
}
```

---

## 6. PAGE PANIER MOBILE

### Cart items

```css
@media (max-width: 768px) {
  .cart-item { flex-wrap: wrap; }
  .cart-item-img { width: 80px; height: 80px; }
  .cart-item-qty { margin-top: 12px; }
}
```

### Bouton checkout sticky

Comme le bouton panier produit, le bouton checkout est sticky en bas :

```css
@media (max-width: 768px) {
  .cart-checkout-sticky {
    position: fixed;
    bottom: 60px;
    left: 0; right: 0;
    padding: 12px 20px;
    background: rgba(0,0,0,0.95);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-top: 1px solid rgba(255,255,255,0.06);
    z-index: 9998;
  }
}
```

---

## 7. PAGES STATIQUES MOBILE

### About, FAQ, Mentions légales

```css
@media (max-width: 768px) {
  .page-content h2 { font-size: 24px; }
  .page-content p { font-size: 15px; }
}
```

### Contact

```css
@media (max-width: 768px) {
  .contact-wrap { grid-template-columns: 1fr; gap: 32px; }
}
```

### Blog

```css
@media (max-width: 768px) {
  .blog-grid { grid-template-columns: 1fr; }
}
```

### Compte client

```css
@media (max-width: 768px) {
  .auth-wrap { max-width: 100%; padding: 0; }
}
```

---

## 8. FOOTER MOBILE

```css
@media (max-width: 768px) {
  .foot { padding: 40px 24px; margin-bottom: 70px; }
  .foot-grid { grid-template-columns: 1fr; gap: 32px; text-align: center; }
  .newsletter-form { flex-direction: column; }
  .newsletter-input { width: 100%; }
}
```

Le `margin-bottom: 70px` empêche le bottom nav de masquer le bas du footer.

---

## 9. SAFE AREAS (iPhone notch / Dynamic Island)

### Bottom safe area

Déjà géré dans le bottom nav :

```css
.mobile-nav {
  padding: 10px 0 max(10px, env(safe-area-inset-bottom));
}
```

### Top safe area

La navbar est à `top: 12px`, ce qui laisse de la marge pour le notch/Dynamic Island. Pas de `env(safe-area-inset-top)` nécessaire car la navbar n'est pas collée au bord.

### Viewport meta pour les safe areas

Ajouter `viewport-fit=cover` pour que le contenu s'étende sous les safe areas (le CSS `env()` gère les marges) :

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
```

---

## 10. PERFORMANCE MOBILE

### Scroll smooth

```css
html { scroll-behavior: smooth; }
```

### Overflow-x

```css
body { overflow-x: hidden; }  /* empêche le scroll horizontal involontaire */
```

### Scrolling touch fluide (iOS)

```css
.product-thumbs,
.filter-drawer {
  -webkit-overflow-scrolling: touch;
}
```

### Images lazy loading

Toutes les images sauf le hero ont `loading="lazy"`. En mobile, c'est encore plus critique car la connexion est souvent plus lente.

### Réduction des animations

Respecter la préférence utilisateur pour les animations réduites :

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## 11. POSITION FIXED — PROBLÈMES iOS

iOS a des bugs connus avec `position: fixed` quand le clavier virtuel est ouvert ou quand le body est scrollé. Solutions :

### Scroll lock quand le menu overlay est ouvert

```css
body.menu-open {
  overflow: hidden;
  position: fixed;
  width: 100%;
  /* top est géré en JS pour mémoriser la position de scroll */
}
```

Le JS sauvegarde `window.scrollY` avant de fixer le body, et restore la position au fermer. Détail dans `specs/NAVIGATION.md` §2.

### Bouton sticky add-to-cart

Le bouton sticky produit utilise `position: fixed` et non `position: sticky`. `sticky` est plus propre mais a des problèmes avec les overflow parents sur iOS. `fixed` est fiable.

---

## 12. CHECKLIST MOBILE

Tests à effectuer sur vrai device (pas uniquement en mode responsive du navigateur) :

### Devices cibles

| Device | Taille | Priorité |
|--------|--------|----------|
| iPhone SE (2022) | 375×667 | 🔴 Plus petit écran courant |
| iPhone 14 / 15 | 390×844 | 🔴 iPhone standard |
| iPhone 14 Pro Max | 430×932 | 🟡 Grand iPhone |
| Samsung Galaxy S23 | 360×780 | 🔴 Android standard |
| iPad Mini | 768×1024 | 🟡 Limite breakpoint tablette |

### Tests par composant

- [ ] **Navbar** : logo 30px, hamburger visible et tappable, pas de liens texte visibles
- [ ] **Menu overlay** : slide-in fluide, tous liens tappables, scroll lock body, fermeture au tap lien
- [ ] **Bottom nav** : visible, 4 icônes, badge panier, page active dorée, pas masqué par le contenu
- [ ] **Hero** : texte lisible (38px), image sous le texte, boutons pleine largeur, pas de textes verticaux
- [ ] **Trust bar** : cartes empilées, texte lisible (14px min)
- [ ] **Collections grille** : 2 colonnes, images pas coupées, texte lisible
- [ ] **Filtres** : bouton FILTRES visible, drawer s'ouvre, filtres tappables, bouton APPLIQUER
- [ ] **Product cards** : 2 colonnes, image + titre + prix visibles, tappable
- [ ] **Page produit** : image full width, swipe fonctionne, infos sous l'image, bouton panier sticky visible
- [ ] **Variantes** : swatches couleur tappables (44px min), boutons taille tappables
- [ ] **Panier** : items lisibles, quantité +/- tappable, bouton checkout sticky visible
- [ ] **Formulaire contact** : champs pleine largeur, pas de zoom au focus (font-size 16px), clavier ne masque pas le contenu
- [ ] **Footer** : 1 colonne, liens tappables, newsletter fonctionnelle, pas masqué par bottom nav
- [ ] **Scroll** : fluide partout, pas de scroll horizontal involontaire, pas de "bounce" bizarre
- [ ] **Safe areas** : contenu pas masqué par notch/Dynamic Island (haut) ni barre home (bas)
- [ ] **Orientation paysage** : le site ne casse pas si le téléphone est tourné (pas d'obligation d'être parfait, juste pas cassé)
- [ ] **Performance** : chargement < 3s en 4G, pas de layout shift visible, images lazy loading

---

## 13. CSS MOBILE COMPLET — RÉSUMÉ

L'ordre des media queries dans `hokuno.css` (section 40-42 de `specs/THEME.md` §13) :

```css
/* ═══ 40. TABLETTE (max-width: 1024px) ═══ */
@media (max-width: 1024px) {
  .hero-title { font-size: 56px; }
  .cols-grid { grid-template-columns: repeat(2, 1fr); }
  .feat-grid { grid-template-columns: repeat(2, 1fr); }
  .products-grid { grid-template-columns: repeat(2, 1fr); }
  .related-grid { grid-template-columns: repeat(2, 1fr); }
  .hero-products { display: none; }
}

/* ═══ 41. MOBILE (max-width: 768px) ═══ */
@media (max-width: 768px) {
  /* Navbar */
  .nav { padding: 12px 20px; top: 12px; width: calc(100% - 24px); border-radius: 10px; }
  .nav-logo img { height: 30px; }
  .nav-links, .nav-right { display: none; }
  .nav-hamburger { display: flex; }

  /* Hero */
  .hero { flex-direction: column; padding: 100px 24px 40px; min-height: auto; gap: 32px; }
  .hero-left { flex: 1; padding-right: 0; }
  .hero-right { width: 100%; }
  .hero-img { max-height: 50vh; }
  .hero-title { font-size: 38px; letter-spacing: 0; }
  .hero-katakana { font-size: 30px; }
  .hero-buttons { flex-direction: column; gap: 12px; }
  .btn-gold, .btn-outline { width: 100%; justify-content: center; padding: 16px 24px; }
  .v-left, .v-right { display: none; }
  .hero-products { display: none; }

  /* Trust */
  .trust { flex-direction: column; padding: 20px 24px; gap: 10px; }
  .trust-card { max-width: 100%; }
  .trust-label, .trust-sub { font-size: 14px; }

  /* Collections */
  .cols { padding: 60px 24px; }
  .cols-title { font-size: 30px; }
  .cols-grid { grid-template-columns: 1fr 1fr; gap: 12px; }
  .col-card img { height: 260px; }
  .col-card-info { padding: 18px; }
  .col-card-info p { font-size: 14px; }

  /* Produits */
  .feat { padding: 60px 24px; }
  .feat-grid, .products-grid, .related-grid { grid-template-columns: 1fr 1fr; gap: 12px; }
  .prod-card img { height: 220px; }
  .prod-info h4 { font-size: 14px; }
  .product-badge { font-size: 14px; }

  /* Page wrap */
  .page-wrap { padding: 100px 24px 100px; }

  /* Produit */
  .product-wrap { flex-direction: column; padding: 100px 24px 40px; gap: 24px; }
  .product-name { font-size: 28px; }
  .product-price-tag { font-size: 24px; }
  .product-accordions { max-width: 100%; }
  .product-thumbs { overflow-x: auto; flex-wrap: nowrap; -webkit-overflow-scrolling: touch; }
  .product-thumbs::-webkit-scrollbar { display: none; }
  .product-wrap { padding-bottom: 140px; }
  .product-actions {
    position: fixed; bottom: 60px; left: 0; right: 0;
    padding: 12px 20px;
    background: rgba(0,0,0,0.95); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
    border-top: 1px solid rgba(255,255,255,0.06); z-index: 9998;
  }

  /* Panier */
  .cart-item-img { width: 80px; height: 80px; }

  /* Pages statiques */
  .page-content h2 { font-size: 24px; }
  .contact-wrap { grid-template-columns: 1fr; }
  .blog-grid { grid-template-columns: 1fr; }
  .auth-wrap { max-width: 100%; }

  /* Footer */
  .foot { padding: 40px 24px; margin-bottom: 70px; }
  .foot-grid { grid-template-columns: 1fr; gap: 32px; text-align: center; }

  /* Bottom nav */
  .mobile-nav { display: flex; }

  /* Filtres */
  .filter-bar { display: none; }
  .filter-mobile-btn { display: flex; }

  /* Breadcrumbs */
  .breadcrumbs { font-size: 14px; }

  /* Pagination */
  .page-num { min-width: 44px; min-height: 44px; }

  /* Inputs */
  input, select, textarea { font-size: 16px !important; }

  /* Similaires */
  .related { padding: 0 24px 80px; }
}

/* ═══ 42. DESKTOP ONLY ═══ */
@media (min-width: 769px) {
  .mobile-nav { display: none; }
  .mobile-menu { display: none; }
  .filter-mobile-btn { display: none; }
}

/* ═══ HOVER ONLY ═══ */
@media (hover: hover) {
  .prod-card:hover { transform: translateY(-4px); border-color: rgba(212,168,83,0.35); box-shadow: 0 12px 40px rgba(0,0,0,0.3); }
  .prod-card:hover img { transform: scale(1.04); }
  .col-card:hover { transform: scale(1.015); box-shadow: 0 8px 40px rgba(212,168,83,0.08); }
  .col-card:hover img { transform: scale(1.03); }
  .btn-gold:hover { background: #c49a3d; transform: translateY(-1px); }
  .col-btn:hover { background: #D4A853; color: #000; }
  .hp-card:hover { border-color: rgba(212,168,83,0.4); }
}

/* ═══ REDUCED MOTION ═══ */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```
