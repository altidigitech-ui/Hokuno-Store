# specs/CHECKLIST.md — Checklist pré-lancement

> Liste de vérification COMPLÈTE à passer avant de désactiver le mot de passe et lancer la boutique.
> Consolide tous les checks des 17 autres specs.
> Chaque item doit être coché. Un seul item non coché = pas de lancement.

---

## A. NAVIGATION (17 checks)

### Desktop

- [ ] Logo navbar cliquable → retour accueil `/`
- [ ] Logo : image `logo-hokuno-transparent.png` affichée, hauteur 65px, mix-blend-mode screen
- [ ] Lien COLLECTIONS → `/collections` (affiche la grille des 4 collections, PAS tous les produits)
- [ ] Lien NOUVEAUTÉS → `/collections/all?sort_by=created-descending` (produits triés par date)
- [ ] Lien À PROPOS → `/pages/about` (page existe, contenu affiché)
- [ ] Lien JOURNAL → `/blogs/journal` (blog existe)
- [ ] Icône recherche → `/search` (page fonctionne, résultats s'affichent)
- [ ] Icône compte → `/account` (formulaire connexion/inscription)
- [ ] Icône panier → `/cart` (panier affiché, compteur correct)
- [ ] Lien actif doré sur la page en cours
- [ ] Sélecteur FR/EN visible et fonctionnel

### Mobile

- [ ] Logo 30px, hamburger visible à droite
- [ ] Hamburger → overlay fullscreen, slide-in depuis la droite
- [ ] Menu overlay : 6 liens tappables, fermeture au tap lien, fermeture au X, fermeture Escape
- [ ] Scroll lock : body ne scroll pas sous l'overlay
- [ ] Bottom nav : 4 icônes (Accueil, Collections, Panier, Compte), page active dorée
- [ ] Bottom nav : badge panier avec compteur, safe-area bottom iPhone

### Footer

- [ ] Logo + tagline ホクノ affichés
- [ ] Colonne Collections : 4 liens fonctionnels (`/collections/wanted`, `direction`, `mythologie`, `design-hokuno`)
- [ ] Colonne Information : 4 liens fonctionnels (`/pages/about`, `/pages/faq`, `/pages/contact`, `/blogs/journal`)
- [ ] Colonne Légal : 4 liens fonctionnels (`/policies/terms-of-service`, `/policies/privacy-policy`, `/policies/refund-policy`, `/pages/mentions-legales`)
- [ ] Newsletter : champ email + bouton S'INSCRIRE fonctionnel
- [ ] Copyright : `© 2026 HOKUNO. Tous droits réservés.`
- [ ] Mobile : 1 colonne, pas masqué par le bottom nav (`margin-bottom: 70px`)

---

## B. COLLECTIONS (14 checks)

### Page /collections

- [ ] Affiche les 4 collections en grille (PAS les produits individuels)
- [ ] Ordre : Wanted, Direction, Mythologie, Design Hokuno
- [ ] Chaque card a son image (`card-wanted.png`, etc.), titre, description, bouton DÉCOUVRIR

### Pages collection individuelles

- [ ] `/collections/wanted` → **277 produits**
- [ ] `/collections/direction` → **80 produits**
- [ ] `/collections/mythologie` → **40 produits**
- [ ] `/collections/design-hokuno` → **33 produits**
- [ ] Total des 4 collections = **430 produits** (aucun orphelin, aucun doublon inter-collection)
- [ ] Filtres fonctionnent : type de produit, couleur, prix
- [ ] Filtre langue FR/EN fonctionne (Wanted + Direction)
- [ ] Tri fonctionne : pertinence, prix ↑↓, plus récent, nom A-Z
- [ ] Pagination : 24 produits/page, boutons page fonctionnels
- [ ] Breadcrumbs affichés : `Accueil › [Collection]`
- [ ] Description de la collection affichée sous le titre

---

## C. PRODUITS (20 checks)

### Images

- [ ] T-shirts Wanted/Direction/Mythologie : **dos affiché en premier** (design visible) — vérifier 5 produits aléatoires
- [ ] T-shirts Design Hokuno : design principal affiché en premier — vérifier les 13
- [ ] Mugs : **côté design** affiché en premier — vérifier 5 mugs aléatoires
- [ ] Coques : face avec design affichée en premier — vérifier les 14
- [ ] Accessoires : design/logo affiché en premier — vérifier les 17
- [ ] Galerie : miniatures cliquables, image principale change au clic
- [ ] Mobile : swipe gauche/droite fonctionne sur l'image principale

### Variantes

- [ ] Swatches couleur : cercles ronds (PAS dropdown), couleurs correctes
- [ ] Changement de couleur → image change automatiquement
- [ ] Boutons taille : S, M, L, XL cliquables (PAS dropdown)
- [ ] Taille indisponible : grisée et barrée
- [ ] Changement de variante → prix se met à jour (si prix différent)
- [ ] Variant ID hidden input se met à jour correctement

### Panier et infos

- [ ] Prix correct : 34.99€ t-shirts, 29.99€ mugs 11oz, 34.99€ mugs 15oz/noir, 24.99€ coques
- [ ] Bouton "AJOUTER AU PANIER" → ajoute en AJAX sans rechargement
- [ ] Notification "✓ Ajouté au panier" apparaît 2.5s
- [ ] Compteur panier navbar + bottom nav se met à jour
- [ ] Quantité +/- fonctionne (min 1, max 10)
- [ ] Description/backstory du personnage affichée (accordéon ouvert par défaut)
- [ ] Guide des tailles accessible (tableau S/M/L/XL avec mesures)
- [ ] Infos produit : matière, grammage, entretien affichés
- [ ] Section "VOUS POURRIEZ AUSSI AIMER" : 4 produits de la même collection
- [ ] Badges confiance : livraison, retours, paiements
- [ ] Breadcrumbs : `Accueil › [Collection] › [Produit]`
- [ ] Mobile : bouton panier sticky au-dessus du bottom nav

---

## D. PANIER & CHECKOUT (10 checks)

- [ ] Panier affiche les produits ajoutés avec images, titres, variantes
- [ ] Modifier quantité +/- fonctionne (met à jour le sous-total)
- [ ] Supprimer un produit (bouton ✕) fonctionne
- [ ] Sous-total calculé correctement
- [ ] Barre progression livraison : affiche `Plus que X€ pour la livraison gratuite !`
- [ ] Livraison gratuite dès 60€ : barre à 100%, message `✓ Livraison gratuite !`
- [ ] Bouton PASSER LA COMMANDE → mène au checkout Shopify
- [ ] Code promo HOKUNO15 : -15% appliqué au checkout (tester avec un t-shirt : 34.99€ → 29.74€)
- [ ] HOKUNO15 : coques exclues (vérifier qu'une coque ne bénéficie PAS de la réduction)
- [ ] Panier vide : message + bouton "DÉCOUVRIR NOS COLLECTIONS"

---

## E. PAGES STATIQUES (10 checks)

- [ ] `/pages/about` — contenu FR affiché, titre, sections histoire/collections/démarche/contact
- [ ] `/pages/faq` — 9 questions en accordéon, clic ouvre/ferme, une seule ouverte à la fois
- [ ] `/pages/contact` — formulaire (nom, email, message), soumission → message de confirmation
- [ ] `/pages/mentions-legales` — contenu légal affiché (raison sociale, SIRET, hébergeur)
- [ ] `/blogs/journal` — page blog avec articles en grille (ou message "aucun article" si vide)
- [ ] `/policies/terms-of-service` — CGV rédigées et accessibles
- [ ] `/policies/privacy-policy` — politique de confidentialité rédigée
- [ ] `/policies/refund-policy` — politique de retour rédigée
- [ ] Page 404 — message brandé Hokuno (404 + ホクノ + bouton retour accueil)
- [ ] Page mot de passe — brandée Hokuno (logo + katakana + formulaire)

---

## F. SEO (19 checks)

### Meta tags

- [ ] Meta title correct sur chaque type de page : `[Page] — HOKUNO ホクノ` (vérifier accueil, 1 collection, 1 produit, 1 page statique)
- [ ] Meta title accueil : `HOKUNO ホクノ — Streetwear Manga Japonais` (PAS juste "HOKUNO ホクノ")
- [ ] Meta description présente et < 155 caractères sur chaque page
- [ ] Canonical URL sur chaque page (`<link rel="canonical">`)
- [ ] Meta robots noindex sur `/cart`, `/account`, `/search`

### Schema JSON-LD

- [ ] Schema Organization sur toutes les pages (tester avec Rich Results Test)
- [ ] Schema Product sur chaque page produit (name, price, availability, brand, image)
- [ ] Schema CollectionPage sur chaque page collection
- [ ] Schema BreadcrumbList sur les pages avec breadcrumbs
- [ ] Schema WebSite + SearchAction sur la page d'accueil
- [ ] Schema FAQPage sur `/pages/faq`
- [ ] Schema Article sur les pages articles blog
- [ ] H1 unique par page (jamais 2 H1)

### Social & technique

- [ ] Open Graph tags : og:title, og:image, og:description (tester avec Facebook Debugger : `https://developers.facebook.com/tools/debug/`)
- [ ] Twitter Card : twitter:card, twitter:title, twitter:image
- [ ] robots.txt : GPTBot, ClaudeBot, PerplexityBot autorisés (vérifier `{{ shop.url }}/robots.txt`)
- [ ] llms.txt accessible (`{{ shop.url }}/llms.txt` ou `/pages/llms`)
- [ ] Sitemap accessible (`{{ shop.url }}/sitemap.xml`)
- [ ] Alt text sur TOUTES les images (aucun alt vide sauf boussole décorative)

---

## G. PERFORMANCE (9 checks)

Tester avec PageSpeed Insights : `https://pagespeed.web.dev/`

- [ ] LCP < 2.5s sur `/` (accueil)
- [ ] LCP < 2.5s sur `/collections/wanted`
- [ ] LCP < 2.5s sur un produit (ex : `/products/t-shirt-lufi-wanted-1-46`)
- [ ] CLS < 0.1 sur toutes les pages testées
- [ ] Images lazy loading : vérifier dans le code source que `loading="lazy"` est sur toutes les images sauf le hero
- [ ] Preconnect : `fonts.googleapis.com`, `fonts.gstatic.com`, `cdn.shopify.com` dans le `<head>`
- [ ] JS defer : `hokuno.js` chargé avec `defer`
- [ ] Pas d'erreur dans la console JS (DevTools → Console) — vérifier sur 3 pages différentes
- [ ] Pas de ressource en erreur 404 dans l'onglet Network (images, CSS, JS)

---

## H. MOBILE (17 checks)

Tester sur un vrai device (iPhone + Android), PAS uniquement en mode responsive navigateur.

- [ ] Navbar : logo 30px, hamburger visible et tappable, pas de liens texte
- [ ] Menu overlay : slide-in fluide, tous liens tappables, scroll lock, fermeture au tap lien
- [ ] Bottom nav : 4 icônes visibles, badge panier, page active dorée, safe-area iPhone
- [ ] Hero : texte 38px lisible, image sous le texte, boutons pleine largeur, pas de textes verticaux
- [ ] Trust bar : cartes empilées, texte ≥ 14px
- [ ] Collections grille : 2 colonnes, images pas coupées, texte lisible
- [ ] Filtres : bouton FILTRES visible, drawer s'ouvre, tappable, bouton APPLIQUER
- [ ] Product cards : 2 colonnes, image + titre + prix visibles
- [ ] Page produit : image full width, swipe fonctionne, infos sous image, bouton panier sticky
- [ ] Variantes : swatches ≥ 44px, boutons taille tappables
- [ ] Panier : items lisibles, +/- tappable, checkout sticky
- [ ] Contact : champs pleine largeur, pas de zoom au focus (font-size 16px)
- [ ] Footer : 1 colonne, liens tappables, pas masqué par bottom nav
- [ ] Scroll : fluide, pas de scroll horizontal, pas de bounce
- [ ] Safe areas : contenu pas masqué par notch ni barre home
- [ ] Orientation paysage : pas de casse (pas besoin d'être parfait)
- [ ] Chargement < 3s en 4G

---

## I. LEGAL & CONFIG (12 checks)

### Legal

- [ ] Bannière cookies RGPD affichée au premier chargement
- [ ] Cookies : "Accepter" charge GA4/Meta Pixel, "Refuser" ne charge PAS les scripts analytics
- [ ] CGV rédigées dans Shopify → Settings → Policies → Terms of service
- [ ] Politique de confidentialité rédigée → Settings → Policies → Privacy policy
- [ ] Politique de retour rédigée → Settings → Policies → Refund policy
- [ ] Mentions légales sur `/pages/mentions-legales` (SIRET, adresse, hébergeur, directeur publication)

### Config Shopify

- [ ] Paiements Shopify Payments activés (Visa, MC, Apple Pay, Google Pay, Shop Pay)
- [ ] Devises : EUR (principal) + USD + GBP + CAD + AUD
- [ ] TVA : "All prices include tax" activé
- [ ] Checkout brandé : logo Hokuno, couleur #D4A853
- [ ] Livraison : règle "gratuite dès 60€" active sur toutes les zones
- [ ] Marchés : France+EU (FR/EUR) + International (EN/USD) configurés

---

## J. ANALYTICS (5 checks)

- [ ] Google Analytics 4 : Measurement ID installé, événements temps réel visibles dans GA4
- [ ] Meta Pixel : Pixel ID installé, événements testés via Facebook Pixel Helper (extension Chrome)
- [ ] TikTok Pixel : installé si TikTok Shop prévu (optionnel au lancement)
- [ ] Scripts analytics chargés uniquement APRÈS acceptation cookies (vérifier : refuser cookies → aucun script GA4/Meta dans Network)
- [ ] Événements e-commerce : `page_view`, `view_item`, `add_to_cart`, `begin_checkout`, `purchase` configurés

---

## K. EMAILS (3 checks)

- [ ] Email confirmation de commande : logo Hokuno, couleurs noir + doré, message personnalisé (tester via commande test)
- [ ] Email panier abandonné : image du produit, bouton "Finaliser ma commande" (vérifier dans Settings → Notifications)
- [ ] Email création de compte : bienvenue + code HOKUNO15 mentionné

---

## L. LANCEMENT (6 checks)

- [ ] Mot de passe boutique DÉSACTIVÉ (Shopify Admin → Online Store → Preferences → décocher Password protection)
- [ ] Domaine custom configuré et SSL actif (cadenas vert dans le navigateur)
- [ ] Redirection www → sans www (ou inversement) fonctionnelle
- [ ] Test commande réelle : commander un produit → payer → vérifier email confirmation → annuler la commande
- [ ] Thème publié en production (pas en mode preview)
- [ ] Vérifier le site live sur un device qui n'a jamais visité le site (pas de cache)

---

## RÉSUMÉ

| Catégorie | Checks | Priorité |
|-----------|:------:|:--------:|
| A. Navigation | 24 | 🔴 |
| B. Collections | 14 | 🔴 |
| C. Produits | 25 | 🔴 |
| D. Panier & Checkout | 10 | 🔴 |
| E. Pages statiques | 10 | 🔴 |
| F. SEO | 19 | 🟡 |
| G. Performance | 9 | 🟡 |
| H. Mobile | 17 | 🔴 |
| I. Legal & Config | 12 | 🔴 |
| J. Analytics | 5 | 🟡 |
| K. Emails | 3 | 🟡 |
| L. Lancement | 6 | 🔴 |
| **TOTAL** | **154** | |

### Priorisation

**🔴 Bloquant** (catégories A-E, H, I, L) : le site ne peut pas lancer si un check échoue.
**🟡 Important** (catégories F, G, J, K) : le site peut lancer avec des checks manquants, mais ils doivent être corrigés dans les 48h après lancement.

### Outils nécessaires

| Outil | URL | Usage |
|-------|-----|-------|
| PageSpeed Insights | `https://pagespeed.web.dev/` | Performance (LCP, CLS) |
| Google Rich Results Test | `https://search.google.com/test/rich-results` | Schema JSON-LD |
| Facebook Sharing Debugger | `https://developers.facebook.com/tools/debug/` | Open Graph |
| Facebook Pixel Helper | Extension Chrome | Meta Pixel |
| iPhone réel | — | Test mobile iOS |
| Android réel | — | Test mobile Android |
| Chrome DevTools | F12 | Console JS, Network, Responsive |
