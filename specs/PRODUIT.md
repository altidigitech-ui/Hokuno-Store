# specs/PRODUIT.md — Page produit

> Contrat pour Claude Code. Chaque élément de la fiche produit est défini ici.
> Le cart AJAX (ajout sans rechargement, notification, compteurs) est dans `specs/NAVIGATION.md` §9.
> Le design system (couleurs, typo) est dans `specs/THEME.md`.

---

## 1. STRUCTURE DE LA PAGE

Template : `product.liquid`
Breadcrumbs : `Accueil › [Collection] › [Titre produit]`
Mockup de référence : `assets/design-reference/product-page.png`

### Layout desktop

```
[BREADCRUMBS]
[──────────────────────────────────────────────────────]
[                    |                                  ]
[   IMAGE GRANDE     |   COLLECTION                     ]
[                    |   TITRE H1                       ]
[                    |   PRIX                           ]
[   [min] [min] [min]|   COULEUR (swatches)             ]
[    miniatures      |   TAILLE (boutons)               ]
[                    |   QUANTITÉ (+/-)                  ]
[                    |   [AJOUTER AU PANIER]   [♡]      ]
[                    |   BADGES CONFIANCE                ]
[──────────────────────────────────────────────────────]
[DESCRIPTION / BACKSTORY          (accordéon)           ]
[INFOS PRODUIT                    (accordéon)           ]
[GUIDE DES TAILLES               (accordéon)           ]
[──────────────────────────────────────────────────────]
[VOUS POURRIEZ AUSSI AIMER — 4 produits                ]
[──────────────────────────────────────────────────────]
[PARTAGE SOCIAL                                         ]
```

### Layout : 2 colonnes

- Colonne gauche (55%) : galerie images
- Colonne droite (45%) : infos produit
- Gap : `48px`
- Padding : `120px 64px 60px`

---

## 2. GALERIE D'IMAGES

### Image principale

- Position : en haut de la colonne gauche
- Largeur : 100% de la colonne
- Border-radius : `12px`
- Fond : `#111` (visible pendant le chargement)
- Source : `{{ product.selected_or_first_available_variant.image | default: product.featured_image | image_url: width: 1200 }}`
- Alt : `{{ product.title }}`
- ID HTML : `id="main-product-image"` (pour le changement via JS)

### Miniatures

- Position : sous l'image principale, en ligne horizontale
- Gap : `8px`
- Margin-top : `12px`
- Chaque miniature : `80×80px`, border-radius `6px`, object-fit `cover`, cursor `pointer`
- Bordure par défaut : `1px solid rgba(255,255,255,0.1)`
- Bordure active/hover : `1px solid #D4A853`
- La miniature correspondant à l'image principale affichée a la bordure dorée

### Comportement au clic sur une miniature

```javascript
// Dans hokuno.js
document.querySelectorAll('.product-thumb').forEach(thumb => {
  thumb.addEventListener('click', () => {
    const mainImg = document.getElementById('main-product-image');
    mainImg.src = thumb.dataset.fullSrc;
    mainImg.alt = thumb.alt;
    // Mettre à jour la bordure active
    document.querySelectorAll('.product-thumb').forEach(t => t.classList.remove('thumb-active'));
    thumb.classList.add('thumb-active');
  });
});
```

### Liquid pour la galerie

```liquid
<div class="product-images">
  <img id="main-product-image"
       src="{{ product.selected_or_first_available_variant.image | default: product.featured_image | image_url: width: 1200 }}"
       alt="{{ product.title }}"
       class="product-main-img">

  <div class="product-thumbs">
    {% for image in product.images %}
      <img class="product-thumb {% if forloop.first %}thumb-active{% endif %}"
           src="{{ image | image_url: width: 200 }}"
           data-full-src="{{ image | image_url: width: 1200 }}"
           alt="{{ product.title }} — vue {{ forloop.index }}"
           loading="lazy">
    {% endfor %}
  </div>
</div>
```

### Ordre des images (géré dans Printify/Shopify, pas dans le thème)

Le thème affiche les images dans l'ordre fourni par Shopify. L'ordre correct est défini dans `specs/MOCKUPS.md` et configuré dans Printify :

