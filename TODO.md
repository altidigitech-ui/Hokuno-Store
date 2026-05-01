# TODO — Hokuno Store

## État actuel (2026-05-01)
- 105 produits Printify (shop ID 22774508, **shop disconnected**)
- 17 personnages Wanted sur Printify (FR uniquement)
- 49 designs Wanted dans Canva (FR + EN traduit)
- 10 personnages Direction sur Printify (FR uniquement)
- 10 personnages Mythologie sur Printify (version universelle)
- Aucun canal de vente connecté (Shopify, TikTok Shop)

---

## PHASE 0 — NETTOYAGE PRINTIFY *(faire en premier — automatisable via API)*

### Doublons à supprimer
- [ ] Supprimer `Copy of TSHIRT ZORO DIRECTION noir/bleu marine` (`684c6ced9a71a3cc7e0f30c0`) — doublon manifeste
- [ ] Supprimer `T-SHIRT BROOK MYTHOLOGIE NOIR VARIANTE 2` (`6849c4469bf7aebaf7048740`) — variante non documentée
- [ ] Décider entre Lufi v1 et v2 Wanted → archiver v1 (`6849d4756ab7f1ef5d06a2e9` light + `684b42ddc1b6866d8600db8f` dark)
- [ ] Décider entre Chanks v1 et v2 Wanted → archiver v1 (`684b39093a95f8f9ac0cd9d7` light + `684b52a24a52709620072dec` dark)

### Titres à corriger
- [ ] Supprimer espaces parasites en début/fin de titre (6 produits Direction, 1 Wanted, 2 Mythologie)
- [ ] Corriger suffixe `(11oz, 15oz)ie de` sur 6 mugs Wanted (Zoro, Sandji, Sharlot, Shoper, Sk Broock)
- [ ] Standardiser `MYTHOLOGIQUE` → `MYTHOLOGIE` (Ussop ×2)
- [ ] Standardiser `T-SHIRT` / `T SHIRT` / `TSHIRT` → choisir une convention et appliquer partout
- [ ] Unifier `Niko robin` (mug) vs `Niko robine` (t-shirt) → une seule orthographe

### Connexions canal de vente
- [ ] Connecter Shopify au shop Printify (actuellement `disconnected`)
- [ ] Connecter TikTok Shop au shop Printify

---

## PHASE 1 — WANTED EN *(designs prêts dans Canva "Copie de THE END")*

**Contexte** : Les 49 designs EN sont traduits dans Canva via l'outil de traduction intégré. Il faut exporter les PNG puis créer les produits Printify.
**Punchline** : "IT WILL NEVER END..." (identique pour tous)

### 1a — Personnages déjà sur Printify (17 × 2 = 34 t-shirts)
Créer la version EN (light + dark) pour chaque personnage Wanted FR existant :
- [ ] Lufi EN (light + dark)
- [ ] Chanks EN (light + dark)
- [ ] Rororoa Zoro EN (light + dark)
- [ ] Namy EN (light + dark)
- [ ] Sandji EN (light + dark)
- [ ] Shoper EN (light + dark)
- [ ] Niko Robine EN (light + dark)
- [ ] Francky EN (light + dark)
- [ ] Broock EN (light + dark)
- [ ] God Ussop EN (light + dark)
- [ ] Gymbey EN (light + dark)
- [ ] Baggy EN (light + dark)
- [ ] Caido EN (light + dark)
- [ ] Doflamyngo EN (light + dark)
- [ ] Marshal Di Tittch EN (light + dark)
- [ ] Sharlot Linline EN (light + dark)
- [ ] Alabastards EN (light + dark)

### 1b — Personnages dans Canva mais PAS sur Printify (29 personnages)
Créer pour chacun : FR light + FR dark + EN light + EN dark + mug + coque
_(soit 116 t-shirts + 29 mugs + 29 coques = 174 produits)_

- [ ] Bartolomiou Kouma
- [ ] Iwankoff
- [ ] Harllong
- [ ] Momonosucke
- [ ] Eustash Cap.Kid
- [ ] Boha Ancock
- [ ] Iamato
- [ ] Kobi
- [ ] Portgas Di Ase
- [ ] Crocockdile
- [ ] Dracule Miok
- [ ] Sabot
- [ ] Trafalgar Di Low
- [ ] Monki Di Dragone
- [ ] Gayko Mauria
- [ ] Aokidji
- [ ] Kaktakoury
- [ ] Kouine
- [ ] Qing
- [ ] Smokerr
- [ ] Hodene
- [ ] Bartolomio
- [ ] Dr Vegan Punck
- [ ] Edouard Niougate
- [ ] Goldiroger
- [ ] Henere
- [ ] Marko The Fenix
- [ ] Quinemone
- [ ] Peronah

