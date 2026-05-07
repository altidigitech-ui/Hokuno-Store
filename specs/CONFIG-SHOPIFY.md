# specs/CONFIG-SHOPIFY.md — Configuration Shopify

> Contrat pour Claude Code / toi. Chaque paramètre de la boutique Shopify est défini ici.
> À configurer dans Shopify Admin → Settings après la publication des produits et du thème.
> Référence croisée : `specs/MIGRATION.md` Phase 7.

---

## 1. INFORMATIONS GÉNÉRALES

Shopify Admin → Settings → Store details

| Paramètre | Valeur |
|-----------|--------|
| Nom du store | `HOKUNO` |
| Email du store | `altidigitech@gmail.com` |
| Email expéditeur | `altidigitech@gmail.com` (ou `contact@hokuno.com` si domaine custom configuré) |
| Secteur d'activité | Clothing & Accessories |
| Adresse | Adresse du siège social (requise pour facturation et mentions légales) |
| Téléphone | Optionnel — ne pas afficher publiquement si auto-entrepreneur |
| Fuseau horaire | `(GMT+01:00) Paris` |
| Système d'unités | Métrique |

---

## 2. LANGUE ET LOCALISATION

### Langue par défaut

Shopify Admin → Settings → Languages

| Paramètre | Valeur |
|-----------|--------|
| Langue par défaut | Français (fr) |
| Langues publiées | Français (fr) + Anglais (en) |

Les traductions du thème sont dans `locales/fr.json` et `locales/en.json` (voir `specs/MULTILINGUE.md`).

### Format de date

| Format | Valeur |
|--------|--------|
| Date | `DD/MM/YYYY` (format français) |
| Heure | `HH:MM` (24h) |

---

## 3. DEVISE

Shopify Admin → Settings → Markets → Pricing

| Paramètre | Valeur |
|-----------|--------|
| Devise principale | **EUR (€)** |
| Devises activées | EUR, USD, GBP, CAD, AUD |
| Taux de conversion | Automatique (Shopify Exchange Rates) |
| Arrondi | Au centime (0.01) |

### Prix par devise

Les prix sont définis en USD dans Printify. Shopify convertit automatiquement selon la devise du client. Les prix affichés sont :

| Produit | Prix EUR (€) | Prix USD ($) | Prix GBP (£) |
|---------|:------------:|:------------:|:------------:|
| T-shirt | 34.99 | 37.99 | ~30.99 |
| Mug 11oz | 29.99 | 19.99 | ~16.99 |
| Mug 15oz | 34.99 | 24.99 | ~20.99 |
| Mug noir | 34.99 | 24.99 | ~20.99 |
| Coque | 24.99 | 24.99 | ~20.99 |

> Note : les prix GBP, CAD, AUD sont convertis automatiquement depuis EUR par Shopify. Pour fixer manuellement les prix par marché, utiliser Shopify Markets → Pricing adjustments.

---

## 4. PAIEMENTS

Shopify Admin → Settings → Payments

### Shopify Payments (principal)

| Méthode | Statut |
|---------|--------|
| Cartes bancaires (Visa, Mastercard, Amex, CB) | ✅ Activer |
| Apple Pay | ✅ Activer |
| Google Pay | ✅ Activer |
| Shop Pay | ✅ Activer |
| Shopify Installments (paiement en 4x) | Optionnel — activer si disponible en France |

### Configuration Shopify Payments

| Paramètre | Valeur |
|-----------|--------|
| Pays du compte | France |
| Devise de règlement | EUR |
| Relevé bancaire | `HOKUNO` (ce qui apparaît sur le relevé du client) |
| Capture des paiements | Automatique (au moment de la commande) |

### Fournisseurs tiers

| Fournisseur | Statut |
|-------------|--------|
| PayPal | ✅ Activer (optionnel mais recommandé — couvre les clients sans CB) |
| Autres (Klarna, etc.) | Non nécessaire pour le lancement |

### Mode test

Activer le mode test de Shopify Payments pendant la Phase 9 (vérification) pour tester le flow de commande sans transaction réelle.

