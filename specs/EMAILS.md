# specs/EMAILS.md — Emails transactionnels & newsletter

> Contrat pour Claude Code / toi. Chaque email envoyé par la boutique est défini ici.
> Configuration dans Shopify Admin → Settings → Notifications.
> Référence croisée : `specs/CONFIG-SHOPIFY.md` §10, `specs/NAVIGATION.md` §5 (newsletter footer).

---

## 1. BRANDING EMAIL — TEMPLATE GLOBAL

Tous les emails Shopify partagent le même template visuel. Configurer dans Shopify Admin → Settings → Notifications → Customer notifications → Customize email templates.

### Paramètres visuels

| Élément | Valeur |
|---------|--------|
| Logo | `logo-hokuno-nav.png` (upload dans la config) |
| Largeur logo | `120px` |
| Couleur accent | `#D4A853` (doré — boutons, liens, highlights) |
| Couleur de fond body | `#000000` |
| Couleur de fond contenu | `#111111` |
| Couleur texte principal | `#FFFFFF` |
| Couleur texte secondaire | `#999999` |
| Couleur liens | `#D4A853` |
| Couleur boutons (fond) | `#D4A853` |
| Couleur boutons (texte) | `#000000` |
| Police | Par défaut Shopify (pas de font custom dans les emails) |

### Structure de chaque email

```
┌──────────────────────────────────┐
│         [LOGO HOKUNO]            │  fond #000000
│                                  │
├──────────────────────────────────┤
│                                  │
│  Titre de l'email                │  fond #111111
│  Contenu personnalisé            │  texte #FFFFFF
│                                  │  liens/accents #D4A853
│  [BOUTON CTA]                    │  bouton doré
│                                  │
├──────────────────────────────────┤
│  ホクノ — Toujours aller         │  fond #000000
│  de l'avant                      │  texte #666666
│  altidigitech@gmail.com          │
└──────────────────────────────────┘
```

### Footer email (tous les emails)

```
ホクノ — Toujours aller de l'avant
HOKUNO — {{ shop.url }}
altidigitech@gmail.com
```

---

## 2. EMAILS TRANSACTIONNELS

Shopify Admin → Settings → Notifications → Customer notifications

### 2.1 Confirmation de commande

**Trigger** : commande passée et payée
**Objet FR** : `Commande confirmée — HOKUNO #{{ order.name }}`
**Objet EN** : `Order confirmed — HOKUNO #{{ order.name }}`

**Message personnalisé (ajout en haut du template)** :

FR :
```
Merci pour votre commande ! 🎌

Votre produit est fabriqué spécialement pour vous — chaque pièce est unique, imprimée à la commande.

Délai estimé : 3-7 jours de fabrication + livraison selon votre destination. Vous recevrez un email avec votre numéro de suivi dès l'expédition.
```

EN :
```
Thank you for your order! 🎌

Your product is being made just for you — each piece is unique, printed on demand.

Estimated timeline: 3-7 business days for production + shipping based on your location. You'll receive a tracking email once shipped.
```

---

### 2.2 Expédition envoyée

**Trigger** : Printify expédie la commande et fournit le tracking
**Objet FR** : `Votre commande HOKUNO est en route ! #{{ order.name }}`
**Objet EN** : `Your HOKUNO order is on its way! #{{ order.name }}`

**Message personnalisé** :

FR :
```
Bonne nouvelle — votre commande a été expédiée ! 📦

Suivez votre colis avec le numéro de suivi ci-dessous. Les délais de livraison varient selon votre destination :
• France / EU : 5-10 jours ouvrés
• USA : 3-7 jours ouvrés
• International : 7-15 jours ouvrés

Merci de votre patience — ça vaut l'attente.
```

EN :
```
Great news — your order has shipped! 📦

Track your package with the tracking number below. Delivery times vary by destination:
• France / EU: 5-10 business days
• USA: 3-7 business days
• International: 7-15 business days

Thank you for your patience — it's worth the wait.
```