| Type de produit | Image 1 (featured) | Image 2 | Image 3 |
|-----------------|---------------------|---------|---------|
| T-shirt | Back 2 (dos — design visible) | Front 2 (devant — logo) | Folded |
| Mug | Left ou Right (côté design) | Back | Front |
| Coque | Front (design visible) | — | — |
| Accessoires | Vue montrant le design/logo en priorité | Autres vues | — |

---

## 3. SÉLECTEUR DE COULEUR — SWATCHES VISUELS

### Rendu

Des cercles de couleur cliquables (PAS un dropdown `<select>`).

### Liquid

```liquid
{% assign color_option_index = nil %}
{% for option in product.options %}
  {% assign option_name_down = option | downcase %}
  {% if option_name_down == 'color' or option_name_down == 'colour' or option_name_down == 'couleur' %}
    {% assign color_option_index = forloop.index0 %}
  {% endif %}
{% endfor %}

{% if color_option_index != nil %}
  <p class="option-label">{{ 'product.color' | t }}</p>
  <div class="color-swatches">
    {% assign seen_colors = "" %}
    {% for variant in product.variants %}
      {% assign color = variant.options[color_option_index] %}
      {% unless seen_colors contains color %}
        {% assign seen_colors = seen_colors | append: color | append: "," %}
        <button type="button"
                class="color-swatch {% if forloop.first %}swatch-active{% endif %}"
                data-color="{{ color }}"
                data-image="{{ variant.image | image_url: width: 1200 }}"
                title="{{ color }}"
                style="background-color: {{ color | handleize | replace: 'black', '#1a1a1a' | replace: 'navy', '#1e3a5f' | replace: 'white', '#f5f5f5' | replace: 'natural', '#f5f0e1' | replace: 'gravel', '#7a7a6d' | replace: 'red', '#dc2626' | replace: 'royal', '#1e40af' | replace: 'safety-pink', '#ff69b4' | replace: 'sky', '#87ceeb' | replace: 'sand', '#c2b280' | replace: 'sport-grey', '#9ca3af' }}">
        </button>
      {% endunless %}
    {% endfor %}
  </div>
{% endif %}
```

### Style swatches

```css
.color-swatches { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px; }
.color-swatch {
  width: 32px; height: 32px; border-radius: 50%; border: 2px solid transparent;
  cursor: pointer; transition: all 0.3s; position: relative;
  outline: 2px solid rgba(255,255,255,0.1); outline-offset: 2px;
}
.color-swatch:hover { outline-color: rgba(255,255,255,0.3); }
.color-swatch.swatch-active { outline-color: #D4A853; outline-width: 2px; }
```

### Comportement au changement de couleur

Quand on clique un swatch couleur :
1. L'image principale change vers l'image associée à cette couleur
2. Le swatch actif change (bordure dorée)
3. Le variant ID caché dans le formulaire se met à jour
4. Le prix se met à jour (si le prix varie par couleur)
5. Les tailles disponibles se mettent à jour (certaines couleurs peuvent ne pas avoir toutes les tailles)

```javascript
// Dans hokuno.js
document.querySelectorAll('.color-swatch').forEach(swatch => {
  swatch.addEventListener('click', () => {
    // Mettre à jour l'image
    const mainImg = document.getElementById('main-product-image');
    if (swatch.dataset.image) {
      mainImg.src = swatch.dataset.image;
    }
    // Mettre à jour le swatch actif
    document.querySelectorAll('.color-swatch').forEach(s => s.classList.remove('swatch-active'));
    swatch.classList.add('swatch-active');
    // Mettre à jour le variant sélectionné
    updateSelectedVariant();
  });
});
```

---

## 4. SÉLECTEUR DE TAILLE — BOUTONS

### Rendu

Des boutons rectangulaires cliquables (PAS un dropdown `<select>`).

### Liquid

