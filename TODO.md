# TODO — Hokuno Store

## État actuel (2026-05-02)

- **97 produits** Printify (shop ID `22774508`, **shop disconnected**)
- **Phase 0 TERMINÉE** : titres corrigés, catalogue nettoyé à 97 produits
- 17 personnages Wanted sur Printify (FR uniquement)
- 49 designs Wanted dans Canva (FR + EN traduit)
- 10 personnages Direction sur Printify (FR uniquement)
- 10 personnages Mythologie sur Printify (version universelle)
- Aucun canal de vente connecté (Shopify, TikTok Shop)

---

## PHASE 0 — NETTOYAGE ✅ TERMINÉ

- [x] Titres corrigés (70 renames via API) : T-SHIRT uniformisé, espaces supprimés, MYTHOLOGIQUE→MYTHOLOGIE, ie de supprimé, Niko Robine unifié
- [x] JSON collections mis à jour (IDs invalides nettoyés)
- [x] INVENTAIRE.md réécrit avec 97 produits classés
- [ ] Connecter Shopify au shop Printify (actuellement `disconnected`)
- [ ] Connecter TikTok Shop au shop Printify

---

## PHASE 1 — WANTED EN *(designs PRÊTS dans Canva)*

**Contexte** : Les 49 designs Wanted EN sont traduits dans Canva via l'outil de traduction intégré (projet "Copie de THE END"). Il faut exporter les PNG puis créer les produits Printify.

**Punchline identique pour tous** : `"IT WILL NEVER END..."` (EN)

**Workflow** : Exporter PNG depuis Canva → Upload Printify → Créer produit avec titre `T-SHIRT [NOM] WANTED EN` / `T-SHIRT [NOM] WANTED NOIR EN`

### Phase 1a — Personnages déjà sur Printify (17 × 2 = 34 t-shirts EN)

Créer la version EN (light + dark) pour chaque personnage Wanted FR existant :

| # | Personnage | EN Light | EN Dark |
|---|-----------|---------|---------|
| 01 | Lufi | [ ] | [ ] |
| 02 | Chanks | [ ] | [ ] |
| 03 | Rororoa Zoro | [ ] | [ ] |
| 04 | Namy | [ ] | [ ] |
| 05 | Sandji | [ ] | [ ] |
| 06 | Shoper | [ ] | [ ] |
| 07 | Niko Robine | [ ] | [ ] |
| 08 | Francky | [ ] | [ ] |
| 09 | Broock | [ ] | [ ] |
| 10 | God Ussop | [ ] | [ ] |
| 11 | Gymbey | [ ] | [ ] |
| 12 | Baggy | [ ] | [ ] |
| 13 | Caido | [ ] | [ ] |
| 14 | Doflamyngo | [ ] | [ ] |
| 15 | Marshal Di Tittch | [ ] | [ ] |
| 16 | Sharlot Linline | [ ] | [ ] |
| 17 | Alabastards | [ ] | [ ] |

### Phase 1b — Personnages dans Canva mais PAS sur Printify (29 personnages)

Créer pour chacun : FR light + FR dark + EN light + EN dark + mug + coque
_(soit 116 t-shirts + 29 mugs + 29 coques = **174 produits**)_

| # | Personnage | FR Light | FR Dark | EN Light | EN Dark | Mug | Coque |
|---|-----------|---------|---------|---------|---------|-----|-------|
| 01 | Bartolomiou Kouma | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 02 | Iwankoff | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 03 | Harllong | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 04 | Momonosucke | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 05 | Eustash Cap.Kid | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 06 | Boha Ancock | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 07 | Iamato | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 08 | Kobi | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 09 | Portgas Di Ase | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 10 | Crocockdile | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 11 | Dracule Miok | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 12 | Sabot | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 13 | Trafalgar Di Low | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 14 | Monki Di Dragone | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 15 | Gayko Mauria | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 16 | Aokidji | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 17 | Kaktakoury | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 18 | Kouine | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 19 | Qing | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 20 | Smokerr | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 21 | Hodene | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 22 | Bartolomio | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 23 | Dr Vegan Punck | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 24 | Edouard Niougate | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 25 | Goldiroger | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 26 | Henere | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 27 | Marko The Fenix | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 28 | Quinemone | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 29 | Peronah | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

---

## PHASE 2 — DIRECTION EN *(designs À RÉGÉNÉRER avec ChatGPT)*

**Contexte** : Le texte est intégré dans l'image IA — impossible de modifier dans Canva. Les versions EN doivent être régénérées entièrement avec ChatGPT / DALL-E.

**Texte à intégrer** : `"I DON'T NEED A PLAN.. JUST A DIRECTION."` + `ホクノ`

**Workflow** : Régénérer la silhouette EN dans ChatGPT (même pose, texte EN) → Exporter PNG → Créer produit Printify

| # | Personnage | Image EN générée | EN Light | EN Dark |
|---|-----------|-----------------|---------|---------|
| 01 | Luffy | [ ] | [ ] | [ ] |
| 02 | Zoro | [ ] | [ ] | [ ] |
| 03 | Nami | [ ] | [ ] | [ ] |
| 04 | Ussop | [ ] | [ ] | [ ] |
| 05 | Sanji | [ ] | [ ] | [ ] |
| 06 | Choper | [ ] | [ ] | [ ] |
| 07 | Franky | [ ] | [ ] | [ ] |
| 08 | Robin | [ ] | [ ] | [ ] |
| 09 | Brook | [ ] | [ ] | [ ] |
| 10 | Jinbe | [ ] | [ ] | [ ] |