---

## PHASE 2 — DIRECTION EN *(designs à régénérer avec ChatGPT)*

**Contexte** : Le texte est intégré dans l'image IA — impossible de modifier dans Canva. Les versions EN doivent être régénérées entièrement avec ChatGPT.
**Texte à intégrer** : `"I DON'T NEED A PLAN.. JUST A DIRECTION."` + `ホクノ`

- [ ] Régénérer les 10 silhouettes Direction EN avec ChatGPT (même pose que FR, texte EN)
- [ ] Exporter les PNG
- [ ] Créer les produits Printify Direction EN (20 t-shirts) :
  - [ ] Luffy EN (light + dark)
  - [ ] Zoro EN (light + dark)
  - [ ] Nami EN (light + dark)
  - [ ] Ussop EN (light + dark)
  - [ ] Sanji EN (light + dark)
  - [ ] Choper EN (light + dark)
  - [ ] Franky EN (light + dark)
  - [ ] Robin EN (light + dark)
  - [ ] Brook EN (light + dark)
  - [ ] Jinbe EN (light + dark)

---

## PHASE 3 — MYTHOLOGIE compléments

### T-shirts light manquants (2)
- [ ] Choper MYTHOLOGIE light (56 variantes — seul NOIR existe actuellement)
- [ ] Robin MYTHOLOGIE light (56 variantes — seul NOIR existe actuellement)

### Mugs manquants (9)
- [ ] Zoro mug Mythologie
- [ ] Nami mug Mythologie
- [ ] Ussop mug Mythologie
- [ ] Sanji mug Mythologie
- [ ] Choper mug Mythologie
- [ ] Franky mug Mythologie
- [ ] Robin mug Mythologie
- [ ] Brook mug Mythologie
- [ ] Jinbe mug Mythologie

### Coques manquantes (9)
- [ ] Luffy coque Mythologie
- [ ] Nami coque Mythologie
- [ ] Ussop coque Mythologie
- [ ] Sanji coque Mythologie
- [ ] Choper coque Mythologie
- [ ] Franky coque Mythologie
- [ ] Robin coque Mythologie
- [ ] Brook coque Mythologie
- [ ] Jinbe coque Mythologie

---

## PHASE 4 — MUGS & COQUES batch toutes collections

### Wanted existants — coques manquantes (17)
- [ ] Lufi coque
- [ ] Chanks coque
- [ ] Rororoa Zoro coque
- [ ] Namy coque
- [ ] Sandji coque
- [ ] Shoper coque
- [ ] Niko Robine coque
- [ ] Francky coque
- [ ] Broock coque
- [ ] God Ussop coque
- [ ] Gymbey coque
- [ ] Baggy coque
- [ ] Caido coque
- [ ] Doflamyngo coque
- [ ] Marshal Di Tittch coque
- [ ] Sharlot Linline coque
- [ ] Alabastards coque

### Direction — mugs manquants (9)
- [ ] Zoro mug Direction
- [ ] Nami mug Direction
- [ ] Ussop mug Direction
- [ ] Sanji mug Direction
- [ ] Choper mug Direction
- [ ] Franky mug Direction
- [ ] Robin mug Direction
- [ ] Brook mug Direction
- [ ] Jinbe mug Direction

### Direction — coques manquantes (10)
- [ ] Luffy coque Direction
- [ ] Zoro coque Direction
- [ ] Nami coque Direction
- [ ] Ussop coque Direction
- [ ] Sanji coque Direction
- [ ] Choper coque Direction
- [ ] Franky coque Direction
- [ ] Robin coque Direction
- [ ] Brook coque Direction
- [ ] Jinbe coque Direction

---

## PHASE 5 — COLLECTION ÉTÉ

**Contexte** : Produits saisonniers avec logo Hokuno (Logpose + ホクノ). Vérifier les blueprints Printify disponibles avant de créer les designs.

- [ ] Vérifier blueprints Printify disponibles : bob/bucket hat, casquette/dad cap, short/boardshort, débardeur
- [ ] Créer les designs logo Hokuno adaptés à chaque format
- [ ] Créer les produits Printify :
  - [ ] Bob / bucket hat
  - [ ] Casquette / dad cap
  - [ ] Short / boardshort
  - [ ] Débardeur
