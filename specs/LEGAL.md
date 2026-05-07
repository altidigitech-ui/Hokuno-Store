# specs/LEGAL.md — Obligations légales

> Contrat pour Claude Code / toi. Bannière cookies, mentions légales, CGV, confidentialité, retours.
> **Les textes ci-dessous sont des modèles.** Adapter avec tes informations réelles (SIRET, adresse) avant publication.
> Le mécanisme de consentement cookies est défini dans `specs/ANALYTICS.md` §1.

---

## 1. BANNIÈRE COOKIES RGPD

### Quand elle s'affiche

- Au **premier chargement** du site si `localStorage.getItem('hokuno-cookie-consent')` est `null` (ni accepté ni refusé)
- Disparaît après clic sur Accepter ou Refuser
- Ne réapparaît PLUS tant que le choix est en localStorage
- Si le visiteur efface ses cookies/localStorage → la bannière réapparaît

### HTML dans theme.liquid

Placer juste avant `</body>`, avant le `<script>` de hokuno.js :

```html
<!-- Bannière cookies RGPD -->
<div class="cookie-banner" id="cookie-banner">
  <div class="cookie-content">
    <p class="cookie-text">
      Ce site utilise des cookies pour améliorer votre expérience et mesurer l'audience.
      <a href="/policies/privacy-policy" class="cookie-link">En savoir plus</a>
    </p>
    <div class="cookie-actions">
      <button class="cookie-btn cookie-refuse" onclick="refuseCookies()">Refuser</button>
      <button class="cookie-btn cookie-accept" onclick="acceptCookies()">Accepter</button>
    </div>
  </div>
</div>
```

> Le plan mentionne un bouton "Personnaliser" — en v1, on simplifie avec Accepter/Refuser uniquement. Un panneau de personnalisation (choix granulaire analytics/marketing/fonctionnel) pourra être ajouté en v2.

### CSS dans hokuno.css

```css
/* ═══ COOKIE BANNER ═══ */
.cookie-banner {
  position: fixed;
  bottom: 0;
  left: 0; right: 0;
  z-index: 10000; /* au-dessus de tout, même la navbar */
  background: rgba(10,10,10,0.97);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-top: 1px solid rgba(255,255,255,0.08);
  padding: 20px 32px;
  display: none; /* caché par défaut, affiché via JS */
}
.cookie-banner.show { display: block; }
.cookie-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
}
.cookie-text {
  font-size: 13px;
  color: rgba(255,255,255,0.7);
  line-height: 1.5;
  flex: 1;
}
.cookie-link { color: #D4A853; text-decoration: underline; }
.cookie-actions { display: flex; gap: 12px; flex-shrink: 0; }
.cookie-refuse {
  padding: 10px 20px;
  background: transparent;
  border: 1px solid rgba(255,255,255,0.2);
  color: rgba(255,255,255,0.6);
  font-size: 13px; font-weight: 600;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}
.cookie-refuse:hover { border-color: rgba(255,255,255,0.4); color: #fff; }
.cookie-accept {
  padding: 10px 20px;
  background: #D4A853;
  color: #000;
  border: none;
  font-size: 13px; font-weight: 700;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}
.cookie-accept:hover { background: #c49a3d; }

/* Mobile */
@media (max-width: 768px) {
  .cookie-banner { padding: 16px 20px; bottom: 60px; } /* au-dessus du bottom nav */
  .cookie-content { flex-direction: column; gap: 16px; text-align: center; }
  .cookie-actions { width: 100%; }
  .cookie-refuse, .cookie-accept { flex: 1; padding: 12px; }
}
```

### JS dans hokuno.js

```javascript
// ═══ COOKIES RGPD ═══

// Afficher la bannière si pas encore de choix
document.addEventListener('DOMContentLoaded', () => {
  const consent = localStorage.getItem('hokuno-cookie-consent');
  if (!consent) {
    document.getElementById('cookie-banner').classList.add('show');
  }
});

function acceptCookies() {
  localStorage.setItem('hokuno-cookie-consent', 'accepted');
  window.hokuno_consent = true;
  loadAnalytics();
  document.getElementById('cookie-banner').classList.remove('show');
}

function refuseCookies() {
  localStorage.setItem('hokuno-cookie-consent', 'refused');
  window.hokuno_consent = false;
  document.getElementById('cookie-banner').classList.remove('show');
}
```

