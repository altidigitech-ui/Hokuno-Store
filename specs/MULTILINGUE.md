# specs/MULTILINGUE.md — Gestion bilingue FR/EN

> Contrat pour Claude Code. Stratégie multilingue, fichiers de traduction, et gestion des produits bilingues.
> Référence croisée : `specs/NAVIGATION.md` §7 (sélecteur langue), `specs/SEO.md` §7 (hreflang), `specs/CONFIG-SHOPIFY.md` §8 (Shopify Markets).

---

## 1. SITUATION ACTUELLE

### Produits

Les produits Printify existent en **deux versions linguistiques séparées** pour Wanted et Direction :

| Collection | Produits FR | Produits EN | Total | Note |
|------------|:-----------:|:-----------:|:-----:|------|
| Wanted | 138 | 138 | 276 | Titres FR (`T-SHIRT LUFI WANTED`) et EN (`T-SHIRT LUFI WANTED EN`) |
| Direction | 40 | 40 | 80 | Texte intégré dans l'image IA — versions FR et EN séparées |
| Mythologie | 40 | — | 40 | Pas de texte sur le design = universel, une seule version |
| Design Hokuno | 33 | — | 33 | Branding pur, pas de version linguistique |
| **Total** | 251 | 178 | 430* | *Mythologie + Design Hokuno comptés une fois (pas de dédoublement) |

**Conséquence** : les produits FR et EN sont des **produits séparés** dans Shopify (IDs différents, fiches différentes). Ce ne sont PAS des traductions Shopify d'un même produit.

### Textes du thème

Le thème (navbar, footer, boutons, messages) doit être traduit via les fichiers `locales/fr.json` et `locales/en.json`. Shopify utilise le filtre `| t` pour charger la bonne traduction selon la locale active.

---

## 2. STRATÉGIE RETENUE

### Deux niveaux de bilinguisme

| Niveau | Quoi | Comment |
|--------|------|---------|
| **Thème** (UI) | Navbar, boutons, messages, footer | Fichiers `locales/` + filtre `| t` |
| **Produits** (contenu) | Titres, descriptions, backstories | Produits séparés FR et EN + tags `lang-fr` / `lang-en` + filtre collection |

### Shopify Markets pour le thème

La langue de l'UI est gérée par Shopify Markets :
- Visiteur FR/EU → locale `fr` → le thème charge `fr.json`
- Visiteur EN/US/UK → locale `en` → le thème charge `en.json`
- Sélecteur manuel FR/EN dans la navbar (voir `specs/NAVIGATION.md` §7)
- Shopify gère automatiquement la redirection selon la localisation du visiteur

### Tags pour les produits

Les produits Wanted et Direction ont des tags `lang-fr` ou `lang-en` (ajoutés lors de la migration — voir `specs/COLLECTIONS.md` §12).

Le filtre langue sur les pages collection permet au visiteur de n'afficher que les produits de sa langue. Le filtre utilise le tag natif Shopify (voir `specs/COLLECTIONS.md` §6).

---

## 3. FICHIER `locales/fr.json`

