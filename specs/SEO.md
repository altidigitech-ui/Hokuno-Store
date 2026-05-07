# specs/SEO.md — SEO & GEO (Generative Engine Optimization)

> Contrat pour Claude Code. Chaque meta tag, chaque schema, chaque fichier technique est défini ici.
> Le SEO est codé en dur dans le thème Liquid — pas d'app tierce.
> Le snippet `snippets/seo-jsonld.liquid` est rendu dans `theme.liquid` via `{% render 'seo-jsonld' %}`.

---

## 1. META TITLE

### Format

```
[Titre de la page] — HOKUNO ホクノ
```

### Implémentation dans theme.liquid

```liquid
<title>{% if page_title %}{{ page_title }} — {% endif %}HOKUNO ホクノ</title>
```

Shopify renseigne `page_title` automatiquement selon le template (nom du produit, nom de la collection, titre de la page, etc.).

### Titles par type de page

| Page | Meta title | Exemple |
|------|-----------|---------|
| Accueil | `HOKUNO ホクノ — Streetwear Manga Japonais` | fixe |
| Collection | `{{ collection.title }} — HOKUNO ホクノ` | `WANTED — HOKUNO ホクノ` |
| Produit | `{{ product.title }} — HOKUNO ホクノ` | `T-SHIRT LUFI WANTED 1/46 — HOKUNO ホクノ` |
| Page statique | `{{ page.title }} — HOKUNO ホクノ` | `À propos — HOKUNO ホクノ` |
| Blog | `{{ blog.title }} — HOKUNO ホクノ` | `Journal — HOKUNO ホクノ` |
| Article | `{{ article.title }} — HOKUNO ホクノ` | `L'histoire de la collection Wanted — HOKUNO ホクノ` |
| Recherche | `Recherche — HOKUNO ホクノ` | fixe |
| Panier | `Panier — HOKUNO ホクノ` | fixe |
| 404 | `Page non trouvée — HOKUNO ホクノ` | fixe |

### Accueil — title spécial

L'accueil ne doit pas afficher juste "HOKUNO ホクノ". Surcharger :

```liquid
<title>
  {%- if template == 'index' -%}
    HOKUNO ホクノ — Streetwear Manga Japonais
  {%- elsif page_title -%}
    {{ page_title }} — HOKUNO ホクノ
  {%- else -%}
    HOKUNO ホクノ
  {%- endif -%}
</title>
```

---

## 2. META DESCRIPTION

### Format

Max **155 caractères**. Inclut le mot-clé principal + proposition de valeur.

### Implémentation

```liquid
<meta name="description" content="
  {%- if template == 'index' -%}
    Hokuno (ホクノ) — Marque streetwear manga française. T-shirts, mugs et accessoires avec des designs originaux inspirés de l'univers manga. Livraison internationale.
  {%- elsif page_description != blank -%}
    {{ page_description | strip_html | truncate: 155 }}
  {%- else -%}
    HOKUNO — ホクノ — Streetwear manga japonais. Toujours aller de l'avant.
  {%- endif -%}
">
```

### Descriptions par type de page

| Page | Meta description |
|------|-----------------|
| Accueil | `Hokuno (ホクノ) — Marque streetwear manga française. T-shirts, mugs et accessoires avec des designs originaux inspirés de l'univers manga. Livraison internationale.` |
| Collection Wanted | `Collection Wanted — Avis de recherche revisités. Des personnages vieillis par 30 ans de manga. T-shirts et mugs en édition limitée. Livraison gratuite dès 60€.` |
| Collection Direction | `Collection Direction — Silhouettes encrées avec la citation « Je n'ai pas besoin d'un plan… juste d'une direction. » T-shirts streetwear manga.` |
| Collection Mythologie | `Collection Mythologie — L'équipage réinventé en divinités grecques. Silhouettes monochromes, chacune dans sa couleur signature. T-shirts, mugs, coques.` |
| Collection Design Hokuno | `Design Hokuno — Le branding Hokuno à l'état pur. T-shirts, casquettes, bobs, polos et accessoires aux couleurs de la marque.` |
| Produit | `{{ product.description | strip_html | truncate: 155 }}` (backstory du personnage) |
| À propos | `Hokuno (北の) — Vers le Nord. Marque streetwear manga française née en 2026. Designs IA, print on demand, livraison internationale.` |
| FAQ | `Questions fréquentes sur Hokuno — Livraison, retours, tailles, fabrication print on demand. Réponses à toutes vos questions.` |
| Contact | `Contactez Hokuno — Une question, une suggestion, une collaboration ? Nous répondons sous 24-48h.` |
| Blog | `Journal Hokuno — Backstories, inspirations et coulisses de la marque streetwear manga.` |

