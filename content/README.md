# `content/` — contenus à coller manuellement dans Shopify Admin

Ces 4 fichiers sont les textes des **policies** Shopify. Ils ne sont pas accessibles via l'API GraphQL Admin sans un token avec scope `write_shop_policies`. À copier-coller à la main :

## Procédure

1. Aller sur **Shopify Admin → Settings → Policies** (`s6btxa-q0.myshopify.com/admin/settings/policies`)
2. Pour chaque policy, cliquer "Edit", coller le contenu correspondant, "Save"

| Fichier | Champ Shopify | URL publique |
|---|---|---|
| `policy-terms-of-service.txt` | Terms of service | `/policies/terms-of-service` |
| `policy-privacy-policy.txt` | Privacy policy | `/policies/privacy-policy` |
| `policy-refund-policy.txt` | Return and refund policy | `/policies/refund-policy` |
| `policy-shipping-policy.txt` | Shipping policy | `/policies/shipping-policy` |

## Pages statiques Shopify

Les **pages** (`/pages/about`, `/pages/faq`, `/pages/contact`, `/pages/mentions-legales`) ne sont pas dans ce dossier — leur contenu est **hardcodé dans les templates Liquid** (`shopify-theme/templates/page.{handle}.liquid`).

Il suffit donc de créer les pages vides dans Shopify Admin et de leur assigner le bon template :

| Handle | Template à choisir | Source du contenu |
|---|---|---|
| `about` | `page.about` | `shopify-theme/templates/page.about.liquid` |
| `faq` | `page.faq` | `shopify-theme/templates/page.faq.liquid` |
| `contact` | `page.contact` | `shopify-theme/templates/page.contact.liquid` (formulaire dans le template) |
| `mentions-legales` | `page.mentions-legales` | `shopify-theme/templates/page.mentions-legales.liquid` |

## Blog

Le blog `journal` doit aussi être créé manuellement (Online Store → Blog posts → Manage blogs → Add blog → handle `journal`). Le template `blog.liquid` affiche un état vide élégant tant qu'il n'y a pas d'articles.
