# specs/MOCKUPS.md — Ordre des mockups produits

> Contrat pour Claude Code / Claude Chrome. Chaque type de produit a un ordre d'images défini.
> Le thème Shopify affiche les images dans l'ordre fourni par Printify — c'est ici qu'on contrôle cet ordre.
> Référence croisée : `specs/PRODUIT.md` §2 (galerie d'images sur la page produit).

---

## PRINCIPE

L'image n°1 (featured) de chaque produit est celle qui apparaît :
- Dans les grilles collection (product-cards)
- Dans les résultats de recherche
- Comme image par défaut sur la page produit
- Dans les Open Graph / réseaux sociaux

**Règle absolue : l'image n°1 doit toujours montrer le DESIGN principal du produit.**

Le design principal est l'artwork — pas le logo, pas la marque, pas un blank. C'est ce pour quoi le client achète le produit.

---

## 1. T-SHIRTS — TOUTES COLLECTIONS

### Emplacement du design

| Collection | Dos (back) | Devant (front) |
|------------|-----------|----------------|
| Wanted | ✅ Poster wanted (LE design) | Logo 74.png (dark) / vide (light) |
| Direction | ✅ Silhouette + citation (LE design) | Logo 74.png (dark) / logo silhouette (light) |
| Mythologie | ✅ Silhouette divine (LE design) | Logo 74.png (dark) / vide (light) |
| Design Hokuno | Variable — design custom front et/ou back | Variable |

Pour Wanted, Direction et Mythologie : le design principal est **au dos**. Pour Design Hokuno : le design peut être au front — vérifier au cas par cas.

### Ordre des mockups — Wanted, Direction, Mythologie

Pour **CHAQUE couleur activée** du produit :

| Position | Mockup Printify | Ce qu'il montre | Pourquoi cette position |
|----------|-----------------|-----------------|------------------------|
| 1 (featured) | **Back 2** | Dos du t-shirt — design complet visible | C'est le design, c'est ce que le client veut voir en premier |
| 2 | **Front 2** | Devant du t-shirt — logo/marque | Montre le branding front |
| 3 | **Folded** | T-shirt plié — vue lifestyle | Vue complémentaire, donne une idée du produit physique |

> **"Back 2" vs "Back 1"** : dans Printify, il existe plusieurs angles de vue pour le dos. "Back 2" est la vue à plat (flat lay) qui montre le design le plus clairement. "Back 1" est souvent un angle moins lisible. Sélectionner la vue qui montre le design le plus lisiblement comme position 1.

### Ordre des mockups — Design Hokuno

Vérifier chaque produit individuellement :
- Si le design est au **dos** → même ordre que ci-dessus (Back 2 en premier)
- Si le design est au **front** → Front 2 en premier, puis Back 2, puis Folded
- Les 7 t-shirts dark avec design custom front : Front 2 en premier

### Couleurs concernées

Les mockups sont générés **par couleur**. Chaque couleur a ses propres vues (Back 2 Black, Back 2 Navy, Back 2 White, etc.). L'image featured doit être le Back 2 de la **couleur par défaut** du produit :

| Collection | Couleur par défaut (featured) |
|------------|-------------------------------|
| Wanted light | White |
| Wanted dark | Black |
| Direction light | White |
| Direction dark | Black |
| Mythologie light | White |
| Mythologie dark | Black |
| Design Hokuno | Variable — voir le produit |

### Nombre de produits concernés

| Sous-groupe | Produits |
|-------------|----------|
| Wanted FR light | 46 |
| Wanted FR dark | 46 |
| Wanted EN light | 46 |
| Wanted EN dark | 46 |
| Direction FR light | 10 |
| Direction FR dark | 10 |
| Direction EN light | 10 |
| Direction EN dark | 10 |
| Mythologie light | 10 |
| Mythologie dark | 10 |
| Design Hokuno t-shirts | 13 |
| **Total t-shirts** | **257** |

---

## 2. MUGS

### Emplacement du design

Le design est imprimé en sublimation autour du mug. Selon le placement dans Printify, le design est plus visible depuis la vue Left ou Right.

### Ordre des mockups

| Position | Mockup Printify | Ce qu'il montre |
|----------|-----------------|-----------------|
| 1 (featured) | **Left ou Right** (celui qui montre le design) | Côté du mug avec le design principal visible |
| 2 | **Back** | Vue dos / côté opposé |
| 3 | **Front** | Vue de face (anse visible, design partiellement visible) |

> **Comment déterminer Left vs Right** : ouvrir le produit dans Printify, regarder les previews. Le côté qui montre la plus grande surface du design est le bon. En général, si le design est centré, Left et Right sont équivalents — prendre Left par convention.

### Variantes par taille

Les mugs ont des variantes 11oz et 15oz. Chaque variante a ses propres mockups. L'image featured doit être celle du **11oz** (taille la plus populaire/première dans la liste).

### Types de mugs

| Type | Blueprint | Couleur mug | Collections |
|------|-----------|-------------|-------------|
| Mug blanc | BP 478 | Blanc | Wanted FR/EN, Direction FR/EN light, Mythologie |
| Mug noir | BP 479 | Noir | Direction FR/EN dark |

### Nombre de produits concernés

| Sous-groupe | Produits |
|-------------|----------|
| Wanted FR mugs | 46 |
| Wanted EN mugs | 46 |
| Direction FR mugs light | 10 |
| Direction FR mugs dark | 10 |
| Direction EN mugs light | 10 |
| Direction EN mugs dark | 10 |
| Mythologie mugs | 10 |
| **Total mugs** | **142** |

---

## 3. COQUES DE TÉLÉPHONE

### Ordre des mockups

| Position | Mockup Printify | Ce qu'il montre |
|----------|-----------------|-----------------|
| 1 (featured) | **Front** | Face arrière de la coque avec le design visible |

Les coques n'ont généralement qu'un seul mockup pertinent (la vue de face montrant le design). Si Printify génère d'autres vues, garder uniquement le Front en position 1.

### Variantes

26 variantes par coque (iPhone 11 → iPhone 17). Les mockups sont identiques visuellement — le design ne change pas selon le modèle d'iPhone. L'image featured est la même pour toutes les variantes.

### Nombre de produits concernés

| Sous-groupe | Produits |
|-------------|----------|
| Mythologie coques | 10 |
| Design Hokuno coques | 3 |
| Wanted coque (The End Brique — après renommage) | 1 |
| **Total coques** | **14** |

---

## 4. ACCESSOIRES DESIGN HOKUNO

### Casquettes (BP 1108)

| Position | Mockup | Ce qu'il montre |
|----------|--------|-----------------|
| 1 (featured) | Vue montrant le **logo brodé** en évidence | Face avant avec le logo Hokuno |
| 2 | Vue de profil ou arrière | Angle complémentaire |

3 casquettes concernées.

### Bob / Bucket Hat (BP 1698)

| Position | Mockup | Ce qu'il montre |
|----------|--------|-----------------|
| 1 (featured) | Vue montrant le **design all-over** | Pattern Hokuno visible |
| 2 | Vue portée ou autre angle | Complément |

1 bob concerné.

### Polos (BP 1970)

| Position | Mockup | Ce qu'il montre |
|----------|--------|-----------------|
| 1 (featured) | Vue montrant le **logo brodé** sur la poitrine | Face avant, logo visible |
| 2 | Vue de dos ou profil | Complément |

3 polos concernés.

### Shorts de bain (BP 978 / 589)

| Position | Mockup | Ce qu'il montre |
|----------|--------|-----------------|
| 1 (featured) | Vue montrant le **design all-over** | Pattern complet visible |
| 2 | Vue de dos ou portée | Complément |

7 shorts concernés.

### Claquettes / Slide Sandals (BP 862)

| Position | Mockup | Ce qu'il montre |
|----------|--------|-----------------|
| 1 (featured) | Vue montrant le **design sur la sangle** | Dessus de la claquette, design visible |
| 2 | Vue de profil ou portée | Complément |

2 claquettes concernées.

### Maillot de bain (BP 978)

| Position | Mockup | Ce qu'il montre |
|----------|--------|-----------------|
| 1 (featured) | Vue montrant le **design all-over** | Pattern complet |

1 maillot concerné.

### Nombre total accessoires : 17

---

## 5. RÉCAPITULATIF GLOBAL

| Type | Produits | Image featured | Priorité |
|------|----------|----------------|----------|
| T-shirts Wanted/Direction/Mythologie | 244 | Back 2 (design au dos) | 🔴 Haute — 244 produits à traiter |
| T-shirts Design Hokuno | 13 | Back 2 ou Front 2 selon le design | 🟡 Moyenne — vérifier au cas par cas |
| Mugs | 142 | Left ou Right (côté design) | 🔴 Haute — 142 produits |
| Coques | 14 | Front (design visible) | 🟢 Probablement déjà correct |
| Accessoires | 17 | Variable selon le type | 🟡 Moyenne — 17 produits |
| **Total** | **430** | | |

---

## 6. MÉTHODE D'EXÉCUTION

### Option A — Claude Chrome (recommandée pour le volume)

Claude Chrome (le browsing agent) se connecte au dashboard Printify et réordonne les images produit par produit.

**Workflow par produit :**
1. Ouvrir `https://printify.com/app/editor/products/{product_id}`
2. Aller dans l'onglet "Mockups" ou "Images"
3. Identifier l'image Back 2 (pour les t-shirts) ou Left/Right (pour les mugs)
4. Drag & drop cette image en position 1
5. Sauvegarder
6. Passer au produit suivant

**Prompt restrictif pour Claude Chrome :**

```
Tu vas réordonner les mockups de produits Printify. 

RÈGLES STRICTES :
- Tu NE SUPPRIMES aucune image
- Tu NE MODIFIES aucun design, prix, titre, description ou variante
- Tu NE CHANGES que l'ORDRE des images mockup
- Tu NE TOUCHES à rien d'autre sur la page produit

POUR CHAQUE T-SHIRT (collections Wanted, Direction, Mythologie) :
1. Ouvre le produit dans Printify
2. Va dans les mockups/images
3. Trouve l'image "Back 2" (vue de dos, t-shirt à plat, design complet visible)
4. Mets-la en position 1 (featured)
5. Mets "Front 2" en position 2
6. Mets "Folded" en position 3
7. Sauvegarde

POUR CHAQUE MUG :
1. Ouvre le produit dans Printify
2. Trouve l'image qui montre le côté avec le design (Left ou Right)
3. Mets-la en position 1 (featured)
4. Sauvegarde

NE FAIS RIEN D'AUTRE. Confirme chaque changement avant de passer au suivant.
```

### Option B — API Printify (si disponible)

L'API Printify permet de modifier l'ordre des images via `PUT /v1/shops/{shop_id}/products/{product_id}.json` en réordonnant le tableau `images[]`. Cependant, cette méthode nécessite de connaître les IDs exacts des images mockup, ce qui est plus complexe.

**Script pattern :**

```python
import requests, json, time

TOKEN = os.environ["PRINTIFY_API_TOKEN"]
SHOP_ID = "22774508"
HEADERS = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

def reorder_images(product_id, desired_order_keywords):
    """
    desired_order_keywords: ["back", "front", "folded"] pour t-shirts
    """
    r = requests.get(f"https://api.printify.com/v1/shops/{SHOP_ID}/products/{product_id}.json", headers=HEADERS)
    product = r.json()
    images = product.get("images", [])
    
    # Trier les images selon les keywords dans le src ou le nom
    sorted_images = []
    for keyword in desired_order_keywords:
        for img in images:
            if keyword.lower() in img.get("src", "").lower():
                if img not in sorted_images:
                    sorted_images.append(img)
    # Ajouter les images restantes
    for img in images:
        if img not in sorted_images:
            sorted_images.append(img)
    
    # Mettre à jour
    requests.put(
        f"https://api.printify.com/v1/shops/{SHOP_ID}/products/{product_id}.json",
        headers=HEADERS,
        json={"images": sorted_images}
    )
    time.sleep(0.5)
```

> ⚠️ L'API Printify a des limitations (erreurs 500 sur certains produits). Tester sur quelques produits avant de lancer en masse. Les 17 produits déjà identifiés comme bloqués API 500 devront être traités manuellement ou via Claude Chrome.

### Option C — Manuel dans le dashboard Printify

Pour les cas restants ou les produits API 500. Ouvrir chaque produit dans le dashboard Printify → Images → Drag & drop → Save.

---

## 7. ORDRE D'EXÉCUTION RECOMMANDÉ

| Étape | Action | Produits | Méthode |
|-------|--------|----------|---------|
| 1 | T-shirts Wanted FR (light + dark) | 92 | Claude Chrome ou API |
| 2 | T-shirts Wanted EN (light + dark) | 92 | Claude Chrome ou API |
| 3 | T-shirts Direction FR + EN | 40 | Claude Chrome ou API |
| 4 | T-shirts Mythologie | 20 | Claude Chrome ou API |
| 5 | Mugs Wanted FR + EN | 92 | Claude Chrome ou API |
| 6 | Mugs Direction FR + EN | 40 | Claude Chrome ou API |
| 7 | Mugs Mythologie | 10 | Claude Chrome ou API |
| 8 | T-shirts Design Hokuno | 13 | Manuel (vérifier chacun) |
| 9 | Coques Mythologie + Design | 14 | Vérifier (probablement OK) |
| 10 | Accessoires Design Hokuno | 17 | Manuel (vérifier chacun) |

Après chaque batch : republier vers Shopify pour que les images mises à jour soient synchronisées.

```bash
# Republier un produit vers Shopify après modification des images
curl -s -X POST "https://api.printify.com/v1/shops/$SHOP_ID/products/{product_id}/publishing_succeeded.json" \
  -H "Authorization: Bearer $PRINTIFY_API_TOKEN" \
  -H "Content-Type: application/json"
```

---

## 8. VÉRIFICATION POST-MOCKUPS

### Checklist par type

- [ ] **T-shirts Wanted/Direction/Mythologie** : ouvrir 5 produits aléatoires sur Shopify → l'image featured montre le DOS avec le design
- [ ] **T-shirts Design Hokuno** : ouvrir les 13 produits → l'image featured montre le design principal (front ou back selon le produit)
- [ ] **Mugs** : ouvrir 5 mugs aléatoires → l'image featured montre le côté avec le design (pas l'anse, pas le blanc)
- [ ] **Coques** : ouvrir les 14 coques → l'image featured montre le design sur la coque
- [ ] **Accessoires** : ouvrir les 17 accessoires → l'image featured montre le design/logo