Les descriptions des collections sont à configurer dans Shopify Admin → Collections → [collection] → Description (Shopify les utilise comme `page_description`).

---

## 3. SCHEMA JSON-LD

Tout le JSON-LD est généré dans le snippet `snippets/seo-jsonld.liquid`, appelé dans le `<head>` de theme.liquid.

### 3.1 Organization (toutes les pages)

```liquid
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "HOKUNO",
  "alternateName": "ホクノ",
  "url": "{{ shop.url }}",
  "logo": "{{ 'logo-hokuno-nav.png' | asset_url | prepend: 'https:' }}",
  "description": "Hokuno (北の) est une marque streetwear manga française. Designs originaux inspirés de l'univers manga, imprimés en print on demand.",
  "email": "altidigitech@gmail.com",
  "sameAs": [
    "https://www.tiktok.com/@hokuno",
    "https://www.instagram.com/hokuno"
  ]
}
</script>
```

### 3.2 Product (pages produit uniquement)

```liquid
{% if template == 'product' %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": {{ product.title | json }},
  "image": [
    {% for image in product.images limit: 3 %}
      "{{ image | image_url: width: 1200 }}"{% unless forloop.last %},{% endunless %}
    {% endfor %}
  ],
  "description": {{ product.description | strip_html | truncate: 500 | json }},
  "brand": {
    "@type": "Brand",
    "name": "HOKUNO"
  },
  "offers": {
    "@type": "Offer",
    "url": "{{ shop.url }}{{ product.url }}",
    "priceCurrency": "{{ cart.currency.iso_code }}",
    "price": "{{ product.price | money_without_currency | strip_html }}",
    "availability": "{% if product.available %}https://schema.org/InStock{% else %}https://schema.org/OutOfStock{% endif %}",
    "seller": {
      "@type": "Organization",
      "name": "HOKUNO"
    }
  },
  "sku": {{ product.selected_or_first_available_variant.sku | json }},
  "mpn": {{ product.selected_or_first_available_variant.barcode | default: product.id | json }}
}
</script>
{% endif %}
```

### 3.3 CollectionPage (pages collection)

```liquid
{% if template == 'collection' %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": {{ collection.title | json }},
  "description": {{ collection.description | strip_html | truncate: 300 | json }},
  "url": "{{ shop.url }}{{ collection.url }}",
  "numberOfItems": {{ collection.products_count }},
  "mainEntity": {
    "@type": "ItemList",
    "numberOfItems": {{ collection.products_count }},
    "itemListElement": [
      {% for product in collection.products limit: 10 %}
      {
        "@type": "ListItem",
        "position": {{ forloop.index }},
        "url": "{{ shop.url }}{{ product.url }}",
        "name": {{ product.title | json }}
      }{% unless forloop.last %},{% endunless %}
      {% endfor %}
    ]
  }
}
</script>
{% endif %}
```

### 3.4 BreadcrumbList (pages avec breadcrumbs)

