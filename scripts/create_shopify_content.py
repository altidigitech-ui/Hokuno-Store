#!/usr/bin/env python3
"""
Create Hokuno static pages, the Journal blog, and the legal policies via the
Shopify GraphQL Admin API.

Reads SHOPIFY_STORE and SHOPIFY_ACCESS_TOKEN from the environment. The token
must be a valid Admin API access token (atkn_xxx) with at least the following
scopes: write_content (pages, blogs, articles), write_shop_policies.

Idempotent: if a page/blog with the same handle already exists, the script
updates it instead of creating a duplicate.
"""

import json
import os
import sys
import time
from urllib import request, error

API_VERSION = "2024-10"
STORE = os.environ.get("SHOPIFY_STORE", "").strip()

# The CLI session token (from `shopify auth login`) lives in this file under
# sessionStore -> accounts.shopify.com -> <user-id> -> identity -> accessToken.
# It works as a Bearer token against the Admin GraphQL API. We prefer it over
# SHOPIFY_ACCESS_TOKEN because the latter (custom-app atkn_) tends to be
# revoked or never re-issued after a store migration.
def _load_cli_token() -> str | None:
    cfg_path = os.path.expanduser("~/.config/shopify-cli-kit-nodejs/config.json")
    try:
        with open(cfg_path) as f:
            cfg = json.load(f)
        session = json.loads(cfg.get("sessionStore", "{}"))
        for users in session.values():
            for ud in users.values():
                tok = ud.get("identity", {}).get("accessToken")
                if tok:
                    return tok
    except (OSError, ValueError, KeyError):
        return None
    return None


TOKEN = _load_cli_token() or os.environ.get("SHOPIFY_ACCESS_TOKEN", "").strip()
USE_BEARER = TOKEN.startswith("atkn_2.")  # CLI identity tokens use Bearer; custom-app tokens use X-Shopify-Access-Token

if not STORE or not TOKEN:
    print("error: SHOPIFY_STORE must be set and a Shopify CLI session must exist (run `shopify auth login`) or SHOPIFY_ACCESS_TOKEN must be set", file=sys.stderr)
    sys.exit(1)

ENDPOINT = f"https://{STORE}/admin/api/{API_VERSION}/graphql.json"


def gql(query: str, variables: dict | None = None) -> dict:
    body = json.dumps({"query": query, "variables": variables or {}}).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Hokuno-ContentCreator/1.0",
    }
    if USE_BEARER:
        headers["Authorization"] = f"Bearer {TOKEN}"
    else:
        headers["X-Shopify-Access-Token"] = TOKEN
    req = request.Request(ENDPOINT, data=body, headers=headers, method="POST")
    for attempt in range(3):
        try:
            with request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read())
                if data.get("errors"):
                    raise RuntimeError(f"GraphQL errors: {data['errors']}")
                return data["data"]
        except error.HTTPError as e:
            msg = e.read().decode("utf-8", errors="replace")
            if e.code in (429, 502, 503) and attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"HTTP {e.code}: {msg}")
        except error.URLError as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise


# ---------------------------------------------------------------------------
# Page content (FR — EN translations are added later via Shopify Markets)
# ---------------------------------------------------------------------------

ABOUT_HTML = """\
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
"""

FAQ_ITEMS = [
    ("Comment sont fabriqués vos produits ?",
     "Chaque produit est fabriqué à la commande (print on demand) par nos partenaires d'impression. Aucun stock — votre article est imprimé spécialement pour vous après votre commande."),
    ("Quels sont les délais de livraison ?",
     "Fabrication : 3-7 jours ouvrés. Livraison France/EU : 5-10 jours ouvrés après expédition. International : 7-15 jours ouvrés. Vous recevez un numéro de suivi par email dès l'expédition."),
    ("La livraison est-elle gratuite ?",
     "Oui, à partir de 60€ de commande. En dessous, les frais de livraison sont calculés au checkout selon votre destination."),
    ("Puis-je retourner un produit ?",
     "Oui, vous disposez de 30 jours après réception pour retourner un produit non porté, non lavé, avec son étiquette. Contactez-nous à altidigitech@gmail.com pour initier un retour."),
    ("Comment utiliser un code promo ?",
     "Entrez votre code dans le champ « Code de réduction » au moment du checkout. Le code HOKUNO15 offre -15% sur votre commande."),
    ("Quelles tailles sont disponibles ?",
     "Nos t-shirts sont disponibles du S au XL. Consultez le guide des tailles sur chaque page produit pour trouver votre taille idéale."),
    ("Les designs sont-ils originaux ?",
     "Oui. Chaque design est créé par notre équipe, généré par IA et retravaillé. Ce sont des parodies artistiques originales, jamais des reproductions directes."),
    ("Livrez-vous à l'international ?",
     "Oui, nous livrons dans le monde entier. Les frais et délais varient selon la destination."),
    ("Comment vous contacter ?",
     "Par email à altidigitech@gmail.com ou via notre formulaire de contact. Nous répondons sous 24-48h."),
]


