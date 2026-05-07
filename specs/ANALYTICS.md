# specs/ANALYTICS.md — Analytics & Tracking

> Contrat pour Claude Code. Chaque pixel, chaque événement, chaque condition de chargement est défini ici.
> **Règle RGPD absolue** : aucun script de tracking ne se charge avant le consentement cookies.
> Référence croisée : `specs/LEGAL.md` (bannière cookies), `specs/NAVIGATION.md` §9 (cart AJAX).

---

## 1. RÈGLE RGPD — CONSENTEMENT OBLIGATOIRE

### Principe

Les scripts GA4, Meta Pixel et TikTok Pixel ne doivent **JAMAIS** se charger automatiquement. Ils se chargent **uniquement** après que le visiteur a cliqué "Accepter" sur la bannière cookies.

### Mécanisme dans le thème

Le thème utilise une variable JS globale `window.hokuno_consent` qui est `false` par défaut et passe à `true` après acceptation.

```javascript
// Dans hokuno.js — au chargement
window.hokuno_consent = localStorage.getItem('hokuno-cookie-consent') === 'accepted';

// Après acceptation (bouton "Accepter" de la bannière cookies)
function acceptCookies() {
  localStorage.setItem('hokuno-cookie-consent', 'accepted');
  window.hokuno_consent = true;
  loadAnalytics(); // Charger les scripts maintenant
  document.querySelector('.cookie-banner').classList.remove('show');
}

// Après refus
function refuseCookies() {
  localStorage.setItem('hokuno-cookie-consent', 'refused');
  window.hokuno_consent = false;
  document.querySelector('.cookie-banner').classList.remove('show');
}
```

### Chargement conditionnel dans theme.liquid

```liquid
<!-- Avant </body> dans theme.liquid -->
<script>
  function loadAnalytics() {
    if (!window.hokuno_consent) return;

    // GA4
    {% if settings.ga4_id != blank %}
    var gs = document.createElement('script');
    gs.src = 'https://www.googletagmanager.com/gtag/js?id={{ settings.ga4_id }}';
    gs.async = true;
    document.head.appendChild(gs);
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', '{{ settings.ga4_id }}', { send_page_view: true });
    window.gtag = gtag;
    {% endif %}

    // Meta Pixel
    {% if settings.meta_pixel_id != blank %}
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;
    n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}
    (window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', '{{ settings.meta_pixel_id }}');
    fbq('track', 'PageView');
    window.fbq = fbq;
    {% endif %}

    // TikTok Pixel
    {% if settings.tiktok_pixel_id != blank %}
    !function(w,d,t){w.TiktokAnalyticsObject=t;var ttq=w[t]=w[t]||[];
    ttq.methods=["page","track","identify","instances","debug","on","off","once","ready","alias","group","enableCookie","disableCookie"];
    ttq.setAndDefer=function(t,e){t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}};
    for(var i=0;i<ttq.methods.length;i++)ttq.setAndDefer(ttq,ttq.methods[i]);
    ttq.instance=function(t){for(var e=ttq._i[t]||[],n=0;n<ttq.methods.length;n++)ttq.setAndDefer(e,ttq.methods[n]);return e};
    ttq.load=function(e,n){var i="https://analytics.tiktok.com/i18n/pixel/events.js";
    ttq._i=ttq._i||{};ttq._i[e]=[];ttq._i[e]._u=i;ttq._t=ttq._t||{};ttq._t[e]=+new Date;
    ttq._o=ttq._o||{};ttq._o[e]=n||{};var o=document.createElement("script");
    o.type="text/javascript";o.async=!0;o.src=i+"?sdkid="+e+"&lib="+t;
    var a=document.getElementsByTagName("script")[0];a.parentNode.insertBefore(o,a)};
    ttq.load('{{ settings.tiktok_pixel_id }}');
    ttq.page();
    }(window,document,'ttq');
    {% endif %}
  }

  // Charger immédiatement si déjà consenti
  if (window.hokuno_consent) { loadAnalytics(); }
</script>
```

