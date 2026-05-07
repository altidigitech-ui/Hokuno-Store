# specs/COLLECTIONS.md — Collections

> Contrat pour Claude Code. Chaque collection, chaque filtre, chaque condition est défini ici.

---

## 1. LES 4 COLLECTIONS

### 1.1 WANTED

| Clé | Valeur |
|-----|--------|
| Handle Shopify | `wanted` |
| URL | `/collections/wanted` |
| Image de couverture | `card-wanted.png` (dans `assets/theme/` et `shopify-theme/assets/`) |
| Type de collection | Automatique |
| Condition | Titre du produit contient `wanted` (case-insensitive) |
| Nombre de produits | 277 |

**Description FR :**
> Des avis de recherche revisités. Les personnages ont traversé 30 ans de manga — ils ont mal vieilli, ils sont épuisés, éreintés par le temps. Ils ne sont plus dangereux. Ils veulent juste que ça se termine.

**Description EN :**
> Reimagined wanted posters. The characters have endured 30 years of manga — they've aged badly, exhausted and worn down by time. They're no longer dangerous. They just want it to end.

**Texte court (card homepage) :**
> Une traque. Un héritage. Une esthétique vintage.

**Produits :**

| Type | Quantité | Détail |
|------|----------|--------|
| T-shirts light FR | 46 | Gildan BP6, White/Natural/Gravel/Red/Royal (20 variantes) |
| T-shirts dark FR | 46 | Gildan BP6, Black/Navy (8 variantes) |
| Mugs FR | 46 | Céramique BP478, 11oz + 15oz |
| T-shirts light EN | 46 | Idem light FR, titre contient "EN" |
| T-shirts dark EN | 46 | Idem dark FR, titre contient "NOIR EN" |
| Mugs EN | 46 | Ceramic mug BP478, 11oz + 15oz |
| Coque | 1 | BP268 Slim Case — "Coque Wanted The End Brique Saga 1" (à renommer sur Printify) |
| **Total** | **277** | |

**Personnages :** 46 — liste complète dans `collections/wanted.json`

**Ton :** Humour noir, fatigue existentielle, satire.

---

### 1.2 DIRECTION

| Clé | Valeur |
|-----|--------|
| Handle Shopify | `direction` |
| URL | `/collections/direction` |
| Image de couverture | `card-direction.png` |
| Type de collection | Automatique |
| Condition | Titre du produit contient `direction` (case-insensitive) |
| Nombre de produits | 80 |

**Description FR :**
> Les silhouettes des membres de l'équipage accompagnées d'une citation motivationnelle : « Je n'ai pas besoin d'un plan… juste d'une direction. » Le cœur de l'identité Hokuno.

**Description EN :**
> Crew member silhouettes paired with a motivational quote: "I don't need a plan… just a direction." The heart of the Hokuno identity.

**Texte court (card homepage) :**
> Toujours aller de l'avant. Le chemin est la raison.

**Produits :**

| Type | Quantité | Détail |
|------|----------|--------|
| T-shirts light FR | 10 | Gildan BP6, palette étendue (40-56 variantes) |
| T-shirts dark FR | 10 | Gildan BP6, Black/Navy (8 variantes) |
| Mugs light FR | 10 | BP478 blanc, 11oz + 15oz |
| Mugs dark FR | 10 | BP479 noir, 11oz + 15oz |
| T-shirts light EN | 10 | Idem FR, texte EN intégré dans l'image |
| T-shirts dark EN | 10 | Idem FR dark |
| Mugs light EN | 10 | BP478 blanc |
| Mugs dark EN | 10 | BP479 noir |
| **Total** | **80** | |

**Personnages :** 10 (équipage complet) — liste dans `collections/direction.json`

**Ton :** Motivationnel, inspirant, force tranquille.

**Note :** Le texte de la citation est intégré dans l'image IA. Les versions FR et EN sont des images différentes — pas une traduction Shopify. Le design a un print front ET back.

