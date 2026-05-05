# TODO — Hokuno Store

## État actuel (2026-05-05)

- **430 produits** Printify (shop ID `22774508`, **shop disconnected**) — audité API le 2026-05-05
- **Tailles t-shirts** : 2XL–5XL désactivées sur 44/48 t-shirts (4 échecs API 500 — à faire manuellement)
- **Collection Wanted** : 46/46 personnages × FR+EN × light+dark + mugs = 276 produits ✅
- **Collection Direction** : 10/10 × FR+EN × light+dark + mugs = 80 produits ✅
- **Collection Mythologie** : 10/10 × light+dark + mugs + coques = 40 produits ✅
- **Collection Design Hokuno** : 13 t-shirts + 21 accessoires = 34 produits ✅
- Aucun canal de vente connecté (Shopify, TikTok Shop)

---

## 🔴 URGENT — Corrections Printify (API 500 — manuel dashboard)

Ces 4 produits Design Hokuno sont bloqués en API 500 sur toute opération PUT :

- [ ] **Désactiver XXL** sur ces 4 t-shirts :
  - `69f8febcbd4ffcafc502864d` — T-Shirt Design Orbite Hokuno Dark (Black+Tweed 2XL–5XL)
  - `69f8c689c7a7db441d0c58fc` — T-Shirt Design Hokuno Dark (Black+Tweed 2XL–5XL)
  - `69f8c577011b67ecf8078e65` — T-Shirt Design HO KU NO Dark (Black+Tweed 2XL–5XL)
  - `69f8959bfeed9979d10d1130` — T-Shirt Sport Design Hokuno Light (Ice Grey+White 2XL–5XL)

- [ ] **Corriger les titres** (trailing space) :
  - `69f8febcbd4ffcafc502864d` → `T-Shirt Design Orbite Hokuno Dark` (supprimer espace en fin)
  - `69f8c689c7a7db441d0c58fc` → `T-Shirt Design Hokuno Dark` (supprimer espace en fin)

- [ ] **Mettre à jour la description** manuellement sur ces 17 produits (même liste que prix) — API 500 permanents
- [ ] **Mettre à jour les prix** sur 17 produits bloqués :
  *(413/430 déjà mis à jour via script le 2026-05-05)*
  - `69f90268ad402ce2b4035348` — Maillot De Bain Design Hokuno Dark → 49.99 $
  - `69f8febcbd4ffcafc502864d` — T-Shirt Design Orbite Hokuno Dark → 37.99 $
  - `69f8ce23b2e670c7080e5639` — Bob Hokuno Design Dark → 39.99 $
  - `69f8cc729822413bd1037c27` — Casquette Design Hokuno Dark → 29.99 $
  - `69f8c86f09f3b73024023a0e` — T-Shirt hokuno Design Target Light → 37.99 $ ⚠️ + activer variantes
  - `69f8c689c7a7db441d0c58fc` — T-Shirt Design Hokuno Dark → 37.99 $
  - `69f8c577011b67ecf8078e65` — T-Shirt Design HO KU NO Dark → 37.99 $
  - `69f8959bfeed9979d10d1130` — T-Shirt Sport Design Hokuno Light → 37.99 $
  - `69f89408feed9979d10d1032` — Short De Bain Design Hokuno Bleu Ciel → 49.99 $
  - `69f8901b25819cdf3d057d73` — Claquette Design Hokuno Light → 54.99 $
  - `69f88e25f55196f8d00a8975` — Casquette Hokuno Light → 29.99 $
  - `69f88aadffbc831dea086dc5` — Polo Design Hokuno Boussole Light → 44.99 $
  - `69f61d909110dda91005e89b` — Coque de téléphone The End sur Brique Saga 1 → 24.99 $
  - `69f603f5ef66d02ffe02b1ce` — T-SHIRT LUFI WANTED NOIR EN 1/17 → 37.99 $
  - `69f6032239e419a2dc02e247` — T-SHIRT LUFI WANTED EN 1/17 → 37.99 $
  - `6855d70f8454e3a28e01200a` — Short de bain Design Hokuno Pattern Light → 49.99 $
  - `6855d1a12c35f6107c040a63` — Coque téléphone Design Hokuno Orbite Dark → 24.99 $