---

## 2. SETTINGS DU THÈME

Ajouter dans `config/settings_schema.json` une section pour les IDs de tracking :

```json
{
  "name": "Analytics",
  "settings": [
    {
      "type": "text",
      "id": "ga4_id",
      "label": "Google Analytics 4 Measurement ID",
      "info": "Format : G-XXXXXXXXXX",
      "placeholder": "G-"
    },
    {
      "type": "text",
      "id": "meta_pixel_id",
      "label": "Meta Pixel ID",
      "info": "Format : numérique (ex : 123456789)",
      "placeholder": ""
    },
    {
      "type": "text",
      "id": "tiktok_pixel_id",
      "label": "TikTok Pixel ID",
      "info": "Format : alphanumeric (ex : CXXXXXXXXX)",
      "placeholder": ""
    }
  ]
}
```

Les IDs sont configurés dans Shopify Admin → Online Store → Themes → Customize → Theme settings → Analytics. Pas hardcodés dans le code.

---

## 3. GOOGLE ANALYTICS 4

### Setup (toi — manuel)

| Étape | Action |
|-------|--------|
| 1 | Aller sur `https://analytics.google.com` |
| 2 | Créer un compte (si pas existant) → nom : "HOKUNO" |
| 3 | Créer une propriété → nom : "Hokuno Store", fuseau : Paris, devise : EUR |
| 4 | Choisir "Web" comme plateforme |
| 5 | URL du site : `https://hokuno.com` (ou URL temporaire Shopify) |
| 6 | Copier le Measurement ID (`G-XXXXXXXXXX`) |
| 7 | Coller dans Shopify → Theme settings → Analytics → GA4 ID |

### Alternative : app Google & YouTube

Shopify Admin → Settings → Apps → Google & YouTube channel → Connecter le compte Google → GA4 se configure automatiquement.

Avantage : les événements e-commerce (purchase, etc.) sont automatiques.
Inconvénient : moins de contrôle, charge du JS supplémentaire.

**Recommandation** : utiliser l'injection manuelle dans le thème (section 1) pour le contrôle RGPD. L'app Shopify ne respecte pas toujours le consentement cookies.

### Événements e-commerce GA4

| Événement | Quand il se déclenche | Données envoyées |
|-----------|----------------------|------------------|
| `page_view` | Chaque chargement de page | URL, titre |
| `view_item` | Ouverture d'une page produit | product_id, name, price, category |
| `add_to_cart` | Clic "Ajouter au panier" | product_id, name, price, quantity |
| `begin_checkout` | Clic "Passer la commande" (page panier) | items[], total |
| `purchase` | Commande complétée (page thank you) | transaction_id, value, items[] |
| `view_item_list` | Page collection | items[], list_name |

### Implémentation des événements dans hokuno.js

```javascript
// Fonction helper — envoie un événement GA4 seulement si consenti
function trackEvent(eventName, params) {
  if (window.hokuno_consent && window.gtag) {
    gtag('event', eventName, params);
  }
}

// view_item — sur les pages produit
{% if template == 'product' %}
document.addEventListener('DOMContentLoaded', () => {
  trackEvent('view_item', {
    currency: '{{ cart.currency.iso_code }}',
    value: {{ product.price | money_without_currency | remove: ',' }},
    items: [{
      item_id: '{{ product.id }}',
      item_name: {{ product.title | json }},
      price: {{ product.price | money_without_currency | remove: ',' }},
      item_category: '{{ product.collections.first.title }}'
    }]
  });
});
{% endif %}

// add_to_cart — dans la fonction addToCart (NAVIGATION.md §9)
// Ajouter après le fetch réussi :
trackEvent('add_to_cart', {
  currency: shopCurrency,
  value: variantPrice,
  items: [{ item_id: variantId, item_name: productTitle, price: variantPrice, quantity: quantity }]
});

// view_item_list — sur les pages collection
{% if template == 'collection' %}
document.addEventListener('DOMContentLoaded', () => {
  trackEvent('view_item_list', {
    item_list_name: {{ collection.title | json }},
    items: [
      {% for product in collection.products limit: 24 %}
      { item_id: '{{ product.id }}', item_name: {{ product.title | json }}, price: {{ product.price | money_without_currency | remove: ',' }} }{% unless forloop.last %},{% endunless %}
      {% endfor %}
    ]
  });
});
{% endif %}
```

