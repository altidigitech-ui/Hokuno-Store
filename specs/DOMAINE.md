# specs/DOMAINE.md — Domaine & DNS

> Contrat pour toi (actions manuelles). Achat, configuration DNS, SSL et email pro.
> Le domaine est la dernière pièce avant le lancement public.
> Référence croisée : `specs/CONFIG-SHOPIFY.md` §12, `specs/MIGRATION.md` Phase 9.

---

## 1. CHOIX DU DOMAINE

### Options par ordre de préférence

| Domaine | Extension | Avantages | Inconvénients | Prix estimé |
|---------|-----------|-----------|---------------|:-----------:|
| `hokuno.com` | .com | Standard mondial, mémorisable, confiance maximale, SEO international | Peut être déjà pris | ~12-15€/an |
| `hokuno.fr` | .fr | Identité française claire, bon pour le marché FR/EU | Moins crédible à l'international | ~6-8€/an |
| `hokuno.store` | .store | Explicite e-commerce, probablement disponible | Extension moins courante, moins de confiance | ~15-20€/an |
| `hokuno.shop` | .shop | E-commerce, court | Même problème que .store | ~25-35€/an |

**Recommandation** : `hokuno.com` si disponible, sinon `hokuno.fr`. Les extensions .store et .shop sont un dernier recours.

### Vérifier la disponibilité

- Via Shopify : Settings → Domains → Buy new domain → taper "hokuno"
- Via Namecheap : `https://www.namecheap.com/domains/registration/results/?domain=hokuno`
- Via OVH : `https://www.ovh.com/fr/domaines/` (recommandé pour les .fr)

### Acheter plusieurs extensions (optionnel)

Si le budget le permet, acheter `hokuno.com` ET `hokuno.fr` et rediriger le second vers le premier. Ceci protège la marque et capte le trafic des deux.

---

## 2. OÙ ACHETER

### Option A — Via Shopify (le plus simple)

Shopify Admin → Settings → Domains → Buy new domain

| Avantage | Détail |
|----------|--------|
| Configuration DNS automatique | Shopify configure tout |
| SSL automatique | Généré en quelques minutes |
| Renouvellement automatique | Pas d'oubli |
| Gestion centralisée | Tout dans Shopify Admin |

Prix : Shopify vend les .com à ~14$/an. Un peu plus cher que les registrars indépendants mais zéro configuration.

### Option B — Registrar externe (Namecheap, OVH, Cloudflare)

| Registrar | .com | .fr | Avantage |
|-----------|:----:|:---:|----------|
| Namecheap | ~10$/an | — | Prix bas, interface simple, WhoisGuard gratuit |
| OVH | ~10€/an | ~7€/an | Registrar français, .fr au meilleur prix |
| Cloudflare | ~9$/an | — | Prix coûtant (0 marge), DNS ultra-rapide |

Si achat externe, la configuration DNS est manuelle (section 3 ci-dessous).

---

## 3. CONFIGURATION DNS

### Si acheté via Shopify

Rien à faire. Shopify configure automatiquement les enregistrements DNS. Passer directement à la section 4.

### Si acheté via un registrar externe

Aller dans le panneau DNS du registrar et ajouter ces enregistrements :

| Type | Nom / Host | Valeur / Target | TTL |
|------|-----------|-----------------|:---:|
| A | `@` | `23.227.38.65` | 3600 |
| CNAME | `www` | `shops.myshopify.com` | 3600 |

> `@` représente le domaine racine (ex : `hokuno.com`).
> Le CNAME `www` redirige `www.hokuno.com` vers Shopify.

### Supprimer les enregistrements par défaut

Les registrars ajoutent souvent des enregistrements par défaut (parking, redirect). Les supprimer avant d'ajouter les enregistrements Shopify, sinon il y aura des conflits.

### Connecter dans Shopify

Après la configuration DNS :