---

### 1.3 MYTHOLOGIE

| Clé | Valeur |
|-----|--------|
| Handle Shopify | `mythologie` |
| URL | `/collections/mythologie` |
| Image de couverture | `card-mythologie.png` |
| Type de collection | Automatique |
| Condition | Titre du produit contient `mythologie` (case-insensitive) |
| Nombre de produits | 40 |

**Description FR :**
> Les ombres de l'équipage réinventées en divinités grecques. Chaque personnage est une silhouette monochrome drapée dans une toge, avec une auréole divine. Une couleur unique par personnage — sa couleur signature.

**Description EN :**
> The shadows of the crew reimagined as Greek deities. Each character is a monochrome silhouette draped in a toga, with a divine halo. One unique color per character — their signature color.

**Texte court (card homepage) :**
> Dieux. Héros. Légendes. Le mythe continue.

**Produits :**

| Type | Quantité | Détail |
|------|----------|--------|
| T-shirts light | 10 | Gildan BP6, palette étendue (56 variantes) |
| T-shirts dark | 10 | Gildan BP6, Black (8 tailles) |
| Mugs | 10 | BP478 blanc, 11oz + 15oz |
| Coques iPhone | 10 | BP268 Slim Cases, SPOKE PP1, iPhone 11 → iPhone 17 (26 variantes) |
| **Total** | **40** | |

**Personnages :** 10 (équipage complet) — liste dans `collections/mythologie.json`

**Ton :** Épique, mystique, iconique.

**Couleurs signature :**

| Personnage | Couleur | Hex |
|------------|---------|-----|
| Luffy | Rouge | `#DC2626` |
| Zoro | Vert | `#16A34A` |
| Nami | Orange | `#EA580C` |
| Sanji | Bleu | `#2563EB` |
| Ussop | Jaune/Doré | `#CA8A04` |
| Chopper | Rose | `#DB2777` |
| Robin | Violet | `#7C3AED` |
| Franky | Cyan | `#0891B2` |
| Brook | Noir/Gris | `#6B7280` |
| Jinbe | Bleu marine | `#1E3A5F` |

**Note :** Pas de texte sur les designs = collection universelle, pas de version FR/EN séparée. Les coques sont UNIQUEMENT dans cette collection.

---

### 1.4 DESIGN HOKUNO

| Clé | Valeur |
|-----|--------|
| Handle Shopify | `design-hokuno` |
| URL | `/collections/design-hokuno` |
| Image de couverture | `card-design-hokuno.png` |
| Type de collection | Automatique |
| Condition | Tag du produit = `design-hokuno` |
| Nombre de produits | 33 |

**Pourquoi un tag et pas le titre :**
Les 3 autres collections utilisent une condition sur le titre (le mot-clé "wanted", "direction", "mythologie" est présent dans chaque titre de produit de façon cohérente). Design Hokuno a des titres irréguliers : "Casquette Hokuno Light" ne contient pas "Design", "T-Shirt hokuno Design Target" a un ordre inversé, etc. Un tag `design-hokuno` sur les 33 produits est plus fiable. Claude Code doit ajouter ce tag via l'API Shopify Admin après la publication des produits sur My Store 5.

**Description FR :**
> L'identité Hokuno à l'état pur. Le logo Logpose, le katakana ホクノ, les motifs signature de la marque — empreinte, orbite, target, boussole. Des produits qui existent au-delà des collections manga.

**Description EN :**
> Pure Hokuno identity. The Logpose logo, the ホクノ katakana, the brand's signature patterns — footprint, orbit, target, compass. Products that exist beyond the manga collections.

**Texte court (card homepage) :**
> L'identité. Le symbole. Le design comme signature.

**Produits :**

