# PRODUCTION.md — Guide technique de production

> Ce fichier contient tout ce qu'il faut pour produire un épisode de A à Z.
> Templates de prompts, settings, workflow, naming, budget.
> Référence : VIDEO-BIBLE.md pour les règles, SERIE.md pour l'ordre.
> Dernière mise à jour : 2026-05-19

---

## 1. PIPELINE PAR ÉPISODE

```
ÉTAPE 1 — Script (Alti)
    └─ Définir l'angle comique (Acte 2-3)
    └─ Écrire dans SCRIPTS/EPXX-NOM.md

ÉTAPE 2 — Images (ChatGPT)
    └─ 4 images, une par acte
    └─ Uploader les wanted posters en référence
    └─ Format 9:16 vertical

ÉTAPE 3 — Animations (Higgsfield / Kling 3.0)
    └─ 4 clips de 5 secondes
    └─ Upload chaque image comme Start frame

ÉTAPE 4 — Voix off (ElevenLabs)
    └─ 4 MP3 séparés (un par acte)
    └─ Voix japonaise (Asahi)

ÉTAPE 5 — Montage (CapCut)
    └─ Assembler les 4 clips
    └─ Caler les 4 MP3
    └─ Ajouter sous-titres, musique, son signature
    └─ Exporter 2 versions (FR + EN)

ÉTAPE 6 — Publication (TikTok)
    └─ @hokuno (EN) à 22h FR
    └─ @hokuno.fr (FR) à 19h FR
    └─ Tag produit TikTok Shop
```

---

## 2. TEMPLATES DE PROMPTS CHATGPT

### Règles communes à TOUS les prompts ChatGPT

**Toujours faire** :
- Uploader le(s) poster(s) wanted concerné(s) en pièce jointe
- Forcer le style : "classic Japanese shounen manga / 90s anime style, hand-drawn flat 2D ink and color, NOT 3D, NOT photorealistic"
- Forcer l'épuisement : "exhausted, weary, worn down, aged by decades of struggle — KEEP THIS APPEARANCE"
- Demander du 9:16 vertical
- Pas de text overlays dans l'image

**Jamais faire** :
- Nommer "One Piece", "Eiichiro Oda", "Luffy", "Shanks", "Marine" (filtre IP OpenAI)
- Laisser ChatGPT rajeunir les personnages
- Demander du 3D ou photoréaliste

---

### TEMPLATE ACTE 1 — Présentation avec affiche

```
I'm uploading my own original bounty poster artwork for reference.
The character on this poster is intentionally drawn as exhausted,
worn down, aged by decades of struggle. KEEP THIS EXHAUSTED,
WEARY APPEARANCE. Do NOT rejuvenate him, do NOT smooth his features.
Match his face, expression, outfit, and scars EXACTLY as on my reference.

Generate a vertical 9:16 cinematic illustration in classic Japanese
shounen manga / 90s anime style — hand-drawn flat 2D ink and color,
slightly faded, NOT 3D, NOT photorealistic.

Scene: [DÉCRIRE LE LIEU — port, taverne, ruelle, marché, pont de bateau, etc.]

The exhausted character from my poster reference is [DÉCRIRE SA POSITION
— adossé à un mur, assis sur un tonneau, debout dans une foule, etc.].
[DÉCRIRE SON EXPRESSION ET SA POSTURE — bras croisés, regard vide,
épaules basses, etc.]

On the wall nearby, at eye level: the character's own bounty poster,
pinned with rusted nails, slightly aged with curled edges and faint dust.
The poster must be clearly visible and faithful to my uploaded reference.

[DÉCRIRE L'ENVIRONNEMENT AUTOUR — foule qui passe sans regarder,
rue vide, pluie, brouillard, marché bruyant, etc.]

Composition: wide vertical 9:16. The character and his poster
occupy [POSITION — left third, center, right third] of the frame.
[DÉCRIRE LA PROFONDEUR — deep perspective, close-up, etc.]

Mood: [DÉCRIRE L'AMBIANCE — deadpan, absurd, quietly comic, etc.]

No text overlays in the image. Flat 2D anime manga illustration only.
```

**Variables à remplir par épisode** :
- `[LIEU]` — adapté au personnage et à son lore
- `[POSITION/POSTURE]` — reflète sa personnalité épuisée
- `[ENVIRONNEMENT]` — soutient la blague ou le ton
- `[AMBIANCE]` — deadpan par défaut, ajuster si besoin

---

### TEMPLATE ACTE 2 — Action drôle