```liquid
{% unless template == 'index' or template == 'cart' or template == 'search' or template == '404' or template == 'password' or template == 'list-collections' %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "{{ 'breadcrumbs.home' | t }}",
      "item": "{{ shop.url }}"
    }
    {% if template == 'collection' %}
    ,{
      "@type": "ListItem",
      "position": 2,
      "name": {{ collection.title | json }},
      "item": "{{ shop.url }}{{ collection.url }}"
    }
    {% elsif template == 'product' %}
      {% if product.collections.size > 0 %}
      ,{
        "@type": "ListItem",
        "position": 2,
        "name": {{ product.collections.first.title | json }},
        "item": "{{ shop.url }}{{ product.collections.first.url }}"
      }
      ,{
        "@type": "ListItem",
        "position": 3,
        "name": {{ product.title | json }},
        "item": "{{ shop.url }}{{ product.url }}"
      }
      {% else %}
      ,{
        "@type": "ListItem",
        "position": 2,
        "name": {{ product.title | json }},
        "item": "{{ shop.url }}{{ product.url }}"
      }
      {% endif %}
    {% elsif template == 'page' %}
    ,{
      "@type": "ListItem",
      "position": 2,
      "name": {{ page.title | json }},
      "item": "{{ shop.url }}{{ page.url }}"
    }
    {% elsif template == 'article' %}
    ,{
      "@type": "ListItem",
      "position": 2,
      "name": {{ blog.title | json }},
      "item": "{{ shop.url }}{{ blog.url }}"
    }
    ,{
      "@type": "ListItem",
      "position": 3,
      "name": {{ article.title | json }},
      "item": "{{ shop.url }}{{ article.url }}"
    }
    {% endif %}
  ]
}
</script>
{% endunless %}
```

### 3.5 Article (pages article blog)

```liquid
{% if template == 'article' %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": {{ article.title | json }},
  "description": {{ article.excerpt_or_content | strip_html | truncate: 200 | json }},
  "image": "{% if article.image %}{{ article.image | image_url: width: 1200 }}{% endif %}",
  "author": {
    "@type": "Organization",
    "name": "HOKUNO"
  },
  "publisher": {
    "@type": "Organization",
    "name": "HOKUNO",
    "logo": {
      "@type": "ImageObject",
      "url": "{{ 'logo-hokuno-nav.png' | asset_url | prepend: 'https:' }}"
    }
  },
  "datePublished": "{{ article.published_at | date: '%Y-%m-%dT%H:%M:%S%z' }}",
  "dateModified": "{{ article.updated_at | date: '%Y-%m-%dT%H:%M:%S%z' }}"
}
</script>
{% endif %}
```

### 3.6 FAQPage (page FAQ)

```liquid
{% if template == 'page' and page.handle == 'faq' %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "Comment sont fabriqués vos produits ?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Chaque produit est fabriqué à la commande (print on demand) par nos partenaires d'impression. Aucun stock — votre article est imprimé spécialement pour vous."
      }
    },
    {
      "@type": "Question",
      "name": "Quels sont les délais de livraison ?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Fabrication : 3-7 jours ouvrés. Livraison France/EU : 5-10 jours. International : 7-15 jours. Numéro de suivi envoyé par email."
      }
    },
    {
      "@type": "Question",
      "name": "La livraison est-elle gratuite ?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Oui, à partir de 60€ de commande. En dessous, frais calculés au checkout selon la destination."
      }
    },
    {
      "@type": "Question",
      "name": "Puis-je retourner un produit ?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Oui, 30 jours après réception. Produit non porté, non lavé, avec étiquette. Contactez altidigitech@gmail.com."
      }
    },
    {
      "@type": "Question",
      "name": "Quelles tailles sont disponibles ?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Nos t-shirts sont disponibles du S au XL. Guide des tailles disponible sur chaque page produit."
      }
    }
  ]
}
</script>
{% endif %}
```

---

## 4. OPEN GRAPH

Dans le `<head>` de theme.liquid :