La fonction `loadAnalytics()` est définie dans `specs/ANALYTICS.md` §1 — elle charge conditionnellement GA4, Meta Pixel et TikTok Pixel.

### Z-index

La bannière cookies est à `z-index: 10000` — au-dessus de la navbar (9999) et du bottom nav (9999). Elle ne doit jamais être cachée.

---

## 2. MENTIONS LÉGALES — `/pages/mentions-legales`

Page Shopify statique. Handle : `mentions-legales`. Template : `page.liquid`.
Lien dans le footer → colonne "Légal".

### Contenu

> **⚠️ Adapter avec tes informations réelles avant publication.**

```html
<div class="page-content">
  <h2>Mentions légales</h2>

  <h3>Éditeur du site</h3>
  <p>
    <strong>HOKUNO</strong><br>
    [Nom et prénom du responsable]<br>
    [Adresse postale complète]<br>
    [Code postal] [Ville], France<br>
    Email : <a href="mailto:altidigitech@gmail.com">altidigitech@gmail.com</a><br>
    SIRET : [numéro SIRET si auto-entrepreneur]<br>
    TVA intracommunautaire : [numéro TVA si applicable, sinon "Non applicable — régime micro-entreprise"]
  </p>

  <h3>Directeur de la publication</h3>
  <p>[Nom et prénom du responsable]</p>

  <h3>Hébergeur</h3>
  <p>
    <strong>Shopify Inc.</strong><br>
    151 O'Connor Street, Ground Floor<br>
    Ottawa, Ontario, K2P 2L8, Canada<br>
    <a href="https://www.shopify.com">www.shopify.com</a>
  </p>

  <h3>Propriété intellectuelle</h3>
  <p>L'ensemble du contenu de ce site (textes, images, designs, logos, marque HOKUNO et ホクノ) est protégé par le droit d'auteur et le droit des marques. Toute reproduction, même partielle, est interdite sans autorisation écrite préalable.</p>
  <p>Les designs vendus sur ce site sont des créations originales. Ils constituent des parodies artistiques au sens de l'article L.122-5 du Code de la propriété intellectuelle.</p>

  <h3>Données personnelles</h3>
  <p>Consultez notre <a href="/policies/privacy-policy">Politique de confidentialité</a> pour en savoir plus sur la collecte et le traitement de vos données personnelles.</p>
</div>
```

---

## 3. CONDITIONS GÉNÉRALES DE VENTE — `/policies/terms-of-service`

Shopify Admin → Settings → Policies → Terms of service.

### Contenu