```json
{
  "general": {
    "404": {
      "title": "Cette page n'existe pas.",
      "subtitle": "Vous vous êtes perdu ? Le Nord est par là.",
      "back": "RETOUR À L'ACCUEIL"
    }
  },
  "nav": {
    "collections": "COLLECTIONS",
    "new_arrivals": "NOUVEAUTÉS",
    "about": "À PROPOS",
    "journal": "JOURNAL",
    "search": "RECHERCHE",
    "account": "COMPTE",
    "cart": "PANIER"
  },
  "hero": {
    "title_line1": "TOUJOURS",
    "title_line2": "ALLER",
    "title_line3": "DE L'AVANT",
    "cta_primary": "DÉCOUVRIR LA COLLECTION",
    "cta_secondary": "NOUVEAUTÉS",
    "featured_label": "PRODUITS PHARES"
  },
  "trust": {
    "shipping": {
      "label": "Livraison Internationale",
      "sub": "Offerte dès 60€"
    },
    "returns": {
      "label": "Retours Faciles",
      "sub": "30 jours pour changer d'avis"
    },
    "payment": {
      "label": "Paiements Sécurisés",
      "sub": "Cryptés et protégés"
    }
  },
  "home": {
    "collections": {
      "title": "EXPLOREZ NOS UNIVERS",
      "subtitle": "Des collections pensées comme des récits. Inspirées par la culture, le symbole et le mouvement."
    },
    "featured": "PRODUITS PHARES"
  },
  "collections": {
    "discover": "DÉCOUVRIR",
    "products": "produits",
    "sort": {
      "relevance": "Pertinence",
      "price_asc": "Prix croissant",
      "price_desc": "Prix décroissant",
      "newest": "Plus récent",
      "name_az": "Nom A-Z"
    },
    "filters": "FILTRES",
    "filters_apply": "APPLIQUER",
    "filters_reset": "Réinitialiser"
  },
  "product": {
    "color": "Couleur",
    "size": "Taille",
    "add_to_cart": "AJOUTER AU PANIER",
    "sold_out": "ÉPUISÉ",
    "add_to_wishlist": "Ajouter aux favoris",
    "description": "Description",
    "details": "Infos produit",
    "size_guide": "Guide des tailles",
    "size_guide_advice": "Nos t-shirts taillent normalement. En cas de doute, prenez la taille au-dessus.",
    "size_guide_na": "Guide des tailles non disponible pour ce type de produit.",
    "related": "VOUS POURRIEZ AUSSI AIMER",
    "share": "PARTAGER",
    "copy_link": "Copier le lien",
    "badge_shipping": "Livraison internationale — Offerte dès 60€",
    "badge_returns": "Retours faciles — 30 jours",
    "badge_payment": "Paiements sécurisés — Cryptés et protégés",
    "cart_notification": "✓ Ajouté au panier"
  },
  "cart": {
    "title": "PANIER",
    "empty": "Votre panier est vide.",
    "discover": "DÉCOUVRIR NOS COLLECTIONS",
    "subtotal": "Sous-total",
    "checkout": "PASSER LA COMMANDE",
    "shipping_free": "✓ Livraison gratuite !",
    "shipping_remaining": "Plus que {{ amount }} pour la livraison gratuite !"
  },
  "breadcrumbs": {
    "home": "Accueil"
  },
  "pagination": {
    "previous": "Précédent",
    "next": "Suivant"
  },
  "blog": {
    "read_more": "Lire la suite",
    "previous": "Article précédent",
    "next": "Article suivant"
  },
  "contact": {
    "name": "Nom",
    "email": "Email",
    "message": "Message",
    "send": "ENVOYER",
    "success": "✓ Message envoyé ! Nous vous répondons sous 24-48h."
  },
  "customer": {
    "login": {
      "title": "CONNEXION",
      "email": "Email",
      "password": "Mot de passe",
      "submit": "SE CONNECTER",
      "no_account": "Pas encore de compte ?",
      "create_account": "Créer un compte",
      "forgot_password": "Mot de passe oublié ?"
    },
    "register": {
      "title": "CRÉER UN COMPTE",
      "first_name": "Prénom",
      "last_name": "Nom",
      "email": "Email",
      "password": "Mot de passe",
      "submit": "CRÉER MON COMPTE"
    },
    "account": {
      "title": "MON COMPTE",
      "orders": "Historique des commandes",
      "logout": "SE DÉCONNECTER"
    },
    "recover": {
      "title": "MOT DE PASSE OUBLIÉ",
      "subtitle": "Entrez votre adresse email, nous vous enverrons un lien de réinitialisation.",
      "submit": "ENVOYER LE LIEN",
      "back_to_login": "Retour à la connexion"
    }
  },
  "footer": {
    "tagline": "ホクノ — Toujours aller de l'avant",
    "col_collections": "Collections",
    "col_information": "Information",
    "col_legal": "Légal",
    "newsletter": {
      "text": "Rejoignez l'équipage — 15% sur votre première commande",
      "placeholder": "Votre adresse email",
      "submit": "S'INSCRIRE",
      "success": "✓ Inscrit ! Vérifiez votre boîte mail."
    },
    "copyright": "© 2026 HOKUNO. Tous droits réservés."
  },
  "gift_cards": {
    "title": "Carte cadeau",
    "expires": "Expire le",
    "no_expiry": "Pas de date d'expiration",
    "shop_now": "ACHETER MAINTENANT"
  },
  "cookie": {
    "text": "Ce site utilise des cookies pour améliorer votre expérience et mesurer l'audience.",
    "learn_more": "En savoir plus",
    "accept": "Accepter",
    "refuse": "Refuser"
  },
  "search": {
    "title": "RECHERCHE",
    "placeholder": "Rechercher un produit, une collection...",
    "submit": "RECHERCHER",
    "results": "{{ count }} résultats pour \"{{ terms }}\"",
    "no_results": "Aucun résultat pour \"{{ terms }}\".",
    "no_results_suggestion": "Essayez un autre mot-clé ou explorez nos collections."
  }
}
```