```liquid
<!-- Open Graph -->
<meta property="og:site_name" content="HOKUNO ホクノ">
<meta property="og:url" content="{{ canonical_url }}">

{% if template == 'product' %}
  <meta property="og:type" content="product">
  <meta property="og:title" content="{{ product.title }} — HOKUNO ホクノ">
  <meta property="og:description" content="{{ product.description | strip_html | truncate: 200 }}">
  <meta property="og:image" content="{{ product.featured_image | image_url: width: 1200 }}">
  <meta property="product:price:amount" content="{{ product.price | money_without_currency }}">
  <meta property="product:price:currency" content="{{ cart.currency.iso_code }}">
{% elsif template == 'article' %}
  <meta property="og:type" content="article">
  <meta property="og:title" content="{{ article.title }} — HOKUNO ホクノ">
  <meta property="og:description" content="{{ article.excerpt_or_content | strip_html | truncate: 200 }}">
  {% if article.image %}
    <meta property="og:image" content="{{ article.image | image_url: width: 1200 }}">
  {% endif %}
{% elsif template == 'collection' %}
  <meta property="og:type" content="website">
  <meta property="og:title" content="{{ collection.title }} — HOKUNO ホクノ">
  <meta property="og:description" content="{{ collection.description | strip_html | truncate: 200 }}">
  <meta property="og:image" content="{{ collection.handle | prepend: 'card-' | append: '.png' | asset_url }}">
{% else %}
  <meta property="og:type" content="website">
  <meta property="og:title" content="{{ page_title | default: 'HOKUNO ホクノ' }}">
  <meta property="og:description" content="{{ page_description | default: 'HOKUNO — ホクノ — Streetwear manga japonais.' | strip_html | truncate: 200 }}">
  <meta property="og:image" content="{{ 'hero-tshirt.png' | asset_url }}">
{% endif %}
```

---

## 5. TWITTER CARD

```liquid
<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{ page_title | default: 'HOKUNO ホクノ' }}">
<meta name="twitter:description" content="{{ page_description | default: 'Streetwear manga japonais' | strip_html | truncate: 200 }}">
{% if template == 'product' %}
  <meta name="twitter:image" content="{{ product.featured_image | image_url: width: 1200 }}">
{% elsif template == 'article' and article.image %}
  <meta name="twitter:image" content="{{ article.image | image_url: width: 1200 }}">
{% else %}
  <meta name="twitter:image" content="{{ 'hero-tshirt.png' | asset_url }}">
{% endif %}
```

---

## 6. CANONICAL URL

```liquid
<link rel="canonical" href="{{ canonical_url }}">
```

Shopify génère `canonical_url` automatiquement. Cela évite le contenu dupliqué (ex : `/collections/wanted?page=2` vs `/collections/wanted`).

---

## 7. HREFLANG

Si Shopify Markets est activé avec FR et EN :

```liquid
{% if request.locale %}
  {% for locale in shop.published_locales %}
    <link rel="alternate" hreflang="{{ locale.iso_code }}" href="{{ canonical_url | replace: request.locale.root_url, locale.root_url }}">
  {% endfor %}
  <link rel="alternate" hreflang="x-default" href="{{ canonical_url | replace: request.locale.root_url, '/' }}">
{% endif %}
```

---

## 8. H1 — RÈGLE UNIQUE

**Jamais plus d'un H1 par page.** Claude Code doit vérifier chaque template.

| Page | H1 |
|------|-----|
| Accueil | `TOUJOURS ALLER DE L'AVANT` (hero) |
| Collection | `{{ collection.title }}` |
| Produit | `{{ product.title }}` |
| Page statique | `{{ page.title }}` |
| Blog | `{{ blog.title }}` |
| Article | `{{ article.title }}` |
| Panier | `PANIER` |
| Recherche | `RECHERCHE` ou le terme de recherche |
| 404 | `404` |
| Connexion | `CONNEXION` |

Les titres de sections (collections section, produits phares, etc.) utilisent `<h2>`, jamais `<h1>`.

---

## 9. ALT TEXT

**Toutes** les images du site ont un alt text. Aucune exception.