| Type | Quantité | Détail |
|------|----------|--------|
| T-shirts Design (BP6) | 11 | HO KU NO (L+D), Hokuno (L+D), Orbite (L+D), Target (D+D+L), Empreinte (L+D) |
| T-shirts Sport (BP145) | 2 | Sport Design Hokuno Light + Dark |
| Bob / Bucket Hat (BP1698) | 1 | Bob Hokuno Design Dark |
| Casquettes (BP1108) | 3 | Casquette Design Hokuno Dark, Casquette Hokuno Dark, Casquette Hokuno Light |
| Claquettes (BP862) | 2 | Claquette Design Hokuno Dark + Light |
| Coques Design (BP268) | 3 | Empreinte Dark, Orbite Dark, Target Dark |
| Maillot de bain (BP978) | 1 | Maillot De Bain Design Hokuno Dark |
| Polos (BP1970) | 3 | Polo Design Hokuno Boussole Light, Polo Design boussole Dark, Polo Signature Dark |
| Shorts de bain (BP978/589) | 7 | Bleu, Bleu Ciel, Jaune, Rose, Rouge, Vert + Pattern Light (BP589) |
| **Total** | **33** (13 t-shirts + 20 accessoires) | |

**Ton :** Décontracté, identité de marque, été.

---

## 2. CONDITIONS AUTOMATIQUES — RÉSUMÉ

| Collection | Type | Condition | Fiabilité |
|------------|------|-----------|-----------|
| Wanted | Automatique | `product title contains "wanted"` | ✅ 277/277 matchent (après renommage coque) |
| Direction | Automatique | `product title contains "direction"` | ✅ 80/80 matchent |
| Mythologie | Automatique | `product title contains "mythologie"` | ✅ 40/40 matchent |
| Design Hokuno | Automatique | `product tag = "design-hokuno"` | ✅ après ajout du tag sur les 33 produits |

**Vérification d'absence de chevauchement :** aucun produit ne contient deux mots-clés de collection dans son titre (un produit Wanted ne contient jamais "direction" ou "mythologie" dans son titre, et inversement). Pas de risque qu'un produit apparaisse dans deux collections.

**Action requise pour Design Hokuno :** après la publication des 430 produits sur My Store 5, exécuter un script qui ajoute le tag `design-hokuno` aux 33 produits concernés via `PUT /admin/api/2024-01/products/{id}.json`. La liste des 33 IDs est dans `INVENTAIRE.md` section "Collection Design Hokuno".

---

## 3. TYPES DE PRODUITS PAR COLLECTION

Pour le filtrage par type sur les pages collection :

| Collection | Types disponibles |
|------------|-------------------|
| Wanted | T-shirt, Mug, Coque (1 seule — The End Brique) |
| Direction | T-shirt, Mug |
| Mythologie | T-shirt, Mug, Coque iPhone |
| Design Hokuno | T-shirt, Casquette, Bob, Claquette, Short de bain, Polo, Maillot de bain, Coque |

Le type du produit est déterminé par le `product_type` Shopify, qui est synchronisé depuis Printify. Si les product_type ne sont pas correctement renseignés, Claude Code doit les mettre à jour via l'API Admin.

---

## 4. PAGE /collections — GRILLE DES 4 COLLECTIONS

### URL et template

- URL : `/collections`
- Template : `list-collections.liquid`
- La page affiche les **4 collections en grille**, PAS les produits individuels

### Contenu

```liquid
<!-- list-collections.liquid -->
<div class="page-wrap">
  {% render 'breadcrumbs' %}

  <p class="cols-label">COLLECTIONS</p>
  <h1 class="cols-title">EXPLOREZ NOS UNIVERS</h1>
  <p class="cols-sub">Des collections pensées comme des récits. Inspirées par la culture, le symbole et le mouvement.</p>
  <img class="cols-icon" src="{{ 'boussole-gold.png' | asset_url }}" alt="" loading="lazy">

  <div class="cols-grid">
    {% for collection in collections %}
      {% unless collection.handle == 'all' or collection.handle == 'frontpage' %}
        {% render 'collection-card', collection: collection %}
      {% endunless %}
    {% endfor %}
  </div>
</div>
```

