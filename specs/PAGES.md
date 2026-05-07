# specs/PAGES.md — Toutes les pages du site

> Contrat pour Claude Code. Chaque page, chaque section, chaque contenu est défini ici.
> Les composants partagés (navbar, footer, breadcrumbs, cart AJAX) sont dans `specs/NAVIGATION.md`.
> Le design system (couleurs, typo, espacements) est dans `specs/THEME.md`.

---

## CARTE DU SITE

| Page | URL | Template | Breadcrumbs |
|------|-----|----------|-------------|
| Accueil | `/` | `index.liquid` | Non |
| Liste collections | `/collections` | `list-collections.liquid` | Non |
| Collection unique | `/collections/{handle}` | `collection.liquid` | Oui |
| Produit | `/products/{handle}` | `product.liquid` | Oui |
| Panier | `/cart` | `cart.liquid` | Non |
| Recherche | `/search` | `search.liquid` | Non |
| À propos | `/pages/about` | `page.liquid` | Oui |
| FAQ | `/pages/faq` | `page.liquid` | Oui |
| Contact | `/pages/contact` | `page.contact.liquid` | Oui |
| Mentions légales | `/pages/mentions-legales` | `page.liquid` | Oui |
| Blog | `/blogs/journal` | `blog.liquid` | Oui |
| Article | `/blogs/journal/{handle}` | `article.liquid` | Oui |
| Nouveautés | `/collections/all?sort_by=created-descending` | `collection.liquid` | Oui |
| Connexion | `/account/login` | `customers/login.liquid` | Non |
| Inscription | `/account/register` | `customers/register.liquid` | Non |
| Récupération MDP | `/account/login#recover` | `customers/login.liquid` | Non |
| Mon compte | `/account` | `customers/account.liquid` | Non |
| Détail commande | `/account/orders/{id}` | `customers/order.liquid` | Non |
| CGV | `/policies/terms-of-service` | Shopify natif (Settings → Policies) | Non |
| Confidentialité | `/policies/privacy-policy` | Shopify natif | Non |
| Retours | `/policies/refund-policy` | Shopify natif | Non |
| Checkout | `/checkout` | Shopify natif (non customisable par thème) | Non |
| 404 | — | `404.liquid` | Non |
| Mot de passe | — | `password.liquid` | Non |
| Carte cadeau | — | `gift_card.liquid` | Non |

---

## 1. PAGE D'ACCUEIL — `/`

Template : `index.liquid`
Pas de `.page-wrap` — le hero gère son propre padding.
Mockup de référence : `assets/design-reference/hero-landing.png`

### Structure complète (de haut en bas)

```
[NAVBAR]                     ← theme.liquid
[HERO]                       ← index.liquid
[BARRE DE CONFIANCE]         ← index.liquid
[SECTION COLLECTIONS]        ← index.liquid
[PRODUITS PHARES]            ← index.liquid
[FOOTER]                     ← theme.liquid
```

### 1.1 HERO

Plein écran (`min-height: 100vh`), deux colonnes sur desktop.

**Colonne gauche (45%) :**

| Élément | Contenu | Traduction EN |
|---------|---------|---------------|
| H1 | `TOUJOURS ALLER DE L'AVANT` | `ALWAYS MOVING FORWARD` |
| Katakana | `ホクノ` | `ホクノ` (identique) |
| Bouton primaire | `DÉCOUVRIR LA COLLECTION →` → `/collections` | `DISCOVER THE COLLECTION →` |
| Bouton secondaire | `NOUVEAUTÉS` → `/collections/all?sort_by=created-descending` | `NEW ARRIVALS` |

Bouton primaire : style `.btn-gold`
Bouton secondaire : style `.btn-outline`

**Colonne droite (55%) :**

Image : `hero-tshirt.png` — t-shirt Wanted avec boussole dorée et glow.
Fondu radial sur les bords pour fusion avec le fond noir :
```css
.hero-img-wrap::after {
  content: '';
  position: absolute;
  inset: -4px;
  background: radial-gradient(ellipse at center, transparent 55%, #000000 100%);
  pointer-events: none;
  z-index: 3;
}
```

**Textes verticaux (desktop uniquement, cachés en mobile) :**

| Position | Contenu |
|----------|---------|
| Gauche | `HOKUNO` — spacer — `STREETWEAR` — spacer — `001` |
| Droite haut | `北へ向かって` (katakana doré, opacité 0.55) |
| Droite bas | `35.6895°N, 139.6917°E` (coordonnées Tokyo, opacité 0.2) |

**Produits phares dans le hero (desktop uniquement, cachés en mobile) :**

Position : en bas à droite du hero, au-dessus du fold.
3 product-cards miniatures avec image, titre tronqué (30 chars), prix.
Source : `collections.all.products limit: 3`
Boutons nav ‹ › pour un futur carrousel (non fonctionnel en v1).

### 1.2 BARRE DE CONFIANCE

3 cartes glassmorphism, alignées horizontalement (desktop) ou empilées verticalement (mobile).