- [ ] **Supprimer** doublon T-Shirt hokuno Design Target Dark :
  - `69f9e82ec12ffe54490a4e8d` — créé 2026-05-05 (le plus récent, à supprimer)
  - Garder `69f927ba9f68ab7cf002315d` — créé 2026-05-04

- [ ] **Enquêter** T-Shirt hokuno Design Target Light `69f8c86f09f3b73024023a0e` :
  - Seule 1 variante active (White/L à $25.96) sur 560 — produit quasi inutilisable
  - Prix et variantes à reconfigurer manuellement dans le dashboard

---

## 🟡 COSMÉTIQUE — Titres à corriger (API — 68 appels)

68 t-shirts Wanted ont conservé la numérotation `/17` de la première fournée (quand il y avait 17 personnages). Le format correct est `/46`.

**Script à exécuter après validation :**
```bash
# 68 PUT /v1/shops/22774508/products/{id}.json → {"title": "T-SHIRT X WANTED Y/46"}
```

| Sous-groupe | Produits | Exemple |
|---|---|---|
| FR light | 17 | `T-SHIRT LUFI WANTED 1/17` → `1/46` |
| FR dark | 17 | `T-SHIRT LUFI WANTED NOIR 1/17` → `1/46` |
| EN light | 17 | `T-SHIRT LUFI WANTED EN 1/17` → `1/46` |
| EN dark | 17 | `T-SHIRT LUFI WANTED NOIR EN 1/17` → `1/46` |

Détail complet dans l'INVENTAIRE.md ou générable via le script d'audit.

---

## 🔵 À VÉRIFIER — Logos front Design Hokuno

7 t-shirts dark de la collection Design Hokuno n'ont **pas** le logo 74.png (`6849b65d8ee17a5b00c03855`) en front. Ils ont à la place leur propre design custom. Confirmer si c'est intentionnel ou si le logo 74.png doit être ajouté en complément :

- `69f9e82ec12ffe54490a4e8d` — T-Shirt hokuno Design Target Dark (doublon — à supprimer)
- `69f927ba9f68ab7cf002315d` — T-Shirt hokuno Design Target Dark
- `69f91fc0300b32baed0d1c48` — T-Shirt Sport Design Hokuno Dark
- `69f8febcbd4ffcafc502864d` — T-Shirt Design Orbite Hokuno Dark
- `69f8d13d05bcfe3fcd0460f9` — T-shirt Hokuno Design Empreinte Dark
- `69f8c689c7a7db441d0c58fc` — T-Shirt Design Hokuno Dark
- `69f8c577011b67ecf8078e65` — T-Shirt Design HO KU NO Dark

> **Note** : Tous les t-shirts Wanted (92 dark) et Direction (20 dark) ont le bon logo front. ✅

---

## 🟠 Produits à créer

> **Aucun produit restant à créer.** Toutes les coques Mythologie sont terminées (2026-05-05).
> Coques Direction et Wanted : hors scope définitif.

---

## 🟡 Plateforme & canaux de vente

- [ ] **Connecter Shopify** au shop Printify `22774508` (sales channel actuellement disconnected)
- [ ] **Connecter TikTok Shop** au shop Printify
- [ ] **Configurer les prix** sur Shopify pour toutes les collections (t-shirts, mugs, coques, accessoires)
- [ ] **Configurer la livraison** Shopify (zones FR, EU, international)

---

## 🟢 Boutique Shopify (à construire)