### purchase — page thank you

L'événement `purchase` se déclenche sur la page de confirmation de commande Shopify. Shopify injecte automatiquement le code de conversion si GA4 est connecté via l'app. Sinon, ajouter dans Shopify Admin → Settings → Checkout → Additional scripts :

```html
{% if first_time_accessed %}
<script>
  if (localStorage.getItem('hokuno-cookie-consent') === 'accepted' && window.gtag) {
    gtag('event', 'purchase', {
      transaction_id: '{{ order.name }}',
      value: {{ total_price | money_without_currency | remove: ',' }},
      currency: '{{ currency }}',
      items: [
        {% for line_item in line_items %}
        {
          item_id: '{{ line_item.product_id }}',
          item_name: {{ line_item.title | json }},
          price: {{ line_item.final_price | money_without_currency | remove: ',' }},
          quantity: {{ line_item.quantity }}
        }{% unless forloop.last %},{% endunless %}
        {% endfor %}
      ]
    });
  }
</script>
{% endif %}
```

---

## 4. META PIXEL (Facebook / Instagram)

### Setup (toi — manuel)

| Étape | Action |
|-------|--------|
| 1 | Aller sur `https://business.facebook.com` → Events Manager |
| 2 | Créer un pixel → nom : "Hokuno Store" |
| 3 | Copier le Pixel ID (numérique) |
| 4 | Coller dans Shopify → Theme settings → Analytics → Meta Pixel ID |

### Événements Meta Pixel

| Événement | Quand | Équivalent GA4 |
|-----------|-------|----------------|
| `PageView` | Chaque page (auto via `fbq('track', 'PageView')`) | `page_view` |
| `ViewContent` | Page produit | `view_item` |
| `AddToCart` | Ajout au panier | `add_to_cart` |
| `InitiateCheckout` | Clic checkout | `begin_checkout` |
| `Purchase` | Commande complétée | `purchase` |

### Implémentation dans hokuno.js

```javascript
// Fonction helper Meta
function trackMeta(eventName, params) {
  if (window.hokuno_consent && window.fbq) {
    fbq('track', eventName, params);
  }
}

// ViewContent — page produit
{% if template == 'product' %}
document.addEventListener('DOMContentLoaded', () => {
  trackMeta('ViewContent', {
    content_name: {{ product.title | json }},
    content_ids: ['{{ product.id }}'],
    content_type: 'product',
    value: {{ product.price | money_without_currency | remove: ',' }},
    currency: '{{ cart.currency.iso_code }}'
  });
});
{% endif %}

// AddToCart — dans addToCart() après succès
trackMeta('AddToCart', {
  content_ids: [variantId],
  content_type: 'product',
  value: variantPrice,
  currency: shopCurrency
});
```

### Purchase — checkout additional scripts

```html
{% if first_time_accessed %}
<script>
  if (localStorage.getItem('hokuno-cookie-consent') === 'accepted' && window.fbq) {
    fbq('track', 'Purchase', {
      value: {{ total_price | money_without_currency | remove: ',' }},
      currency: '{{ currency }}',
      content_ids: [{% for line_item in line_items %}'{{ line_item.product_id }}'{% unless forloop.last %},{% endunless %}{% endfor %}],
      content_type: 'product',
      num_items: {{ line_items.size }}
    });
  }
</script>
{% endif %}
```

---

## 5. TIKTOK PIXEL

### Setup (toi — manuel)

| Étape | Action |
|-------|--------|
| 1 | Aller sur `https://ads.tiktok.com` → Assets → Events → Web Events |
| 2 | Créer un pixel → nom : "Hokuno Store" → mode : Manual |
| 3 | Copier le Pixel ID |
| 4 | Coller dans Shopify → Theme settings → Analytics → TikTok Pixel ID |