| Icône | Label | Sous-texte | Traduction EN |
|-------|-------|-----------|---------------|
| 🌐 | Livraison Internationale | Offerte dès 60€ | International Shipping — Free from €60 |
| ↩️ | Retours Faciles | 30 jours pour changer d'avis | Easy Returns — 30 days to change your mind |
| 🔒 | Paiements Sécurisés | Cryptés et protégés | Secure Payments — Encrypted and protected |

Utiliser les clés de traduction : `{{ 'trust.shipping.label' | t }}`, etc.

### 1.3 SECTION COLLECTIONS

Détaillée dans `specs/COLLECTIONS.md` section 10.
Titre : "EXPLOREZ NOS UNIVERS"
Sous-titre : "Des collections pensées comme des récits. Inspirées par la culture, le symbole et le mouvement."
Icône boussole dorée entre le sous-titre et la grille.
Grille 4 colonnes avec les 4 collection-cards dans l'ordre : Wanted, Direction, Mythologie, Design Hokuno.

### 1.4 PRODUITS PHARES

Titre : `PRODUITS PHARES` (h2, centré)
Grille : 4 colonnes desktop, 2 colonnes mobile.
Source : `collections.all.products limit: 8`
Chaque produit utilise le snippet `{% render 'product-card', product: product %}`.

> Note : les 8 produits affichés sont les premiers de la collection "all" dans l'ordre par défaut de Shopify. Pour contrôler lesquels apparaissent, on pourra créer une collection manuelle "Produits phares" (`frontpage`) plus tard.

### 1.5 Mobile (<768px)

- Hero : colonnes empilées (texte au-dessus, image en dessous), texte centré à gauche
- Titre H1 : `38px` au lieu de `76px`
- Katakana : `30px` au lieu de `52px`
- Boutons : pleine largeur, empilés verticalement
- Textes verticaux : `display: none`
- Produits phares hero : `display: none`
- Trust bar : empilée verticalement
- Collections : grille 2 colonnes
- Produits phares section : grille 2 colonnes

---

## 2. PANIER — `/cart`

Template : `cart.liquid`
Pas de breadcrumbs.

### Structure

```
[PAGE-WRAP]
  [TITRE H1 : PANIER]
  [LISTE DES ARTICLES]        ← si cart non vide
  [SOUS-TOTAL + CHECKOUT]     ← si cart non vide
  [PANIER VIDE]               ← si cart vide
[/PAGE-WRAP]
```

### Panier non vide

**Chaque article :**

```liquid
{% for item in cart.items %}
<div class="cart-item">
  <a href="{{ item.url }}">
    <img src="{{ item.image | image_url: width: 200 }}" alt="{{ item.title }}" class="cart-item-img">
  </a>
  <div class="cart-item-details">
    <h4 class="cart-item-title">{{ item.product.title }}</h4>
    <p class="cart-item-variant">{{ item.variant.title }}</p>
    <p class="cart-item-price">{{ item.original_line_price | money }}</p>
  </div>
  <div class="cart-item-qty">
    <button class="qty-btn" onclick="updateQty('{{ item.key }}', {{ item.quantity | minus: 1 }})">−</button>
    <span class="qty-val">{{ item.quantity }}</span>
    <button class="qty-btn" onclick="updateQty('{{ item.key }}', {{ item.quantity | plus: 1 }})">+</button>
  </div>
  <button class="cart-item-remove" onclick="updateQty('{{ item.key }}', 0)" aria-label="Supprimer">✕</button>
</div>
{% endfor %}
```

**Styles cart-item :**
- Layout : `display: flex; gap: 24px; align-items: center`
- Séparateur : `border-bottom: 1px solid rgba(255,255,255,0.06); padding: 24px 0`
- Image : `100×100px`, border-radius `8px`, object-fit `cover`
- Titre : font-weight `600`, couleur `#FFFFFF`
- Variante : font-size `13px`, couleur `rgba(255,255,255,0.5)`
- Prix : font-weight `700`, couleur `#D4A853`
- Boutons quantité : `36×36px`, border-radius `6px`, fond `rgba(255,255,255,0.04)`, bordure `rgba(255,255,255,0.1)`, couleur `#FFFFFF`
- Bouton supprimer : `36×36px`, couleur `rgba(255,255,255,0.3)`, hover `#ff6b6b`

**Mise à jour quantité AJAX :**

```javascript
// Dans hokuno.js
async function updateQty(key, qty) {
  await fetch('/cart/change.js', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: key, quantity: qty })
  });
  window.location.reload(); // v1 : rechargement. v2 : update AJAX du DOM.
}
```

**Sous-total et checkout :**

```
[LIVRAISON GRATUITE]    ← barre de progression vers 60€
[SOUS-TOTAL]            ← montant total
[BOUTON CHECKOUT]       ← lien vers /checkout
```

Barre de progression livraison :
```liquid
{% assign threshold = 6000 %} <!-- 60€ en centimes -->
{% assign remaining = threshold | minus: cart.total_price %}
{% if remaining > 0 %}
  <p class="cart-shipping">Plus que {{ remaining | money }} pour la livraison gratuite !</p>
  <div class="cart-progress">
    <div class="cart-progress-bar" style="width: {{ cart.total_price | times: 100 | divided_by: threshold }}%"></div>
  </div>
{% else %}
  <p class="cart-shipping cart-shipping-free">✓ Livraison gratuite !</p>
{% endif %}
```