_Total Phase 2 : 20 t-shirts EN (10 light + 10 dark)_

---

## PHASE 3 — MYTHOLOGIE compléments

**Contexte** : Pas de version EN nécessaire (design sans texte = universel).

### T-shirts light manquants (2)
- [ ] T-SHIRT CHOPER MYTHOLOGIE (light, 56 variantes — seul NOIR existe)
- [ ] T-SHIRT ROBIN MYTHOLOGIE (light, 56 variantes — seul NOIR existe)

### Mugs manquants (9)

| # | Personnage | Mug |
|---|-----------|-----|
| 01 | Zoro | [ ] |
| 02 | Nami | [ ] |
| 03 | Ussop | [ ] |
| 04 | Sanji | [ ] |
| 05 | Choper | [ ] |
| 06 | Franky | [ ] |
| 07 | Robin | [ ] |
| 08 | Brook | [ ] |
| 09 | Jinbe | [ ] |

### Coques manquantes (9)

| # | Personnage | Coque |
|---|-----------|-------|
| 01 | Luffy | [ ] |
| 02 | Nami | [ ] |
| 03 | Ussop | [ ] |
| 04 | Sanji | [ ] |
| 05 | Choper | [ ] |
| 06 | Franky | [ ] |
| 07 | Robin | [ ] |
| 08 | Brook | [ ] |
| 09 | Jinbe | [ ] |

---

## PHASE 4 — MUGS & COQUES batch

### Wanted existants — Mugs EN (non créés)
_(à créer lors de la Phase 1)_

### Wanted existants — Coques FR manquantes (17)

| # | Personnage | Coque FR |
|---|-----------|---------|
| 01 | Lufi | [ ] |
| 02 | Chanks | [ ] |
| 03 | Rororoa Zoro | [ ] |
| 04 | Namy | [ ] |
| 05 | Sandji | [ ] |
| 06 | Shoper | [ ] |
| 07 | Niko Robine | [ ] |
| 08 | Francky | [ ] |
| 09 | Broock | [ ] |
| 10 | God Ussop | [ ] |
| 11 | Gymbey | [ ] |
| 12 | Baggy | [ ] |
| 13 | Caido | [ ] |
| 14 | Doflamyngo | [ ] |
| 15 | Marshal Di Tittch | [ ] |
| 16 | Sharlot Linline | [ ] |
| 17 | Alabastards | [ ] |

### Direction — Mugs manquants (9)

| # | Personnage | Mug |
|---|-----------|-----|
| 01 | Zoro | [ ] |
| 02 | Nami | [ ] |
| 03 | Ussop | [ ] |
| 04 | Sanji | [ ] |
| 05 | Choper | [ ] |
| 06 | Franky | [ ] |
| 07 | Robin | [ ] |
| 08 | Brook | [ ] |
| 09 | Jinbe | [ ] |

### Direction — Coques manquantes (10)

| # | Personnage | Coque |
|---|-----------|-------|
| 01 | Luffy | [ ] |
| 02 | Zoro | [ ] |
| 03 | Nami | [ ] |
| 04 | Ussop | [ ] |
| 05 | Sanji | [ ] |
| 06 | Choper | [ ] |
| 07 | Franky | [ ] |
| 08 | Robin | [ ] |
| 09 | Brook | [ ] |
| 10 | Jinbe | [ ] |

---

## PHASE 5 — COLLECTION ÉTÉ

**Concept** : Produits saisonniers avec logo Hokuno (Logpose + ホクノ). Accessoires et vêtements d'été pour étendre la marque au-delà des t-shirts.

- [ ] Vérifier blueprints Printify disponibles : bob/bucket hat, casquette/dad cap, short/boardshort, débardeur
- [ ] Créer les designs logo Hokuno adaptés à chaque format

| # | Produit | Design prêt | Printify |
|---|---------|------------|---------|
| 01 | Bob / Bucket hat | [ ] | [ ] |
| 02 | Casquette / Dad cap | [ ] | [ ] |
| 03 | Short / Boardshort | [ ] | [ ] |
| 04 | Débardeur | [ ] | [ ] |

---

## Résumé global

| Phase | Description | Produits à créer | Designs disponibles | Statut |
|-------|-------------|-----------------|--------------------|----|
| **0** | Nettoyage catalogue | — | — | ✅ FAIT |
| **1a** | Wanted EN (existants) | 34 t-shirts | ✅ Prêts (Canva "Copie de THE END") | ⏳ |
| **1b** | Wanted FR+EN (nouveaux 29) | 174 produits | ✅ Prêts (Canva FR+EN) | ⏳ |
| **2** | Direction EN | 20 t-shirts | ❌ À régénérer (ChatGPT) | ⏳ |
| **3** | Mythologie compléments | 20 produits | ✅ Designs existants | ⏳ |
| **4** | Mugs & coques batch | 45 produits | ✅ Designs existants | ⏳ |
| **5** | Collection Été | 4 produits | ❌ À créer | ⏳ |
| | **TOTAL nouveaux produits** | **~297** | | |

_Note : Le total est estimatif. Les phases 1b et 4 (mugs/coques des 29 nouveaux) peuvent être réalisées simultanément._