---

## 4. FICHIER `locales/en.json`

```json
{
  "general": {
    "404": {
      "title": "This page doesn't exist.",
      "subtitle": "Lost? North is this way.",
      "back": "BACK TO HOME"
    }
  },
  "nav": {
    "collections": "COLLECTIONS",
    "new_arrivals": "NEW ARRIVALS",
    "about": "ABOUT",
    "journal": "JOURNAL",
    "search": "SEARCH",
    "account": "ACCOUNT",
    "cart": "CART"
  },
  "hero": {
    "title_line1": "ALWAYS",
    "title_line2": "MOVING",
    "title_line3": "FORWARD",
    "cta_primary": "DISCOVER THE COLLECTION",
    "cta_secondary": "NEW ARRIVALS",
    "featured_label": "FEATURED PRODUCTS"
  },
  "trust": {
    "shipping": {
      "label": "International Shipping",
      "sub": "Free from €60"
    },
    "returns": {
      "label": "Easy Returns",
      "sub": "30 days to change your mind"
    },
    "payment": {
      "label": "Secure Payments",
      "sub": "Encrypted and protected"
    }
  },
  "home": {
    "collections": {
      "title": "EXPLORE OUR WORLDS",
      "subtitle": "Collections designed as stories. Inspired by culture, symbolism and movement."
    },
    "featured": "FEATURED PRODUCTS"
  },
  "collections": {
    "discover": "DISCOVER",
    "products": "products",
    "sort": {
      "relevance": "Relevance",
      "price_asc": "Price: Low to High",
      "price_desc": "Price: High to Low",
      "newest": "Newest",
      "name_az": "Name A-Z"
    },
    "filters": "FILTERS",
    "filters_apply": "APPLY",
    "filters_reset": "Reset"
  },
  "product": {
    "color": "Color",
    "size": "Size",
    "add_to_cart": "ADD TO CART",
    "sold_out": "SOLD OUT",
    "add_to_wishlist": "Add to wishlist",
    "description": "Description",
    "details": "Product details",
    "size_guide": "Size guide",
    "size_guide_advice": "Our t-shirts have a regular fit. When in doubt, size up.",
    "size_guide_na": "Size guide not available for this product type.",
    "related": "YOU MIGHT ALSO LIKE",
    "share": "SHARE",
    "copy_link": "Copy link",
    "badge_shipping": "International shipping — Free from €60",
    "badge_returns": "Easy returns — 30 days",
    "badge_payment": "Secure payments — Encrypted and protected",
    "cart_notification": "✓ Added to cart"
  },
  "cart": {
    "title": "CART",
    "empty": "Your cart is empty.",
    "discover": "DISCOVER OUR COLLECTIONS",
    "subtotal": "Subtotal",
    "checkout": "PROCEED TO CHECKOUT",
    "shipping_free": "✓ Free shipping!",
    "shipping_remaining": "Only {{ amount }} more for free shipping!"
  },
  "breadcrumbs": {
    "home": "Home"
  },
  "pagination": {
    "previous": "Previous",
    "next": "Next"
  },
  "blog": {
    "read_more": "Read more",
    "previous": "Previous article",
    "next": "Next article"
  },
  "contact": {
    "name": "Name",
    "email": "Email",
    "message": "Message",
    "send": "SEND",
    "success": "✓ Message sent! We'll reply within 24-48h."
  },
  "customer": {
    "login": {
      "title": "LOGIN",
      "email": "Email",
      "password": "Password",
      "submit": "LOG IN",
      "no_account": "Don't have an account?",
      "create_account": "Create account",
      "forgot_password": "Forgot password?"
    },
    "register": {
      "title": "CREATE ACCOUNT",
      "first_name": "First name",
      "last_name": "Last name",
      "email": "Email",
      "password": "Password",
      "submit": "CREATE MY ACCOUNT"
    },
    "account": {
      "title": "MY ACCOUNT",
      "orders": "Order history",
      "logout": "LOG OUT"
    },
    "recover": {
      "title": "FORGOT PASSWORD",
      "subtitle": "Enter your email address and we'll send you a reset link.",
      "submit": "SEND RESET LINK",
      "back_to_login": "Back to login"
    }
  },
  "footer": {
    "tagline": "ホクノ — Always moving forward",
    "col_collections": "Collections",
    "col_information": "Information",
    "col_legal": "Legal",
    "newsletter": {
      "text": "Join the crew — 15% off your first order",
      "placeholder": "Your email address",
      "submit": "SUBSCRIBE",
      "success": "✓ Subscribed! Check your inbox."
    },
    "copyright": "© 2026 HOKUNO. All rights reserved."
  },
  "gift_cards": {
    "title": "Gift card",
    "expires": "Expires on",
    "no_expiry": "No expiration date",
    "shop_now": "SHOP NOW"
  },
  "cookie": {
    "text": "This site uses cookies to improve your experience and measure audience.",
    "learn_more": "Learn more",
    "accept": "Accept",
    "refuse": "Refuse"
  },
  "search": {
    "title": "SEARCH",
    "placeholder": "Search for a product, a collection...",
    "submit": "SEARCH",
    "results": "{{ count }} results for \"{{ terms }}\"",
    "no_results": "No results for \"{{ terms }}\".",
    "no_results_suggestion": "Try another keyword or explore our collections."
  }
}
```