**Statut : optionnel au lancement.** À activer quand TikTok Shop est connecté.

### Événements TikTok

| Événement | Quand |
|-----------|-------|
| `page_view` | Auto via `ttq.page()` |
| `ViewContent` | Page produit |
| `AddToCart` | Ajout au panier |
| `InitiateCheckout` | Clic checkout |
| `CompletePayment` | Commande complétée |

### Implémentation

```javascript
function trackTikTok(eventName, params) {
  if (window.hokuno_consent && window.ttq) {
    ttq.track(eventName, params);
  }
}

// ViewContent
{% if template == 'product' %}
trackTikTok('ViewContent', {
  content_id: '{{ product.id }}',
  content_name: {{ product.title | json }},
  value: {{ product.price | money_without_currency | remove: ',' }},
  currency: '{{ cart.currency.iso_code }}'
});
{% endif %}

// AddToCart — dans addToCart()
trackTikTok('AddToCart', { content_id: variantId, value: variantPrice, currency: shopCurrency });
```

---

## 6. SHOPIFY ANALYTICS

Intégré par défaut — aucune configuration nécessaire.

| Fonction | Accès |
|----------|-------|
| Dashboard | Shopify Admin → Analytics → Dashboard |
| Rapports | Shopify Admin → Analytics → Reports |
| Live View | Shopify Admin → Analytics → Live View |
| Ventes par produit | Reports → Sales by product |
| Trafic par source | Reports → Sessions by referrer |
| Conversions | Reports → Online store conversion rate |

Shopify Analytics fonctionne **indépendamment du consentement cookies** car c'est du first-party analytics côté serveur.

---

## 7. FONCTIONS CONSOLIDÉES DANS HOKUNO.JS

Toutes les fonctions de tracking sont regroupées dans un bloc cohérent :

```javascript
// ═══ ANALYTICS ═══

function trackEvent(eventName, params) {
  if (!window.hokuno_consent) return;
  if (window.gtag) gtag('event', eventName, params);
}

function trackMeta(eventName, params) {
  if (!window.hokuno_consent) return;
  if (window.fbq) fbq('track', eventName, params);
}

function trackTikTok(eventName, params) {
  if (!window.hokuno_consent) return;
  if (window.ttq) ttq.track(eventName, params);
}

// Fonction combinée — envoie à tous les pixels en un appel
function trackAll(ga4Event, metaEvent, tiktokEvent, params) {
  trackEvent(ga4Event, params);
  if (metaEvent) trackMeta(metaEvent, params);
  if (tiktokEvent) trackTikTok(tiktokEvent, params);
}
```

### Intégration dans les événements du site

| Action utilisateur | Appel dans hokuno.js |
|-------------------|---------------------|
| Page produit chargée | `trackAll('view_item', 'ViewContent', 'ViewContent', {...})` |
| Ajout au panier (dans `addToCart()`) | `trackAll('add_to_cart', 'AddToCart', 'AddToCart', {...})` |
| Clic checkout (dans cart.liquid) | `trackAll('begin_checkout', 'InitiateCheckout', 'InitiateCheckout', {...})` |
| Page collection chargée | `trackEvent('view_item_list', {...})` (GA4 uniquement) |
| Commande complétée | Via checkout additional scripts (section 3 + 4) |

---

## 8. MÉTRIQUES À SUIVRE

### Semaine 1 post-lancement

| Métrique | Outil | Cible |
|----------|-------|-------|
| Visiteurs uniques | GA4 → Real-time | > 0 (vérifier que le tracking marche) |
| Pages vues / session | GA4 → Engagement | > 2 |
| Taux de rebond | GA4 → Engagement | < 70% |
| add_to_cart events | GA4 → Events | > 0 |
| Taux de conversion | Shopify Analytics | Benchmark : 1-3% (e-commerce) |

### Mois 1