1. Shopify Admin → Settings → Domains → Connect existing domain
2. Entrer `hokuno.com` (ou le domaine choisi)
3. Shopify vérifie les DNS (peut prendre jusqu'à 48h, souvent < 1h)
4. Statut : "Connected" → prêt

### Propagation DNS

Les changements DNS prennent entre 15 minutes et 48h pour se propager mondialement. En pratique, c'est souvent 1-2h.

Vérifier la propagation : `https://www.whatsmydns.net/#A/hokuno.com`

---

## 4. SSL (HTTPS)

### Génération automatique

Shopify génère automatiquement un certificat SSL (Let's Encrypt) pour chaque domaine connecté. Le processus prend quelques minutes après la connexion du domaine.

### Vérification

1. Ouvrir `https://hokuno.com` dans le navigateur
2. Vérifier le cadenas vert dans la barre d'adresse
3. Si le cadenas n'apparaît pas après 1h → Settings → Domains → Activate SSL certificate

### Forcer HTTPS

Shopify force automatiquement HTTPS sur toutes les pages. Aucune configuration nécessaire. Les requêtes HTTP sont redirigées vers HTTPS.

---

## 5. REDIRECTION WWW

### Configuration

Shopify Admin → Settings → Domains → Choisir le domaine principal.

| Option | Résultat |
|--------|---------|
| `hokuno.com` comme principal | `www.hokuno.com` redirige vers `hokuno.com` |
| `www.hokuno.com` comme principal | `hokuno.com` redirige vers `www.hokuno.com` |

**Recommandation** : `hokuno.com` sans www — plus court, plus moderne.

Shopify gère la redirection 301 automatiquement.

---

## 6. EMAIL PROFESSIONNEL

Le domaine permet de créer un email pro (`contact@hokuno.com` au lieu de `altidigitech@gmail.com`).

### Option A — Google Workspace (recommandé)

| Paramètre | Valeur |
|-----------|--------|
| Plan | Business Starter (6$/mois/utilisateur) |
| Adresses | `contact@hokuno.com`, `support@hokuno.com` |
| Avantages | Gmail familier, Google Drive, Calendar, 30 Go stockage |

Configuration DNS (enregistrements MX à ajouter chez le registrar) :

| Type | Priorité | Valeur |
|------|:--------:|--------|
| MX | 1 | `ASPMX.L.GOOGLE.COM` |
| MX | 5 | `ALT1.ASPMX.L.GOOGLE.COM` |
| MX | 5 | `ALT2.ASPMX.L.GOOGLE.COM` |
| MX | 10 | `ALT3.ASPMX.L.GOOGLE.COM` |
| MX | 10 | `ALT4.ASPMX.L.GOOGLE.COM` |

### Option B — Zoho Mail (gratuit jusqu'à 5 utilisateurs)

| Paramètre | Valeur |
|-----------|--------|
| Plan | Free (5 utilisateurs, 5 Go/utilisateur) |
| Adresses | `contact@hokuno.com` |
| Avantages | Gratuit, suffisant pour démarrer |
| Inconvénients | Interface moins familière que Gmail |

### Option C — Pas d'email pro (v1)

Garder `altidigitech@gmail.com` pour le lancement. Configurer l'email pro plus tard quand les ventes justifient le coût.

**Recommandation** : Option C pour le lancement, Option A quand les revenus le permettent.

---

## 7. MISE À JOUR APRÈS ACHAT DU DOMAINE

Après l'achat et la configuration du domaine, mettre à jour :

| Où | Quoi changer |
|----|-------------|
| Shopify → Settings → Store details | URL du store |
| Shopify → Settings → Markets | Domaines par marché |
| Google Search Console | Ajouter la propriété `https://hokuno.com` |
| Google Analytics 4 | Mettre à jour l'URL du site |
| Meta Business Suite | Mettre à jour le domaine vérifié |
| `specs/SEO.md` → llms.txt | Remplacer les URLs placeholder |
| `specs/SEO.md` → Schema Organization | `url` reflète le nouveau domaine |
| Réseaux sociaux | Lien en bio TikTok, Instagram |

---

## 8. TIMING

```
Phase 6 — Thème codé et validé visuellement
Phase 7 — Configuration Shopify (pages, paiements, livraison, etc.)
Phase 8 — Vérification (checklist complète)
   ↓
▶ ACHETER LE DOMAINE ICI
   ↓
Phase 9 — Lancement (publier thème, désactiver mot de passe)
```

**Pourquoi attendre** : acheter le domaine trop tôt signifie payer pour un domaine inutilisé pendant les semaines de développement. Le domaine est la dernière pièce — on le connecte quand tout le reste est prêt.

**Exception** : si `hokuno.com` est disponible et que tu crains qu'il soit pris, achète-le immédiatement pour le réserver, même si tu ne le connectes pas tout de suite.

---

## 9. CHECKLIST DOMAINE

- [ ] Domaine acheté (hokuno.com / .fr / .store)
- [ ] DNS configurés (A Record + CNAME)
- [ ] Domaine connecté dans Shopify (Settings → Domains → statut "Connected")
- [ ] SSL actif (cadenas vert dans le navigateur)
- [ ] Redirection www fonctionnelle
- [ ] Google Search Console : propriété ajoutée et vérifiée
- [ ] GA4 : URL du site mise à jour
- [ ] Sitemap soumis dans Search Console (`https://hokuno.com/sitemap.xml`)