Style barre : hauteur `4px`, fond `rgba(255,255,255,0.08)`, barre remplie `#D4A853`, border-radius `2px`

Sous-total : font-size `28px`, font-weight `700`, couleur `#D4A853`
Bouton checkout : `.btn-gold`, pleine largeur, texte `PASSER LA COMMANDE →` → lien vers `/checkout`

**Note code promo :** le code promo HOKUNO15 est saisi au checkout Shopify, pas sur la page panier. Shopify gère nativement les codes promo au checkout. Pas besoin de champ promo sur `/cart`.

### Panier vide

```liquid
<div class="cart-empty">
  <p>{{ 'cart.empty' | t }}</p>
  <a href="/collections" class="btn-gold">{{ 'cart.discover' | t }}</a>
</div>
```

Texte FR : "Votre panier est vide."
Bouton : "DÉCOUVRIR NOS COLLECTIONS"
Style : centré, margin-top `40px`

### Mobile

- Image article : `80×80px`
- Layout article : flex-wrap, image + infos sur une ligne, quantité + supprimer en dessous
- Bouton checkout : sticky en bas de l'écran (si panier non vide), au-dessus du bottom nav

---

## 3. À PROPOS — `/pages/about`

Template : `page.liquid`
Handle Shopify : `about`
Breadcrumbs : `Accueil › À propos`

### Contenu à créer dans Shopify Admin (page statique)

**Titre :** À propos de Hokuno

**Corps HTML :**

```html
<div class="about-content">
  <h2>ホクノ — Vers le Nord</h2>
  <p>Hokuno (北の) signifie « Vers le Nord » en japonais. C'est une philosophie avant d'être une marque : toujours aller de l'avant, ne jamais s'arrêter.</p>

  <h3>Notre histoire</h3>
  <p>Née en 2026, Hokuno est une marque streetwear française qui revisite l'univers du manga à travers la parodie, le temps qui passe et la mythologie. Chaque design raconte une histoire — celle de personnages transformés, vieillis, divinisés ou réduits à leur silhouette.</p>

  <h3>Nos collections</h3>
  <p><strong>Wanted</strong> — Des avis de recherche revisités. 30 ans de manga, et ils sont épuisés. Humour noir garanti.</p>
  <p><strong>Direction</strong> — Des silhouettes encrées avec une citation universelle : « Je n'ai pas besoin d'un plan… juste d'une direction. »</p>
  <p><strong>Mythologie</strong> — L'équipage réinventé en divinités grecques. Chaque personnage dans sa couleur signature.</p>
  <p><strong>Design Hokuno</strong> — Le branding pur. Le logpose, le katakana, les motifs signature.</p>

  <h3>Notre démarche</h3>
  <p>Chaque produit est fabriqué à la commande (print on demand) — zéro gaspillage, zéro stock mort. Les designs sont générés par IA et retravaillés pour atteindre une qualité graphique professionnelle.</p>

  <h3>Contact</h3>
  <p>Une question, une idée, une collaboration ? Écrivez-nous à <a href="mailto:altidigitech@gmail.com">altidigitech@gmail.com</a> ou via notre <a href="/pages/contact">formulaire de contact</a>.</p>
</div>
```

**Contenu EN (via Shopify Markets) :**

```html
<div class="about-content">
  <h2>ホクノ — Towards the North</h2>
  <p>Hokuno (北の) means "Towards the North" in Japanese. It's a philosophy before it's a brand: always moving forward, never stopping.</p>

  <h3>Our Story</h3>
  <p>Born in 2026, Hokuno is a French streetwear brand that reimagines the manga universe through parody, the passage of time, and mythology. Each design tells a story — of characters transformed, aged, deified, or reduced to their silhouette.</p>

  <h3>Our Collections</h3>
  <p><strong>Wanted</strong> — Reimagined wanted posters. 30 years of manga, and they're exhausted. Dark humor guaranteed.</p>
  <p><strong>Direction</strong> — Inked silhouettes with a universal quote: "I don't need a plan… just a direction."</p>
  <p><strong>Mythology</strong> — The crew reimagined as Greek deities. Each character in their signature color.</p>
  <p><strong>Design Hokuno</strong> — Pure branding. The logpose, the katakana, the signature patterns.</p>

  <h3>Our Approach</h3>
  <p>Every product is made to order (print on demand) — zero waste, zero dead stock. Designs are AI-generated and refined to professional graphic quality.</p>

  <h3>Contact</h3>
  <p>A question, an idea, a collaboration? Write to us at <a href="mailto:altidigitech@gmail.com">altidigitech@gmail.com</a> or via our <a href="/pages/contact">contact form</a>.</p>
</div>
```

### Style page statique (dans hokuno.css)