### Ordre d'affichage

Les 4 collections doivent toujours s'afficher dans cet ordre :
1. Wanted
2. Direction
3. Mythologie
4. Design Hokuno

Si Shopify ne les retourne pas dans cet ordre, forcer l'ordre en hardcodant les handles :

```liquid
{% assign ordered_handles = "wanted,direction,mythologie,design-hokuno" | split: "," %}
<div class="cols-grid">
  {% for handle in ordered_handles %}
    {% assign col = collections[handle] %}
    {% if col %}
      {% render 'collection-card', collection: col %}
    {% endif %}
  {% endfor %}
</div>
```

### Snippet collection-card

```liquid
<!-- snippets/collection-card.liquid -->
<a href="{{ collection.url }}" class="col-card">
  <img src="{{ collection.handle | prepend: 'card-' | append: '.png' | asset_url }}" 
       alt="{{ collection.title }}" loading="lazy">
  <div class="col-card-info">
    <h3>{{ collection.title | upcase }}</h3>
    <p>{{ collection.description | truncate: 80 }}</p>
    <span class="col-btn">{{ 'collections.discover' | t }} ↗</span>
  </div>
</a>
```

**Note sur les images de couverture :** on utilise les images statiques du thème (`card-wanted.png`, etc.) plutôt que `collection.image` car les images Shopify collections sont moins maîtrisables. Le handle de la collection sert à construire le nom du fichier : `card-{handle}.png`.

### Style de la grille (rappel, défini dans `hokuno.css`)

- Grid : `grid-template-columns: repeat(4, 1fr)`, gap `18px`
- Mobile : `grid-template-columns: 1fr 1fr`, gap `12px`
- Card : border-radius `14px`, fond `#111`, bordure `rgba(255,255,255,0.05)`
- Image card : height `420px` desktop, `260px` mobile, `object-fit: cover`
- Info card : padding `28px`, fond `rgba(0,0,0,0.75)` avec blur
- Hover : `scale(1.015)`, ombre dorée `rgba(212,168,83,0.08)`
- Bouton : bordure dorée, texte doré, hover fond doré texte noir

---

## 5. PAGE COLLECTION UNIQUE — /collections/{handle}

### URL et template

- URL : `/collections/wanted`, `/collections/direction`, etc.
- Template : `collection.liquid`

### Structure de la page

```
[BREADCRUMBS]
[TITRE H1 + DESCRIPTION]
[BARRE FILTRES + TRI]
[GRILLE PRODUITS]
[PAGINATION]
```

### En-tête

```liquid
<!-- collection.liquid -->
<div class="page-wrap">
  {% render 'breadcrumbs' %}

  <h1 class="page-title">{{ collection.title }}</h1>
  {% if collection.description != blank %}
    <p class="collection-desc">{{ collection.description }}</p>
  {% endif %}
```

Style description : `color: rgba(255,255,255,0.5); max-width: 600px; line-height: 1.6; margin-bottom: 40px; font-size: 15px`

### Nombre de produits

Afficher le nombre total sous la description :

```liquid
<p class="collection-count">{{ collection.products_count }} {{ 'collections.products' | t }}</p>
```

Style : `font-size: 13px; color: rgba(255,255,255,0.35); letter-spacing: 1px; margin-bottom: 32px`

---

## 6. FILTRES

### Barre de filtres

Position : entre la description et la grille de produits. Sur une seule ligne desktop, en accordéon/drawer sur mobile.

### Filtres disponibles

| Filtre | Type | Valeurs | Applicable à |
|--------|------|---------|-------------|
| Type de produit | Multi-select | T-shirt, Mug, Coque, Accessoires | Toutes collections |
| Couleur | Multi-select | Noir, Blanc, Bleu, Rouge, etc. | T-shirts uniquement |
| Prix | Plage | Min — Max (curseur ou inputs) | Tous |
| Langue | Toggle | FR / EN | Wanted, Direction uniquement |