```
I'm uploading my own original bounty poster artwork for reference.
The character is intentionally drawn as exhausted, weary, worn down.
KEEP THIS EXHAUSTED APPEARANCE. Match his face and outfit EXACTLY.

Generate a vertical 9:16 cinematic illustration in classic Japanese
shounen manga / 90s anime style — hand-drawn flat 2D ink and color,
slightly faded, NOT 3D, NOT photorealistic.

Scene: [DÉCRIRE LA SCÈNE COMIQUE — c'est ici que la blague se joue.
Être TRÈS PRÉCIS sur ce que le personnage FAIT, où il est, ce qui
l'entoure. La description doit être assez détaillée pour que ChatGPT
comprenne la situation absurde sans ambiguïté.]

The exhausted character from my reference is [DÉCRIRE L'ACTION
PRÉCISE — il fait quoi exactement, avec quoi, comment].
His expression is [DÉCRIRE L'EXPRESSION — résigné, perplexe,
blasé, agacé, deadpan amused, etc.].

[DÉCRIRE LES DÉTAILS QUI PORTENT L'HUMOUR — un objet incongru,
une situation contradictoire avec son statut, un détail absurde
dans le décor, etc.]

Composition: wide vertical 9:16. [DÉCRIRE LE CADRAGE —
le personnage au centre avec l'objet comique visible, etc.]

Mood: deadpan comedic, absurd, slightly tragic. The contrast between
the character's legendary status and his current pathetic situation
is the entire subject of this image.

No text overlays. Flat 2D anime manga illustration only.
```

**Note critique** : l'Acte 2 est LE plus important visuellement. C'est la blague.
La description de la scène doit être **hyper précise**. Plus c'est vague, plus
ChatGPT invente n'importe quoi. Si Alti veut Zoro perdu dans un marché,
écrire EXACTEMENT ce qu'il fait dans ce marché, ce qu'il tient, où il regarde.

---

### TEMPLATE ACTE 3 — Continuation ou résolution

```
I'm uploading my own original bounty poster artwork for reference.
KEEP THE EXHAUSTED, WEARY APPEARANCE from my reference exactly.

Generate a vertical 9:16 cinematic illustration in classic Japanese
shounen manga / 90s anime style — hand-drawn flat 2D, NOT 3D.

Scene: [DÉCRIRE LA SUITE DE LA BLAGUE OU LA TRANSITION —
la situation s'aggrave, le perso réagit, quelque chose change,
ou il commence à marcher vers un autre lieu pour préparer l'Acte 4.]

The exhausted character is [DÉCRIRE CE QU'IL FAIT MAINTENANT].
His expression is [DÉCRIRE — plus fatigué, résigné, un léger
sourire en coin, ou au contraire choqué].

[DÉCRIRE L'ENVIRONNEMENT — peut changer par rapport à l'Acte 2
si le perso se déplace, ou rester le même si la blague continue.]

Composition: vertical 9:16. [CADRAGE]
Mood: [TON — deadpan, escalation comique, pivot vers le sérieux, etc.]
No text overlays. Flat 2D anime manga illustration only.
```

---

### TEMPLATE ACTE 4 — Découverte de l'affiche + choc

```
I'm uploading TWO of my original bounty poster artworks.

POSTER 1 = the main character of this scene ([NOM HOKUNO]).
KEEP HIS EXHAUSTED, WEARY APPEARANCE from my reference.
Match face, scars, outfit EXACTLY.

POSTER 2 = the second character ([NOM HOKUNO DU PERSO TEASÉ]).
This poster must appear pinned on a wall in this image.
Reproduce poster 2 EXACTLY as I uploaded it — same drawing,
same face, same expression, same outfit, same text, same layout.
Do NOT redraw the character on the poster.

Generate a vertical 9:16 cinematic illustration in classic Japanese
shounen manga / 90s anime style — hand-drawn flat 2D, NOT 3D.

Scene: [DÉCRIRE LE LIEU DE DÉCOUVERTE — ruelle, mur de taverne,
port, poteau en bois, etc.]

The exhausted character from POSTER 1 is standing in [LIEU],
his body turned slightly toward [DIRECTION]. He has just stopped
[walking/sitting/moving]. His posture is frozen.

On the [left/right] wall, at eye level, pinned with rusted nails:
the bounty poster of [NOM HOKUNO 2] (POSTER 2, reproduced exactly
from my second reference). The poster is slightly aged but the
artwork must remain identical to my upload.

The character's face: THIS IS THE CRITICAL MOMENT. His expression
shows [CHOISIR PARMI] :
- shock and amusement (sourcils levés, bouche entrouverte, début de sourire moqueur)
- disbelief and mockery (sourcil levé, smirk, regard de haut)
- stunned recognition (yeux écarquillés, bouche entrouverte, figé)
- dark amusement (sourire en coin, regard qui dit "toi aussi")

Both faces — the character's reaction and the poster's drawn face —
must be readable in the same glance.

Composition: vertical 9:16. [NOM 1] occupies [right/center],
the poster of [NOM 2] occupies [left third], clearly visible
and lit. Deep perspective.

Mood: quietly stunned, darkly amused, teasing. The image conveys
"[PHRASE QUI RÉSUME LE LIEN ENTRE LES DEUX PERSOS]".

No additional text overlays. Flat 2D anime manga illustration only.
```

