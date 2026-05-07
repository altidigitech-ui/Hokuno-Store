# HOKUNO — Plan de reconstruction complet
## My Store 5 (nouvelle boutique Shopify)
### 7 mai 2026 — v2.0

---

## A. OUTILS À INSTALLER DANS LE CODESPACE

### 1. Shopify CLI
```bash
npm install -g @shopify/cli @shopify/theme
```

### 2. Shopify AI Toolkit (Plugin officiel Shopify pour Claude Code)
```bash
claude install-plugin shopify
```
Source : https://shopify.dev/docs/apps/build/ai-toolkit
→ MCP server Shopify (GraphQL Admin API, theme dev, products, collections)

### 3. Skill Shopify Theme Design (par dylanreed)
```bash
cd ~/.claude/plugins/local
git clone https://github.com/dylanreed/shopify-theme-design.git
```
→ Workflow : HTML preview d'abord → conversion en Liquid ensuite

### 4. ClaudeKit Skills — Shopify (par mrgoonie)
```bash
/plugin marketplace add mrgoonie/claudekit-skills
/plugin install shopify@claudekit-skills
```
→ Skills pour apps, extensions, thèmes, Liquid, GraphQL

### 5. Skills Shopify Products (par jezweb)
```bash
cd ~/.claude/plugins/local
git clone https://github.com/jezweb/claude-skills.git
```
→ Skills pour gérer les produits via GraphQL Admin API

### 6. ImageMagick (pour traiter les images)
```bash
sudo apt-get install -y imagemagick
```

---

## B. FICHIERS DE RÉFÉRENCE À METTRE DANS LE REPO

### 7. CLAUDE.md Shopify Best Practices (par Karim Tarek)
Télécharger depuis : https://gist.github.com/karimmtarek/3a8a636a05ae1c349ad0bba9d10425f0
→ Mettre à la racine du repo comme base du CLAUDE.md
→ Adapter avec les conventions spécifiques Hokuno (couleurs, typo, structure)

---

## C. CLÉS API À CONFIGURER

### 8. Token Printify
```bash
export PRINTIFY_API_TOKEN=ton_token_printify
```
→ Déjà existant, ne change pas

### 9. Token Shopify Admin API (My Store 5)
```bash
export SHOPIFY_ACCESS_TOKEN=shpat_xxxxxxxxxx
export SHOPIFY_STORE=mystore5.myshopify.com
```
→ À récupérer dans My Store 5 → Settings → Apps → Develop apps → Create app → Admin API scopes → Install → Copier le token shpat_

### 10. Scopes API Shopify nécessaires
- read_products, write_products
- read_themes, write_themes
- read_content, write_content
- read_customers
- read_orders
- read_inventory
- read_script_tags, write_script_tags
- read_locales, write_locales
- read_publications, write_publications

---

## D. LES 18 FICHIERS SPECS À CRÉER

Tous dans le dossier `specs/` du repo.

---

### 1. specs/ARCHITECTURE.md
- Structure globale de la boutique
- Nouveau store My Store 5 (URL, identifiants)
- Ancien store storemdtesttt (à abandonner)
- Organisation du repo (dossiers, fichiers)
- Stack technique : Shopify + Printify + Liquid + CSS + JS vanilla
- Principes : thème from scratch sans Dawn, tout dans theme.liquid, fond #000000

---

### 2. specs/NAVIGATION.md
- NAVBAR desktop : chaque lien, texte affiché, href exact, comportement au hover
- NAVBAR mobile : hamburger menu, overlay fullscreen, animation slide-in
- BOTTOM NAV mobile : 4 icônes, textes, liens, style glassmorphism
- FOOTER : 4 colonnes, chaque lien listé, newsletter
- Fil d'Ariane (breadcrumbs) : Accueil > Collections > Wanted > T-shirt Lufi
- Sélecteur de langue FR/EN
- Barre de recherche : comportement, suggestions, résultats

---