---

## 5. LIVRAISON

Shopify Admin → Settings → Shipping and delivery

### Stratégie

La livraison est gérée par Printify — les tarifs réels sont ceux des print providers. Shopify doit être configuré pour afficher ces tarifs au checkout.

### Option recommandée : Printify Shipping Profiles

Quand Printify est connecté via l'app Shopify, il crée automatiquement des profils de livraison (shipping profiles) pour les produits Printify. Les tarifs sont calculés par Printify au checkout.

**Vérifier** que les profils Printify sont actifs : Shopify Admin → Settings → Shipping → Shipping profiles → Les produits Printify doivent apparaître dans un profil géré par Printify.

### Livraison gratuite dès 60€

Ajouter une règle de livraison gratuite :

| Paramètre | Valeur |
|-----------|--------|
| Nom | Livraison gratuite |
| Condition | Montant de la commande ≥ 60€ |
| Zones | Toutes les zones |
| Tarif | 0€ |

**Configurer dans** : Shopify Admin → Settings → Shipping → Shipping profiles → General shipping rates → Chaque zone → Add rate → "Free shipping" → Price based condition → Minimum order subtotal: 60.

### Zones de livraison

| Zone | Pays | Tarif standard (1er t-shirt) | Livraison gratuite |
|------|------|------------------------------|-------------------|
| France | France | ~9.20€ (10.00$) | Dès 60€ |
| EU | Allemagne, Belgique, Espagne, Italie, Pays-Bas, etc. | ~9.20€ | Dès 60€ |
| UK | Royaume-Uni | ~9.20€ | Dès 60€ |
| USA | États-Unis | ~7.35$ (Printify direct) | Dès $65 (~60€) |
| Canada | Canada | ~8.64$ | Dès $65 |
| Australie | Australie | ~11.49$ | Dès $65 |
| Reste du monde | Tous les autres pays | ~9.20€ | Dès 60€ |

> Note : les tarifs exacts sont ceux de Printify, qui varient par produit et provider. Le seuil de livraison gratuite est 60€ pour tous les marchés EUR et ~$65 pour les marchés USD (conversion approximative).

### Délais de livraison affichés

| Zone | Fabrication | Livraison | Total estimé |
|------|-------------|-----------|-------------|
| France / EU | 3-7 jours ouvrés | 5-10 jours ouvrés | 8-17 jours ouvrés |
| USA | 3-7 jours ouvrés | 3-7 jours ouvrés | 6-14 jours ouvrés |
| Canada | 3-7 jours ouvrés | 5-12 jours ouvrés | 8-19 jours ouvrés |
| Australie | 3-7 jours ouvrés | 7-15 jours ouvrés | 10-22 jours ouvrés |
| International | 3-7 jours ouvrés | 7-21 jours ouvrés | 10-28 jours ouvrés |

---

## 6. TAXES

Shopify Admin → Settings → Taxes and duties

| Paramètre | Valeur |
|-----------|--------|
| Région de collecte | France |
| TVA | Incluse dans les prix (toggle ON) |
| Taux TVA France | 20% (configuré automatiquement par Shopify) |
| TVA EU | Shopify gère automatiquement les taux par pays EU |
| US Sales Tax | Calculé automatiquement par Shopify selon l'état |
| Droits de douane | Non applicable pour la plupart des commandes (Printify gère) |

**Important** : activer "All prices include tax" pour que les prix affichés (34.99€) soient TTC. Sinon Shopify ajoute la TVA au checkout, ce qui surprend le client.

---

## 7. CODE PROMO

Shopify Admin → Discounts → Create discount

### HOKUNO15 — Remise de lancement