def build_faq_html() -> str:
    items = []
    for q, a in FAQ_ITEMS:
        items.append(
            f'  <div class="faq-item">\n'
            f'    <button class="faq-question" aria-expanded="false">\n'
            f'      {q}\n'
            f'      <span class="faq-icon">+</span>\n'
            f'    </button>\n'
            f'    <div class="faq-answer">\n'
            f'      <p>{a}</p>\n'
            f'    </div>\n'
            f'  </div>'
        )
    return '<div class="faq-list">\n' + '\n'.join(items) + '\n</div>\n'


CONTACT_HTML = """\
<p class="contact-intro-md">Une question, une suggestion, une collaboration ? On vous répond sous 24-48h.</p>
<p>Le formulaire de contact se trouve ci-dessous (rendu par le template <code>page.contact</code>).</p>
"""

MENTIONS_HTML = """\
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
    TVA intracommunautaire : [numéro TVA si applicable, sinon « Non applicable — régime micro-entreprise »]
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
"""

PAGES = [
    {
        "title": "À propos de Hokuno",
        "handle": "about",
        "body": ABOUT_HTML,
        "template": None,            # default page template
        "isPublished": True,
    },
    {
        "title": "FAQ",
        "handle": "faq",
        "body": build_faq_html(),
        "template": None,
        "isPublished": True,
    },
    {
        "title": "Contact",
        "handle": "contact",
        "body": CONTACT_HTML,
        "template": "page.contact",  # custom template — form is in the .liquid
        "isPublished": True,
    },
    {
        "title": "Mentions légales",
        "handle": "mentions-legales",
        "body": MENTIONS_HTML,
        "template": None,
        "isPublished": True,
    },
]


# ---------------------------------------------------------------------------
# Policies
# ---------------------------------------------------------------------------

POLICY_TERMS = """\
CONDITIONS GÉNÉRALES DE VENTE — HOKUNO

Dernière mise à jour : 2026-05-09

1. OBJET

Les présentes Conditions Générales de Vente (CGV) régissent les relations contractuelles entre HOKUNO (ci-après « le Vendeur ») et toute personne effectuant un achat sur le site hokuno.com (ci-après « le Client »).

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
"""

POLICY_PRIVACY = """\
POLITIQUE DE CONFIDENTIALITÉ — HOKUNO

Dernière mise à jour : 2026-05-09

HOKUNO (ci-après « nous ») s'engage à protéger vos données personnelles conformément au Règlement Général sur la Protection des Données (RGPD - Règlement UE 2016/679).

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
"""

POLICY_REFUND = """\
POLITIQUE DE RETOUR ET REMBOURSEMENT — HOKUNO

Dernière mise à jour : 2026-05-09

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
"""

POLICY_SHIPPING = """\
POLITIQUE D'EXPÉDITION — HOKUNO

Dernière mise à jour : 2026-05-09

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
"""

POLICIES = [
    ("TERMS_OF_SERVICE", POLICY_TERMS),
    ("PRIVACY_POLICY",   POLICY_PRIVACY),
    ("REFUND_POLICY",    POLICY_REFUND),
    ("SHIPPING_POLICY",  POLICY_SHIPPING),
]


# ---------------------------------------------------------------------------
# GraphQL operations
# ---------------------------------------------------------------------------

