---
name: printify-api
description: >
  Interact with the Printify API to manage products, shops, and orders.
  Use when listing products, syncing catalog data, filling collection JSON files,
  creating or updating products, publishing to sales channels, or managing orders.
  Requires PRINTIFY_API_TOKEN environment variable.
---

# Printify API Skill

## Authentication

All requests require the `PRINTIFY_API_TOKEN` environment variable.

```bash
# Verify token is set
if [ -z "$PRINTIFY_API_TOKEN" ]; then
  echo "ERROR: Set PRINTIFY_API_TOKEN first: export PRINTIFY_API_TOKEN=your_token"
  exit 1
fi
```

**Base URL**: `https://api.printify.com`

**Headers** (every request):
```
Authorization: Bearer $PRINTIFY_API_TOKEN
Content-Type: application/json
User-Agent: ClaudeCode-Hokuno/1.0
```

## Rate Limits

- Global: 600 requests/minute
- Catalog endpoints: 100 requests/minute
- Product publishing: 200 requests/30 minutes
- Error responses must stay under 5% of total requests

Always add a 200ms delay between sequential requests. On 429 responses, wait 60 seconds.

## Workflow: List Products & Fill Collection JSONs

### Step 1 — Get Shop ID

```bash
curl -s https://api.printify.com/v1/shops.json \
  -H "Authorization: Bearer $PRINTIFY_API_TOKEN" \
  -H "User-Agent: ClaudeCode-Hokuno/1.0" | jq .
```

Response: `[{"id": 5432, "title": "My new store", "sales_channel": "..."}]`
Note the `id` — use it as `{shop_id}` in all subsequent calls.

### Step 2 — List All Products

```bash
curl -s "https://api.printify.com/v1/shops/{shop_id}/products.json?limit=100" \
  -H "Authorization: Bearer $PRINTIFY_API_TOKEN" \
  -H "User-Agent: ClaudeCode-Hokuno/1.0" | jq .
```

Response contains `current_page`, `last_page`, `data[]`. Paginate with `?page=2` if needed.

Each product in `data[]` has:
- `id` — Printify product ID (use for `printify_product_ids` in collection JSONs)
- `title` — Product name
- `description` — HTML description
- `tags[]` — Product tags
- `images[]` — Mockup images with `src` URL
- `variants[]` — Size/color combinations with prices
- `print_areas[]` — Print configuration
- `blueprint_id` — Base product type (e.g., Gildan 5000)
- `print_provider_id` — Print provider

### Step 3 — Get Single Product Details

```bash
curl -s "https://api.printify.com/v1/shops/{shop_id}/products/{product_id}.json" \
  -H "Authorization: Bearer $PRINTIFY_API_TOKEN" \
  -H "User-Agent: ClaudeCode-Hokuno/1.0" | jq .
```

### Step 4 — Map Products to Collection JSONs

Match products to collections based on title patterns:
- Title contains "WANTED" or "THE END" → `collections/wanted.json`
- Title contains "DIRECTION" → `collections/direction.json`
- Title contains "MYTHOLOGIE" or "MYTHO" → `collections/mythologie.json`

For each product, extract and map:
- `id` → `printify_product_ids.tshirt_fr` or `tshirt_en` (based on title language cues)
- `title` → derive `nom` du personnage
- `images[0].src` → reference for visual description
- `tags` → `tags` array in JSON
- `variants` → verify available colors

## Workflow: Publish Products to Shopify

### Publish a Product

```bash
curl -s -X POST "https://api.printify.com/v1/shops/{shop_id}/products/{product_id}/publish.json" \
  -H "Authorization: Bearer $PRINTIFY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -H "User-Agent: ClaudeCode-Hokuno/1.0" \
  -d '{
    "title": true,
    "description": true,
    "images": true,
    "variants": true,
    "tags": true
  }'
```

### Set Publishing Succeeded

After Shopify confirms the product is live:

```bash
curl -s -X POST "https://api.printify.com/v1/shops/{shop_id}/products/{product_id}/publishing_succeeded.json" \
  -H "Authorization: Bearer $PRINTIFY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -H "User-Agent: ClaudeCode-Hokuno/1.0" \
  -d '{"external": {"id": "shopify_product_id", "handle": "product-handle"}}'
```

## Workflow: Create a Product