---

### 2.3 Livraison effectuée

**Trigger** : transporteur confirme la livraison
**Objet FR** : `Votre commande HOKUNO est arrivée ! #{{ order.name }}`
**Objet EN** : `Your HOKUNO order has arrived! #{{ order.name }}`

**Message personnalisé** :

FR :
```
Votre commande est arrivée — on espère que vous allez l'adorer ! 🙌

Vous avez 2 minutes ? Laissez-nous un avis sur le produit. Ça nous aide énormément et ça aide les prochains clients à choisir.

Un problème avec votre commande ? Contactez-nous à altidigitech@gmail.com — on s'occupe de tout.
```

EN :
```
Your order has arrived — we hope you love it! 🙌

Got 2 minutes? Leave us a review on the product. It helps us a lot and helps future customers choose.

Any issue with your order? Contact us at altidigitech@gmail.com — we'll take care of everything.
```

---

### 2.4 Panier abandonné

**Trigger** : client ajoute au panier, commence le checkout, ne finalise pas (après ~1h ou ~10h selon config Shopify)
**Objet FR** : `Vous avez oublié quelque chose — HOKUNO`
**Objet EN** : `You forgot something — HOKUNO`

**Message personnalisé** :

FR :
```
Votre panier vous attend. 

Le produit que vous avez choisi est toujours disponible — mais il est fabriqué à la commande, chaque pièce est unique.

Finalisez votre commande avant qu'on change d'avis. 😏
```

EN :
```
Your cart is waiting.

The product you chose is still available — but it's made to order, each piece is unique.

Complete your order before we change our mind. 😏
```

**CTA** : bouton "FINALISER MA COMMANDE" / "COMPLETE MY ORDER" — lien vers le checkout abandonné

> Note : Shopify inclut automatiquement l'image du produit et le lien de récupération du checkout dans l'email de panier abandonné.

**Configuration** : Shopify Admin → Settings → Checkout → Abandoned checkouts → Activer "Automatically send abandoned checkout emails" → Délai : 10 hours (recommandé).

---

### 2.5 Création de compte

**Trigger** : client crée un compte sur le site
**Objet FR** : `Bienvenue dans l'équipage — HOKUNO ホクノ`
**Objet EN** : `Welcome aboard — HOKUNO ホクノ`

**Message personnalisé** :

FR :
```
Bienvenue chez Hokuno ! 🎌

Vous faites maintenant partie de l'équipage. Explorez nos collections et trouvez le design qui vous parle.

Pour célébrer, voici un code exclusif :

HOKUNO15 → -15% sur votre première commande

Valable 2 semaines. Utilisez-le au checkout.

Toujours aller de l'avant.
ホクノ
```

EN :
```
Welcome to Hokuno! 🎌

You're now part of the crew. Explore our collections and find the design that speaks to you.

To celebrate, here's an exclusive code:

HOKUNO15 → 15% off your first order

Valid for 2 weeks. Use it at checkout.

Always moving forward.
ホクノ
```

**CTA** : bouton "DÉCOUVRIR LES COLLECTIONS" / "EXPLORE COLLECTIONS" → `/collections`

---

### 2.6 Réinitialisation mot de passe

**Trigger** : client demande une réinitialisation de mot de passe
**Objet FR** : `Réinitialiser votre mot de passe — HOKUNO`
**Objet EN** : `Reset your password — HOKUNO`

**Message** : template Shopify par défaut avec le branding Hokuno (logo + couleurs). Pas de personnalisation du texte nécessaire — Shopify gère le lien de réinitialisation.

---

### 2.7 Confirmation de remboursement

**Trigger** : remboursement émis
**Objet FR** : `Remboursement émis — HOKUNO #{{ order.name }}`
**Objet EN** : `Refund issued — HOKUNO #{{ order.name }}`

**Message personnalisé** :