```liquid
{% assign size_option_index = nil %}
{% for option in product.options %}
  {% assign option_name_down = option | downcase %}
  {% if option_name_down == 'size' or option_name_down == 'taille' %}
    {% assign size_option_index = forloop.index0 %}
  {% endif %}
{% endfor %}

{% if size_option_index != nil %}
  <p class="option-label">{{ 'product.size' | t }}</p>
  <div class="size-buttons">
    {% assign seen_sizes = "" %}
    {% for variant in product.variants %}
      {% assign size = variant.options[size_option_index] %}
      {% unless seen_sizes contains size %}
        {% assign seen_sizes = seen_sizes | append: size | append: "," %}
        <button type="button"
                class="size-btn {% if forloop.first %}active{% endif %} {% unless variant.available %}disabled{% endunless %}"
                data-size="{{ size }}"
                {% unless variant.available %}disabled{% endunless %}>
          {{ size }}
        </button>
      {% endunless %}
    {% endfor %}
  </div>
{% endif %}
```

### Style

```css
.size-buttons { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 12px; }
.size-btn {
  padding: 12px 20px; min-width: 52px; text-align: center;
  border: 1px solid rgba(255,255,255,0.15); background: transparent;
  color: #fff; font-size: 14px; font-weight: 600; border-radius: 4px;
  cursor: pointer; transition: all 0.3s;
}
.size-btn:hover, .size-btn.active { border-color: #D4A853; color: #D4A853; }
.size-btn.disabled {
  opacity: 0.25; cursor: not-allowed; text-decoration: line-through;
  pointer-events: none;
}
```

### Tailles disponibles

- T-shirts : S, M, L, XL (2XL–5XL désactivées)
- Mugs : 11oz, 15oz (option "Size" ou variantes directes)
- Coques : variantes par modèle iPhone (iPhone 11 → iPhone 17)
- Accessoires : variable selon le produit

Un bouton de taille est `disabled` (grisé, barré) si `variant.available == false` pour cette combinaison couleur + taille.

---

## 5. LOGIQUE DE SÉLECTION DES VARIANTS (JS)

### Matrice de variants

Au chargement de la page, construire un objet JS avec tous les variants :

```liquid
<script>
  const productVariants = [
    {% for variant in product.variants %}
    {
      id: {{ variant.id }},
      available: {{ variant.available }},
      price: {{ variant.price }},
      compareAtPrice: {{ variant.compare_at_price | default: 0 }},
      options: {{ variant.options | json }},
      image: "{{ variant.image | image_url: width: 1200 }}"
    }{% unless forloop.last %},{% endunless %}
    {% endfor %}
  ];
</script>
```

### Fonction de sélection

```javascript
// Dans hokuno.js
function updateSelectedVariant() {
  const selectedColor = document.querySelector('.color-swatch.swatch-active')?.dataset.color;
  const selectedSize = document.querySelector('.size-btn.active')?.dataset.size;

  const variant = productVariants.find(v =>
    v.options.includes(selectedColor) && v.options.includes(selectedSize)
  );

  if (variant) {
    // Mettre à jour l'input hidden du formulaire
    document.querySelector('input[name="id"]').value = variant.id;
    // Mettre à jour le prix
    updatePrice(variant.price, variant.compareAtPrice);
    // Activer/désactiver le bouton d'ajout
    const addBtn = document.querySelector('.add-cart');
    addBtn.disabled = !variant.available;
    addBtn.textContent = variant.available
      ? (addBtn.dataset.textAdd || 'AJOUTER AU PANIER')
      : (addBtn.dataset.textSoldout || 'ÉPUISÉ');
  }
}
```

---

## 6. PRIX

### Affichage

```liquid
<div class="product-pricing">
  {% if product.compare_at_price > product.price %}
    <span class="product-price-compare">{{ product.compare_at_price | money }}</span>
    <span class="product-price-tag product-price-sale">{{ product.price | money }}</span>
    <span class="product-price-badge">-{{ product.compare_at_price | minus: product.price | times: 100 | divided_by: product.compare_at_price }}%</span>
  {% else %}
    <span class="product-price-tag">{{ product.price | money }}</span>
  {% endif %}
</div>
```

### Style

```css
.product-pricing { display: flex; align-items: baseline; gap: 12px; margin-top: 16px; }
.product-price-tag { font-size: 28px; font-weight: 700; color: #D4A853; }
.product-price-compare { font-size: 18px; color: rgba(255,255,255,0.35); text-decoration: line-through; }
.product-price-sale { color: #ff4444; }
.product-price-badge {
  font-size: 12px; font-weight: 700; background: rgba(255,68,68,0.15);
  color: #ff4444; padding: 4px 8px; border-radius: 4px; letter-spacing: 0.5px;
}
```