**Variables critiques** :
- `[EXPRESSION DU CHOC]` — varie selon la relation entre les deux persos
  - Amis/frères : stunned recognition
  - Rivaux : disbelief and mockery
  - Ennemis : dark amusement
  - Inconnus : bewildered curiosity

---

## 3. TEMPLATES DE PROMPTS HIGGSFIELD

### Règles communes

- **Modèle** : Kling 3.0
- **Durée** : 5 secondes par clip
- **Format** : 9:16 vertical
- **Start frame** : image ChatGPT de l'acte correspondant
- **End frame** : vide (sauf cas spécial)
- **Multi-shot** : OFF
- **Coût** : ~25 crédits par clip

---

### TEMPLATE ANIMATION ACTE 1

```
Static cinematic shot of an exhausted weary [DESCRIPTION COURTE
DU PERSO] in [LIEU]. Subtle ambient motion: [DÉCRIRE CE QUI BOUGE
DANS LE DÉCOR — foule qui passe, poussière, vent, vagues, fumée,
lanternes qui balancent, etc.]. The character stays [POSTURE],
[ACTION MINIMALE — blinks slowly once, shifts weight slightly,
exhales through nose]. His expression remains exhausted, patient.
[DÉCRIRE L'AFFICHE — the bounty poster on the wall stays still,
edges curling very faintly]. Camera completely static, no zoom,
no pan. Cinematic [TYPE DE LUMIÈRE] lighting. Slow, [TON] pace.
```

### TEMPLATE ANIMATION ACTE 2

```
[DÉCRIRE LA SCÈNE EN MOUVEMENT — c'est l'acte le plus animé.
Le personnage FAIT quelque chose. Être précis sur le mouvement.]
Subtle ambient motion: [DÉCOR QUI BOUGE]. The exhausted character
[ACTION PRINCIPALE — walks slowly, reaches for something, sits
down, looks around confused, etc.]. His expression is [EXPRESSION].
[DÉTAILS D'ANIMATION SPÉCIFIQUES — un objet qui tombe, quelque
chose qui glisse, une réaction physique, etc.]. Camera completely
static, no zoom, no pan. Cinematic lighting. [TON] pace.
```

**Note** : l'Acte 2 est le seul où le personnage peut avoir un mouvement
ample (marcher, se baisser, tourner la tête). Les autres actes restent
en micro-mouvements. Kling 3.0 gère mieux les mouvements amples quand
le décor autour est simple et statique.

### TEMPLATE ANIMATION ACTE 3

```
Static cinematic shot of [DESCRIPTION DE LA SCÈNE].
Subtle ambient motion: [DÉCOR]. The exhausted character
[ACTION MINIMALE OU CONTINUATION DU MOUVEMENT DE L'ACTE 2].
[TRANSITION VISUELLE SI CHANGEMENT DE LIEU]. Camera completely
static. Cinematic lighting. [TON] pace.
```

### TEMPLATE ANIMATION ACTE 4

```
Static cinematic shot of an exhausted weary [PERSO] standing
[frozen/still] in [LIEU], facing a bounty poster pinned on
[SURFACE]. Subtle ambient motion: [DÉCOR — lanterns sway,
dust drifts, etc.]. Over 5 seconds: the character's expression
shifts from [ÉTAT INITIAL — neutral, tired] to [ÉTAT FINAL —
wide-eyed shock, smirk of mockery, dark amusement]. His eyes
[widen/narrow], his [mouth parts/lips curl into smirk],
[optional: he takes half a step closer to the poster].
The bounty poster on the wall stays still, clearly visible.
Camera completely static, no zoom, no pan. Cinematic
[warm evening/dim/dramatic] lighting. Slow, suspended,
[deadpan/darkly amused] pace.
```