### 3. specs/COLLECTIONS.md
- Les 4 collections principales : Wanted, Direction, Mythologie, Design Hokuno
- Handle Shopify exact de chaque collection
- Conditions automatiques (titre contient X)
- Contenu de chaque collection (quels types de produits)
- Sous-catégories par type dans chaque collection : T-shirts, Mugs, Coques, Accessoires
- Filtres disponibles sur chaque page collection : type, couleur, prix, langue FR/EN
- Options de tri : par défaut, prix croissant/décroissant, plus récent, plus populaire
- Pagination : 24 produits par page, boutons page 1/2/3/suivant/précédent
- Image de couverture de chaque collection (les 4 cards ChatGPT)
- Description texte de chaque collection
- Page /collections : affiche les 4 collections en grille (pas les produits)

---

### 4. specs/PAGES.md
Chaque page du site détaillée avec son contenu exact :
- **ACCUEIL** (/) : hero, trust bar, 4 cards collections, produits phares, footer
- **LISTE COLLECTIONS** (/collections) : grille des 4 collections avec images et descriptions
- **COLLECTION UNIQUE** (/collections/wanted) : titre, description, filtres, grille produits, pagination
- **PRODUIT** (/products/xxx) : galerie images, infos, tailles, couleurs, panier, backstory, similaires
- **PANIER** (/cart) : liste produits, quantités, modifier/supprimer, sous-total, code promo, bouton checkout
- **RECHERCHE** (/search) : barre de recherche, résultats en grille, pas de résultats
- **À PROPOS** (/pages/about) : histoire de Hokuno, mission, valeurs
- **FAQ** (/pages/faq) : questions/réponses en accordéon
- **CONTACT** (/pages/contact) : formulaire (nom, email, message) + email direct
- **BLOG** (/blogs/journal) : liste articles avec image, titre, extrait
- **ARTICLE** (/blogs/journal/xxx) : article complet avec image, titre, contenu
- **COMPTE** (/account) : connexion, inscription, historique commandes
- **404** : message d'erreur stylé avec lien retour accueil
- **MOT DE PASSE** : page branded Hokuno quand la boutique est protégée

---

### 5. specs/PRODUIT.md
La fiche produit complète :
- Ordre des images (dos en premier pour t-shirts, côté design pour mugs)
- Galerie d'images avec miniatures cliquables en bas
- Quand on clique une miniature, la grande image change
- Sélecteur de couleur (swatches visuels ronds, pas dropdown)
- Quand on change la couleur, l'image change automatiquement
- Sélecteur de taille (S, M, L, XL — boutons cliquables, pas dropdown)
- Tailles disponibles vs indisponibles (grisé si stock 0)
- Prix affiché avec la devise (34.99€ pour t-shirts, etc.)
- Prix barré si remise active (HOKUNO15)
- Bouton "AJOUTER AU PANIER" doré — comportement : ajoute sans rediriger, notification "Ajouté !"
- Bouton favoris (coeur)
- Quantité : sélecteur +/- (défaut 1)
- Description / backstory du personnage (HTML depuis Printify)
- Badges de confiance (livraison, retours, paiement)
- Section "Vous pourriez aussi aimer" — 4 produits de la même collection
- Guide des tailles (popup ou accordéon avec tableau S/M/L/XL)
- Infos produit : matière, coupe, entretien (lavage 30°C)
- Partage social : boutons partager sur Instagram, TikTok, copier le lien

---

### 6. specs/MOCKUPS.md
Ordre des mockups par type de produit :
- **T-shirts** : Back 2 (primary), Front 2, Folded — pour CHAQUE couleur (Black, Navy, White, Sand, Sport Grey, Natural)
- **Mugs** : Left ou Right (primary — celui qui montre le design), Back, Front — pour CHAQUE variante (11oz, 15oz)
- **Coques** : Front (primary)
- **Casquettes** : le mockup qui montre le logo en priorité
- **Bobs** : le mockup qui montre le design en priorité
- **Polos** : le mockup qui montre le logo en priorité
- **Shorts de bain** : le mockup qui montre le design all-over
- **Claquettes** : le mockup qui montre le design sur la sangle
- Instructions détaillées pour Claude Chrome pour automatiser les changements (prompt restrictif)
- Vérification : chaque produit doit montrer le design en premier