| Paramètre | Valeur |
|-----------|--------|
| Code | `HOKUNO15` |
| Type | Pourcentage |
| Valeur | -15% |
| Utilisation | Illimitée (pas de limite d'utilisation totale) |
| Usage par client | 1 fois par client |
| Minimum d'achat | Aucun |
| Produits éligibles | Tous les produits SAUF les coques |
| Date de début | Jour du lancement |
| Date de fin | 14 jours après le lancement |
| Combiner avec d'autres codes | Non |

### Exclure les coques du code promo

Les coques iPhone ont une marge EU de 2.39€ seulement. Avec -15%, la marge devient **-1.36€** (perte).

Pour exclure les coques dans Shopify :
1. Créer le discount → "Specific products" au lieu de "All products"
2. Sélectionner toutes les collections SAUF les coques
3. Ou utiliser "Specific collections" : Wanted, Direction, Mythologie, Design Hokuno → puis exclure les coques manuellement si le filtre par type n'est pas disponible

Alternative : créer une collection cachée "Promo eligible" avec tous les produits sauf les coques, et appliquer le code à cette collection.

---

## 8. SHOPIFY MARKETS

Shopify Admin → Settings → Markets

### Marché principal — France + EU

| Paramètre | Valeur |
|-----------|--------|
| Nom | France & Union Européenne |
| Pays | France, Belgique, Allemagne, Espagne, Italie, Pays-Bas, Portugal, Autriche, Suisse, Luxembourg |
| Langue | Français (fr) |
| Devise | EUR (€) |
| Domaine | `hokuno.com` ou `hokuno.fr` (une fois acheté) |
| Tarification | Prix de base (pas d'ajustement) |

### Marché international — Anglophone

| Paramètre | Valeur |
|-----------|--------|
| Nom | International |
| Pays | États-Unis, Canada, Royaume-Uni, Australie, Irlande, Nouvelle-Zélande |
| Langue | English (en) |
| Devise | USD ($) pour USA/CA, GBP (£) pour UK, AUD ($) pour AU |
| Domaine | Sous-chemin `/en` (ex : `hokuno.com/en`) |
| Tarification | Ajustement possible pour aligner sur les prix EN de `PRICING.md` |

### Marché reste du monde

| Paramètre | Valeur |
|-----------|--------|
| Nom | Reste du monde |
| Pays | Tous les autres |
| Langue | English (en) par défaut |
| Devise | USD ($) |

### Redirection automatique

Shopify Markets détecte la localisation du visiteur et propose automatiquement la bonne langue/devise. Configurer :
- Popup de redirection : "Il semble que vous êtes en [pays]. Voulez-vous voir le site en [langue] avec les prix en [devise] ?"
- Ne PAS forcer la redirection sans consentement

---

## 9. CHECKOUT

Shopify Admin → Settings → Checkout

### Branding

| Paramètre | Valeur |
|-----------|--------|
| Logo | Upload `logo-hokuno-nav.png` |
| Couleur principale (accent) | `#D4A853` (doré) |
| Couleur des boutons | `#D4A853` |
| Couleur du texte des boutons | `#000000` |
| Couleur de fond | Aussi sombre que possible (Shopify limite les options) |
| Police | Par défaut Shopify (pas de fonts custom au checkout) |

### Options checkout

| Paramètre | Valeur |
|-----------|--------|
| Compte client | Optionnel (le client peut checkout en guest ou créer un compte) |
| Adresse de facturation | Même que livraison par défaut |
| Autoriser les pourboires | Non |
| Champ de note de commande | Non (pas utile pour le POD) |
| Marketing email opt-in | Affiché au checkout, pré-coché : Non (RGPD) |

### Personnalisation

| Section | Personnalisation |
|---------|-----------------|
| Bannière supérieure | Logo Hokuno |
| Message post-achat | "Merci pour votre commande ! Votre produit est fabriqué spécialement pour vous." |
| Lien retour | "Continuer vos achats" → `/collections` |

---

## 10. NOTIFICATIONS CLIENT

Shopify Admin → Settings → Notifications

Les emails transactionnels sont détaillés dans `specs/EMAILS.md`. Résumé des personnalisations :

| Notification | Personnalisation |
|-------------|-----------------|
| Confirmation de commande | Logo Hokuno, couleurs noir + doré, message : "Votre commande est en cours de préparation !" |
| Expédition envoyée | Numéro de suivi, délai estimé selon la zone |
| Livraison effectuée | Invitation à laisser un avis |
| Panier abandonné | Rappel avec image du produit, bouton "Finaliser ma commande" |
| Création de compte | Bienvenue + code promo HOKUNO15 |
| Réinitialisation MDP | Standard brandé |

---

## 11. APPLICATIONS SHOPIFY

### Installées obligatoirement

| App | Usage | Gratuite ? |
|-----|-------|:----------:|
| Printify | Connexion production POD | ✅ Oui (gratuit sans Premium) |
| Google & YouTube | Connexion GA4 + Google Shopping (optionnel) | ✅ Oui |
| Facebook & Instagram | Meta Pixel + Instagram Shopping (optionnel) | ✅ Oui |

### À installer si besoin

| App | Usage | Gratuite ? |
|-----|-------|:----------:|
| Judge.me | Avis clients + schema aggregateRating | ✅ Plan gratuit |
| Shopify Email | Newsletter | ✅ Inclus (1000 emails/mois) |

### À NE PAS installer

| App | Pourquoi pas |
|-----|-------------|
| Apps SEO tierces | Le SEO est codé en dur dans le thème (`specs/SEO.md`) |
| Apps de cookies tierces | La bannière cookies est dans le thème (`specs/LEGAL.md`) |
| Apps de reviews payantes | Judge.me gratuit suffit |
| Apps de chat live | Pas nécessaire au lancement |
| Apps de countdown/urgence | Hors brand — Hokuno n'est pas du fast fashion |
| Apps de popup email | Le formulaire newsletter est dans le footer |

**Chaque app ajoutée = JS supplémentaire = impact sur la performance.** Minimalisme.

---

## 12. DOMAINE

Détaillé dans `specs/DOMAINE.md`. Résumé :

| Paramètre | Valeur |
|-----------|--------|
| Domaine cible | `hokuno.com` ou `hokuno.fr` ou `hokuno.store` |
| Achat | Via Shopify (Settings → Domains) ou Namecheap/OVH |
| DNS | A Record → `23.227.38.65`, CNAME → `shops.myshopify.com` |
| SSL | Automatique (Shopify le génère) |
| Timing | Acheter APRÈS validation du thème, AVANT le lancement public |

---

## 13. PAGES POLICIES

Shopify Admin → Settings → Policies

Le contenu des pages policies est défini dans `specs/LEGAL.md`. Les configurer dans :

| Policy | Champ Shopify |
|--------|--------------|
| CGV | Terms of service |
| Politique de confidentialité | Privacy policy |
| Politique de retour | Refund policy |
| Politique d'expédition | Shipping policy |

Shopify crée automatiquement les URLs `/policies/terms-of-service`, `/policies/privacy-policy`, `/policies/refund-policy`.

La page "Mentions légales" est une PAGE statique (pas une policy) → créée dans Pages → handle `mentions-legales`.

---

## 14. RÉCAPITULATIF — ORDRE DE CONFIGURATION

Après le push du thème (Phase 6 migration), configurer dans cet ordre :

| # | Section | Où dans Shopify Admin | Dépendances |
|---|---------|----------------------|-------------|
| 1 | Infos générales | Settings → Store details | Aucune |
| 2 | Paiements | Settings → Payments | Informations bancaires |
| 3 | Taxes | Settings → Taxes | Paiements activés |
| 4 | Livraison | Settings → Shipping | Printify connecté |
| 5 | Devise | Settings → Markets → Pricing | Marchés configurés |
| 6 | Marchés | Settings → Markets | Langue + devise |
| 7 | Langue | Settings → Languages | Fichiers locales dans le thème |
| 8 | Policies | Settings → Policies | Contenu LEGAL.md rédigé |
| 9 | Code promo | Discounts → Create | Produits publiés |
| 10 | Checkout | Settings → Checkout | Logo uploadé |
| 11 | Notifications | Settings → Notifications | Template email brandé |
| 12 | Apps | Settings → Apps | Printify, GA4, Meta Pixel |
| 13 | Domaine | Settings → Domains | Thème validé |