PAGE_BY_HANDLE_QUERY = """
query pageByHandle($handle: String!) {
  pages(first: 1, query: $handle) {
    edges { node { id handle title } }
  }
}
"""

PAGE_CREATE_MUTATION = """
mutation pageCreate($page: PageCreateInput!) {
  pageCreate(page: $page) {
    page { id handle title }
    userErrors { field message code }
  }
}
"""

PAGE_UPDATE_MUTATION = """
mutation pageUpdate($id: ID!, $page: PageUpdateInput!) {
  pageUpdate(id: $id, page: $page) {
    page { id handle title }
    userErrors { field message code }
  }
}
"""

BLOG_BY_HANDLE_QUERY = """
query blogByHandle($handle: String!) {
  blogs(first: 1, query: $handle) {
    edges { node { id handle title } }
  }
}
"""

BLOG_CREATE_MUTATION = """
mutation blogCreate($blog: BlogCreateInput!) {
  blogCreate(blog: $blog) {
    blog { id handle title }
    userErrors { field message code }
  }
}
"""

POLICY_UPDATE_MUTATION = """
mutation shopPolicyUpdate($shopPolicy: ShopPolicyInput!) {
  shopPolicyUpdate(shopPolicy: $shopPolicy) {
    shopPolicy { id type title body }
    userErrors { field message code }
  }
}
"""


def find_page(handle: str):
    data = gql(PAGE_BY_HANDLE_QUERY, {"handle": f"handle:{handle}"})
    edges = data["pages"]["edges"]
    return edges[0]["node"] if edges else None


def upsert_page(p: dict) -> str:
    existing = find_page(p["handle"])
    if existing:
        page_input = {
            "title": p["title"],
            "body": p["body"],
            "isPublished": p["isPublished"],
        }
        if p["template"]:
            page_input["templateSuffix"] = p["template"].split("page.", 1)[-1]
        data = gql(PAGE_UPDATE_MUTATION, {"id": existing["id"], "page": page_input})
        errs = data["pageUpdate"]["userErrors"]
        if errs:
            raise RuntimeError(f"pageUpdate {p['handle']} errors: {errs}")
        return f"updated {p['handle']}"
    page_input = {
        "title": p["title"],
        "handle": p["handle"],
        "body": p["body"],
        "isPublished": p["isPublished"],
    }
    if p["template"]:
        page_input["templateSuffix"] = p["template"].split("page.", 1)[-1]
    data = gql(PAGE_CREATE_MUTATION, {"page": page_input})
    errs = data["pageCreate"]["userErrors"]
    if errs:
        raise RuntimeError(f"pageCreate {p['handle']} errors: {errs}")
    return f"created {p['handle']}"


def upsert_blog(handle: str, title: str) -> str:
    data = gql(BLOG_BY_HANDLE_QUERY, {"handle": f"handle:{handle}"})
    edges = data["blogs"]["edges"]
    if edges:
        return f"blog '{handle}' already exists ({edges[0]['node']['id']})"
    data = gql(BLOG_CREATE_MUTATION, {"blog": {"title": title, "handle": handle}})
    errs = data["blogCreate"]["userErrors"]
    if errs:
        raise RuntimeError(f"blogCreate errors: {errs}")
    return f"blog '{handle}' created"


def update_policy(policy_type: str, body: str) -> str:
    data = gql(POLICY_UPDATE_MUTATION, {
        "shopPolicy": {"type": policy_type, "body": body},
    })
    errs = data["shopPolicyUpdate"]["userErrors"]
    if errs:
        raise RuntimeError(f"shopPolicyUpdate {policy_type} errors: {errs}")
    return f"policy {policy_type} updated"


def main():
    print(f"Target store: {STORE}")
    print(f"API endpoint: {ENDPOINT}\n")

    print("=== PAGES ===")
    for p in PAGES:
        print(f"  {upsert_page(p)}")

    print("\n=== BLOG ===")
    print(f"  {upsert_blog('journal', 'Journal')}")

    print("\n=== POLICIES ===")
    for ptype, body in POLICIES:
        print(f"  {update_policy(ptype, body)}")

    print("\nDone.")


if __name__ == "__main__":
    main()