### Implémentation

Utiliser le système de filtrage natif Shopify (Storefront Filtering API) :

```liquid
{% for filter in collection.filters %}
  <div class="filter-group">
    <h4 class="filter-title">{{ filter.label }}</h4>
    <div class="filter-options">
      {% for value in filter.values %}
        <label class="filter-option {% if value.active %}active{% endif %}">
          <input type="checkbox" 
                 name="{{ value.param_name }}" 
                 value="{{ value.value }}"
                 {% if value.active %}checked{% endif %}
                 onchange="this.form.submit()">
          <span>{{ value.label }} ({{ value.count }})</span>
        </label>
      {% endfor %}
    </div>
  </div>
{% endfor %}
```

Le tout enveloppé dans un `<form>` avec l'action `{{ collection.url }}`.

### Filtre langue (FR/EN) — spécifique Wanted et Direction

Ces deux collections contiennent des produits en français ET en anglais. Le filtre langue permet d'afficher seulement les produits d'une langue.

**Implémentation :** via tags Shopify. Ajouter le tag `lang-fr` ou `lang-en` sur chaque produit Wanted et Direction lors de la migration. Le filtre utilise alors le tag natif Shopify.

Si les tags ne sont pas disponibles, le filtre peut s'appuyer sur le titre : les produits EN contiennent " EN " ou " EN/" dans leur titre.

### Style filtres

- Titre filtre : font-size `12px`, font-weight `600`, letter-spacing `1.5px`, uppercase, couleur `rgba(255,255,255,0.5)`
- Options : font-size `13px`, couleur `rgba(255,255,255,0.6)`, padding `8px 12px`
- Option active : couleur `#D4A853`, bordure `1px solid #D4A853`, border-radius `4px`
- Compteur `(N)` : couleur `rgba(255,255,255,0.3)`

### Filtres mobile (<768px)

- Bouton "FILTRES" visible en haut de la grille
- Au clic : drawer qui slide depuis le bas (ou accordéon qui se déploie)
- Fond drawer : `#000000`, bordure top `1px solid rgba(255,255,255,0.08)`
- Bouton "APPLIQUER" en bas du drawer : style `.btn-gold`
- Bouton "RÉINITIALISER" : texte simple, couleur `rgba(255,255,255,0.5)`

---

## 7. TRI

### Options de tri

| Texte affiché | Valeur Shopify `sort_by` |
|---------------|--------------------------|
| Pertinence | `manual` (ordre par défaut) |
| Prix croissant | `price-ascending` |
| Prix décroissant | `price-descending` |
| Plus récent | `created-descending` |
| Nom A-Z | `title-ascending` |

### Implémentation

```liquid
<select class="sort-select" onchange="window.location.href = '{{ collection.url }}?sort_by=' + this.value">
  <option value="manual" {% if collection.sort_by == 'manual' %}selected{% endif %}>
    {{ 'collections.sort.relevance' | t }}
  </option>
  <option value="price-ascending" {% if collection.sort_by == 'price-ascending' %}selected{% endif %}>
    {{ 'collections.sort.price_asc' | t }}
  </option>
  <option value="price-descending" {% if collection.sort_by == 'price-descending' %}selected{% endif %}>
    {{ 'collections.sort.price_desc' | t }}
  </option>
  <option value="created-descending" {% if collection.sort_by == 'created-descending' %}selected{% endif %}>
    {{ 'collections.sort.newest' | t }}
  </option>
  <option value="title-ascending" {% if collection.sort_by == 'title-ascending' %}selected{% endif %}>
    {{ 'collections.sort.name_az' | t }}
  </option>
</select>
```

### Style du select

