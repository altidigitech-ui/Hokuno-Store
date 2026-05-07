# specs/SOCIAL.md — Réseaux sociaux & intégrations

> Contrat pour Claude Code / toi. Connexions sociales, favicon, Open Graph, partage produit, présence off-site.
> Référence croisée : `specs/NAVIGATION.md` §5 (footer liens sociaux), `specs/PRODUIT.md` §14 (partage), `specs/SEO.md` §4-5 (Open Graph / Twitter Card).

---

## 1. COMPTES SOCIAUX À CRÉER

| Plateforme | Handle cible | URL | Statut |
|------------|-------------|-----|--------|
| TikTok | `@hokuno` | `https://www.tiktok.com/@hokuno` | ⏳ À créer |
| Instagram | `@hokuno` | `https://www.instagram.com/hokuno` | ⏳ À créer |

Si `@hokuno` est déjà pris, alternatives : `@hokuno.store`, `@hokuno_official`, `@hokunobrand`.

### Bio (identique sur les deux plateformes)

```
HOKUNO ホクノ
Streetwear Manga — Toujours aller de l'avant.
🎌 Designs originaux | Print on demand
🌍 Livraison internationale
⬇️ Découvrir la boutique
[lien boutique]
```

### Lien en bio

Utiliser directement l'URL de la boutique (`https://hokuno.com` ou l'URL Shopify) comme lien en bio. Pas besoin de Linktree — un seul lien vers le site suffit pour le lancement.

---

## 2. TIKTOK SHOP

### Connexion Shopify

1. Shopify Admin → Sales channels → "+" → TikTok
2. Installer l'app TikTok channel
3. Connecter le compte TikTok Business `@hokuno`
4. Lier le TikTok Ads Manager (même compte que le TikTok Pixel — `specs/ANALYTICS.md` §5)
5. Activer la synchronisation du catalogue produits

### Synchronisation produits

TikTok Shop synchronise automatiquement les produits Shopify :
- Titres, descriptions, images, prix, variantes
- Les produits sont visibles dans l'onglet Shop du profil TikTok
- Mise à jour automatique quand les produits changent dans Shopify

### Shopping dans les vidéos

Une fois le catalogue synchronisé :
- Taguer des produits dans les vidéos TikTok (Shopping Tags)
- Activer les Product Links dans les lives
- Le viewer peut acheter sans quitter TikTok (checkout TikTok) ou être redirigé vers Shopify

### Stratégie contenu TikTok

| Type de vidéo | Fréquence | Objectif |
|---------------|-----------|---------|
| Reveal design (unboxing/mockup) | 3-4/semaine | Viralité, découverte |
| Backstory personnage | 1/semaine | Engagement, lore |
| Behind the scenes (création IA) | 1/semaine | Authenticité |
| Comparaison avant/après (manga → design) | 1/semaine | Éducation |
| Tendances/sons populaires + produit | Opportuniste | Reach |

**Format** : vidéos courtes (15-30s), sous-titres intégrés, hook dans les 2 premières secondes. Pas de texte "lien en bio" (TikTok pénalise) — utiliser les Shopping Tags directement.

### Timing

TikTok Shop peut être connecté dès le lancement. La synchronisation des produits prend quelques heures.

---

## 3. INSTAGRAM SHOPPING

### Connexion Shopify

1. Shopify Admin → Sales channels → "+" → Facebook & Instagram
2. Connecter le compte Meta Business Suite
3. Lier la page Facebook Hokuno (à créer si pas existante — requise par Instagram Shopping)
4. Lier le compte Instagram `@hokuno`
5. Attendre la validation du catalogue par Meta (1-7 jours)

### Prérequis Meta

| Prérequis | Statut |
|-----------|--------|
| Page Facebook | ⏳ À créer (même juste une page vitrine minimale) |
| Compte Instagram Business ou Creator | ⏳ À configurer |
| Catalogue produits dans Meta Commerce Manager | Automatique via Shopify app |
| Conformité politique commerciale Meta | Vérifier que les designs respectent les règles Meta |

### Fonctionnalités une fois activé

- Tags produit dans les posts Instagram (tap → fiche produit → acheter)
- Tags dans les Stories et les Reels
- Onglet Shop dans le profil Instagram
- Checkout via Shopify (le client est redirigé vers le site)

### Stratégie contenu Instagram

| Type de post | Fréquence | Format |
|-------------|-----------|--------|
| Post produit (photo mockup) | 3-4/semaine | Carrousel (3-5 images : mockup + détail design + porté) |
| Story quotidienne | 1/jour | Sondages, coulisses, code promo |
| Reel (format vidéo court) | 2-3/semaine | Même contenu que TikTok adapté |
| Story Highlight | Permanent | Collections : Wanted, Direction, Mythologie, Design |

---

## 4. LIENS SOCIAUX DANS LE FOOTER

Détail dans `specs/NAVIGATION.md` §5.

### Emplacement

Footer, colonne 1 (sous le logo et la tagline).

### Rendu

