# TODO — Hokuno Store

## État actuel (2026-05-04)

- **391 produits** Printify (shop ID `22774508`, **shop disconnected**) — vérifié API le 2026-05-04
- **Phase 0** TERMINÉE : titres corrigés, numérotation N/TOTAL
- **Phase 1** TERMINÉE : 46/46 personnages Wanted FR+EN × light+dark+mug = 276 produits
- **Phase 2** TERMINÉE : 10/10 Direction EN light+dark = 20 t-shirts créés
- **Phase 3** TERMINÉE : 40/40 mugs Direction FR+EN (light+dark) créés
- 10/10 personnages Direction FR (light+dark+mugs) créés
- 10/10 personnages Direction EN (light+dark+mugs) créés
- 10/10 personnages Mythologie créés (light+dark+mugs+1 coque Zoro)
- **Phase 4 mugs** TERMINÉE : 10/10 mugs Mythologie créés (2026-05-04)
- Aucun canal de vente connecté (Shopify, TikTok Shop)

---

## PHASE 0 — NETTOYAGE ✅ TERMINÉ

- [x] Titres corrigés (70 renames via API) : T-SHIRT uniformisé, espaces supprimés
- [x] JSON collections mis à jour avec tous les product IDs
- [x] INVENTAIRE.md réécrit (322 produits vérifiés)
- [x] wanted.json : 46/46 personnages complets (t-shirt FR+EN light+dark + mug FR+EN)
- [ ] Connecter Shopify au shop Printify (actuellement `disconnected`)
- [ ] Connecter TikTok Shop au shop Printify

---

## PHASE 1 — WANTED COMPLET ✅ TERMINÉ

- [x] 46 × T-shirt FR light (560 var)
- [x] 46 × T-shirt FR dark (560 var)
- [x] 46 × T-shirt EN light (560 var) — dont 2 à renommer (Lufi + Bartolomiou Kouma)
- [x] 46 × T-shirt EN dark (560 var) — dont 2 à renommer
- [x] 46 × Mug FR (2 var)
- [x] 46 × Mug EN (2 var)
- [ ] **Renommer** 2 produits *(API 500 — à faire manuellement dans le dashboard Printify)* :
  - `Copy of T-SHIRT LUFI WANTED EN 1/17` (`69f6032239e419a2dc02e247`) → `T-SHIRT LUFI WANTED EN 1/46`
  - `Copy of T-SHIRT LUFI WANTED NOIR EN 1/17` (`69f603f5ef66d02ffe02b1ce`) → `T-SHIRT LUFI WANTED NOIR EN 1/46`
- [x] `TEST-BARTOLOMIOU-KOUMA-WANTED-EN` → `T-SHIRT BARTOLOMIOU KOUMA WANTED EN 18/46`
- [x] `TEST-BARTOLOMIOU-KOUMA-WANTED-NOIR-EN` → `T-SHIRT BARTOLOMIOU KOUMA WANTED NOIR EN 18/46`

---

## PHASE 2 — DIRECTION EN ✅ TERMINÉ

**Quote** : `"I DON'T NEED A PLAN.. JUST A DIRECTION."` + `ホクノ`
**Workflow utilisé** : Images EN fournies manuellement → exports/direction-en-dark/ + direction-en-light/ → `scripts/create_direction_en.py`

| # | Personnage | Image EN | EN Light | EN Dark |
|---|-----------|---------|---------|---------|
| 1/10 | Luffy | [x] | [x] `69f79ad4` | [x] `69f79b4a` |
| 2/10 | Zoro | [x] | [x] `69f79ae2` | [x] `69f79b58` |
| 3/10 | Nami | [x] | [x] `69f79aef` | [x] `69f79b62` |
| 4/10 | Ussop | [x] | [x] `69f79afa` | [x] `69f79b6e` |
| 5/10 | Sanji | [x] | [x] `69f79b0f` | [x] `69f79b7a` |
| 6/10 | Choper | [x] | [x] `69f79b19` | [x] `69f79b85` |
| 7/10 | Franky | [x] | [x] `69f79b22` | [x] `69f79b8f` |
| 8/10 | Robin | [x] | [x] `69f79b2a` | [x] `69f79ba0` |
| 9/10 | Brook | [x] | [x] `69f79b34` | [x] `69f79bac` |
| 10/10 | Jinbe | [x] | [x] `69f79b3e` | [x] `69f79bb9` |

_IDs complets dans INVENTAIRE.md section 4 et collections/direction.json_

---

## PHASE 3 — DIRECTION MUGS & COQUES

### Mugs Direction (40/40 créés — FR+EN light+dark) ✅

| # | Personnage | Mug FR Light | Mug FR Dark | Mug EN Light | Mug EN Dark |
|---|-----------|------------|------------|------------|------------|
| 1/10 | Luffy | [x] `69f7aa5e` | [x] `69f7aaab` | [x] `69f7aaea` | [x] `69f7ab29` |
| 2/10 | Zoro | [x] `69f7aa64` | [x] `69f7aab2` | [x] `69f7aaf0` | [x] `69f7ab32` |
| 3/10 | Nami | [x] `69f7aa6b` | [x] `69f7aab7` | [x] `69f7aaf6` | [x] `69f7ab3b` |
| 4/10 | Ussop | [x] `69f7aa73` | [x] `69f7aabb` | [x] `69f7aafd` | [x] `69f7ab42` |
| 5/10 | Sanji | [x] `69f7aa83` | [x] `69f7aac2` | [x] `69f7ab04` | [x] `69f7ab47` |
| 6/10 | Choper | [x] `69f7aa8b` | [x] `69f7aac9` | [x] `69f7ab09` | [x] `69f7ab4d` |
| 7/10 | Franky | [x] `69f7aa90` | [x] `69f7aad3` | [x] `69f7ab0e` | [x] `69f7ab53` |
| 8/10 | Robin | [x] `69f7aa98` | [x] `69f7aadb` | [x] `69f7ab12` | [x] `69f7ab59` |
| 9/10 | Brook | [x] `69f7aa9f` | [x] `69f7aae1` | [x] `69f7ab1c` | [x] `69f7ab60` |
| 10/10 | Jinbe | [x] `69f7aaa6` | [x] `69f7aae5` | [x] `69f7ab25` | [x] `69f7ab66` |