```css
.page-content h2 { font-size: 32px; font-weight: 900; margin-bottom: 16px; text-transform: uppercase; }
.page-content h3 { font-size: 18px; font-weight: 700; margin-top: 40px; margin-bottom: 12px; color: #D4A853; }
.page-content p { font-size: 15px; line-height: 1.8; color: rgba(255,255,255,0.7); margin-bottom: 16px; max-width: 700px; }
.page-content a { color: #D4A853; text-decoration: underline; }
.page-content a:hover { color: #fff; }
.page-content strong { color: #fff; font-weight: 600; }
```

---

## 4. FAQ — `/pages/faq`

Template : `page.liquid`
Handle Shopify : `faq`
Breadcrumbs : `Accueil › FAQ`

### Contenu : accordéon Q/R

Le contenu est créé dans Shopify Admin comme page statique HTML. Le JS dans `hokuno.js` transforme les éléments en accordéon cliquable.

**Questions et réponses :**

| # | Question FR | Réponse FR |
|---|-------------|------------|
| 1 | Comment sont fabriqués vos produits ? | Chaque produit est fabriqué à la commande (print on demand) par nos partenaires d'impression. Aucun stock — votre article est imprimé spécialement pour vous après votre commande. |
| 2 | Quels sont les délais de livraison ? | Fabrication : 3-7 jours ouvrés. Livraison France/EU : 5-10 jours ouvrés après expédition. International : 7-15 jours ouvrés. Vous recevez un numéro de suivi par email dès l'expédition. |
| 3 | La livraison est-elle gratuite ? | Oui, à partir de 60€ de commande. En dessous, les frais de livraison sont calculés au checkout selon votre destination. |
| 4 | Puis-je retourner un produit ? | Oui, vous disposez de 30 jours après réception pour retourner un produit non porté, non lavé, avec son étiquette. Contactez-nous à altidigitech@gmail.com pour initier un retour. |
| 5 | Comment utiliser un code promo ? | Entrez votre code dans le champ "Code de réduction" au moment du checkout. Le code HOKUNO15 offre -15% sur votre commande. |
| 6 | Quelles tailles sont disponibles ? | Nos t-shirts sont disponibles du S au XL. Consultez le guide des tailles sur chaque page produit pour trouver votre taille idéale. |
| 7 | Les designs sont-ils originaux ? | Oui. Chaque design est créé par notre équipe, généré par IA et retravaillé. Ce sont des parodies artistiques originales, jamais des reproductions directes. |
| 8 | Livrez-vous à l'international ? | Oui, nous livrons dans le monde entier. Les frais et délais varient selon la destination. |
| 9 | Comment vous contacter ? | Par email à altidigitech@gmail.com ou via notre formulaire de contact. Nous répondons sous 24-48h. |

### Structure HTML

```html
<div class="faq-list">
  <div class="faq-item">
    <button class="faq-question" aria-expanded="false">
      Comment sont fabriqués vos produits ?
      <span class="faq-icon">+</span>
    </button>
    <div class="faq-answer">
      <p>Chaque produit est fabriqué à la commande...</p>
    </div>
  </div>
  <!-- répéter pour chaque question -->
</div>
```

### Style accordéon

```css
.faq-item { border-bottom: 1px solid rgba(255,255,255,0.06); }
.faq-question {
  width: 100%; text-align: left; background: none; border: none;
  padding: 24px 0; color: #fff; font-size: 16px; font-weight: 600;
  cursor: pointer; display: flex; justify-content: space-between; align-items: center;
  transition: color 0.3s;
}
.faq-question:hover { color: #D4A853; }
.faq-icon { font-size: 20px; color: #D4A853; transition: transform 0.3s; }
.faq-item.open .faq-icon { transform: rotate(45deg); }
.faq-answer {
  max-height: 0; overflow: hidden; transition: max-height 0.3s ease;
}
.faq-item.open .faq-answer { max-height: 300px; }
.faq-answer p {
  padding: 0 0 24px; font-size: 14px; line-height: 1.8;
  color: rgba(255,255,255,0.6); max-width: 700px;
}
```

### JS accordéon (dans hokuno.js)

```javascript
document.querySelectorAll('.faq-question').forEach(btn => {
  btn.addEventListener('click', () => {
    const item = btn.parentElement;
    const isOpen = item.classList.contains('open');
    // Fermer tous les autres
    document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
    // Toggle celui-ci
    if (!isOpen) item.classList.add('open');
    btn.setAttribute('aria-expanded', !isOpen);
  });
});
```

---

## 5. CONTACT — `/pages/contact`

Template : `page.contact.liquid` (template dédié car le formulaire utilise `{% form 'contact' %}` qui est du Liquid — impossible à stocker dans le contenu HTML de Shopify Admin)
Handle Shopify : `contact`
Assignation : dans Shopify Admin → Pages → Contact → Template : `page.contact`
Breadcrumbs : `Accueil › Contact`

### Contenu

**Texte introductif :**
> Une question, une suggestion, une collaboration ? On vous répond sous 24-48h.

**Formulaire :**