```
CONDITIONS GÉNÉRALES DE VENTE — HOKUNO

Dernière mise à jour : [date de lancement]

1. OBJET

Les présentes Conditions Générales de Vente (CGV) régissent les relations contractuelles entre HOKUNO (ci-après "le Vendeur") et toute personne effectuant un achat sur le site hokuno.com (ci-après "le Client").

2. PRODUITS

2.1. Les produits proposés sont des articles textiles, mugs, coques de téléphone et accessoires imprimés à la demande (print on demand). Chaque produit est fabriqué après commande par nos partenaires de production.

2.2. Les photographies et descriptions des produits sont aussi fidèles que possible. Des variations mineures de couleur peuvent survenir en raison des différences d'écrans et du processus d'impression.

2.3. Tailles disponibles pour les t-shirts : S, M, L, XL.

3. PRIX

3.1. Les prix sont indiqués en euros (€) toutes taxes comprises (TTC) pour le marché européen, et en dollars ($) pour le marché international.

3.2. Les frais de livraison sont calculés au moment du checkout selon la destination. La livraison est gratuite à partir de 60€ de commande.

3.3. Le Vendeur se réserve le droit de modifier ses prix à tout moment. Les produits sont facturés au prix en vigueur au moment de la commande.

4. COMMANDE

4.1. Le Client passe commande via le site internet en ajoutant les produits au panier et en complétant le processus de checkout.

4.2. La validation de la commande implique l'acceptation des présentes CGV.

4.3. Un email de confirmation est envoyé au Client après validation du paiement.

5. PAIEMENT

5.1. Le paiement est exigible immédiatement à la commande.

5.2. Moyens de paiement acceptés : Visa, Mastercard, American Express, Apple Pay, Google Pay, Shop Pay, PayPal.

5.3. Les paiements sont sécurisés via Shopify Payments (cryptage SSL).

6. FABRICATION ET LIVRAISON

6.1. Les produits étant fabriqués à la commande, un délai de fabrication de 3 à 7 jours ouvrés s'applique avant l'expédition.

6.2. Délais de livraison estimés après expédition :
- France / Union Européenne : 5 à 10 jours ouvrés
- États-Unis : 3 à 7 jours ouvrés
- Canada : 5 à 12 jours ouvrés
- International : 7 à 21 jours ouvrés

6.3. Un numéro de suivi est communiqué par email dès l'expédition.

6.4. Le Vendeur ne peut être tenu responsable des retards imputables au transporteur ou aux services douaniers.

7. DROIT DE RÉTRACTATION

7.1. Conformément à l'article L.221-18 du Code de la consommation, le Client dispose d'un délai de 14 jours à compter de la réception du produit pour exercer son droit de rétractation, sans avoir à justifier de motifs ni à payer de pénalités.

7.2. Les produits fabriqués à la commande et personnalisés peuvent être exclus du droit de rétractation conformément à l'article L.221-28 du Code de la consommation. Cependant, HOKUNO accepte les retours sous les conditions définies à l'article 8.

8. RETOURS ET REMBOURSEMENTS

8.1. Le Client dispose de 30 jours après réception pour retourner un produit.

8.2. Conditions de retour :
- Le produit doit être non porté, non lavé et dans son état d'origine
- L'étiquette doit être présente
- Le Client doit contacter altidigitech@gmail.com avant tout retour pour obtenir les instructions

8.3. Les frais de retour sont à la charge du Client, sauf en cas de produit défectueux ou d'erreur de livraison.

8.4. Le remboursement est effectué sous 14 jours après réception et vérification du produit retourné, sur le moyen de paiement utilisé lors de la commande.

8.5. Les frais de livraison initiaux ne sont pas remboursés, sauf en cas de produit défectueux.

8.6. L'échange est possible sous réserve de disponibilité.

9. GARANTIES

9.1. Tous les produits bénéficient de la garantie légale de conformité (articles L.217-4 à L.217-14 du Code de la consommation) et de la garantie contre les vices cachés (articles 1641 à 1649 du Code civil).

9.2. En cas de produit défectueux (erreur d'impression, défaut de fabrication), le Client peut demander le remplacement ou le remboursement intégral, frais de retour inclus.

10. PROPRIÉTÉ INTELLECTUELLE

10.1. Les designs, logos, textes et contenus du site sont la propriété exclusive de HOKUNO.

10.2. Toute reproduction, diffusion ou utilisation sans autorisation est interdite.

11. DONNÉES PERSONNELLES

Le traitement des données personnelles est détaillé dans notre Politique de confidentialité, accessible à l'adresse /policies/privacy-policy.

12. DROIT APPLICABLE

12.1. Les présentes CGV sont soumises au droit français.

12.2. En cas de litige, le Client peut recourir à un médiateur de la consommation. Le médiateur compétent est : [nom et coordonnées du médiateur — à compléter, ou utiliser la plateforme européenne de résolution des litiges : https://ec.europa.eu/consumers/odr].

12.3. À défaut de résolution amiable, les tribunaux français seront compétents.

13. CONTACT

Pour toute question relative aux présentes CGV :
Email : altidigitech@gmail.com
```

---

## 4. POLITIQUE DE CONFIDENTIALITÉ — `/policies/privacy-policy`

Shopify Admin → Settings → Policies → Privacy policy.

### Contenu