### Mise à jour dynamique via JS

Quand le variant change (couleur ou taille), le prix affiché se met à jour :

```javascript
function updatePrice(price, compareAtPrice) {
  const priceEl = document.querySelector('.product-price-tag');
  const compareEl = document.querySelector('.product-price-compare');
  const badgeEl = document.querySelector('.product-price-badge');
  // price est en centimes — convertir en format monétaire
  priceEl.textContent = formatMoney(price);
  if (compareAtPrice && compareAtPrice > price) {
    if (compareEl) compareEl.textContent = formatMoney(compareAtPrice);
    if (compareEl) compareEl.style.display = '';
    if (badgeEl) badgeEl.style.display = '';
  } else {
    if (compareEl) compareEl.style.display = 'none';
    if (badgeEl) badgeEl.style.display = 'none';
  }
}
```

> Note : `formatMoney()` doit utiliser le format de devise configuré dans Shopify (`{{ shop.money_format }}`).

---

## 7. QUANTITÉ

### Sélecteur +/−

```html
<div class="product-qty">
  <button type="button" class="qty-btn" onclick="changeQty(-1)">−</button>
  <input type="number" class="qty-input" id="product-qty" name="quantity" value="1" min="1" max="10">
  <button type="button" class="qty-btn" onclick="changeQty(1)">+</button>
</div>
```

```javascript
function changeQty(delta) {
  const input = document.getElementById('product-qty');
  let val = parseInt(input.value) + delta;
  if (val < 1) val = 1;
  if (val > 10) val = 10;
  input.value = val;
}
```

### Style

```css
.product-qty { display: flex; align-items: center; gap: 0; margin-top: 20px; }
.qty-btn {
  width: 44px; height: 44px; border: 1px solid rgba(255,255,255,0.15);
  background: transparent; color: #fff; font-size: 18px;
  cursor: pointer; transition: all 0.3s; display: flex;
  align-items: center; justify-content: center;
}
.qty-btn:first-child { border-radius: 6px 0 0 6px; }
.qty-btn:last-child { border-radius: 0 6px 6px 0; }
.qty-btn:hover { border-color: #D4A853; color: #D4A853; }
.qty-input {
  width: 52px; height: 44px; text-align: center; border: 1px solid rgba(255,255,255,0.15);
  border-left: none; border-right: none; background: transparent;
  color: #fff; font-size: 16px; font-weight: 600; font-family: 'Inter', sans-serif;
  -moz-appearance: textfield;
}
.qty-input::-webkit-inner-spin-button { -webkit-appearance: none; }
```

---

## 8. BOUTON AJOUTER AU PANIER + FAVORIS

### Layout

```html
<div class="product-actions">
  <button type="button" class="add-cart"
          data-text-add="{{ 'product.add_to_cart' | t }}"
          data-text-soldout="{{ 'product.sold_out' | t }}"
          onclick="addToCart(document.querySelector('input[name=id]').value, document.getElementById('product-qty').value)">
    {{ 'product.add_to_cart' | t }} 🛒
  </button>
  <button type="button" class="wishlist-btn" aria-label="{{ 'product.add_to_wishlist' | t }}">
    ♡
  </button>
</div>
```

### Style

```css
.product-actions { display: flex; gap: 12px; margin-top: 24px; }
.add-cart {
  flex: 1; padding: 18px; background: #D4A853; color: #000000; border: none;
  font-size: 15px; font-weight: 700; letter-spacing: 1.5px; text-transform: uppercase;
  border-radius: 6px; cursor: pointer; transition: all 0.3s;
  display: flex; align-items: center; justify-content: center; gap: 10px;
}
.add-cart:hover { background: #c49a3d; transform: translateY(-1px); }
.add-cart:disabled { background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.3); cursor: not-allowed; transform: none; }
.wishlist-btn {
  width: 56px; height: 56px; border: 1px solid rgba(255,255,255,0.15);
  background: transparent; color: rgba(255,255,255,0.5); font-size: 22px;
  border-radius: 6px; cursor: pointer; transition: all 0.3s;
  display: flex; align-items: center; justify-content: center;
}
.wishlist-btn:hover { border-color: #ff4444; color: #ff4444; }
.wishlist-btn.active { color: #ff4444; background: rgba(255,68,68,0.1); border-color: #ff4444; }
```