```html
<div class="contact-wrap">
  <div class="contact-info">
    <h2>Contactez-nous</h2>
    <p>Une question, une suggestion, une collaboration ? On vous répond sous 24-48h.</p>
    <p class="contact-email">📧 <a href="mailto:altidigitech@gmail.com">altidigitech@gmail.com</a></p>
  </div>

  <form class="contact-form" method="post" action="/contact#contact_form">
    <input type="hidden" name="form_type" value="contact">
    <input type="hidden" name="utf8" value="✓">

    <label for="contact-name">{{ 'contact.name' | t }}</label>
    <input type="text" id="contact-name" name="contact[name]" required placeholder="Votre nom">

    <label for="contact-email">{{ 'contact.email' | t }}</label>
    <input type="email" id="contact-email" name="contact[email]" required placeholder="Votre email">

    <label for="contact-message">{{ 'contact.message' | t }}</label>
    <textarea id="contact-message" name="contact[body]" rows="6" required placeholder="Votre message"></textarea>

    <button type="submit" class="btn-gold">{{ 'contact.send' | t }}</button>
  </form>
</div>
```

### Style formulaire

```css
.contact-wrap { display: grid; grid-template-columns: 1fr 1.5fr; gap: 60px; }
.contact-info h2 { font-size: 28px; font-weight: 900; text-transform: uppercase; }
.contact-email { margin-top: 24px; }
.contact-email a { color: #D4A853; }
.contact-form label {
  display: block; font-size: 12px; font-weight: 600; letter-spacing: 1.5px;
  text-transform: uppercase; color: rgba(255,255,255,0.5); margin-bottom: 8px; margin-top: 24px;
}
.contact-form input, .contact-form textarea {
  width: 100%; padding: 14px 16px; background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1); border-radius: 6px;
  color: #fff; font-size: 14px; font-family: 'Inter', sans-serif;
}
.contact-form input:focus, .contact-form textarea:focus {
  border-color: #D4A853; outline: none;
}
.contact-form .btn-gold { margin-top: 24px; width: 100%; }
```

### Mobile

Colonnes empilées : info au-dessus, formulaire en dessous. Pleine largeur.

### Message de confirmation

Après soumission, Shopify redirige vers la même page avec un message de succès :

```liquid
{% if form.posted_successfully? %}
  <p class="form-success">✓ Message envoyé ! Nous vous répondons sous 24-48h.</p>
{% endif %}
```

Style : fond `rgba(212,168,83,0.1)`, bordure `1px solid #D4A853`, padding `16px`, border-radius `6px`, couleur `#D4A853`

---

## 6. BLOG — `/blogs/journal`

Template : `blog.liquid`
Breadcrumbs : `Accueil › Journal`

### Structure

```liquid
<div class="page-wrap">
  {% render 'breadcrumbs' %}
  <h1 class="page-title">{{ blog.title }}</h1>

  <div class="blog-grid">
    {% for article in blog.articles %}
      <a href="{{ article.url }}" class="blog-card">
        {% if article.image %}
          <img src="{{ article.image | image_url: width: 600 }}" alt="{{ article.title }}" loading="lazy">
        {% endif %}
        <div class="blog-card-info">
          <time class="blog-date">{{ article.published_at | date: "%d %B %Y" }}</time>
          <h3>{{ article.title }}</h3>
          <p>{{ article.excerpt_or_content | strip_html | truncate: 120 }}</p>
          <span class="blog-read">{{ 'blog.read_more' | t }} →</span>
        </div>
      </a>
    {% endfor %}
  </div>

  {% if blog.articles_count == 0 %}
    <p class="blog-empty">Aucun article pour le moment. Revenez bientôt !</p>
  {% endif %}
</div>
```

### Style

```css
.blog-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.blog-card {
  background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.06);
  border-radius: 12px; overflow: hidden; transition: all 0.35s; text-decoration: none;
}
.blog-card:hover { border-color: rgba(212,168,83,0.35); transform: translateY(-4px); }
.blog-card img { width: 100%; height: 200px; object-fit: cover; }
.blog-card-info { padding: 20px; }
.blog-date { font-size: 11px; color: rgba(255,255,255,0.35); letter-spacing: 1px; text-transform: uppercase; }
.blog-card-info h3 { font-size: 16px; font-weight: 700; margin-top: 8px; color: #fff; }
.blog-card-info p { font-size: 13px; color: rgba(255,255,255,0.5); margin-top: 8px; line-height: 1.6; }
.blog-read { display: inline-block; margin-top: 12px; font-size: 12px; color: #D4A853; font-weight: 600; letter-spacing: 1px; }
```

### Mobile

Grille : `grid-template-columns: 1fr` (1 seule colonne)

---

## 7. ARTICLE — `/blogs/journal/{handle}`

Template : `article.liquid`
Breadcrumbs : `Accueil › Journal › [Titre]`

### Structure

```liquid
<div class="page-wrap">
  {% render 'breadcrumbs' %}

  <article class="article">
    <time class="article-date">{{ article.published_at | date: "%d %B %Y" }}</time>
    <h1 class="article-title">{{ article.title }}</h1>

    {% if article.image %}
      <img class="article-hero" src="{{ article.image | image_url: width: 1200 }}" alt="{{ article.title }}">
    {% endif %}

    <div class="article-body">
      {{ article.content }}
    </div>

    <div class="article-nav">
      {% if blog.previous_article %}
        <a href="{{ blog.previous_article }}">← {{ 'blog.previous' | t }}</a>
      {% endif %}
      {% if blog.next_article %}
        <a href="{{ blog.next_article }}">{{ 'blog.next' | t }} →</a>
      {% endif %}
    </div>
  </article>
</div>
```