```bash
curl -s -X POST "https://api.printify.com/v1/shops/{shop_id}/products.json" \
  -H "Authorization: Bearer $PRINTIFY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -H "User-Agent: ClaudeCode-Hokuno/1.0" \
  -d '{
    "title": "T-SHIRT BAGGY WANTED FR",
    "description": "<p>Description HTML</p>",
    "blueprint_id": 145,
    "print_provider_id": 99,
    "variants": [
      {"id": 45740, "price": 2999, "is_enabled": true}
    ],
    "print_areas": [
      {
        "variant_ids": [45740],
        "placeholders": [
          {
            "position": "front",
            "images": [
              {"id": "upload_id", "x": 0.5, "y": 0.5, "scale": 1, "angle": 0}
            ]
          }
        ]
      }
    ]
  }'
```

Prices are in **cents** (2999 = $29.99).

## Workflow: Upload Images

### Step 1 — Upload an image

```bash
curl -s -X POST "https://api.printify.com/v1/uploads/images.json" \
  -H "Authorization: Bearer $PRINTIFY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -H "User-Agent: ClaudeCode-Hokuno/1.0" \
  -d '{
    "file_name": "baggy-wanted.png",
    "url": "https://example.com/baggy-wanted.png"
  }'
```

Response: `{"id": "image_id", "file_name": "...", "width": ..., "height": ...}`

Use the `id` in product creation `print_areas.placeholders.images`.

## Catalog Reference

### List Blueprints (base products)

```bash
curl -s "https://api.printify.com/v1/catalog/blueprints.json" \
  -H "Authorization: Bearer $PRINTIFY_API_TOKEN" \
  -H "User-Agent: ClaudeCode-Hokuno/1.0" | jq '.[] | {id, title}' | head -50
```

Common blueprints:
- Gildan 5000 Unisex Heavy Cotton Tee: check `blueprint_id` from existing products
- Mug 11oz: check catalog
- Phone case: check catalog

### List Print Providers for a Blueprint

```bash
curl -s "https://api.printify.com/v1/catalog/blueprints/{blueprint_id}/print_providers.json" \
  -H "Authorization: Bearer $PRINTIFY_API_TOKEN" \
  -H "User-Agent: ClaudeCode-Hokuno/1.0" | jq .
```

### List Variants for Blueprint + Provider

```bash
curl -s "https://api.printify.com/v1/catalog/blueprints/{blueprint_id}/print_providers/{provider_id}/variants.json" \
  -H "Authorization: Bearer $PRINTIFY_API_TOKEN" \
  -H "User-Agent: ClaudeCode-Hokuno/1.0" | jq .
```

## Orders

### List Orders

```bash
curl -s "https://api.printify.com/v1/shops/{shop_id}/orders.json" \
  -H "Authorization: Bearer $PRINTIFY_API_TOKEN" \
  -H "User-Agent: ClaudeCode-Hokuno/1.0" | jq .
```

### Get Order Details

```bash
curl -s "https://api.printify.com/v1/shops/{shop_id}/orders/{order_id}.json" \
  -H "Authorization: Bearer $PRINTIFY_API_TOKEN" \
  -H "User-Agent: ClaudeCode-Hokuno/1.0" | jq .
```

## Webhooks

### Create a Webhook

```bash
curl -s -X POST "https://api.printify.com/v1/shops/{shop_id}/webhooks.json" \
  -H "Authorization: Bearer $PRINTIFY_API_TOKEN" \
  -H "Content-Type: application/json" \
  -H "User-Agent: ClaudeCode-Hokuno/1.0" \
  -d '{
    "topic": "order:created",
    "url": "https://your-webhook-url.com/printify"
  }'
```

Available topics: `order:created`, `order:updated`, `order:sent-to-production`, `order:shipping-update`, `order:completed`, `product:deleted`, `product:publish:started`

## Error Handling

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Process response |
| 400 | Bad request | Check request body/params |
| 401 | Unauthorized | Check PRINTIFY_API_TOKEN |
| 403 | Forbidden | Check token scopes |
| 404 | Not found | Check shop_id/product_id |
| 429 | Rate limited | Wait 60s, retry |
| 500 | Server error | Retry after 5s, max 3 retries |

## Important Notes

- Never commit API tokens to git — use environment variables only
- Product IDs are strings, not integers
- All prices are in cents (integer)
- Images must be PNG/JPEG, minimum 300 DPI for quality prints
- The API does not return design/artwork files, only mockup images
- Always check `is_enabled` on variants — disabled variants should not be published