### Favoris — comportement v1

Le bouton toggle la classe `.active` (coeur rempli rouge). En v1, stockage en `localStorage` uniquement — pas de compte client.

```javascript
document.querySelector('.wishlist-btn')?.addEventListener('click', function() {
  this.classList.toggle('active');
  this.textContent = this.classList.contains('active') ? '♥' : '♡';
  // v1 : localStorage pour persister
  const productId = '{{ product.id }}';
  let wishlist = JSON.parse(localStorage.getItem('hokuno-wishlist') || '[]');
  if (this.classList.contains('active')) {
    if (!wishlist.includes(productId)) wishlist.push(productId);
  } else {
    wishlist = wishlist.filter(id => id !== productId);
  }
  localStorage.setItem('hokuno-wishlist', JSON.stringify(wishlist));
});
```

> Note : la spec ARCHITECTURE interdit localStorage dans les artifacts React, mais ici c'est du JS vanilla dans un contexte Shopify, pas un artifact. L'usage est approprié.

---

## 9. BADGES DE CONFIANCE

Sous le bouton panier. Identiques à la trust bar de l'accueil mais en version compacte.

```liquid
<div class="product-badges">
  <div class="product-badge">🌐 {{ 'product.badge_shipping' | t }}</div>
  <div class="product-badge">↩️ {{ 'product.badge_returns' | t }}</div>
  <div class="product-badge">🔒 {{ 'product.badge_payment' | t }}</div>
</div>
```

Textes FR : "Livraison internationale — Offerte dès 60€" / "Retours faciles — 30 jours" / "Paiements sécurisés — Cryptés et protégés"

### Style

```css
.product-badges { display: flex; flex-direction: column; gap: 12px; margin-top: 28px; }
.product-badge {
  display: flex; align-items: center; gap: 10px;
  font-size: 12px; color: rgba(255,255,255,0.5); letter-spacing: 0.5px;
}
```

---

## 10. DESCRIPTION / BACKSTORY

### Structure accordéon

Sous la zone de 2 colonnes (pleine largeur), 3 sections en accordéon :

```html
<div class="product-accordions">
  <!-- Section 1 : Description / Backstory -->
  <div class="accord-item open">
    <button class="accord-header">
      {{ 'product.description' | t }}
      <span class="accord-icon">−</span>
    </button>
    <div class="accord-body">
      {{ product.description }}
    </div>
  </div>

  <!-- Section 2 : Infos produit -->
  <div class="accord-item">
    <button class="accord-header">
      {{ 'product.details' | t }}
      <span class="accord-icon">+</span>
    </button>
    <div class="accord-body">
      <!-- voir section 11 -->
    </div>
  </div>

  <!-- Section 3 : Guide des tailles -->
  <div class="accord-item">
    <button class="accord-header">
      {{ 'product.size_guide' | t }}
      <span class="accord-icon">+</span>
    </button>
    <div class="accord-body">
      <!-- voir section 12 -->
    </div>
  </div>
</div>
```

La description contient le HTML injecté via Printify (backstory du personnage). Elle est ouverte par défaut (`.open`).

### Style accordéon

```css
.product-accordions { max-width: 900px; margin: 48px auto 0; }
.accord-item { border-top: 1px solid rgba(255,255,255,0.06); }
.accord-header {
  width: 100%; text-align: left; background: none; border: none;
  padding: 20px 0; color: #fff; font-size: 14px; font-weight: 600;
  letter-spacing: 1.5px; text-transform: uppercase; cursor: pointer;
  display: flex; justify-content: space-between; align-items: center;
  transition: color 0.3s;
}
.accord-header:hover { color: #D4A853; }
.accord-icon { font-size: 18px; color: #D4A853; }
.accord-body {
  max-height: 0; overflow: hidden; transition: max-height 0.4s ease;
}
.accord-item.open .accord-body { max-height: 1000px; }
.accord-item.open .accord-icon { content: '−'; }
.accord-body { padding: 0 0 20px; font-size: 14px; line-height: 1.8; color: rgba(255,255,255,0.6); }
```

