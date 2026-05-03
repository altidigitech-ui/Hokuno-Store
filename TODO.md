# TODO — Hokuno Store

## État actuel (2026-05-03)

- **342 produits** Printify (shop ID `22774508`, **shop disconnected**)
- **Phase 0** TERMINÉE : titres corrigés, numérotation N/TOTAL
- **Phase 1** TERMINÉE : 46/46 personnages Wanted FR+EN × light+dark+mug = 276 produits
- **Phase 2** TERMINÉE : 10/10 Direction EN light+dark = 20 t-shirts créés
- 10/10 personnages Direction FR (light+dark) créés, 1 mug (Luffy uniquement)
- 10/10 personnages Direction EN (light+dark) créés
- 10/10 personnages Mythologie créés (light+dark+1 mug+1 coque)
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
- [ ] **Renommer** 4 produits *(cosmétique — le contenu est correct)* :
  - `Copy of T-SHIRT LUFI WANTED EN 1/17` → `T-SHIRT LUFI WANTED EN 1/46`
  - `Copy of T-SHIRT LUFI WANTED NOIR EN 1/17` → `T-SHIRT LUFI WANTED NOIR EN 1/46`
  - `TEST-BARTOLOMIOU-KOUMA-WANTED-EN` → `T-SHIRT BARTOLOMIOU KOUMA WANTED EN 18/46`
  - `TEST-BARTOLOMIOU-KOUMA-WANTED-NOIR-EN` → `T-SHIRT BARTOLOMIOU KOUMA WANTED NOIR EN 18/46`

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

### Mugs Direction (Luffy FR seul créé — 0 EN)

| # | Personnage | Mug FR | Mug EN |
|---|-----------|--------|--------|
| 1/10 | Luffy | [x] `684d56c5` | [ ] |
| 2/10 | Zoro | [ ] | [ ] |
| 3/10 | Nami | [ ] | [ ] |
| 4/10 | Ussop | [ ] | [ ] |
| 5/10 | Sanji | [ ] | [ ] |
| 6/10 | Choper | [ ] | [ ] |
| 7/10 | Franky | [ ] | [ ] |
| 8/10 | Robin | [ ] | [ ] |
| 9/10 | Brook | [ ] | [ ] |
| 10/10 | Jinbe | [ ] | [ ] |

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

_Total Phase 3 restant : 39 produits (9 mugs FR + 10 mugs EN + 20 coques FR+EN)_

---

## PHASE 4 — MYTHOLOGIE compléments

### Mugs Mythologie manquants (9/10 — Luffy déjà créé)

| # | Personnage | Mug |
|---|-----------|-----|
| 2/10 | Zoro | [ ] |
| 3/10 | Nami | [ ] |
| 4/10 | Ussop | [ ] |
| 5/10 | Sanji | [ ] |
| 6/10 | Choper | [ ] |
| 7/10 | Franky | [ ] |
| 8/10 | Robin | [ ] |
| 9/10 | Brook | [ ] |
| 10/10 | Jinbe | [ ] |

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

- [ ] `T-SHIRT BROOK MYTHOLOGIE NOIR 9/10` — seule la variante 2 existe, créer le standard

_Total Phase 4 : 19 produits (9 mugs + 9 coques + 1 t-shirt)_

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
| **1-fix** | Renommer 4 produits Wanted EN | — | ⏳ cosmétique |
| **2** | Direction EN (t-shirts light+dark) | 20 | ✅ FAIT |
| **3** | Direction mugs + coques | 39 | ⏳ |
| **4** | Mythologie mugs + coques + Brook NOIR | 19 | ⏳ |
| **5** | Wanted coques | 92 | ⏳ priorité basse |
| **6** | Collection Été | 4 | ⏳ |
| | **TOTAL restant** | **~154** | |