```
POLITIQUE DE CONFIDENTIALITÉ — HOKUNO

Dernière mise à jour : [date de lancement]

HOKUNO (ci-après "nous") s'engage à protéger vos données personnelles conformément au Règlement Général sur la Protection des Données (RGPD - Règlement UE 2016/679).

1. DONNÉES COLLECTÉES

Nous collectons les données suivantes :
- Données d'identification : nom, prénom, adresse email
- Données de livraison : adresse postale, téléphone
- Données de paiement : traitées directement par Shopify Payments (nous ne stockons pas vos données bancaires)
- Données de navigation : pages visitées, durée de visite (uniquement si vous acceptez les cookies)

2. FINALITÉS DU TRAITEMENT

Vos données sont utilisées pour :
- Traiter et livrer vos commandes (base légale : exécution du contrat)
- Vous envoyer les emails transactionnels liés à votre commande (base légale : exécution du contrat)
- Vous envoyer la newsletter (base légale : consentement — inscription volontaire)
- Mesurer l'audience du site via Google Analytics et Meta Pixel (base légale : consentement — acceptation des cookies)
- Améliorer nos services et notre site (base légale : intérêt légitime)

3. PARTAGE DES DONNÉES

Vos données sont partagées avec :
- Printify (fabrication et expédition des commandes) — sous-traitant basé en Lettonie/USA
- Transporteurs (livraison) — DHL, USPS, ou autre selon la destination
- Shopify Inc. (hébergement de la boutique) — basé au Canada
- Google Analytics (mesure d'audience) — uniquement si cookies acceptés
- Meta / Facebook (publicité et mesure) — uniquement si cookies acceptés

Nous ne vendons jamais vos données à des tiers.

4. DURÉE DE CONSERVATION

- Données de commande : 5 ans (obligation comptable et fiscale)
- Données de compte client : jusqu'à suppression du compte par le client
- Données de newsletter : jusqu'à désinscription
- Données de navigation (cookies) : 13 mois maximum (recommandation CNIL)

5. VOS DROITS (RGPD)

Vous disposez des droits suivants :
- Droit d'accès : obtenir une copie de vos données personnelles
- Droit de rectification : corriger des données inexactes
- Droit à l'effacement : demander la suppression de vos données
- Droit à la portabilité : recevoir vos données dans un format structuré
- Droit d'opposition : vous opposer au traitement de vos données
- Droit à la limitation : demander la restriction du traitement

Pour exercer ces droits, contactez-nous à : altidigitech@gmail.com

Délai de réponse : 30 jours maximum.

6. COOKIES

Notre site utilise des cookies :
- Cookies essentiels : fonctionnement du panier, session client (toujours actifs)
- Cookies analytiques : Google Analytics — mesure d'audience (soumis à consentement)
- Cookies marketing : Meta Pixel, TikTok Pixel — publicité ciblée (soumis à consentement)

Vous pouvez accepter ou refuser les cookies non essentiels via la bannière affichée à votre première visite. Votre choix est conservé et peut être modifié à tout moment en effaçant les cookies de votre navigateur.

7. SÉCURITÉ

Vos données sont protégées par :
- Chiffrement SSL/TLS sur toutes les pages du site
- Hébergement sécurisé par Shopify (certifié PCI DSS Level 1)
- Accès restreint aux données (seul le responsable du site y a accès)

8. TRANSFERTS HORS UE

Certains de nos sous-traitants sont basés hors de l'Union Européenne (Shopify au Canada, Printify aux USA/Lettonie, Google et Meta aux USA). Ces transferts sont encadrés par les Clauses Contractuelles Types de la Commission Européenne et/ou les décisions d'adéquation applicables.

9. RÉCLAMATION

Si vous estimez que le traitement de vos données n'est pas conforme, vous pouvez introduire une réclamation auprès de la CNIL :
Commission Nationale de l'Informatique et des Libertés
3 place de Fontenoy, 75007 Paris
www.cnil.fr

10. CONTACT

Pour toute question relative à vos données personnelles :
Email : altidigitech@gmail.com
```

---

## 5. POLITIQUE DE RETOUR — `/policies/refund-policy`

Shopify Admin → Settings → Policies → Refund policy.

### Contenu