### JS accordéon (même logique que FAQ)

```javascript
document.querySelectorAll('.accord-header').forEach(btn => {
  btn.addEventListener('click', () => {
    const item = btn.parentElement;
    item.classList.toggle('open');
    const icon = btn.querySelector('.accord-icon');
    icon.textContent = item.classList.contains('open') ? '−' : '+';
  });
});
```

---

## 11. INFOS PRODUIT

Contenu de la section "Infos produit" dans l'accordéon. Adapté dynamiquement selon le type de produit.

### T-shirts (Gildan 5000)

| Propriété | Valeur |
|-----------|--------|
| Matière | 100% coton (Gildan Heavy Cotton 5000) |
| Grammage | 180 g/m² |
| Coupe | Regular fit — Unisexe |
| Impression | DTG (Direct-to-Garment) haute définition |
| Entretien | Lavage machine 30°C — Ne pas javelliser — Séchage basse température — Repassage température moyenne envers |
| Fabrication | Print on Demand — Fabriqué à la commande |

### T-shirts Sport (Softstyle BP145)

| Propriété | Valeur |
|-----------|--------|
| Matière | 100% coton ring-spun (Gildan Softstyle) |
| Grammage | 150 g/m² |
| Coupe | Semi-fitted — Unisexe |

_(reste identique)_

### Mugs

| Propriété | Valeur |
|-----------|--------|
| Matière | Céramique |
| Contenance | 11oz (325 ml) / 15oz (440 ml) |
| Impression | Sublimation — résistant au lave-vaisselle et micro-ondes |
| Entretien | Compatible lave-vaisselle — Compatible micro-ondes |

### Coques iPhone

| Propriété | Valeur |
|-----------|--------|
| Type | Coque slim (Slim Case) |
| Matière | Polycarbonate rigide |
| Protection | Protège dos et côtés — accès à tous les ports et boutons |
| Impression | UV haute définition |
| Compatibilité | iPhone 11 → iPhone 17 |

### Implémentation Liquid

```liquid
{% if product.type contains 'T-Shirt' or product.type contains 'T-shirt' %}
  <p><strong>Matière :</strong> 100% coton (Gildan Heavy Cotton 5000)</p>
  <p><strong>Grammage :</strong> 180 g/m²</p>
  <p><strong>Coupe :</strong> Regular fit — Unisexe</p>
  <p><strong>Impression :</strong> DTG haute définition</p>
  <p><strong>Entretien :</strong> Lavage machine 30°C — Ne pas javelliser — Séchage basse température</p>
  <p><strong>Fabrication :</strong> Print on Demand — Fabriqué à la commande</p>
{% elsif product.type contains 'Mug' or product.type contains 'tasse' %}
  <!-- infos mug -->
{% elsif product.type contains 'Coque' or product.type contains 'Case' %}
  <!-- infos coque -->
{% else %}
  <p><strong>Fabrication :</strong> Print on Demand — Fabriqué à la commande</p>
{% endif %}
```

---

## 12. GUIDE DES TAILLES

Affiché uniquement pour les t-shirts. Contenu de la section "Guide des tailles" dans l'accordéon.

### Tableau

| Taille | Largeur (cm) | Longueur (cm) | Tour de poitrine (cm) |
|--------|:------------:|:-------------:|:---------------------:|
| S | 46 | 71 | 92 |
| M | 51 | 74 | 102 |
| L | 56 | 76 | 112 |
| XL | 61 | 79 | 122 |

> Mesures approximatives basées sur le Gildan 5000. Peuvent varier légèrement selon la couleur.

### Conseil

Texte sous le tableau : "Nos t-shirts taillent normalement. En cas de doute, prenez la taille au-dessus."

### Style tableau

