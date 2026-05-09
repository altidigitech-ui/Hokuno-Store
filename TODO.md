# TODO — Hokuno Store

## État actuel (2026-05-07)

- **430 produits** Printify (shop ID `22774508`) — tous corrigés et à jour ✅
- **Printify connecté** à storemdtesttt via app Printify ✅
- **Prix** : 430/430 à jour ✅
- **Descriptions** : 430/430 à jour ✅
- **Tailles** : 48/48 t-shirts XL max ✅
- **Doublons** : aucun ✅
- **Variantes** : toutes configurées ✅

---

## 🟡 COSMÉTIQUE — Titres à corriger (API — 68 appels)

68 t-shirts Wanted ont conservé la numérotation `/17` de la première fournée. Le format correct est `/46`.

| Sous-groupe | Produits | Exemple |
|---|---|---|
| FR light | 17 | `T-SHIRT LUFI WANTED 1/17` → `1/46` |
| FR dark | 17 | `T-SHIRT LUFI WANTED NOIR 1/17` → `1/46` |
| EN light | 17 | `T-SHIRT LUFI WANTED EN 1/17` → `1/46` |
| EN dark | 17 | `T-SHIRT LUFI WANTED NOIR EN 1/17` → `1/46` |

---

## 🟠 Migration storemdtesttt → My Store 5

- [x] Créer l'app dev sur My Store 5, récupérer le token atkn_ ✅ (2026-05-08)
- [x] Connecter Printify à My Store 5 (Printify → Add store → Shopify) ✅ (2026-05-08)
- [x] Republier les 430 produits vers My Store 5 ✅ (2026-05-08)
- [ ] Créer les 4 collections automatiques sur My Store 5
- [ ] Vérifier que les produits sont dans les bonnes collections
- [ ] Corriger les 68 titres /17→/46 pendant la migration
- [x] Renommer la coque Printify → "Coque Wanted The End Brique Saga 1" ✅ (2026-05-08)
- [ ] **Action manuelle Shopify Admin — installer "Search & Discovery"** (App Store Shopify, gratuit, par Shopify). Sans cette app, `collection.filters` retourne vide et la barre de filtres par type sur les pages collection ne s'affiche pas. Une fois installée : Apps → Search & Discovery → Filters → activer le filtre **Product type** sur toutes les collections. Non automatisable via API : l'installation d'app passe obligatoirement par OAuth merchant.

---

## 🟢 Boutique Shopify (specs en cours de rédaction)

- [x] Rédiger les 18 fichiers specs dans `specs/` ✅ (2026-05-08)
- [ ] Landing page immersive
- [ ] Pages collection
- [ ] Pages produit
- [ ] Navigation complète
- [ ] Bilingue FR/EN
- [ ] SEO/GEO
- [ ] Pages statiques
- [ ] Blog
- [ ] Configuration Shopify
- [ ] Analytics
- [ ] Legal
- [ ] Checklist avant lancement
- [ ] Domaine custom
- [ ] LANCEMENT

---

## 🔵 Canaux de vente (post-lancement)

- [ ] TikTok Shop
- [ ] Etsy (phase 2)
- [ ] Amazon (phase 3)

---

## ✅ Déjà fait

- [x] Wanted complet FR+EN (276 produits)
- [x] Direction complet FR+EN (80 produits)
- [x] Mythologie complet (40 produits)
- [x] Design Hokuno complet (34 produits → 33 après renommage coque The End Brique vers Wanted)
- [x] Tailles XL max sur 48/48 t-shirts
- [x] Variante 15oz activée sur 142 mugs
- [x] Logo front correct sur tous les dark Wanted (92) + Direction (20)
- [x] Prix 430/430 à jour
- [x] Descriptions 430/430 à jour
- [x] Doublons supprimés
- [x] Target Light reconfiguré
- [x] Inventaire complet
- [x] Connexion Printify → storemdtesttt
- [x] Publication 430/430 produits