```html
<div class="foot-social">
  <a href="https://www.tiktok.com/@hokuno" target="_blank" rel="noopener" aria-label="TikTok">
    <svg class="social-icon" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path d="M19.59 6.69a4.83 4.83 0 0 1-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 0 1-2.88 2.5 2.89 2.89 0 0 1-2.89-2.89 2.89 2.89 0 0 1 2.89-2.89c.28 0 .54.04.79.1v-3.5a6.37 6.37 0 0 0-.79-.05A6.34 6.34 0 0 0 3.15 15a6.34 6.34 0 0 0 6.34 6.34 6.34 6.34 0 0 0 6.34-6.34V8.75a8.28 8.28 0 0 0 4.86 1.56V6.84a4.84 4.84 0 0 1-1.1-.15z"/>
    </svg>
  </a>
  <a href="https://www.instagram.com/hokuno" target="_blank" rel="noopener" aria-label="Instagram">
    <svg class="social-icon" viewBox="0 0 24 24" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.406-11.845a1.44 1.44 0 1 0 0 2.881 1.44 1.44 0 0 0 0-2.881z"/>
    </svg>
  </a>
</div>
```

### CSS

```css
.foot-social { display: flex; gap: 16px; margin-top: 16px; }
.social-icon { width: 24px; height: 24px; color: rgba(255,255,255,0.4); transition: color 0.3s; }
.social-icon:hover { color: #D4A853; }

@media (max-width: 768px) {
  .foot-social { justify-content: center; }
}
```

### Schema JSON-LD

Les URLs sociales sont dans le schema Organization (`specs/SEO.md` §3.1) :

```json
"sameAs": [
  "https://www.tiktok.com/@hokuno",
  "https://www.instagram.com/hokuno"
]
```

---

## 5. FAVICON

### Fichiers à créer

| Fichier | Taille | Usage |
|---------|:------:|-------|
| `favicon.ico` | 32×32 px | Onglet navigateur (format ICO, multi-résolution) |
| `favicon-32x32.png` | 32×32 px | Navigateurs modernes |
| `favicon-16x16.png` | 16×16 px | Fallback petits affichages |
| `apple-touch-icon.png` | 180×180 px | Raccourci écran d'accueil iPhone/iPad |
| `android-chrome-192x192.png` | 192×192 px | Android, PWA manifest |
| `android-chrome-512x512.png` | 512×512 px | Android splash screen |

### Design

La boussole Hokuno dorée (`boussole-gold.png`) redimensionnée et recadrée :
- Fond transparent (PNG)
- Boussole centrée, occupant ~80% de l'espace
- Couleur dorée `#D4A853` sur fond transparent
- Pour les petites tailles (16px, 32px), simplifier le design pour rester lisible

### Génération

À partir de `boussole-gold.png` (1572×? px), générer les variantes avec ImageMagick :

```bash
# Générer toutes les tailles
convert boussole-gold.png -resize 180x180 -gravity center -background none -extent 180x180 apple-touch-icon.png
convert boussole-gold.png -resize 192x192 android-chrome-192x192.png
convert boussole-gold.png -resize 512x512 android-chrome-512x512.png
convert boussole-gold.png -resize 32x32 favicon-32x32.png
convert boussole-gold.png -resize 16x16 favicon-16x16.png
convert favicon-32x32.png favicon.ico
```

### Intégration dans theme.liquid

```html
<link rel="icon" type="image/png" sizes="32x32" href="{{ 'favicon-32x32.png' | asset_url }}">
<link rel="icon" type="image/png" sizes="16x16" href="{{ 'favicon-16x16.png' | asset_url }}">
<link rel="apple-touch-icon" sizes="180x180" href="{{ 'apple-touch-icon.png' | asset_url }}">
```

### Alternative : upload dans Shopify Admin

Shopify Admin → Online Store → Themes → Customize → Theme settings → Favicon → Upload. Shopify gère automatiquement les tailles. Méthode plus simple mais moins de contrôle sur les tailles.

---

## 6. OPEN GRAPH IMAGES

Détail dans `specs/SEO.md` §4-5.

### Images par type de page

| Page | Image OG | Source |
|------|---------|--------|
| Accueil | `hero-tshirt.png` | Asset du thème |
| Collection | `card-[handle].png` | Asset du thème (card-wanted.png, etc.) |
| Produit | Image principale du produit | `{{ product.featured_image | image_url: width: 1200 }}` |
| Article blog | Image de l'article | `{{ article.image | image_url: width: 1200 }}` |
| Pages statiques | `hero-tshirt.png` | Fallback par défaut |

### Dimensions recommandées

| Plateforme | Ratio | Taille |
|------------|:-----:|:------:|
| Facebook / Open Graph | 1.91:1 | 1200×630 px |
| Twitter | 2:1 | 1200×600 px |
| Instagram (lien en story) | Variable | Image carrée ou portrait |

Shopify CDN (`| image_url: width: 1200`) sert automatiquement les images à la bonne largeur. Le ratio dépend de l'image source — les mockups Printify sont généralement carrés ou portrait.

### Image OG par défaut

Si aucune image spécifique n'est disponible (page sans image), le fallback est `hero-tshirt.png` — l'image hero qui montre un t-shirt Hokuno. Cette image doit être de haute qualité et recadrée/composée pour un ratio ~1200×630.