```css
.size-guide-table { width: 100%; border-collapse: collapse; margin: 16px 0; }
.size-guide-table th {
  font-size: 12px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;
  color: rgba(255,255,255,0.5); padding: 12px; text-align: center;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}
.size-guide-table td {
  font-size: 14px; color: rgba(255,255,255,0.7); padding: 12px; text-align: center;
  border-bottom: 1px solid rgba(255,255,255,0.04);
}
```

### Liquid conditionnel

```liquid
{% if product.type contains 'T-Shirt' or product.type contains 'T-shirt' %}
  <table class="size-guide-table">
    <!-- tableau ci-dessus -->
  </table>
  <p style="font-size:13px;color:rgba(255,255,255,0.4);margin-top:12px">
    {{ 'product.size_guide_advice' | t }}
  </p>
{% else %}
  <p style="color:rgba(255,255,255,0.5)">{{ 'product.size_guide_na' | t }}</p>
{% endif %}
```

---

## 13. PRODUITS SIMILAIRES — "VOUS POURRIEZ AUSSI AIMER"

### Source

4 produits de la même collection que le produit affiché. Si le produit est dans plusieurs collections, utiliser la première (hors "all").

```liquid
{% assign related_collection = nil %}
{% for col in product.collections %}
  {% unless col.handle == 'all' or col.handle == 'frontpage' %}
    {% assign related_collection = col %}
    {% break %}
  {% endunless %}
{% endfor %}

{% if related_collection %}
<section class="related">
  <h2 class="related-title">{{ 'product.related' | t }}</h2>
  <div class="related-grid">
    {% for item in related_collection.products limit: 5 %}
      {% if item.id != product.id %}
        {% render 'product-card', product: item %}
      {% endif %}
    {% endfor %}
  </div>
</section>
{% endif %}
```

> Note : `limit: 5` car on exclut le produit courant du loop, ce qui laisse 4 produits affichés.

### Style

```css
.related { margin-top: 80px; padding: 0 64px 80px; }
.related-title {
  font-size: 14px; font-weight: 600; letter-spacing: 3px;
  text-transform: uppercase; text-align: center; margin-bottom: 40px;
  color: rgba(255,255,255,0.7);
}
.related-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; }
```

Texte FR : "VOUS POURRIEZ AUSSI AIMER"
Texte EN : "YOU MIGHT ALSO LIKE"

### Mobile

Grille : `repeat(2, 1fr)`, gap `12px`. Padding : `0 24px 80px`.

---

## 14. PARTAGE SOCIAL

Sous la section produits similaires.

```html
<div class="product-share">
  <span class="share-label">{{ 'product.share' | t }}</span>
  <button class="share-btn" onclick="shareOnTikTok()" title="TikTok">
    <!-- SVG TikTok -->
  </button>
  <button class="share-btn" onclick="shareOnInstagram()" title="Instagram">
    <!-- SVG Instagram -->
  </button>
  <button class="share-btn" onclick="copyLink()" title="{{ 'product.copy_link' | t }}">
    <!-- SVG Link/Chain -->
  </button>
</div>
```

### JS

```javascript
function copyLink() {
  navigator.clipboard.writeText(window.location.href);
  const btn = event.target.closest('.share-btn');
  btn.classList.add('copied');
  setTimeout(() => btn.classList.remove('copied'), 2000);
}

function shareOnTikTok() {
  window.open('https://www.tiktok.com/share?url=' + encodeURIComponent(window.location.href), '_blank');
}

function shareOnInstagram() {
  // Instagram n'a pas d'API de partage web direct
  // Copier le lien et ouvrir Instagram
  navigator.clipboard.writeText(window.location.href);
  window.open('https://www.instagram.com/', '_blank');
}
```

### Style

```css
.product-share { display: flex; align-items: center; gap: 16px; justify-content: center; padding: 24px 0 40px; }
.share-label { font-size: 12px; color: rgba(255,255,255,0.4); letter-spacing: 1px; text-transform: uppercase; }
.share-btn {
  width: 40px; height: 40px; border-radius: 50%; border: 1px solid rgba(255,255,255,0.1);
  background: transparent; color: rgba(255,255,255,0.5); cursor: pointer;
  display: flex; align-items: center; justify-content: center; transition: all 0.3s;
}
.share-btn:hover { border-color: #D4A853; color: #D4A853; }
.share-btn.copied { border-color: #22c55e; color: #22c55e; }
.share-btn svg { width: 18px; height: 18px; }
```