- Fond : `rgba(255,255,255,0.04)`
- Bordure : `1px solid rgba(255,255,255,0.1)`
- Border-radius : `6px`
- Padding : `10px 16px`
- Couleur texte : `rgba(255,255,255,0.7)`
- Font-size : `13px`
- Apparence custom (flèche SVG, pas le select natif)

### Position

Desktop : aligné à droite, sur la même ligne que les filtres.
Mobile : pleine largeur, sous le bouton filtres.

---

## 8. GRILLE DE PRODUITS

### Layout

- Desktop : `grid-template-columns: repeat(4, 1fr)`, gap `18px`
- Tablette (768-1024px) : `repeat(3, 1fr)`
- Mobile (<768px) : `repeat(2, 1fr)`, gap `12px`

### Card produit

Chaque produit utilise le snippet `{% render 'product-card', product: product %}`.

```liquid
<!-- snippets/product-card.liquid -->
<a href="{{ product.url }}" class="prod-card">
  <div class="prod-card-img">
    <img src="{{ product.featured_image | image_url: width: 600 }}" 
         alt="{{ product.title }}" 
         loading="lazy">
  </div>
  <div class="prod-info">
    <h4>{{ product.title | truncate: 40 }}</h4>
    <p class="prod-price">{{ product.price | money }}</p>
  </div>
</a>
```

### Style card (rappel, défini dans `hokuno.css`)

- Fond : `rgba(255,255,255,0.02)`
- Bordure : `1px solid rgba(255,255,255,0.06)`
- Border-radius : `12px` (la `div.prod-card-img` a `overflow: hidden` et arrondi en haut)
- Image : height `320px` desktop, `220px` mobile, `object-fit: cover`
- Hover : bordure `rgba(212,168,83,0.35)`, `translateY(-4px)`, ombre `0 12px 40px rgba(0,0,0,0.3)`, image `scale(1.04)`
- Titre : font-size `13px`, font-weight `600`, couleur `rgba(255,255,255,0.85)`
- Prix : font-size `17px`, font-weight `700`, couleur `#D4A853`
- Padding info : `18px 20px`

---

## 9. PAGINATION

### Paramètres

- **24 produits par page** (la collection Wanted en a 277, donc 12 pages)
- Afficher la pagination uniquement si plus d'une page

### Implémentation

```liquid
{% paginate collection.products by 24 %}
  <!-- grille de produits -->
  <div class="products-grid">
    {% for product in collection.products %}
      {% render 'product-card', product: product %}
    {% endfor %}
  </div>

  <!-- pagination -->
  {% if paginate.pages > 1 %}
    {% render 'pagination', paginate: paginate %}
  {% endif %}
{% endpaginate %}
```

### Snippet pagination

```liquid
<!-- snippets/pagination.liquid -->
<nav class="pagination" aria-label="Pagination">
  {% if paginate.previous %}
    <a href="{{ paginate.previous.url }}" class="page-btn">‹ {{ 'pagination.previous' | t }}</a>
  {% endif %}

  {% for part in paginate.parts %}
    {% if part.is_link %}
      <a href="{{ part.url }}" class="page-num">{{ part.title }}</a>
    {% elsif part.title == paginate.current_page %}
      <span class="page-num active">{{ part.title }}</span>
    {% else %}
      <span class="page-num ellipsis">{{ part.title }}</span>
    {% endif %}
  {% endfor %}

  {% if paginate.next %}
    <a href="{{ paginate.next.url }}" class="page-btn">{{ 'pagination.next' | t }} ›</a>
  {% endif %}
</nav>
```

### Style pagination

- Position : centré, margin-top `48px`, margin-bottom `24px`
- Display : `flex`, gap `8px`, `align-items: center`, `justify-content: center`
- Boutons page : `40×40px`, border-radius `6px`, fond `rgba(255,255,255,0.04)`, bordure `1px solid rgba(255,255,255,0.08)`, couleur `rgba(255,255,255,0.6)`, font-size `14px`, font-weight `500`
- Page active : fond `#D4A853`, couleur `#000000`, font-weight `700`
- Hover : bordure `rgba(212,168,83,0.5)`
- Précédent/Suivant : même style, padding `10px 16px` au lieu de 40×40