```
POLITIQUE DE RETOUR ET REMBOURSEMENT — HOKUNO

Dernière mise à jour : [date de lancement]

1. DÉLAI DE RETOUR

Vous disposez de 30 jours après réception de votre commande pour demander un retour.

2. CONDITIONS

Pour être éligible au retour, le produit doit être :
- Non porté et non lavé
- Dans son état d'origine
- Avec l'étiquette d'origine

3. PROCÉDURE

1. Contactez-nous à altidigitech@gmail.com en précisant votre numéro de commande et le motif du retour
2. Nous vous enverrons les instructions de retour sous 48h
3. Expédiez le produit à l'adresse indiquée
4. Dès réception et vérification, nous procédons au remboursement

4. FRAIS DE RETOUR

Les frais de retour sont à la charge du client, sauf en cas de :
- Produit défectueux (erreur d'impression, défaut de fabrication)
- Erreur de livraison (mauvais produit ou mauvaise taille)

Dans ces cas, nous prenons en charge les frais de retour et proposons un remplacement ou un remboursement intégral.

5. REMBOURSEMENT

- Délai : sous 14 jours après réception du produit retourné
- Moyen : sur le moyen de paiement utilisé lors de la commande
- Montant : prix du produit (les frais de livraison initiaux ne sont pas remboursés, sauf erreur de notre part)

6. ÉCHANGE

L'échange est possible sous réserve de disponibilité. Contactez-nous pour vérifier.

7. PRODUITS NON RETOURNABLES

Les produits suivants ne peuvent pas être retournés :
- Produits portés, lavés ou endommagés par le client
- Produits sans étiquette d'origine

8. PRODUITS DÉFECTUEUX

Si vous recevez un produit défectueux, contactez-nous immédiatement avec une photo du défaut. Nous vous proposerons un remplacement ou un remboursement intégral sans frais.

9. CONTACT

Email : altidigitech@gmail.com
Délai de réponse : 24-48h
```

---

## 6. POLITIQUE D'EXPÉDITION — `/policies/shipping-policy`

Shopify Admin → Settings → Policies → Shipping policy.

### Contenu

```
POLITIQUE D'EXPÉDITION — HOKUNO

Dernière mise à jour : [date de lancement]

1. FABRICATION

Tous nos produits sont fabriqués à la commande (print on demand). Chaque pièce est imprimée spécialement pour vous après validation de votre commande.

Délai de fabrication : 3 à 7 jours ouvrés.

2. LIVRAISON

Délais de livraison estimés après expédition :

| Destination | Délai estimé |
|-------------|-------------|
| France | 5-10 jours ouvrés |
| Union Européenne | 5-10 jours ouvrés |
| États-Unis | 3-7 jours ouvrés |
| Canada | 5-12 jours ouvrés |
| Australie | 7-15 jours ouvrés |
| International | 7-21 jours ouvrés |

Délai total (fabrication + livraison) : 8 à 28 jours ouvrés selon la destination.

3. FRAIS DE LIVRAISON

- Livraison GRATUITE à partir de 60€ de commande
- En dessous de 60€ : frais calculés automatiquement au checkout selon votre destination

4. SUIVI

Un numéro de suivi vous est envoyé par email dès l'expédition de votre commande. Vous pouvez suivre votre colis en temps réel.

5. PROBLÈMES DE LIVRAISON

En cas de colis perdu, endommagé ou non livré, contactez-nous à altidigitech@gmail.com avec votre numéro de commande. Nous ferons le nécessaire avec le transporteur.

6. DOUANES ET TAXES

Pour les livraisons hors Union Européenne, des droits de douane ou taxes d'importation peuvent s'appliquer. Ces frais sont à la charge du client et dépendent de la réglementation du pays de destination.
```

---

## 7. RÉCAPITULATIF — OÙ CONFIGURER QUOI

| Contenu | Emplacement Shopify | URL publique |
|---------|--------------------:|-------------|
| Bannière cookies | Theme.liquid (code HTML/CSS/JS) | Apparaît sur toutes les pages |
| Mentions légales | Pages → Nouvelle page (handle: `mentions-legales`) | `/pages/mentions-legales` |
| CGV | Settings → Policies → Terms of service | `/policies/terms-of-service` |
| Confidentialité | Settings → Policies → Privacy policy | `/policies/privacy-policy` |
| Retours | Settings → Policies → Refund policy | `/policies/refund-policy` |
| Expédition | Settings → Policies → Shipping policy | `/policies/shipping-policy` |

### Éléments à personnaliser avant publication

| Placeholder | Où le trouver | Quoi mettre |
|------------|--------------|-------------|
| `[Nom et prénom du responsable]` | Mentions légales | Ton nom complet |
| `[Adresse postale complète]` | Mentions légales | Ton adresse pro |
| `[numéro SIRET]` | Mentions légales | Ton SIRET auto-entrepreneur |
| `[numéro TVA]` | Mentions légales | TVA intracommunautaire ou "Non applicable" |
| `[date de lancement]` | Tous les documents | Date réelle du lancement |
| `[médiateur]` | CGV §12.2 | Nom du médiateur de la consommation |