---

## 15. MOBILE (<768px)

### Layout

- Colonnes empilées : image full width en haut, infos en dessous
- Padding : `100px 24px 80px`

### Galerie mobile

- Image principale : full width
- Miniatures : scroll horizontal (pas de wrap)
- **Swipe gauche/droite** sur l'image principale pour changer d'image :

```javascript
// Dans hokuno.js — détection swipe
let touchStartX = 0;
const mainImg = document.getElementById('main-product-image');
if (mainImg) {
  mainImg.addEventListener('touchstart', e => { touchStartX = e.touches[0].clientX; });
  mainImg.addEventListener('touchend', e => {
    const diff = e.changedTouches[0].clientX - touchStartX;
    const thumbs = document.querySelectorAll('.product-thumb');
    const currentIndex = [...thumbs].findIndex(t => t.classList.contains('thumb-active'));
    if (diff < -50 && currentIndex < thumbs.length - 1) {
      thumbs[currentIndex + 1].click();
    } else if (diff > 50 && currentIndex > 0) {
      thumbs[currentIndex - 1].click();
    }
  });
}
```

### Bouton "Ajouter au panier" sticky

Sur mobile, le bouton d'ajout au panier est **sticky en bas de l'écran**, au-dessus du bottom nav :

```css
@media (max-width: 768px) {
  .product-actions {
    position: fixed; bottom: 60px; /* au-dessus du bottom nav */
    left: 0; right: 0; padding: 12px 20px;
    background: rgba(0,0,0,0.95); backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-top: 1px solid rgba(255,255,255,0.06);
    z-index: 9998; display: flex; gap: 12px;
  }
  .product-wrap { padding-bottom: 140px; } /* espace pour le sticky + bottom nav */
}
```

### Autres adaptations mobile

- Titre : font-size `28px` (vs `36px` desktop)
- Prix : font-size `24px` (vs `28px`)
- Swatches couleur : même taille (32px — touch target OK)
- Boutons taille : padding `10px 16px` (légèrement plus petits)
- Accordéons : pleine largeur, pas de max-width
- Produits similaires : grille 2 colonnes
- Partage social : centré

---

## 16. STRUCTURE COMPLÈTE DU TEMPLATE

Ordre exact des éléments dans `product.liquid` :

```liquid
<!-- templates/product.liquid -->
<div class="page-wrap product-page">
  {% render 'breadcrumbs' %}

  <div class="product-wrap">
    <!-- Colonne gauche : galerie -->
    <div class="product-images">
      <!-- image principale + miniatures (section 2) -->
    </div>

    <!-- Colonne droite : infos -->
    <div class="product-details">
      <p class="product-collection"><!-- collection name (section 1) --></p>
      <h1 class="product-name">{{ product.title }}</h1>
      <!-- Prix (section 6) -->
      <!-- Swatches couleur (section 3) -->
      <!-- Boutons taille (section 4) -->
      <!-- Quantité (section 7) -->
      <!-- Bouton panier + favoris (section 8) -->
      <!-- Badges confiance (section 9) -->
    </div>
  </div>

  <!-- Accordéons pleine largeur -->
  <div class="product-accordions">
    <!-- Description/backstory (section 10) -->
    <!-- Infos produit (section 11) -->
    <!-- Guide des tailles (section 12) -->
  </div>

  <!-- Produits similaires (section 13) -->
  <!-- Partage social (section 14) -->
</div>

<!-- Variant data pour JS -->
<script>
  const productVariants = [ /* section 5 */ ];
</script>
```

---

## 17. DONNÉES SEO PRODUIT

Détaillées dans `specs/SEO.md`. Résumé des données à inclure :

- Schema JSON-LD `Product` : name, image, description, brand, offers (price, availability, currency)
- Open Graph : og:type `product`, og:title, og:image (featured_image), og:price:amount, og:price:currency
- Meta title : `{{ product.title }} — HOKUNO ホクノ`
- Meta description : backstory tronquée à 155 caractères
- Canonical URL : `{{ canonical_url }}`