---

## 5. UTILISATION DANS LE LIQUID

### Principe

Tous les textes affichés dans le thème utilisent le filtre `| t` :

```liquid
<!-- Au lieu de : -->
<h1>TOUJOURS ALLER DE L'AVANT</h1>

<!-- Écrire : -->
<h1>{{ 'hero.title_line1' | t }}<br>{{ 'hero.title_line2' | t }}<br>{{ 'hero.title_line3' | t }}</h1>
```

### Textes avec variables

```liquid
<!-- Résultats de recherche -->
<p>{{ 'search.results' | t: count: search.results_count, terms: search.terms }}</p>

<!-- Livraison gratuite restante -->
<p>{{ 'cart.shipping_remaining' | t: amount: remaining | money }}</p>
```

### Règle stricte

**Aucun texte en dur dans le HTML Liquid.** Tout passe par `| t`. Ceci inclut :
- Les labels de navigation
- Les boutons
- Les messages (panier vide, 404, etc.)
- Les textes d'accroche (hero, collections)
- Les labels de formulaires
- Le footer
- La bannière cookies

Exceptions autorisées :
- Le katakana `ホクノ` — identique dans toutes les langues
- Les noms de collections (Wanted, Direction, Mythologie) — tirés de `{{ collection.title }}`
- Les coordonnées Tokyo dans le hero (`35.6895°N, 139.6917°E`) — décoratif

---

## 6. GESTION DES PRODUITS BILINGUES

### Problème

Les produits FR et EN sont des produits Shopify **séparés**. Un visiteur anglophone qui navigue sur `/collections/wanted` voit les 277 produits mélangés (FR + EN + Mythologie universelle).

### Solution : filtre par langue

Détaillée dans `specs/COLLECTIONS.md` §6.