---

## 4. SETTINGS ELEVENLABS

### Voix
- **Nom** : Asahi (ou équivalent mature JP dans la Voice Library)
- **Langue** : Japonais
- **Type** : Narration, Deep, Documentary

### Paramètres fixes
| Paramètre | Valeur |
|---|---|
| Stability | 75 |
| Similarity | 80 |
| Style exaggeration | 5 |
| Speed | 0.85 |

### Méthode de génération
**4 MP3 séparés par épisode** (un par acte).
Ne PAS utiliser les balises `<break>` — ElevenLabs JP les lit comme du texte.

### Structure du texte japonais

Chaque script dans `SCRIPTS/` contient le texte JP exact à coller dans ElevenLabs.
Les pauses entre phrases sont gérées dans CapCut (silence entre les MP3), pas dans ElevenLabs.

### Contrôle qualité voix off
Après génération, vérifier :
1. Prononciation correcte des noms (ルフィ, シャンクス, etc.)
2. Ton grave et posé (pas dramatique, pas emphatique)
3. Durée de chaque MP3 ≤ 5 secondes (sinon speed up à 0.9 ou couper un mot)

---

## 5. MONTAGE CAPCUT

### Structure du projet

```
Format : 9:16 vertical
Durée totale : ~22 secondes (20s contenu + 2s signature)
FPS : 30
Résolution : 1080x1920
```

### Timeline

```
PISTE VIDÉO :
[0-5s]    Clip Acte 1 (5s)
[5-10s]   Clip Acte 2 (5s)
[10-15s]  Clip Acte 3 (5s)
[15-20s]  Clip Acte 4 (5s)
[20-22s]  Fond noir + texte signature + logo HOKUNO

PISTE AUDIO 1 — VOIX OFF :
[0.5s]    MP3 Acte 1 (début à 0.5s, pas à 0s — laisser respirer)
[5.3s]    MP3 Acte 2 (0.3s après le cut pour sync naturelle)
[10.3s]   MP3 Acte 3
[15.3s]   MP3 Acte 4

PISTE AUDIO 2 — MUSIQUE DE FOND :
[0-22s]   Track choisie par Alti
           Volume : 20-25%
           Fade in : 1s au début
           Fade out : 1s à 20s (silence sous la signature)

PISTE AUDIO 3 — SON SIGNATURE :
[20s]     Bruit de page qui se déchire
           Volume : 70%
           Durée : ~1s

PISTE TEXTE — SOUS-TITRES :
           Japonais en haut (taille 28-32, police Noto Sans JP)
           Traduction en bas (taille 38-42, police Inter ou Bebas Neue)
           Blanc avec contour noir léger (2px)
           Position : tiers inférieur de l'écran
           Synchronisés au début de chaque phrase de la voix off
           Fade in 0.2s par ligne

PISTE TEXTE — SIGNATURE FINALE :
[20-22s]  "ÇA NE FINIRA JAMAIS..." (FR) ou "IT WILL NEVER END..." (EN)
           Centré, blanc, bold, taille 48
           Fade in 0.3s
[21.5-22s] Logo HOKUNO ホクノ (petit, bas droite)
```

### Transitions entre actes
- **Cut sec** entre chaque acte (pas de fondu, pas de transition fancy)
- Le cut sec renforce le ton deadpan
- Exception : si l'Acte 3 est une continuation directe de l'Acte 2 (même lieu), un léger crossfade de 5 frames est acceptable

### Export
- Format : MP4
- Résolution : 1080x1920
- FPS : 30
- Qualité : maximale
- **Exporter 2 fois** : une version FR (sous-titres FR), une version EN (sous-titres EN)

---

## 6. NAMING CONVENTION

### Fichiers de production

