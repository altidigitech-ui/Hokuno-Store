# TODO — Hokuno Store

## État actuel (2026-05-05)

- **430 produits** Printify (shop ID `22774508`, **shop disconnected**) — vérifié API le 2026-05-05
- **Tailles t-shirts** : 2XL–5XL désactivées sur 44/48 t-shirts (4 échecs API 500 — à faire manuellement)
- **Collection Wanted** : 46/46 personnages × FR+EN × light+dark + mugs = 276 produits ✅
- **Collection Direction** : 10/10 × FR+EN × light+dark + mugs = 80 produits ✅ (+1 doublon à supprimer)
- **Collection Mythologie** : 10/10 × light+dark + mugs + 1 coque = 31 produits ✅
- **Collection Design Hokuno** : 13 t-shirts + 21 accessoires = 34 produits ✅
- Aucun canal de vente connecté (Shopify, TikTok Shop)

---

## 🔴 URGENT — Corrections Printify

- [ ] **Désactiver XXL manuellement** sur 4 t-shirts (API 500 bloque le script) :
  - `69f8febcbd4ffcafc502864d` — T-Shirt Design Orbite Hokuno Dark
  - `69f8c689c7a7db441d0c58fc` — T-Shirt Design Hokuno Dark
  - `69f8c577011b67ecf8078e65` — T-Shirt Design HO KU NO Dark
  - `69f8959bfeed9979d10d1130` — T-Shirt Sport Design Hokuno Light

- [ ] **Mettre à jour les prix manuellement** sur 18 produits bloqués (API 500 persistant) :
  *(413/431 déjà mis à jour via script le 2026-05-05)*
  - `69f90268ad402ce2b4035348` — Maillot De Bain Design Hokuno Dark → 49.99 $
  - `69f8febcbd4ffcafc502864d` — T-Shirt Design Orbite Hokuno Dark → 37.99 $
  - `69f8ce23b2e670c7080e5639` — Bob Hokuno Design Dark → 39.99 $
  - `69f8cc729822413bd1037c27` — Casquette Design Hokuno Dark → 29.99 $
  - `69f8c86f09f3b73024023a0e` — T-Shirt hokuno Design Target Light → 37.99 $
  - `69f8c689c7a7db441d0c58fc` — T-Shirt Design Hokuno Dark → 37.99 $
  - `69f8c577011b67ecf8078e65` — T-Shirt Design HO KU NO Dark → 37.99 $
  - `69f8959bfeed9979d10d1130` — T-Shirt Sport Design Hokuno Light → 37.99 $
  - `69f89408feed9979d10d1032` — Short De Bain Design Hokuno Bleu Ciel → 49.99 $
  - `69f8901b25819cdf3d057d73` — Claquette Design Hokuno Light → 54.99 $
  - `69f88e25f55196f8d00a8975` — Casquette Hokuno Light → 29.99 $
  - `69f88aadffbc831dea086dc5` — Polo Design Hokuno Boussole Light → 44.99 $
  - `69f61d909110dda91005e89b` — Coque de téléphone The End sur Brique Saga 1 → 24.99 $
  - `69f603f5ef66d02ffe02b1ce` — Copy of T-SHIRT LUFI WANTED NOIR EN 1/17 → 37.99 $
  - `69f6032239e419a2dc02e247` — Copy of T-SHIRT LUFI WANTED EN 1/17 → 37.99 $
  - `6855d70f8454e3a28e01200a` — Short de bain Design Hokuno Pattern Light → 49.99 $
  - `6855d1a12c35f6107c040a63` — Coque téléphone Design Hokuno Orbite Dark → 24.99 $
  - `684d613ffef859492303a65a` — Coque de téléphone Dark ZORO MYTHOLOGIE 2/10 → 24.99 $

- [x] **Activer variante 15oz** sur 93 mugs — fait le 2026-05-05 (Wanted FR+EN + Mythologie)

- [x] **Supprimer** doublon mug Direction Luffy EN : `684d56c509bce0c2370d3254` — fait le 2026-05-05

- [ ] **Renommer** 2 produits Wanted EN (API 500 — faire manuellement dans le dashboard) :
  - `69f6032239e419a2dc02e247` → `T-SHIRT LUFI WANTED EN 1/46`
  - `69f603f5ef66d02ffe02b1ce` → `T-SHIRT LUFI WANTED NOIR EN 1/46`

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
- [x] **Inventaire complet** : INVENTAIRE.md restructuré 422 produits — 2026-05-05
- [x] **Collection Design Hokuno** : inventoriée — 13 t-shirts + 21 accessoires

---

## Résumé global

| Phase | Description | Statut |
|-------|-------------|--------|
| **0** | Nettoyage + titres | ✅ FAIT |
| **1** | Wanted complet FR+EN (t-shirts + mugs) — 276 produits | ✅ FAIT |
| **1-fix** | Renommer 2 Lufi EN (API 500 — manuel dashboard) | ⏳ cosmétique |
| **2** | Direction EN (t-shirts light+dark) | ✅ FAIT |
| **3** | Direction complet — mugs ✅ / coques abandonnées | ✅ FAIT |
| **4** | Mythologie mugs (✅) + Brook NOIR (✅) + coques Mythologie (✅ 10/10) | ✅ FAIT |
| **XL** | Désactiver 2XL–5XL sur tous les t-shirts | 44/48 ✅ — 4 manuels |
| **Design** | Collection Design Hokuno inventoriée | ✅ existant |
| **Shop** | Connexion Shopify + TikTok Shop | ⏳ |
| **Boutique** | Shopify FR/EN immersif | ⏳ |