1. Les produits Wanted et Direction ont un tag `lang-fr` ou `lang-en`
2. Les produits Mythologie et Design Hokuno n'ont pas de tag langue (universels)
3. Le filtre "Langue" sur les pages collection permet de filtrer FR ou EN
4. Par défaut (sans filtre) : tous les produits sont affichés

### Auto-filtre par locale (v2)

En v2, on pourra auto-filtrer les produits selon la locale active du visiteur :

```liquid
{% if request.locale.iso_code == 'en' %}
  {% comment %} Filtrer automatiquement les produits EN {% endcomment %}
  {% assign filtered_products = collection.products | where: 'tags', 'lang-en' %}
{% else %}
  {% assign filtered_products = collection.products | where: 'tags', 'lang-fr' %}
{% endif %}
```

> Note : le filtre `where` sur les tags n'est pas natif Liquid Shopify. L'auto-filtre nécessitera du JS ou un paramètre URL. Pour la v1, le filtre manuel suffit.

### Titres et descriptions produits

Les titres et descriptions des produits sont en français pour les produits FR et en anglais pour les produits EN. Ils ne sont PAS traduits via Shopify Markets — ce sont des fiches produit différentes.

Shopify Markets traduit les textes du **thème** (via `locales/`), pas le contenu des produits. C'est pour ça que les produits existent en double.

---

## 7. PAGES STATIQUES BILINGUES

### Méthode

Les pages statiques (about, FAQ, contact) ont leur contenu dans Shopify Admin. Shopify Markets permet de stocker une version traduite par langue.

Shopify Admin → Pages → [page] → dans la barre latérale, changer de langue et rédiger la version EN.

Les contenus FR et EN sont définis dans `specs/PAGES.md` §3 (about), §4 (FAQ), §5 (contact).

### Blog

Les articles du blog peuvent être rédigés en FR et en EN. Deux approches :
- **Un article par langue** (ex : "L'histoire de Wanted" FR + "The Story of Wanted" EN) — plus simple
- **Un article bilingue** avec Shopify Markets — Shopify affiche la bonne version selon la locale

Pour le lancement, un article par langue est suffisant.

---

## 8. CONFIGURATION SHOPIFY MARKETS — RÉSUMÉ

Détail dans `specs/CONFIG-SHOPIFY.md` §8.

| Action | Où |
|--------|-----|
| Ajouter la langue English (en) | Settings → Languages → Add language → English |
| Publier la langue | Settings → Languages → English → Publish |
| Upload fr.json et en.json | Dans le thème `shopify-theme/locales/` puis push |
| Configurer le marché FR+EU | Settings → Markets → Primary → langue FR, devise EUR |
| Configurer le marché International | Settings → Markets → International → langue EN, devise USD |
| Traduire les pages statiques | Pages → [page] → changer de langue → rédiger EN |
| Traduire les descriptions collections | Collections → [collection] → changer de langue → description EN |
| Traduire les policies | Settings → Policies → changer de langue → rédiger EN |

---

## 9. RÉCAPITULATIF DES CLÉS DE TRADUCTION

| Groupe | Clés | Sections du thème |
|--------|:----:|-------------------|
| `general` | 3 | Page 404 |
| `nav` | 7 | Navbar desktop + mobile |
| `hero` | 6 | Hero page d'accueil |
| `trust` | 6 | Barre de confiance |
| `home` | 3 | Sections accueil |
| `collections` | 9 | Pages collection, filtres, tri |
| `product` | 17 | Page produit |
| `cart` | 7 | Page panier |
| `breadcrumbs` | 1 | Fil d'Ariane |
| `pagination` | 2 | Navigation pages |
| `blog` | 3 | Blog et articles |
| `contact` | 5 | Page contact |
| `customer` | 16 | Login, register, account, recover |
| `footer` | 8 | Footer + newsletter |
| `gift_cards` | 4 | Carte cadeau |
| `cookie` | 4 | Bannière cookies |
| `search` | 6 | Page recherche |
| **Total** | **107** | |

107 clés de traduction, toutes avec leur valeur FR et EN.