| Image | Alt text |
|-------|----------|
| Logo navbar | `HOKUNO` |
| Hero | `HOKUNO — T-shirt Wanted` |
| Collection-card | `Collection {{ collection.title }}` ou alt statique (`Collection Wanted`, etc.) |
| Product-card | `{{ product.title }}` |
| Image produit | `{{ product.title }} — vue {{ forloop.index }}` |
| Miniatures produit | `{{ product.title }} — vue {{ forloop.index }}` |
| Boussole | vide (`alt=""`) — image décorative |
| Blog article image | `{{ article.title }}` |
| Cart item image | `{{ item.title }}` |
| Icônes (SVG inline) | via `aria-label` sur le bouton parent |

---

## 10. ROBOTS.TXT

Shopify génère automatiquement `/robots.txt`. Par défaut, il bloque certains crawlers IA. Hokuno doit les **autoriser**.

Configurer via Shopify Admin → Settings → Custom `robots.txt` additions, ou via le fichier `robots.txt.liquid` du thème :

```liquid
# robots.txt — HOKUNO

User-agent: *
Disallow: /admin
Disallow: /cart
Disallow: /checkout
Disallow: /orders
Disallow: /account
Allow: /

# Crawlers IA — AUTORISÉS
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Googlebot
Allow: /

Sitemap: {{ shop.url }}/sitemap.xml
```

---

## 11. LLMS.TXT

Fichier à placer à la racine du site. Décrit la boutique pour les LLMs (standard émergent 2026).

Implémentation : créer une page Shopify avec le handle `llms-txt`, puis une route ou un redirect. Ou plus simplement, ajouter le contenu dans un asset et le servir via un proxy/redirect Shopify.

**Alternative pragmatique v1 :** créer une page `/pages/llms` avec le contenu ci-dessous, puis configurer un redirect `/llms.txt` → `/pages/llms` dans Shopify Admin → Settings → Navigation → URL redirects.

```
# Hokuno
> Hokuno (北の) est une marque streetwear manga française. Le nom signifie "Vers le Nord" en japonais — philosophie de toujours aller de l'avant.

## À propos
Hokuno est née en 2026. Chaque design est une parodie artistique originale générée par IA — jamais une reproduction directe. Les produits sont fabriqués à la commande (print on demand) via Printify.

## Collections
- Wanted : Avis de recherche parodiques de personnages de manga vieillis par 30 ans de publication. 46 personnages, t-shirts et mugs. T-shirts à 34.99€.
- Direction : Silhouettes en encre noire avec la citation « Je n'ai pas besoin d'un plan… juste d'une direction. » 10 personnages, t-shirts et mugs.
- Mythologie : Silhouettes divines en toge grecque, chaque personnage dans sa couleur signature. 10 personnages, t-shirts, mugs et coques iPhone.
- Design Hokuno : Produits avec le branding Hokuno pur — logpose, katakana ホクノ, motifs signature. T-shirts, casquettes, bobs, polos, shorts de bain, claquettes.

## Produits
- 430 produits au total
- T-shirts : Gildan 5000, 100% coton, tailles S à XL, 34.99€ (FR) / $37.99 (EN)
- Mugs : Céramique 11oz/15oz, 29.99€ à 34.99€
- Coques iPhone : Slim case, iPhone 11 à iPhone 17, 24.99€
- Accessoires : Casquettes 29.99€, Bobs 39.99€, Polos 44.99€, Shorts 49.99€, Claquettes 54.99€
- Livraison gratuite dès 60€

## Contact
- Email : altidigitech@gmail.com
- Site : {{ shop.url }}

## Liens
- Toutes les collections : {{ shop.url }}/collections
- Collection Wanted : {{ shop.url }}/collections/wanted
- Collection Direction : {{ shop.url }}/collections/direction
- Collection Mythologie : {{ shop.url }}/collections/mythologie
- Collection Design Hokuno : {{ shop.url }}/collections/design-hokuno
- À propos : {{ shop.url }}/pages/about
- FAQ : {{ shop.url }}/pages/faq
- Contact : {{ shop.url }}/pages/contact
```