FR :
```
Votre remboursement a été traité. Le montant sera crédité sur votre moyen de paiement sous 5-10 jours ouvrés selon votre banque.

Désolé que ça n'ait pas marché cette fois. On espère vous revoir bientôt.

Une question ? altidigitech@gmail.com
```

---

## 3. NEWSLETTER

### Formulaire dans le footer

Détail complet dans `specs/NAVIGATION.md` §5.

- Position : sous la grille footer, séparé visuellement
- Texte d'accroche : "Rejoignez l'équipage — 15% sur votre première commande"
- Champ : email
- Bouton : "S'INSCRIRE" (`.btn-gold`)
- Snippet : `{% render 'newsletter-form' %}`

### Implémentation Liquid

```liquid
<!-- snippets/newsletter-form.liquid -->
<div class="newsletter">
  <p class="newsletter-text">{{ 'footer.newsletter.text' | t }}</p>
  {% form 'customer', id: 'newsletter-form' %}
    {{ form.errors | default_errors }}
    <input type="hidden" name="contact[tags]" value="newsletter">
    <div class="newsletter-row">
      <input type="email"
             name="contact[email]"
             class="newsletter-input"
             placeholder="{{ 'footer.newsletter.placeholder' | t }}"
             required
             autocomplete="email">
      <button type="submit" class="btn-gold newsletter-btn">
        {{ 'footer.newsletter.submit' | t }}
      </button>
    </div>
    {% if form.posted_successfully? %}
      <p class="newsletter-success">{{ 'footer.newsletter.success' | t }}</p>
    {% endif %}
  {% endform %}
</div>
```

Textes de traduction :
- `footer.newsletter.text` : "Rejoignez l'équipage — 15% sur votre première commande" / "Join the crew — 15% off your first order"
- `footer.newsletter.placeholder` : "Votre adresse email" / "Your email address"
- `footer.newsletter.submit` : "S'INSCRIRE" / "SUBSCRIBE"
- `footer.newsletter.success` : "✓ Inscrit ! Vérifiez votre boîte mail." / "✓ Subscribed! Check your inbox."

### Outil newsletter

**Shopify Email** (recommandé pour le lancement) :
- Inclus dans Shopify (1000 emails/mois gratuits, puis 0.001$/email)
- Accès : Shopify Admin → Marketing → Campaigns → Shopify Email
- Utilise la liste des clients avec le tag `newsletter`
- Templates email personnalisables avec le branding Hokuno

**Alternative (si besoin de plus de fonctionnalités)** :
- Klaviyo : segmentation avancée, automations, analytics — gratuit jusqu'à 250 contacts
- Mailchimp : plus simple, intégration Shopify native — gratuit jusqu'à 500 contacts

### Email de bienvenue newsletter

Créer un email de bienvenue automatique envoyé à l'inscription :

**Objet FR** : `Bienvenue chez Hokuno — Voici votre code -15% 🎌`
**Objet EN** : `Welcome to Hokuno — Here's your 15% off code 🎌`

**Contenu** :

```
Bienvenue dans l'équipage Hokuno !

Comme promis, voici votre code de réduction :

━━━━━━━━━━━━━━━━━━━━━
    HOKUNO15
    -15% sur votre commande
━━━━━━━━━━━━━━━━━━━━━

Valable 2 semaines sur toute la boutique.

→ Nos collections :
• Wanted — Avis de recherche revisités
• Direction — Silhouettes & citations
• Mythologie — Divinités en couleurs
• Design Hokuno — Le branding pur

[DÉCOUVRIR LA BOUTIQUE]

Toujours aller de l'avant.
ホクノ
```

**Configuration** : créer cette automation dans Shopify Email ou Klaviyo. Trigger : client ajouté avec tag `newsletter`.

---

## 4. PERSONNALISATION DES TEMPLATES SHOPIFY

### Comment modifier les templates email

Shopify Admin → Settings → Notifications → Cliquer sur une notification → Customize email template