```
SCRIPTS/EP01-LUFI.md              → Script épisode 1
SCRIPTS/EP02-CHANKS.md            → Script épisode 2
SCRIPTS/EP34-DOFLAMYNGO.md        → Script épisode 34

ASSETS/EP01/EP01-ACT1-IMG.png     → Image ChatGPT Acte 1
ASSETS/EP01/EP01-ACT2-IMG.png     → Image ChatGPT Acte 2
ASSETS/EP01/EP01-ACT3-IMG.png     → Image ChatGPT Acte 3
ASSETS/EP01/EP01-ACT4-IMG.png     → Image ChatGPT Acte 4

ASSETS/EP01/EP01-ACT1-VID.mp4     → Clip Higgsfield Acte 1
ASSETS/EP01/EP01-ACT2-VID.mp4     → Clip Higgsfield Acte 2
ASSETS/EP01/EP01-ACT3-VID.mp4     → Clip Higgsfield Acte 3
ASSETS/EP01/EP01-ACT4-VID.mp4     → Clip Higgsfield Acte 4

ASSETS/EP01/EP01-ACT1-VO.mp3      → Voix off Acte 1
ASSETS/EP01/EP01-ACT2-VO.mp3      → Voix off Acte 2
ASSETS/EP01/EP01-ACT3-VO.mp3      → Voix off Acte 3
ASSETS/EP01/EP01-ACT4-VO.mp3      → Voix off Acte 4

EXPORTS/EP01-LUFI-FR.mp4          → Export final FR
EXPORTS/EP01-LUFI-EN.mp4          → Export final EN
```

### Noms sur TikTok

```
Titre vidéo : "LUFI — EP.01"
Description : "Lufi a 19 ans depuis 28 ans. hokunostore.com #onepiece #luffy #manga #wanted #hokuno"
```

Pas de numéro de saison dans le titre TikTok — les viewers n'en ont rien à faire.
Juste le nom du perso + numéro d'épisode.

---

## 7. WORKFLOW BATCH — 1 DIMANCHE = 7 ÉPISODES

### Prérequis
- 7 scripts écrits dans SCRIPTS/ (angles comiques définis par Alti)
- 14 posters wanted en haute résolution (7 héros + 7 teasés)
- Compte ChatGPT, Higgsfield, ElevenLabs actifs

### Dimanche matin — Images (3-4h)
1. Ouvrir ChatGPT
2. Pour chaque épisode : uploader poster(s), coller prompt Acte 1, générer
3. Vérifier, regénérer si besoin
4. Répéter pour Actes 2, 3, 4
5. Total : 28 images (4 × 7 épisodes)
6. Temps estimé : ~30 min par épisode × 7 = 3.5h