| Métrique | Outil | Cible |
|----------|-------|-------|
| Sessions | GA4 | Croissance semaine/semaine |
| Sources de trafic | GA4 → Acquisition | Identifier top sources (TikTok, Instagram, organique) |
| Produits les plus vus | GA4 → Events → view_item | Top 10 |
| Produits les plus achetés | Shopify → Reports → Sales by product | Top 10 |
| Panier moyen | Shopify → Reports | Cible : > 60€ (seuil livraison gratuite) |
| Taux d'abandon panier | Shopify → Reports | Benchmark : 60-80% (normal e-commerce) |

### GEO (Generative Engine Optimization)

| Métrique | Méthode | Fréquence |
|----------|---------|-----------|
| Mention Hokuno dans ChatGPT | Prompt test : "Connais-tu la marque Hokuno ?" | Hebdomadaire |
| Mention dans Perplexity | Recherche : "streetwear manga français" | Hebdomadaire |
| Mention dans Google AI Overviews | Recherche Google : "t-shirt manga parodie" | Hebdomadaire |
| Citation avec URL | Vérifier si l'URL Shopify est citée dans les réponses IA | Hebdomadaire |

---

## 9. CONFIGURATION CHECKOUT — ADDITIONAL SCRIPTS

Shopify Admin → Settings → Checkout → Order status page → Additional scripts

Ce champ contient les scripts de conversion qui se déclenchent uniquement sur la page de remerciement après achat :

```html
<!-- HOKUNO — Analytics conversion tracking -->
{% if first_time_accessed %}
<script>
  var consent = localStorage.getItem('hokuno-cookie-consent');
  if (consent === 'accepted') {
    // GA4 Purchase
    if (typeof gtag === 'function') {
      gtag('event', 'purchase', {
        transaction_id: '{{ order.name }}',
        value: {{ total_price | money_without_currency | remove: ',' }},
        currency: '{{ currency }}',
        items: [{% for line_item in line_items %}{item_id:'{{ line_item.product_id }}',item_name:{{ line_item.title | json }},price:{{ line_item.final_price | money_without_currency | remove: ',' }},quantity:{{ line_item.quantity }}}{% unless forloop.last %},{% endunless %}{% endfor %}]
      });
    }
    // Meta Pixel Purchase
    if (typeof fbq === 'function') {
      fbq('track', 'Purchase', {
        value: {{ total_price | money_without_currency | remove: ',' }},
        currency: '{{ currency }}',
        content_ids: [{% for line_item in line_items %}'{{ line_item.product_id }}'{% unless forloop.last %},{% endunless %}{% endfor %}],
        content_type: 'product',
        num_items: {{ line_items.size }}
      });
    }
    // TikTok Pixel Purchase
    if (typeof ttq !== 'undefined') {
      ttq.track('CompletePayment', {
        value: {{ total_price | money_without_currency | remove: ',' }},
        currency: '{{ currency }}'
      });
    }
  }
</script>
{% endif %}
```

> `{% if first_time_accessed %}` garantit que l'événement ne se déclenche qu'une fois (pas à chaque refresh de la page de confirmation).

---

## 10. VÉRIFICATION

### Tester GA4

1. Ouvrir GA4 → Real-time → Events
2. Visiter le site dans un autre onglet (accepter les cookies)
3. Naviguer sur une page produit → vérifier `view_item`
4. Ajouter au panier → vérifier `add_to_cart`
5. Les événements doivent apparaître en temps réel

### Tester Meta Pixel

1. Installer l'extension Chrome "Facebook Pixel Helper"
2. Visiter le site (cookies acceptés)
3. L'extension doit afficher les événements : PageView, ViewContent, AddToCart
4. Vérifier dans Meta Events Manager → Test Events

### Tester le consentement RGPD

1. Ouvrir le site en navigation privée
2. **Refuser** les cookies
3. Ouvrir DevTools → Network → filtrer par "gtag\|fbevents\|analytics"
4. **Aucune requête** ne doit apparaître vers Google Analytics ou Meta
5. Accepter les cookies → les requêtes doivent maintenant apparaître