- [ ] **Landing page** immersive — Three.js 3D, glassmorphisme, animations GSAP
- [ ] **Pages collection** — Wanted / Direction / Mythologie / Design Hokuno avec storytelling
- [ ] **Pages produit** — backstory personnage, variantes, schema JSON-LD Product
- [ ] **Fichier `llms.txt`** à la racine
- [ ] **`robots.txt`** — ne pas bloquer GPTBot, ChatGPT-User, ClaudeBot, PerplexityBot
- [ ] **Bilingue FR/EN** — routing i18n
- [ ] **SEO/GEO** — JSON-LD Organization, CollectionPage, BreadcrumbList sur chaque page
- [ ] **SSR obligatoire** — contenu dans le HTML initial (Next.js ou Remix)

---

## ✅ Déjà fait

- [x] **Wanted FR** : 46/46 t-shirts light + 46/46 dark + 46/46 mugs FR = 138 produits
- [x] **Wanted EN** : 46/46 t-shirts light + 46/46 dark + 46/46 mugs EN = 138 produits
- [x] Bartolomiou Kouma ×2 EN renommés
- [x] **Direction FR t-shirts** : 10/10 light + 10/10 dark (dos + logo front scale 53.59 UI / 0.21105 API)
- [x] **Direction FR mugs** : 10/10 light (bp 478) + 10/10 dark (bp 479)
- [x] **Direction EN t-shirts** : 10/10 light + 10/10 dark
- [x] **Direction EN mugs** : 10/10 light (bp 478) + 10/10 dark (bp 479)
- [x] **Direction NOIR logo** : corrigé sur 20 t-shirts FR+EN (74.png → scale 53.59 UI)
- [x] **Mythologie t-shirts** : 10/10 light + 10/10 dark
- [x] **Mythologie mugs** : 10/10 (bp 478, images réutilisées depuis t-shirts back)
- [x] **Mythologie coques** : 10/10 slim phone cases créées (Zoro + 9 nouveaux)
- [x] **Mythologie Brook tshirt_noir standard** : créé `69f87c8cbe136844f0003b0a`
- [x] **Tailles XL max** : 2XL–5XL désactivées sur 44/48 t-shirts via API (2026-05-05)
- [x] **Variante 15oz** : activée sur 142 mugs (Wanted FR+EN + Direction FR+EN + Mythologie)
- [x] **Doublon mug Direction Luffy EN** : supprimé `684d56c509bce0c2370d3254`
- [x] **Inventaire complet** : INVENTAIRE.md régénéré depuis API — 430 produits (2026-05-05)
- [x] **Collection Design Hokuno** : inventoriée — 13 t-shirts + 21 accessoires
- [x] **Audit complet** : rapport A–F généré (2026-05-05)
- [x] **Descriptions produit** : 413/430 injectées via API (2026-05-05) — 17 bloqués API 500 (manuels)

---

## Résumé global

| Phase | Description | Statut |
|-------|-------------|--------|
| **0** | Nettoyage + titres | ✅ FAIT |
| **1** | Wanted complet FR+EN (t-shirts + mugs) — 276 produits | ✅ FAIT |
| **1-fix** | 68 titres /17→/46 (API) + 2 prix Lufi EN (manuel) | ⏳ cosmétique |
| **2** | Direction EN (t-shirts light+dark) | ✅ FAIT |
| **3** | Direction complet — mugs ✅ / coques abandonnées | ✅ FAIT |
| **4** | Mythologie mugs (✅) + Brook NOIR (✅) + coques Mythologie (✅ 10/10) | ✅ FAIT |
| **XL** | Désactiver 2XL–5XL sur tous les t-shirts | 44/48 ✅ — 4 manuels |
| **Design** | Collection Design Hokuno inventoriée | ✅ existant |
| **Audit** | Rapport A–F — 430 produits | ✅ 2026-05-05 |
| **Desc** | Descriptions HTML — 413/430 via API, 17 manuels | ✅ 2026-05-05 |
| **Shop** | Connexion Shopify + TikTok Shop | ⏳ |
| **Boutique** | Shopify FR/EN immersif | ⏳ |