---

## 7. PARTAGE SOCIAL SUR LES PAGES PRODUIT

Détail dans `specs/PRODUIT.md` §14.

### Boutons

3 boutons de partage : TikTok, Instagram, Copier le lien.

### Fonctionnement

```javascript
function shareOnTikTok() {
  // TikTok n'a pas d'API de partage web directe
  // Ouvrir la page produit en tant que lien — le visiteur copie depuis TikTok
  window.open('https://www.tiktok.com/', '_blank');
}

function shareOnInstagram() {
  // Instagram n'a pas d'API de partage web directe
  // Ouvrir Instagram — le visiteur partage en story avec screenshot
  window.open('https://www.instagram.com/', '_blank');
}

function copyLink() {
  navigator.clipboard.writeText(window.location.href).then(() => {
    const btn = document.querySelector('.share-copy-btn');
    btn.textContent = '✓';
    btn.style.color = '#22c55e';
    setTimeout(() => {
      btn.textContent = '';  // remettre l'icône lien
      btn.style.color = '';
    }, 2000);
  });
}
```

> Note : ni TikTok ni Instagram n'offrent d'API de partage direct depuis le web. Le bouton ouvre simplement la plateforme. L'option la plus utile est "Copier le lien" — le visiteur le colle ensuite où il veut. On peut envisager en v2 un partage via l'API Web Share (`navigator.share()`) sur mobile, qui propose nativement TikTok, Instagram, Messages, etc.

### Web Share API (v2 — mobile uniquement)

```javascript
function shareProduct(title, url) {
  if (navigator.share) {
    navigator.share({ title: title, url: url });
  } else {
    copyLink(); // fallback desktop
  }
}
```

`navigator.share()` ouvre le menu de partage natif du téléphone (iOS/Android) avec toutes les apps installées. Bien plus efficace que des boutons individuels.

---

## 8. PRÉSENCE OFF-SITE (GEO & ACQUISITION)

Source : `CONTEXT.md` → SEO & GEO → Présence externe.

### Plateformes prioritaires

| Plateforme | Usage | Impact GEO | Priorité |
|------------|-------|:----------:|:--------:|
| TikTok | Contenu vidéo, shopping, viralité | Moyen (indexé partiellement par les LLMs) | 🔴 Lancement |
| Instagram | Catalogue visuel, communauté | Moyen | 🔴 Lancement |
| Reddit | r/streetwear, r/OnePiece, r/anime | 🔴 Fort (source primaire des LLMs) | 🟡 Post-lancement |
| YouTube | Vidéos longues, storytelling | Fort (indexé par Google + LLMs) | 🟡 Post-lancement |
| LinkedIn | Thought leadership POD + streetwear | Moyen | 🟢 Optionnel |
| Pinterest | Catalogue visuel passif | Faible | 🟢 Optionnel |

### Reddit — fort impact GEO

Les LLMs (ChatGPT, Perplexity, Gemini) indexent fortement Reddit. Publier du contenu authentique (pas du spam promotionnel) sur :

- `r/streetwear` — "Just launched my manga-inspired streetwear brand"
- `r/OnePiece` — partage de designs (attention aux règles du sub)
- `r/anime` — même approche
- `r/Entrepreneur` — retour d'expérience POD + IA
- `r/PrintOnDemand` — insights techniques

**Règle** : contribuer d'abord, promouvoir ensuite. 80% de valeur, 20% de promo. Reddit détecte et supprime le spam.

### YouTube — fort impact GEO

Créer une chaîne YouTube `HOKUNO` avec :
- Vidéos de présentation de chaque collection (3-5 min)
- Process de création des designs (IA + retouche)
- Behind the scenes de la marque
- Des vidéos bien titrées et décrites (les descriptions YouTube sont indexées par les LLMs)

---

## 9. CHECKLIST SOCIAL

### Avant le lancement

- [ ] Compte TikTok `@hokuno` créé (Business account)
- [ ] Compte Instagram `@hokuno` créé (Business ou Creator)
- [ ] Page Facebook "HOKUNO" créée (requise pour Instagram Shopping)
- [ ] Bio identique sur TikTok et Instagram
- [ ] Lien boutique dans la bio
- [ ] Favicon uploadé dans Shopify (ou dans les assets du thème)
- [ ] Icônes SVG TikTok + Instagram dans le footer
- [ ] Schema Organization → `sameAs` mis à jour avec les URLs sociales

### Dans les 48h post-lancement

- [ ] TikTok Shop connecté (Sales channels → TikTok)
- [ ] Catalogue TikTok synchronisé (vérifier que les produits apparaissent)
- [ ] Première vidéo TikTok publiée avec Shopping Tag
- [ ] Instagram Shopping demandé (Facebook & Instagram channel)
- [ ] 3 premiers posts Instagram publiés
- [ ] Story Instagram avec code HOKUNO15

### Première semaine

- [ ] Premier post Reddit (r/streetwear ou r/Entrepreneur)
- [ ] Contenu TikTok quotidien (1 vidéo/jour minimum)
- [ ] Stories Instagram quotidiennes