---

## 10. SECTION COLLECTIONS SUR LA PAGE D'ACCUEIL

La page d'accueil (index.liquid) a aussi une section qui affiche les 4 collections. Elle réutilise le même snippet `collection-card` mais avec une mise en page différente (titre de section, icône boussole).

```liquid
<!-- Dans index.liquid -->
<section class="cols">
  <p class="cols-label">COLLECTIONS</p>
  <h2 class="cols-title">{{ 'home.collections.title' | t }}</h2>
  <p class="cols-sub">{{ 'home.collections.subtitle' | t }}</p>
  <img class="cols-icon" src="{{ 'boussole-gold.png' | asset_url }}" alt="" loading="lazy">
  <div class="cols-grid">
    {% assign ordered_handles = "wanted,direction,mythologie,design-hokuno" | split: "," %}
    {% for handle in ordered_handles %}
      {% assign col = collections[handle] %}
      {% if col %}
        {% render 'collection-card', collection: col %}
      {% endif %}
    {% endfor %}
  </div>
</section>
```

Différence avec la page /collections : la page d'accueil n'a PAS de breadcrumbs ni de `.page-wrap`, et a un titre de section (h2) au-dessus de la grille.

---

## 11. PRIX PAR TYPE DE PRODUIT (RAPPEL)

Pour référence dans les pages collection et produit — source : `PRICING.md`

| Produit | Prix FR (€) | Prix EN ($) |
|---------|:-----------:|:-----------:|
| T-shirt (toutes collections) | 34.99 | 37.99 |
| Mug blanc 11oz | 29.99 | 19.99 |
| Mug blanc 15oz | 34.99 | 24.99 |
| Mug noir 11oz | 34.99 | 24.99 |
| Coque iPhone (Mythologie) | 24.99 | 24.99 |
| Casquette | 29.99 | 29.99 |
| Bob / Bucket Hat | 39.99 | 39.99 |
| Polo | 44.99 | 44.99 |
| Short de bain | 49.99 | 49.99 |
| Claquette | 54.99 | 54.99 |

---

## 12. ACTIONS REQUISES LORS DE LA MIGRATION

Lors de la configuration de My Store 5, Claude Code doit :

1. **Créer les 4 collections automatiques** avec les conditions définies en section 2
2. **Renommer la coque** "Coque de téléphone The End sur Brique Saga 1" → "Coque Wanted The End Brique Saga 1" sur Printify (action manuelle propriétaire) pour qu'elle matche la condition auto Wanted
3. **Ajouter le tag `design-hokuno`** sur les 33 produits Design Hokuno via API Admin
4. **Ajouter les tags `lang-fr` et `lang-en`** sur les produits Wanted et Direction pour le filtre langue
5. **Vérifier l'assignation** : chaque produit doit appartenir à exactement 1 collection (pas de chevauchement, pas d'orphelin)
6. **Configurer l'image de couverture** de chaque collection dans Shopify Admin (upload des 4 card PNGs)
7. **Rédiger les descriptions** de chaque collection dans Shopify Admin (textes FR ci-dessus, textes EN via Shopify Markets)
8. **Vérifier le product_type** de chaque produit pour que les filtres par type fonctionnent

### Vérification post-migration

| Check | Attendu |
|-------|---------|
| `/collections/wanted` | 277 produits |
| `/collections/direction` | 80 produits |
| `/collections/mythologie` | 40 produits |
| `/collections/design-hokuno` | 33 produits |
| Total 4 collections | 430 (= total Printify) |
| Produits sans collection | 0 |
| Produits dans 2+ collections | 0 |