### Test visuel sur les pages collection

- [ ] `/collections/wanted` — les cards produit montrent les posters wanted, pas les logos
- [ ] `/collections/direction` — les cards montrent les silhouettes avec citation, pas les logos
- [ ] `/collections/mythologie` — les cards montrent les silhouettes colorées, pas du blanc/noir uni
- [ ] `/collections/design-hokuno` — les cards montrent les designs/logos Hokuno

### Produits à surveiller

| Produit | Risque | Vérification |
|---------|--------|-------------- |
| T-shirts light (toutes collections) | Le front est souvent vide (pas de logo) → le Front 2 est un t-shirt blanc uni = mauvais featured | S'assurer que Back 2 est bien en position 1 |
| Mugs noir (BP 479) | Le design sur fond noir peut être moins visible → vérifier le contraste | Choisir le côté (Left/Right) le plus lisible |
| Design Hokuno dark — 7 avec custom front | Le design EST au front → ne pas mettre Back en premier | Front 2 en position 1 pour ces 7 produits |

---

## 9. TIMING

Cette tâche (Phase 4 du plan) doit être exécutée **AVANT** le push du thème sur Shopify (Phase 5), car le thème affiche les images dans l'ordre Printify. Si les mockups sont dans le mauvais ordre, le site affinera un t-shirt blanc uni comme image principale de chaque produit Wanted — catastrophique pour la conversion.

**Estimation de temps :**
- Claude Chrome : ~2-3 secondes par produit × 430 = ~20-25 minutes
- API script : ~1 seconde par produit × 430 = ~8-10 minutes (hors erreurs 500)
- Manuel : ~15-30 secondes par produit = non viable pour 430 produits