---

### 7. specs/MIGRATION.md
Plan de migration storemdtesttt → My Store 5 :
- Étape 1 : Créer l'app développeur sur My Store 5, récupérer le token shpat_
- Étape 2 : Configurer les variables d'environnement dans le Codespace
- Étape 3 : Connecter Printify à My Store 5 (dans Printify → Add store → Shopify)
- Étape 4 : Republier les 430 produits vers My Store 5 via API Printify
- Étape 5 : Vérifier que tous les produits sont sur My Store 5
- Étape 6 : Créer les 4 collections automatiques sur My Store 5
- Étape 7 : Pousser le thème Hokuno sur My Store 5
- Étape 8 : Créer les pages (about, faq, contact)
- Étape 9 : Créer le blog (journal)
- Étape 10 : Configurer paiements, livraison, code promo, devises
- Étape 11 : Configurer SEO, analytics, légal
- Étape 12 : Vérifier chaque lien et bouton (checklist)
- Étape 13 : Désactiver le mot de passe
- Étape 14 : LANCEMENT
- Note : l'ancien store storemdtesttt reste comme backup/test

---

### 8. specs/THEME.md
Design system complet — chaque valeur CSS exacte :
- **Couleurs** : #000000 (fond body), #050505 (fond footer), #111 (fond cartes), #D4A853 (doré accent), rgba values pour glassmorphism
- **Typographie** : font-family Inter (Google Fonts), poids 900/700/600/500/400/300
- **Tailles de texte** : h1=76px, h2=52px, h3=18px, label=13px, body=14px, small=11px
- **Espacements** : padding sections 100px 64px, gap grilles 18px, margin boutons 36px top
- **Border-radius** : 14px cartes collections, 12px trust bar, 10px cards produits, 6px boutons, 4px boutons CTA
- **Glassmorphism** : background rgba(255,255,255,0.04), backdrop-filter blur(24px), border 1px solid rgba(255,255,255,0.08)
- **Boutons** : .btn-gold (fond #D4A853, texte #000000, padding 18px 36px), .btn-outline (fond transparent, bordure rgba(255,255,255,0.25))
- **Cartes produit** : fond rgba(255,255,255,0.02), bordure rgba(255,255,255,0.06), hover bordure dorée
- **Animations** : fadeUp au chargement (0.8s ease-out), hover scale(1.015) sur cartes, transitions 0.3s ease partout
- **Breakpoints** : desktop >1024px, tablette 768-1024px, mobile <768px
- **Z-index** : navbar 9999, mobile nav 9999, overlays 9998, hero content 3, hero image 2, textes verticaux 1
- **Images** : fond #000000 pour matcher le body, mix-blend-mode screen sur le logo transparent

---

### 9. specs/SEO.md
- **Meta title** par page : format "Titre — HOKUNO ホクノ"
- **Meta description** par page : max 160 caractères, inclut le mot-clé principal
- **Schema JSON-LD** :
  - Product (sur chaque page produit) : name, price, image, availability, brand
  - Organization (sur toutes les pages) : name, logo, url, sameAs (réseaux)
  - BreadcrumbList (sur chaque page) : fil d'Ariane structuré
  - CollectionPage (sur chaque collection)
- **Open Graph** : og:title, og:image, og:description, og:type, og:url
- **Twitter Card** : twitter:card, twitter:title, twitter:image
- **robots.txt** : autoriser GPTBot, ClaudeBot, PerplexityBot, Googlebot
- **llms.txt** : description de la boutique pour les IA (produits, collections, prix)
- **Sitemap** : généré automatiquement par Shopify (/sitemap.xml)
- **URLs propres** : /collections/wanted, /products/t-shirt-lufi-wanted
- **Alt text** : sur TOUTES les images (nom du produit + collection)
- **H1 unique** par page : jamais 2 H1 sur la même page
- **Canonical URL** : sur chaque page pour éviter le contenu dupliqué
- **Hreflang** : fr pour le marché FR, en pour le marché EN (si multilingue activé)

---

### 10. specs/CONFIG-SHOPIFY.md
Configuration complète de la boutique :
- **Nom du store** : HOKUNO
- **Email** : altidigitech@gmail.com
- **Langue par défaut** : Français
- **Devise principale** : EUR
- **Paiements** : Shopify Payments (CB Visa/MC/Amex, Apple Pay, Google Pay, Shop Pay)
- **Livraison** :
  - France : gratuite dès 60€, sinon tarif standard Printify
  - EU : gratuite dès 60€, sinon tarif standard Printify
  - USA : tarif standard Printify
  - Canada : tarif standard Printify
  - Australie : tarif standard Printify
  - Reste du monde : tarif standard Printify
- **Code promo** : HOKUNO15 = -15%, tous produits, durée 2 semaines après lancement
- **Devises acceptées** : EUR (principal), USD, GBP, CAD, AUD
- **Taxes** : TVA EU configurée automatiquement par Shopify
- **Politiques** :
  - CGV : à rédiger (vente en ligne, POD, livraison)
  - Retours : 30 jours, produit non porté/utilisé
  - Confidentialité : conforme RGPD
  - Expédition : délais Printify (3-7 jours production + livraison)
- **Marchés Shopify** :
  - Marché principal : France + EU (EUR)
  - Marché international : US/CA/AU/UK (devises locales)
- **Checkout** : logo Hokuno, couleur dorée #D4A853
- **Notifications client** : personnaliser avec branding Hokuno

---

### 11. specs/MOBILE.md
Comportement mobile spécifique (<768px) :
- **Header sticky** : glassmorphism, logo gauche (height 30px), hamburger droite
- **Menu hamburger** : overlay fullscreen fond #000000, liste des liens en grand, animation slide-in depuis la droite, bouton fermer (X)
- **Hero** : texte full width au-dessus, image t-shirt full width en dessous
- **Textes verticaux** : display none (cachés)
- **Trust bar** : empilée verticalement (3 cartes l'une sous l'autre)
- **Section collections** : grille 2 colonnes ou scroll horizontal
- **Produits phares** : grille 2 colonnes
- **Page collection** : grille 2 colonnes, filtres en accordéon ou drawer
- **Page produit** :
  - Image full width en haut
  - Swipe gauche/droite pour changer d'image
  - Infos produit en dessous
  - Bouton "AJOUTER AU PANIER" sticky en bas de l'écran
- **Bottom nav** : position fixed en bas, glassmorphism, 4 icônes (Accueil 🏠, Collections 📦, Panier 🛒, Compte 👤)
- **Touch targets** : minimum 44x44px pour tous les boutons/liens
- **Pas de hover** sur mobile (uniquement tap)
- **Font-size minimum** : 14px partout
- **Pas de pinch-to-zoom désactivé** (laisser le zoom natif)
- **Footer** : colonnes empilées, 1 seule colonne
- **Carrousel produits phares dans le hero** : caché sur mobile

---

### 12. specs/CHECKLIST.md
Liste de vérification COMPLÈTE avant lancement :

**Navigation :**
- [ ] Logo navbar → retour accueil
- [ ] Lien COLLECTIONS → /collections (page avec les 4 collections)
- [ ] Lien NOUVEAUTÉS → /collections/all?sort_by=created-descending
- [ ] Lien À PROPOS → /pages/about (page existe et a du contenu)
- [ ] Lien JOURNAL → /blogs/journal (blog existe)
- [ ] Lien RECHERCHE → /search (fonctionne)
- [ ] Lien COMPTE → /account (connexion/inscription)
- [ ] Lien PANIER → /cart (affiche le panier)
- [ ] Footer : tous les liens fonctionnent
- [ ] Mobile : hamburger menu s'ouvre et se ferme
- [ ] Mobile : bottom nav fonctionne (4 boutons)
- [ ] Mobile : menu hamburger — tous les liens marchent

**Collections :**
- [ ] /collections/wanted → affiche les produits Wanted (t-shirts + mugs)
- [ ] /collections/direction → affiche les produits Direction
- [ ] /collections/mythologie → affiche les produits Mythologie
- [ ] /collections/design-hokuno → affiche les produits Design Hokuno
- [ ] Pagination fonctionne (page 1, 2, 3...)
- [ ] Filtres fonctionnent (type, couleur, prix)
- [ ] Tri fonctionne (prix, récent, populaire)
- [ ] Chaque card collection affiche le bon nombre de produits

**Produits :**
- [ ] T-shirts : dos affiché en premier (design visible)
- [ ] Mugs : côté avec design affiché en premier
- [ ] Sélecteur de taille fonctionne (S, M, L, XL)
- [ ] Sélecteur de couleur fonctionne et change l'image
- [ ] Prix correct affiché (34.99€ t-shirts, 29.99€ mugs, etc.)
- [ ] Bouton "Ajouter au panier" fonctionne
- [ ] Description/backstory affichée correctement
- [ ] Section "Vous pourriez aussi aimer" affiche 4 produits
- [ ] Guide des tailles accessible

**Panier & Checkout :**
- [ ] Panier affiche les bons produits avec images
- [ ] Modifier la quantité fonctionne
- [ ] Supprimer un produit fonctionne
- [ ] Sous-total calculé correctement
- [ ] Code promo HOKUNO15 fonctionne (-15%)
- [ ] Bouton checkout mène au paiement Shopify
- [ ] Livraison gratuite dès 60€ fonctionne

**Pages :**
- [ ] /pages/about — contenu affiché
- [ ] /pages/faq — accordéon fonctionne
- [ ] /pages/contact — formulaire fonctionne
- [ ] /blogs/journal — articles affichés
- [ ] /policies/terms-of-service — CGV affichées
- [ ] /policies/privacy-policy — politique affichée
- [ ] /policies/refund-policy — retours affichés

**SEO :**
- [ ] Meta titles corrects sur chaque page
- [ ] Meta descriptions présentes
- [ ] Schema JSON-LD Product présent sur chaque page produit
- [ ] Schema JSON-LD Organization présent
- [ ] Open Graph tags présents (tester avec Facebook Debugger)
- [ ] robots.txt correct (GPTBot, ClaudeBot autorisés)
- [ ] llms.txt présent à la racine
- [ ] Sitemap accessible (/sitemap.xml)
- [ ] Alt text sur toutes les images

**Technique :**
- [ ] Performance LCP < 2.5s (tester avec PageSpeed Insights)
- [ ] CLS < 0.1
- [ ] Images lazy loading activé
- [ ] SSL HTTPS partout
- [ ] Responsive : iPhone SE, iPhone 14, iPad, desktop
- [ ] Pas d'erreur console JS
- [ ] Pas de lien cassé (404)

**Legal & Config :**
- [ ] Bannière cookies RGPD affichée
- [ ] CGV rédigées et accessibles
- [ ] Politique de confidentialité rédigée
- [ ] Politique de retour rédigée
- [ ] Mentions légales présentes
- [ ] Paiements Shopify configurés
- [ ] Devises EUR/USD/GBP configurées

**Analytics :**
- [ ] Google Analytics 4 connecté
- [ ] Meta Pixel installé
- [ ] TikTok Pixel installé (si TikTok Shop prévu)

**Lancement :**
- [ ] Mot de passe boutique DÉSACTIVÉ
- [ ] Domaine custom configuré (si applicable)
- [ ] Test commande réelle effectué (commande test + annulation)

---

### 13. specs/ANALYTICS.md
Tracking et mesure :
- **Google Analytics 4** :
  - Créer une propriété GA4 sur analytics.google.com
  - Récupérer le Measurement ID (G-XXXXXXXXXX)
  - Installer dans Shopify : Settings → Apps → Google & YouTube channel
  - OU injecter le gtag.js dans theme.liquid
  - Événements à tracker : page_view, view_item, add_to_cart, begin_checkout, purchase
  - Conversion tracking : achat = événement purchase avec valeur
- **Meta Pixel (Facebook/Instagram)** :
  - Créer le pixel dans Meta Business Suite
  - Récupérer le Pixel ID
  - Installer dans Shopify : Settings → Apps → Facebook & Instagram channel
  - OU injecter le pixel code dans theme.liquid
  - Événements : PageView, ViewContent, AddToCart, InitiateCheckout, Purchase
- **TikTok Pixel** :
  - Créer le pixel dans TikTok Ads Manager
  - Installer via TikTok channel dans Shopify
  - Événements : page_view, view_content, add_to_cart, checkout, purchase
- **Shopify Analytics** : intégré par défaut (dashboard, rapports, Live View)

---

### 14. specs/EMAILS.md
Emails automatiques et branding :
- **Emails transactionnels Shopify** (Settings → Notifications → Customize) :
  - Confirmation de commande : logo Hokuno, couleurs #000000 + #D4A853, message personnalisé
  - Expédition envoyée : numéro de suivi, délai estimé
  - Livraison effectuée : demander un avis
  - Panier abandonné : rappel avec image du produit, bouton "Finaliser ma commande"
  - Création de compte : bienvenue + code promo HOKUNO15
  - Réinitialisation mot de passe
- **Template email** : fond #000000, texte blanc, accents #D4A853, logo en haut
- **Newsletter** (optionnel pour le lancement) :
  - Formulaire dans le footer : email + bouton "S'INSCRIRE"
  - Outil : Shopify Email (inclus) ou Mailchimp/Klaviyo
  - Email de bienvenue avec code promo HOKUNO15

---

### 15. specs/LEGAL.md
Obligations légales EU :
- **Bannière cookies RGPD** :
  - Afficher au premier chargement : "Ce site utilise des cookies pour améliorer votre expérience"
  - Boutons : "Accepter" / "Refuser" / "Personnaliser"
  - Shopify app recommandée : Cookie Banner (gratuit)
  - Les scripts analytics (GA4, Meta Pixel) ne se chargent PAS avant acceptation
- **Mentions légales** (/pages/mentions-legales) :
  - Raison sociale, adresse, email, numéro SIRET (si auto-entrepreneur)
  - Hébergeur : Shopify Inc.
  - Directeur de publication
- **Conditions Générales de Vente** (/policies/terms-of-service) :
  - Print on demand : produit fabriqué à la commande
  - Délais de fabrication : 3-7 jours ouvrés
  - Délais de livraison : variable selon destination
  - Droit de rétractation : 14 jours (loi EU)
  - Retours : 30 jours, produit non porté
  - Remboursement : sous 14 jours après réception du retour
- **Politique de confidentialité** (/policies/privacy-policy) :
  - Données collectées : nom, email, adresse, paiement
  - Utilisation : traitement commande, newsletter (si consentement)
  - Partage : Printify (fabrication), transporteur (livraison), analytics
  - Droits RGPD : accès, rectification, suppression, portabilité
  - Contact : altidigitech@gmail.com
- **Politique de retour** (/policies/refund-policy) :
  - 30 jours pour retourner
  - Produit non porté, non lavé, avec étiquette
  - Remboursement du prix produit (pas les frais de livraison)
  - Échange possible

---

### 16. specs/MULTILINGUE.md
Gestion FR/EN :
- **Situation actuelle** : produits en FR et EN (titres et descriptions bilingues)
- **Collections** : même collection contient les produits FR et EN
- **Option 1 — Shopify Markets (recommandée)** :
  - Marché France : langue FR, devise EUR
  - Marché International : langue EN, devise USD/GBP
  - Shopify gère automatiquement la redirection selon la localisation
  - Le thème doit utiliser les traductions Shopify (locales/)
- **Option 2 — Filtres manuels** :
  - Ajouter un tag "FR" ou "EN" sur chaque produit
  - Filtre langue sur les pages collection
  - Sélecteur FR/EN dans la navbar
- **Textes du thème à traduire** :
  - Navbar : COLLECTIONS, NOUVEAUTÉS, À PROPOS, JOURNAL, RECHERCHE, COMPTE, PANIER
  - Hero : "TOUJOURS ALLER DE L'AVANT" / "ALWAYS MOVING FORWARD"
  - Boutons : "DÉCOUVRIR LA COLLECTION" / "DISCOVER THE COLLECTION", "AJOUTER AU PANIER" / "ADD TO CART"
  - Trust bar : livraison, retours, paiements
  - Footer : tous les textes
- **Fichiers locales/** : fr.json + en.json avec toutes les clés de traduction

---

### 17. specs/DOMAINE.md
Domaine et DNS :
- **Domaine idéal** : hokuno.com ou hokuno.fr ou hokuno.store
- **Vérifier la disponibilité** : via Shopify (Settings → Domains → Buy new domain) ou Namecheap/OVH
- **Prix moyen** : 10-15€/an pour un .com, 5-8€/an pour un .fr
- **Configuration DNS** :
  - A Record → IP Shopify (23.227.38.65)
  - CNAME → shops.myshopify.com
  - Shopify génère automatiquement le certificat SSL
- **Redirection** : www.hokuno.com → hokuno.com (ou inversement)
- **Email** : configurer un email pro (contact@hokuno.com) via Google Workspace ou Zoho Mail
- **Timing** : acheter le domaine APRÈS la validation du thème et AVANT le lancement public

---

### 18. specs/SOCIAL.md
Réseaux sociaux et intégrations :
- **TikTok Shop** :
  - Connecter via Shopify : Sales channels → TikTok
  - Synchroniser les produits
  - Activer le shopping dans les vidéos TikTok
- **Instagram Shopping** :
  - Connecter via Shopify : Sales channels → Facebook & Instagram
  - Catalogue produits synchronisé
  - Tags produits dans les posts/stories Instagram
- **Liens sociaux** (dans le footer) :
  - TikTok : @hokuno (à créer)
  - Instagram : @hokuno (à créer)
- **Favicon** : icône boussole Hokuno en 32x32 et 180x180 (Apple Touch Icon)
- **Open Graph images** :
  - Image par défaut : hero-tshirt.png (1200x630 recadré)
  - Chaque produit : featured_image du produit
  - Chaque collection : card de la collection
- **Partage social sur les pages produit** :
  - Bouton "Partager sur Instagram"
  - Bouton "Copier le lien"
  - Bouton "Partager sur TikTok"

---

## E. ASSETS VISUELS À GARDER DANS LE REPO

### assets/theme/ (8 images)
- hero-tshirt.png — Hero landing (t-shirt Wanted + boussole dorée)
- boussole-gold.png — Logo boussole dorée
- card-wanted.png — Image collection Wanted
- card-direction.png — Image collection Direction
- card-mythologie.png — Image collection Mythologie
- card-design-hokuno.png — Image collection Design Hokuno
- logo-hokuno-nav.png — Logo navbar (fond noir)
- logo-hokuno-transparent.png — Logo navbar (fond transparent)

### assets/design-reference/ (4 mockups ChatGPT)
- hero-landing.png — Mockup landing page desktop
- collections-grid.png — Mockup section collections
- product-page.png — Mockup page produit
- mobile-version.png — Mockup version mobile

---

## F. FICHIERS REPO EXISTANTS À GARDER

### Fichiers de données
- CONTEXT.md — Brand bible
- CLAUDE.md — Instructions Claude Code (à fusionner avec Karim Tarek)
- INVENTAIRE.md — 430 produits
- PRICING.md — Coûts et prix de vente
- TODO.md — Plan d'action
- README.md — Documentation

### Collections JSON
- collections/wanted.json — 46 personnages avec backstories FR/EN
- collections/direction.json — 10 personnages
- collections/mythologie.json — 10 personnages

### Skills Claude Code existantes
- .claude/skills/printify/SKILLS.md — API Printify

---

## G. ORDRE D'EXÉCUTION

### Phase 1 — Préparer les specs (ici avec moi)
1. Créer les 18 fichiers specs ensemble (un par un, on valide chaque)
2. Mettre à jour CLAUDE.md avec les best practices Shopify (Karim Tarek + Hokuno)
3. Commit et push

### Phase 2 — Configurer le Codespace
4. Installer les 6 outils (Shopify CLI, plugins, skills)
5. Configurer les variables d'environnement (tokens Printify + Shopify My Store 5)
6. Tester la connexion API Shopify

### Phase 3 — Configurer My Store 5
7. Créer l'app dev et récupérer le token shpat_
8. Connecter Printify à My Store 5
9. Republier les 430 produits vers My Store 5
10. Créer les 4 collections automatiques
11. Vérifier que les produits sont dans les bonnes collections

### Phase 4 — Mockups produits
12. Changer les mockups t-shirts (dos en premier) via Claude Chrome
13. Changer les mockups mugs (côté design en premier) via Claude Chrome
14. Republier les produits modifiés sur Shopify

### Phase 5 — Coder le thème
15. Claude Code crée le thème en suivant les 18 specs
16. Workflow dylanreed : HTML preview d'abord → validation visuelle
17. Conversion en Liquid
18. Push sur My Store 5 en mode dev
19. Itérations et corrections visuelles

### Phase 6 — Configuration Shopify
20. Créer les pages (about, faq, contact, mentions légales)
21. Créer le blog (journal)
22. Configurer paiements (Shopify Payments)
23. Configurer livraison (gratuite dès 60€)
24. Créer le code promo HOKUNO15
25. Configurer les devises (EUR principal + USD/GBP/CAD/AUD)
26. Personnaliser les emails transactionnels

### Phase 7 — SEO & Analytics
27. Meta tags et JSON-LD sur chaque page
28. robots.txt + llms.txt
29. Installer GA4
30. Installer Meta Pixel
31. Installer TikTok Pixel (optionnel)

### Phase 8 — Legal
32. Bannière cookies RGPD
33. Rédiger CGV
34. Rédiger politique de confidentialité
35. Rédiger politique de retour
36. Rédiger mentions légales

### Phase 9 — Vérification
37. Passer la CHECKLIST complète (tous les points)
38. Test mobile (iPhone + Android)
39. Test desktop (Chrome, Firefox, Safari)
40. Test commande réelle (commander + annuler)

### Phase 10 — Lancement
41. Acheter le domaine (hokuno.com / .fr / .store)
42. Configurer DNS
43. Désactiver le mot de passe
44. Publier le thème en production
45. Annoncer sur TikTok + Instagram
46. LANCEMENT 🚀

---

## RÉSUMÉ FINAL

| Catégorie | Nombre |
|-----------|--------|
| Outils à installer | 6 |
| Fichiers de référence | 1 (CLAUDE.md Karim Tarek) |
| Clés API | 2 (Printify + Shopify) |
| Fichiers specs à créer | 18 |
| Assets visuels | 8 + 4 mockups |
| Fichiers repo existants | 9 + 3 JSON + 1 skill |
| Phases d'exécution | 10 phases, 46 étapes |
| Produits | 430 |
| Collections | 4 |