### Dimanche après-midi — Animations (2-3h de queue)
1. Ouvrir Higgsfield
2. Pour chaque image : upload Start frame, coller prompt, Generate
3. Les générations Kling 3.0 prennent 2-5 min chacune
4. Lancer en parallèle (plusieurs onglets)
5. Total : 28 clips (4 × 7)
6. Temps actif : ~1h (le reste est du temps d'attente)
7. Vérifier chaque clip, regénérer les ratés (~30% de regénération)

### Dimanche après-midi — Voix off (1h)
1. Ouvrir ElevenLabs
2. Pour chaque acte : coller le texte JP, générer, télécharger
3. Total : 28 MP3 (4 × 7)
4. Temps estimé : ~10 min par épisode × 7 = 1h
5. Écouter chaque MP3, regénérer si prononciation foireuse

### Dimanche soir — Montage (3-4h)
1. Ouvrir CapCut
2. Pour chaque épisode :
   - Importer 4 clips + 4 MP3
   - Caler sur la timeline (template sauvegardé)
   - Ajouter sous-titres (JP + FR ou EN)
   - Ajouter musique de fond
   - Ajouter son signature
   - Ajouter texte final + logo
   - Exporter version FR
   - Changer sous-titres → exporter version EN
3. Temps estimé : ~25 min par épisode × 7 = 3h

### Dimanche soir — Programmation (30 min)
1. Ouvrir TikTok Creator Center
2. Programmer les 7 × 2 vidéos (FR + EN)
3. 1 par jour, FR à 19h, EN à 22h
4. Ajouter description + hashtags + produit tag

### Total dimanche
| Étape | Durée |
|---|---|
| Images ChatGPT | 3-4h |
| Animations Higgsfield | 2-3h (dont attente) |
| Voix off ElevenLabs | 1h |
| Montage CapCut | 3-4h |
| Programmation TikTok | 30 min |
| **TOTAL** | **~10-12h** |

Un dimanche complet = une semaine de contenu (7 épisodes × 2 versions = 14 vidéos).

---

## 8. BUDGET PAR ÉPISODE

### Abonnements existants (déjà payés pour d'autres projets)

| Outil | Plan | Coût mensuel | Usage HOKUNO |
|---|---|---|---|
| ChatGPT | Forfait | 8€/mois | Images (4 par épisode) |
| Higgsfield | Pro | 50€/mois | Animations (4 clips de 5s par épisode) |
| ElevenLabs | Gratuit | 0€ | Voix off JP (4 MP3 par épisode) |
| CapCut | Gratuit | 0€ | Montage |

### Coût additionnel HOKUNO = 0€/mois

Ces abonnements sont déjà payés pour d'autres projets. La production vidéo HOKUNO ne génère aucun surcoût. Chaque t-shirt vendu (~10€ marge nette) est du profit direct.

### Limites à surveiller

- **Higgsfield** : vérifier que 50€/mois donne assez de crédits pour 28 clips/semaine (4 actes × 7 épisodes) + regénérations (~30%). Si les crédits sont insuffisants, réduire le batch à 5 épisodes/semaine.
- **ElevenLabs gratuit** : quota de caractères limité. 28 MP3 courts par semaine (~4000-5000 caractères JP) peut toucher le plafond gratuit. Si le quota est atteint, passer au plan Starter (~5$/mois) ou réduire à 5 épisodes/semaine.
- **ChatGPT à 8€** : vérifier le nombre de générations d'images autorisées par jour/mois sur ce plan. 28 images/semaine devrait passer mais à confirmer.

---

## 9. TEMPLATE DE SCRIPT (fichier SCRIPTS/)

Chaque épisode a un fichier `SCRIPTS/EPXX-NOM.md` avec cette structure :

```markdown
# EP[XX] — [NOM HOKUNO]

## Infos
- **Héros** : [Nom HOKUNO] ([Nom original])
- **Teasé par** : EP[XX-1] — [Nom précédent]
- **Teaser vers** : EP[XX+1] — [Nom suivant]
- **Lien narratif Acte 4** : [Pourquoi le héros réagit à l'affiche du suivant]
- **Produit** : T-shirt [light/dark ID] / Mug [ID]

## Angle comique (défini par Alti)
[Description de la situation drôle — ce que le perso fait à l'Acte 2-3]

## Acte 1 — Présentation
**Visuel** : [Description de la scène]
**Voix off JP** : [Texte japonais]
**Sous-titre FR** : [Traduction]
**Sous-titre EN** : [Traduction]

## Acte 2 — Action drôle
**Visuel** : [Description de la scène]
**Voix off JP** : [Texte japonais]
**Sous-titre FR** : [Traduction]
**Sous-titre EN** : [Traduction]

## Acte 3 — Continuation / résolution
**Visuel** : [Description de la scène]
**Voix off JP** : [Texte japonais]
**Sous-titre FR** : [Traduction]
**Sous-titre EN** : [Traduction]

## Acte 4 — Découverte affiche + choc
**Visuel** : [Description de la scène]
**Expression du choc** : [shock/mockery/dark amusement/bewildered]
**Voix off JP** : [Texte japonais]
**Sous-titre FR** : [Traduction]
**Sous-titre EN** : [Traduction]

## Prompts ChatGPT
### Acte 1
[Prompt complet à copier-coller]
### Acte 2
[Prompt complet à copier-coller]
### Acte 3
[Prompt complet à copier-coller]
### Acte 4
[Prompt complet à copier-coller]

## Prompts Higgsfield
### Acte 1
[Prompt complet]
### Acte 2
[Prompt complet]
### Acte 3
[Prompt complet]
### Acte 4
[Prompt complet]

## Notes de production
[Toute remarque spéciale pour cet épisode — attention au visage,
objet difficile à générer, détail de timing, etc.]
```

---

## 10. CHECKLIST PRÉ-PUBLICATION

Avant de publier un épisode, vérifier :

- [ ] Les 4 clips sont cohérents visuellement (même perso reconnaissable)
- [ ] Les affiches wanted sont lisibles dans les Actes 1 et 4
- [ ] Le personnage a l'air ÉPUISÉ (pas rajeuni par ChatGPT)
- [ ] La voix off JP est claire et bien prononcée
- [ ] Les sous-titres sont synchronisés (pas en avance ni en retard)
- [ ] Les sous-titres JP sont au-dessus, la traduction en dessous
- [ ] La musique de fond ne couvre pas la voix off
- [ ] Le son signature (page déchirée) est à 20s exactement
- [ ] Le texte "ÇA NE FINIRA JAMAIS..." apparaît proprement
- [ ] Le logo HOKUNO est visible en fin
- [ ] La version FR ET la version EN sont exportées
- [ ] Le produit TikTok Shop est tagué (si activé)
- [ ] La description contient le nom du perso + hokunostore.com + hashtags
- [ ] La cover thumbnail est la frame la plus impactante