### Style

```css
.article { max-width: 760px; margin: 0 auto; }
.article-date { font-size: 12px; color: rgba(255,255,255,0.35); letter-spacing: 1px; text-transform: uppercase; }
.article-title { font-size: 36px; font-weight: 900; margin-top: 8px; text-transform: uppercase; line-height: 1.15; }
.article-hero { width: 100%; border-radius: 12px; margin: 32px 0; }
.article-body { font-size: 16px; line-height: 1.9; color: rgba(255,255,255,0.75); }
.article-body h2 { font-size: 24px; font-weight: 800; margin-top: 40px; margin-bottom: 16px; color: #fff; }
.article-body h3 { font-size: 18px; font-weight: 700; margin-top: 32px; margin-bottom: 12px; color: #D4A853; }
.article-body a { color: #D4A853; }
.article-body img { border-radius: 8px; margin: 24px 0; }
.article-nav {
  display: flex; justify-content: space-between; margin-top: 60px; padding-top: 24px;
  border-top: 1px solid rgba(255,255,255,0.06); font-size: 14px;
}
.article-nav a { color: #D4A853; font-weight: 600; }
```

---

## 8. COMPTE CLIENT — `/account`

### 8.1 Connexion — `/account/login`

Template : `customers/login.liquid`

```liquid
<div class="page-wrap">
  <div class="auth-wrap">
    <h1 class="auth-title">{{ 'customer.login.title' | t }}</h1>

    {% form 'customer_login' %}
      {% if form.errors %}
        <p class="form-error">{{ form.errors | default_errors }}</p>
      {% endif %}

      <label for="email">{{ 'customer.login.email' | t }}</label>
      <input type="email" id="email" name="customer[email]" autocomplete="email" required>

      <label for="password">{{ 'customer.login.password' | t }}</label>
      <input type="password" id="password" name="customer[password]" required>

      <button type="submit" class="btn-gold">{{ 'customer.login.submit' | t }}</button>
    {% endform %}

    <p class="auth-link">
      {{ 'customer.login.no_account' | t }}
      <a href="/account/register">{{ 'customer.login.create_account' | t }}</a>
    </p>
    <p class="auth-link">
      <a href="/account/login#recover">{{ 'customer.login.forgot_password' | t }}</a>
    </p>
  </div>
</div>
```

### 8.2 Inscription — `/account/register`

Même layout que login. Champs : prénom, nom, email, mot de passe. Bouton "CRÉER MON COMPTE".

### 8.3 Mon compte — `/account`

Affiche :
- Nom du client : `{{ customer.name }}`
- Email : `{{ customer.email }}`
- Historique des commandes : tableau avec date, numéro, statut, total
- Bouton "SE DÉCONNECTER" → lien vers `/account/logout`

### Style auth

```css
.auth-wrap { max-width: 420px; margin: 0 auto; }
.auth-title { font-size: 28px; font-weight: 900; text-transform: uppercase; margin-bottom: 32px; text-align: center; }
.auth-wrap label {
  display: block; font-size: 12px; font-weight: 600; letter-spacing: 1.5px;
  text-transform: uppercase; color: rgba(255,255,255,0.5); margin-bottom: 8px; margin-top: 20px;
}
.auth-wrap input {
  width: 100%; padding: 14px 16px; background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; color: #fff; font-size: 14px;
}
.auth-wrap input:focus { border-color: #D4A853; outline: none; }
.auth-wrap .btn-gold { width: 100%; margin-top: 24px; }
.auth-link { text-align: center; margin-top: 16px; font-size: 13px; color: rgba(255,255,255,0.5); }
.auth-link a { color: #D4A853; }
.form-error { background: rgba(255,0,0,0.08); border: 1px solid rgba(255,0,0,0.3); padding: 12px; border-radius: 6px; color: #ff6b6b; font-size: 13px; margin-bottom: 16px; }
```

---

## 9. PAGE 404

Template : `404.liquid`

```liquid
<div class="page-wrap error-page">
  <h1 class="error-code">404</h1>
  <p class="error-katakana">ホクノ</p>
  <p class="error-msg">{{ 'general.404.title' | t }}</p>
  <p class="error-sub">{{ 'general.404.subtitle' | t }}</p>
  <a href="/" class="btn-gold">{{ 'general.404.back' | t }}</a>
</div>
```

Texte FR : "Cette page n'existe pas." / "Vous vous êtes perdu ? Le Nord est par là."
Texte EN : "This page doesn't exist." / "Lost? North is this way."

### Style