---

## 12. SITEMAP

Shopify génère automatiquement `/sitemap.xml` avec tous les produits, collections, pages et articles.

**Actions :**
1. Vérifier que le sitemap est accessible : `{{ shop.url }}/sitemap.xml`
2. Soumettre le sitemap dans Google Search Console : `https://search.google.com/search-console` → Sitemaps → Ajouter `{{ shop.url }}/sitemap.xml`
3. Vérifier que les 430 produits apparaissent dans le sitemap

---

## 13. URLS

Shopify génère automatiquement des URLs propres basées sur les handles des produits, collections et pages.

### Règles

- Collections : `/collections/{handle}` — ex : `/collections/wanted`
- Produits : `/products/{handle}` — ex : `/products/t-shirt-lufi-wanted-1-46`
- Pages : `/pages/{handle}` — ex : `/pages/about`
- Blog : `/blogs/{blog_handle}/{article_handle}`
- Pas de paramètres inutiles dans les URLs

### Handle Shopify

Le handle est généré automatiquement depuis le titre. Shopify le slugifie (minuscules, tirets, pas d'accents). On ne le modifie pas manuellement sauf si le résultat est incompréhensible.

---

## 14. PERFORMANCE — CORE WEB VITALS

### Cibles

| Métrique | Cible | Mesure |
|----------|-------|--------|
| LCP (Largest Contentful Paint) | < 2.5s | PageSpeed Insights |
| CLS (Cumulative Layout Shift) | < 0.1 | PageSpeed Insights |
| FID / INP (Interaction to Next Paint) | < 200ms | PageSpeed Insights |

### Optimisations dans le thème

| Technique | Implémentation |
|-----------|---------------|
| Lazy loading images | `loading="lazy"` sur toutes les images sauf hero |
| Font display swap | `&display=swap` sur le lien Google Fonts |
| CSS externe caché | `assets/hokuno.css` — caché par le CDN Shopify après la 1ère visite |
| JS defer | `<script src="{{ 'hokuno.js' | asset_url }}" defer></script>` |
| Images Shopify CDN | `{{ image | image_url: width: 600 }}` — Shopify sert en WebP auto |
| Pas de JS framework | Pas de React/Vue = pas de bundle lourd |
| Dimensions images | Définir `width` et `height` sur les images pour éviter le CLS |

### Shopify CDN images

Shopify convertit et sert automatiquement les images en WebP via son CDN. Utiliser les filtres Liquid pour spécifier la taille :

```liquid
{{ product.featured_image | image_url: width: 600 }}     <!-- product cards -->
{{ product.featured_image | image_url: width: 1200 }}    <!-- page produit -->
{{ image | image_url: width: 200 }}                       <!-- miniatures -->
```

---

## 15. GEO — OPTIMISATION MOTEURS IA

### Principes dans le thème

| Principe | Implémentation |
|----------|---------------|
| Première phrase = définition de l'entité | Description de chaque collection commence par "Hokuno est..." ou "[Collection] — [définition]" |
| Données factuelles denses | Prix, matériaux, tailles, disponibilité visibles dans le HTML initial |
| FAQ structurées | Schema FAQPage sur la page FAQ |
| Pas de JS-only content | Tout le contenu textuel est dans le HTML initial (SSR natif Shopify/Liquid) |
| robots.txt ouvert | GPTBot, ClaudeBot, PerplexityBot autorisés |
| llms.txt | Description complète du site à la racine |

### Stratégie éditoriale (hors thème — recommandations)

- Blog Hokuno : publier toutes les 2 semaines (les citations IA décroissent après ~14 jours sans update)
- Présence Reddit : r/streetwear, r/OnePiece, r/anime (source primaire pour les LLMs)
- YouTube : contenu vidéo sur la marque et les collections
- Chaque article de blog doit inclure des données factuelles vérifiables

---

## 16. STRUCTURE DU SNIPPET `seo-jsonld.liquid`

Le snippet est appelé une seule fois dans `<head>` de theme.liquid :

```liquid
<!-- Dans theme.liquid <head> -->
{% render 'seo-jsonld' %}
```

Le snippet contient tous les schemas conditionnels :

```liquid
<!-- snippets/seo-jsonld.liquid -->

<!-- Organization (toutes les pages) -->
<script type="application/ld+json">
  <!-- Section 3.1 -->
</script>

<!-- Product (pages produit) -->
{% if template == 'product' %}
<script type="application/ld+json">
  <!-- Section 3.2 -->
</script>
{% endif %}

<!-- CollectionPage (pages collection) -->
{% if template == 'collection' %}
<script type="application/ld+json">
  <!-- Section 3.3 -->
</script>
{% endif %}

<!-- BreadcrumbList (pages avec breadcrumbs) -->
{% unless template == 'index' or template == 'cart' or template == 'search' or template == '404' or template == 'password' or template == 'list-collections' %}
<script type="application/ld+json">
  <!-- Section 3.4 -->
</script>
{% endunless %}

<!-- Article (pages article blog) -->
{% if template == 'article' %}
<script type="application/ld+json">
  <!-- Section 3.5 -->
</script>
{% endif %}

<!-- FAQPage (page FAQ) -->
{% if template == 'page' and page.handle == 'faq' %}
<script type="application/ld+json">
  <!-- Section 3.6 -->
</script>
{% endif %}
```

---

## 17. VÉRIFICATION SEO

### Outils

| Outil | URL | Ce qu'il vérifie |
|-------|-----|------------------|
| Google Rich Results Test | `https://search.google.com/test/rich-results` | Schema JSON-LD valide |
| Facebook Sharing Debugger | `https://developers.facebook.com/tools/debug/` | Open Graph tags |
| PageSpeed Insights | `https://pagespeed.web.dev/` | Core Web Vitals |
| Google Search Console | `https://search.google.com/search-console` | Indexation, sitemap, erreurs |

### Checklist SEO (intégrée dans `specs/CHECKLIST.md`)

- [ ] Meta title correct sur chaque type de page (vérifier 1 page par template)
- [ ] Meta description présente et < 155 caractères
- [ ] Schema JSON-LD Product valide (tester avec Rich Results Test)
- [ ] Schema Organization présent sur toutes les pages
- [ ] Schema WebSite avec SearchAction présent sur l'accueil
- [ ] Schema BreadcrumbList présent sur les pages avec breadcrumbs
- [ ] Schema FAQPage sur la page FAQ
- [ ] Open Graph tags présents (tester avec Facebook Debugger)
- [ ] Twitter Card tags présents
- [ ] Canonical URL sur chaque page
- [ ] Meta robots noindex sur /cart, /account, /search
- [ ] robots.txt : GPTBot, ClaudeBot autorisés (vérifier `/robots.txt`)
- [ ] llms.txt accessible (vérifier `/llms.txt` ou `/pages/llms`)
- [ ] Sitemap accessible (`/sitemap.xml`)
- [ ] H1 unique par page (jamais 2)
- [ ] Alt text sur toutes les images (aucun `alt=""` sauf images décoratives)
- [ ] Preconnect/preload dans le `<head>`
- [ ] LCP < 2.5s sur accueil et page collection (PageSpeed Insights)
- [ ] CLS < 0.1

---

## 18. SCHEMA WEBSITE + SEARCHACTION (sitelinks search box)

Ce schema permet à Google d'afficher un mini champ de recherche directement dans les résultats pour les recherches de marque ("Hokuno").

Ajouter dans `seo-jsonld.liquid`, uniquement sur la page d'accueil :

```liquid
{% if template == 'index' %}
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "HOKUNO ホクノ",
  "url": "{{ shop.url }}",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "{{ shop.url }}/search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
</script>
{% endif %}
```

---

## 19. META ROBOTS — NOINDEX SUR PAGES NON-INDEXABLES

Certaines pages ne doivent PAS apparaître dans Google. Ajouter dans le `<head>` de theme.liquid :

```liquid
{% if template == 'cart' or template == 'search' or template contains 'customers' %}
  <meta name="robots" content="noindex, nofollow">
{% endif %}
```

Pages concernées :
- `/cart` — contenu dynamique, aucune valeur SEO
- `/search` et `/search?q=...` — contenu dupliqué des collections
- `/account/*` — données privées
- Pages policies (`/policies/*`) — Shopify ajoute son propre noindex si nécessaire

---

## 20. PRECONNECT ET PRELOAD

Optimisations de chargement dans le `<head>` de theme.liquid, AVANT les liens CSS et fonts :

```liquid
<!-- DNS Prefetch & Preconnect -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://cdn.shopify.com" crossorigin>

<!-- Preload police critique -->
<link rel="preload" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" as="style">

<!-- Preload hero image (LCP) -->
{% if template == 'index' %}
  <link rel="preload" href="{{ 'hero-tshirt.png' | asset_url }}" as="image">
{% endif %}
```

**Pourquoi :**
- `preconnect` : établit la connexion TCP + TLS avec les domaines externes AVANT qu'ils soient nécessaires (économise ~100-300ms)
- `preload` : charge la font et le hero image en priorité (améliore LCP)
- `dns-prefetch` : résout le DNS en avance (fallback pour navigateurs sans preconnect)

---

## 21. LLMS.TXT — FORMAT STRUCTURÉ v0.1

Mettre à jour le contenu llms.txt pour inclure le format structuré v0.1 (en-tête key-value + contenu markdown) :

```
# llms.txt v0.1

version: 0.1
site-purpose: E-commerce streetwear manga français — designs originaux en print on demand
primary-audience: Fans de manga et streetwear, 18-35 ans, francophones et anglophones
authoritative-pages:
  - /collections
  - /collections/wanted
  - /collections/direction
  - /collections/mythologie
  - /collections/design-hokuno
  - /pages/about
  - /pages/faq
update-frequency: biweekly
contact: altidigitech@gmail.com
last-updated: 2026-05-07
language: fr, en

# Hokuno
> Hokuno (北の) est une marque streetwear manga française. Le nom signifie "Vers le Nord" en japonais — philosophie de toujours aller de l'avant.

## À propos
Hokuno est née en 2026. Chaque design est une parodie artistique originale générée par IA — jamais une reproduction directe. Les produits sont fabriqués à la commande (print on demand) via Printify.

## Collections
- Wanted : Avis de recherche parodiques de personnages de manga vieillis par 30 ans de publication. 46 personnages, t-shirts et mugs. T-shirts à 34.99€.
- Direction : Silhouettes en encre noire avec la citation « Je n'ai pas besoin d'un plan… juste d'une direction. » 10 personnages, t-shirts et mugs.
- Mythologie : Silhouettes divines en toge grecque, chaque personnage dans sa couleur signature. 10 personnages, t-shirts, mugs et coques iPhone.
- Design Hokuno : Produits avec le branding Hokuno pur — logpose, katakana ホクノ, motifs signature. T-shirts, casquettes, bobs, polos, shorts de bain, claquettes.

## Produits
- 430 produits au total
- T-shirts : Gildan 5000, 100% coton, tailles S à XL, 34.99€ (FR) / $37.99 (EN)
- Mugs : Céramique 11oz/15oz, 29.99€ à 34.99€
- Coques iPhone : Slim case, iPhone 11 à iPhone 17, 24.99€
- Accessoires : Casquettes 29.99€, Bobs 39.99€, Polos 44.99€, Shorts 49.99€, Claquettes 54.99€
- Livraison gratuite dès 60€

## Contact
- Email : altidigitech@gmail.com
```

> Ce format remplace la section 11 ci-dessus. Utiliser ce contenu mis à jour.