Les templates utilisent du HTML + Liquid. Les variables disponibles :

| Variable | Contenu |
|----------|---------|
| `{{ shop.name }}` | HOKUNO |
| `{{ shop.url }}` | URL de la boutique |
| `{{ order.name }}` | Numéro de commande (#1001, etc.) |
| `{{ customer.first_name }}` | Prénom du client |
| `{{ order.total_price \| money }}` | Total de la commande |
| `{{ order.shipping_address.city }}` | Ville de livraison |
| `{{ fulfillment.tracking_url }}` | Lien de suivi |

### Ajout de contenu personnalisé

Pour chaque notification, Shopify offre un champ "Additional text" ou une zone éditable. Y coller les messages personnalisés de la section 2 ci-dessus.

Pour une personnalisation plus profonde (modifier le HTML complet), cliquer "Edit code" sur chaque template de notification.

### Personnalisation CSS inline

Les emails ne supportent pas les fichiers CSS externes. Tout le style est en inline. Le template Shopify par défaut utilise les couleurs configurées dans la section branding (section 1). Pour des ajustements :

```html
<!-- Exemple : ajouter le katakana dans le footer de l'email -->
<tr>
  <td style="text-align:center; padding:20px; color:#D4A853; font-size:18px; letter-spacing:4px;">
    ホクノ
  </td>
</tr>
<tr>
  <td style="text-align:center; padding:0 0 20px; color:#666666; font-size:12px;">
    Toujours aller de l'avant — <a href="{{ shop.url }}" style="color:#D4A853;">hokuno.com</a>
  </td>
</tr>
```

---

## 5. RÉCAPITULATIF DES EMAILS

| Email | Trigger | Objet FR | Personnalisé ? |
|-------|---------|----------|:--------------:|
| Confirmation commande | Commande payée | `Commande confirmée — HOKUNO #...` | ✅ |
| Expédition | Colis expédié | `Votre commande est en route !` | ✅ |
| Livraison | Colis livré | `Votre commande est arrivée !` | ✅ |
| Panier abandonné | Checkout non finalisé (~10h) | `Vous avez oublié quelque chose` | ✅ |
| Création compte | Compte créé | `Bienvenue dans l'équipage` | ✅ Code HOKUNO15 |
| Réinitialisation MDP | Demande de reset | `Réinitialiser votre mot de passe` | Branding seulement |
| Remboursement | Remboursement émis | `Remboursement émis` | ✅ |
| Newsletter bienvenue | Inscription newsletter | `Voici votre code -15%` | ✅ Code HOKUNO15 |

### Ton des emails

Cohérent avec le brand (voir `CONTEXT.md` → Ton & Voix) :
- Décalé et intelligent, jamais vulgaire
- Le tutoiement n'est PAS utilisé (vouvoiement)
- Pas d'excès d'emojis (1-2 max par email)
- Référence subtile au manga/aventure ("équipage", pas "équipe")
- Signature : `ホクノ — Toujours aller de l'avant`

---

## 6. ORDRE DE CONFIGURATION

| # | Action | Où |
|---|--------|-----|
| 1 | Configurer le branding email (logo, couleurs) | Settings → Notifications → Customize |
| 2 | Personnaliser "Confirmation de commande" | Settings → Notifications → Order confirmation |
| 3 | Personnaliser "Expédition envoyée" | Settings → Notifications → Shipping confirmation |
| 4 | Personnaliser "Livraison effectuée" | Settings → Notifications → Delivered |
| 5 | Activer et personnaliser "Panier abandonné" | Settings → Checkout → Abandoned checkouts |
| 6 | Personnaliser "Création de compte" | Settings → Notifications → Customer account welcome |
| 7 | Personnaliser "Remboursement" | Settings → Notifications → Refund |
| 8 | Créer l'email de bienvenue newsletter | Marketing → Shopify Email ou Klaviyo |
| 9 | Tester chaque email (commande test) | Effectuer une commande réelle puis annuler |