```css
.error-page { text-align: center; min-height: 60vh; display: flex; flex-direction: column; align-items: center; justify-content: center; }
.error-code { font-size: 120px; font-weight: 900; color: rgba(255,255,255,0.08); line-height: 1; }
.error-katakana { font-size: 32px; color: #D4A853; margin-top: -20px; }
.error-msg { font-size: 18px; font-weight: 600; margin-top: 24px; }
.error-sub { font-size: 14px; color: rgba(255,255,255,0.5); margin-top: 8px; }
.error-page .btn-gold { margin-top: 32px; }
```

---

## 10. PAGE MOT DE PASSE

Template : `password.liquid`

Page standalone (son propre `<html>`, pas de theme.liquid). Déjà codée dans le thème actuel. À garder telle quelle.

**Contenu :**
- Logo Hokuno nav
- Titre : "HOKUNO"
- Katakana : "ホクノ"
- Texte : "Toujours aller de l'avant — Bientôt disponible"
- Formulaire mot de passe
- Message d'erreur si mot de passe incorrect

---

## 11. TEMPLATE `page.liquid` — GESTION DES PAGES STATIQUES

Le template `page.liquid` est utilisé par les pages about, FAQ et mentions légales. Le contenu HTML est stocké dans Shopify Admin → Pages.

```liquid
<!-- templates/page.liquid -->
<div class="page-wrap">
  {% render 'breadcrumbs' %}
  <h1 class="page-title">{{ page.title }}</h1>
  <div class="page-content">
    {{ page.content }}
  </div>
</div>
```

Le JS dans `hokuno.js` détecte automatiquement les éléments `.faq-question` pour activer l'accordéon FAQ — pas besoin de template séparé pour la FAQ.

La page contact utilise son propre template `page.contact.liquid` (section 5 ci-dessus) car elle nécessite du Liquid (`{% form 'contact' %}`).

**Template à ajouter dans `shopify-theme/templates/` :**
- `page.contact.liquid` — template dédié contact

**Assignation dans Shopify Admin :**
- Page "Contact" → Template suffix : `contact` (→ utilise `page.contact.liquid`)
- Pages "À propos", "FAQ", "Mentions légales" → Template par défaut (→ utilise `page.liquid`)

---

## 12. PAGES POLICIES — `/policies/*`

Les pages de politique sont des pages **natives Shopify**, pas des templates du thème. Leur contenu est rédigé dans Shopify Admin → Settings → Policies.

| URL | Page | Contenu rédigé dans |
|-----|------|---------------------|
| `/policies/terms-of-service` | Conditions générales de vente | `specs/LEGAL.md` |
| `/policies/privacy-policy` | Politique de confidentialité | `specs/LEGAL.md` |
| `/policies/refund-policy` | Politique de retour | `specs/LEGAL.md` |

Shopify applique un style par défaut. Le thème Hokuno n'a pas besoin de template custom pour ces pages — le fond noir et la typographie Inter s'appliquent via theme.liquid quand Shopify les rend dans le layout.

---

## 13. CHECKOUT — `/checkout`

Le checkout est **géré entièrement par Shopify** — pas customisable via le thème Liquid.

**Branding à configurer dans Shopify Admin → Settings → Checkout :**

| Élément | Valeur |
|---------|--------|
| Logo | `logo-hokuno-nav.png` (upload dans Settings → Checkout) |
| Couleur accent | `#D4A853` (boutons, liens) |
| Couleur fond | `#000000` ou le plus sombre disponible |
| Police | Laisser par défaut (Shopify ne supporte pas les fonts custom au checkout) |

---

## 14. PAGE NOUVEAUTÉS — `/collections/all?sort_by=created-descending`

Pas de template dédié. Cette URL utilise le template `collection.liquid` avec la collection "all" (tous les produits) triée par date de création décroissante.

Le lien "NOUVEAUTÉS" dans la navbar pointe vers cette URL. Le rendu est identique à une page collection normale (filtres, tri, pagination).

---

## 15. CARTE CADEAU — `gift_card.liquid`

Page standalone affichée quand un client reçoit une carte cadeau. Styling minimal Hokuno :

```liquid
<!-- templates/gift_card.liquid -->
<!DOCTYPE html>
<html lang="{{ request.locale.iso_code }}">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{ 'gift_cards.title' | t }} — HOKUNO</title>
  {{ content_for_header }}
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
  <style>
    body { background: #000; color: #fff; font-family: 'Inter', sans-serif; display: flex; align-items: center; justify-content: center; min-height: 100vh; }
    .gc-wrap { text-align: center; max-width: 400px; padding: 40px; }
    .gc-title { font-size: 28px; font-weight: 900; text-transform: uppercase; }
    .gc-amount { font-size: 48px; font-weight: 900; color: #D4A853; margin: 24px 0; }
    .gc-code { font-size: 18px; letter-spacing: 4px; background: rgba(255,255,255,0.04); padding: 16px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.1); margin: 24px 0; }
    .gc-shop { display: inline-block; margin-top: 24px; background: #D4A853; color: #000; padding: 14px 28px; font-weight: 700; font-size: 13px; letter-spacing: 1.5px; text-transform: uppercase; border-radius: 4px; text-decoration: none; }
  </style>
</head>
<body>
  <div class="gc-wrap">
    <h1 class="gc-title">HOKUNO ホクノ</h1>
    <p class="gc-amount">{{ gift_card.balance | money }}</p>
    <p class="gc-code">{{ gift_card.code | format_code }}</p>
    <p style="color:rgba(255,255,255,0.5);font-size:13px">
      {% if gift_card.expires_on %}
        {{ 'gift_cards.expires' | t }}: {{ gift_card.expires_on | date: "%d/%m/%Y" }}
      {% else %}
        {{ 'gift_cards.no_expiry' | t }}
      {% endif %}
    </p>
    <a href="{{ shop.url }}" class="gc-shop">{{ 'gift_cards.shop_now' | t }}</a>
  </div>
</body>
</html>
```