### Coques Direction (aucune créée)

| # | Personnage | Coque FR | Coque EN |
|---|-----------|---------|---------|
| 1/10 | Luffy | [ ] | [ ] |
| 2/10 | Zoro | [ ] | [ ] |
| 3/10 | Nami | [ ] | [ ] |
| 4/10 | Ussop | [ ] | [ ] |
| 5/10 | Sanji | [ ] | [ ] |
| 6/10 | Choper | [ ] | [ ] |
| 7/10 | Franky | [ ] | [ ] |
| 8/10 | Robin | [ ] | [ ] |
| 9/10 | Brook | [ ] | [ ] |
| 10/10 | Jinbe | [ ] | [ ] |

_Phase 3 mugs : ✅ TERMINÉ (40/40) — Restant Phase 3 : 20 coques FR+EN_

---

## PHASE 4 — MYTHOLOGIE compléments

### Mugs Mythologie ✅ 10/10 TERMINÉ (2026-05-04)

| # | Personnage | Mug | Product ID |
|---|-----------|-----|-----------|
| 1/10 | Luffy | [x] | `684d59ac1d7c908d840c9497` |
| 2/10 | Zoro | [x] | `69f867caffbc831dea085700` |
| 3/10 | Nami | [x] | `69f867cd2592a8ad8e0f076f` |
| 4/10 | Ussop | [x] | `69f867d283a8608fd80f10f1` |
| 5/10 | Sanji | [x] | `69f867d6feed9979d10cf101` |
| 6/10 | Choper | [x] | `69f867d8ffbc831dea085705` |
| 7/10 | Franky | [x] | `69f867ddf9374ed4f105c870` |
| 8/10 | Robin | [x] | `69f867e15da263f75f04e914` |
| 9/10 | Brook | [x] | `69f867e32592a8ad8e0f077c` |
| 10/10 | Jinbe | [x] | `69f867e75da263f75f04e91b` |

### Coques Mythologie manquantes (9/10 — Zoro déjà créé)

| # | Personnage | Coque |
|---|-----------|-------|
| 1/10 | Luffy | [ ] |
| 3/10 | Nami | [ ] |
| 4/10 | Ussop | [ ] |
| 5/10 | Sanji | [ ] |
| 6/10 | Choper | [ ] |
| 7/10 | Franky | [ ] |
| 8/10 | Robin | [ ] |
| 9/10 | Brook | [ ] |
| 10/10 | Jinbe | [ ] |

### Brook T-shirt NOIR standard

- [x] `T-SHIRT BROOK MYTHOLOGIE NOIR 9/10` — créé le 2026-05-04 → `69f87c8cbe136844f0003b0a`

_Total Phase 4 restant : 9 produits (9 coques)_

---

## PHASE 5 — WANTED coques (0 créé)

*(Priorité basse — la collection Wanted est complète en t-shirts et mugs)*

| # | Personnage | Coque FR | Coque EN |
|---|-----------|---------|---------|
| 1/46 | Lufi | [ ] | [ ] |
| … | … | [ ] | [ ] |
| 46/46 | Peronah | [ ] | [ ] |

_Total Phase 5 : 92 coques (46 × FR + 46 × EN)_

---

## PHASE 6 — COLLECTION ÉTÉ

| # | Produit | Design prêt | Printify |
|---|---------|------------|---------|
| 1 | Bob / Bucket hat | [ ] | [ ] |
| 2 | Casquette / Dad cap | [ ] | [ ] |
| 3 | Short / Boardshort | [ ] | [ ] |
| 4 | Débardeur | [ ] | [ ] |

---

## CONNEXION CANAUX DE VENTE

- [ ] Shopify → connecter shop Printify (actuellement `disconnected`)
- [ ] TikTok Shop → connecter shop Printify
- [ ] Etsy → phase 2 (après lancement Shopify)

---

## Résumé global

| Phase | Description | Produits à créer | Statut |
|-------|-------------|-----------------|--------|
| **0** | Nettoyage + titres | — | ✅ FAIT |
| **1** | Wanted complet FR+EN (t-shirts + mugs) | 276 produits | ✅ FAIT |
| **1-fix** | Renommer 2 Lufi EN (API 500 — manuel dashboard) | — | ⏳ cosmétique |
| **2** | Direction EN (t-shirts light+dark) | 20 | ✅ FAIT |
| **3** | Direction mugs + coques | 39 (mugs ✅, coques ⏳) | ⏳ |
| **4** | Mythologie mugs + coques + Brook NOIR | mugs ✅, Brook ✅, coques ⏳ (9) | ⏳ |
| **5** | Wanted coques | 92 | ⏳ priorité basse |
| **6** | Collection Été | 4 | ⏳ |
| | **TOTAL restant** | **~104** | |