---

## 16. RÉCUPÉRATION MOT DE PASSE — `/account/login#recover`

Intégré dans `customers/login.liquid`. Quand l'ancre `#recover` est présente, afficher le formulaire de récupération au lieu du formulaire de connexion :

```liquid
<div id="recover" class="auth-wrap" style="display:none">
  <h2 class="auth-title">{{ 'customer.recover.title' | t }}</h2>
  <p style="color:rgba(255,255,255,0.5);text-align:center;margin-bottom:24px;font-size:14px">
    {{ 'customer.recover.subtitle' | t }}
  </p>
  {% form 'recover_customer_password' %}
    <label for="recover-email">{{ 'customer.login.email' | t }}</label>
    <input type="email" id="recover-email" name="email" autocomplete="email" required>
    <button type="submit" class="btn-gold">{{ 'customer.recover.submit' | t }}</button>
  {% endform %}
  <p class="auth-link">
    <a href="/account/login">← {{ 'customer.recover.back_to_login' | t }}</a>
  </p>
</div>
```

JS pour toggle entre login et recover :
```javascript
// Dans hokuno.js
if (window.location.hash === '#recover') {
  document.querySelector('#login-form')?.style.display = 'none';
  document.querySelector('#recover')?.style.display = 'block';
}
```

Texte FR : "Entrez votre adresse email, nous vous enverrons un lien de réinitialisation."
Bouton : "ENVOYER LE LIEN"

---

## 17. PAGES RÉFÉRENCÉES DANS D'AUTRES SPECS

| Page | Spec de référence | Ce qui y est détaillé |
|------|-------------------|-----------------------|
| Liste collections `/collections` | `specs/COLLECTIONS.md` §4 | Grille des 4 collections, ordre, snippet |
| Collection unique `/collections/{handle}` | `specs/COLLECTIONS.md` §5-9 | Filtres, tri, pagination, grille produits |
| Produit `/products/{handle}` | `specs/PRODUIT.md` | Galerie, variantes, backstory, similaires, guide tailles |
| Recherche `/search` | `specs/NAVIGATION.md` §8 | Champ recherche, résultats, pas de résultats |
| Policies `/policies/*` | `specs/LEGAL.md` | Contenu CGV, confidentialité, retours |
| Checkout `/checkout` | `specs/CONFIG-SHOPIFY.md` | Configuration paiements, devise |

---

## 18. RÉCAPITULATIF DES PAGES ET TEMPLATES

### Templates à créer dans `shopify-theme/templates/`

| Template | Page(s) | Note |
|----------|---------|------|
| `index.liquid` | Accueil | Hero, trust bar, collections, produits phares |
| `collection.liquid` | Collection + Nouveautés | Filtres, tri, pagination |
| `list-collections.liquid` | /collections | Grille des 4 collections |
| `product.liquid` | Produit | Détaillé dans `specs/PRODUIT.md` |
| `cart.liquid` | Panier | Quantité +/−, barre livraison, checkout |
| `search.liquid` | Recherche | Détaillé dans `specs/NAVIGATION.md` |
| `page.liquid` | About, FAQ, Mentions légales | Contenu HTML depuis Shopify Admin |
| `page.contact.liquid` | Contact | Formulaire Liquid dédié |
| `blog.liquid` | Journal | Grille articles |
| `article.liquid` | Article unique | Layout article + nav prev/next |
| `404.liquid` | 404 | Brandé Hokuno |
| `password.liquid` | Mot de passe | Standalone, déjà codé |
| `gift_card.liquid` | Carte cadeau | Standalone, brandé Hokuno |
| `customers/login.liquid` | Connexion + récupération MDP | Toggle via #recover |
| `customers/register.liquid` | Inscription | Formulaire création compte |
| `customers/account.liquid` | Mon compte | Infos + historique commandes |
| `customers/order.liquid` | Détail commande | Résumé d'une commande |

### Pages statiques à créer dans Shopify Admin

| Handle | Titre | Template | Contenu |
|--------|-------|----------|---------|
| `about` | À propos | `page` (défaut) | HTML section 3 |
| `faq` | FAQ | `page` (défaut) | HTML accordéon section 4 |
| `contact` | Contact | `page.contact` | Formulaire Liquid section 5 |
| `mentions-legales` | Mentions légales | `page` (défaut) | Contenu `specs/LEGAL.md` |

### Blog à créer

- Handle : `journal`
- Titre : "Journal"
- Créer dans Shopify Admin → Blog posts → Manage blogs
