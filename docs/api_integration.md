# API Integration Details

## Inventory Endpoint Batch Querying
The robotic assistant integrates with external databases using robust querying.
**Configuration:** `INVENTORY_API=https://studio-website/api/inventory`

## Query Format
Uses `requests` with parameters. During batch checks (e.g. "Check ABS and PLA"), it iterates parameters gracefully with retry loops of 3 attempts:
```http
GET /api/inventory?item=PLA HTTP/1.1
GET /api/inventory?item=ABS HTTP/1.1
```

## CSV Data Sink
All inventory calls are logged asynchronously to `/logs/inventory_queries.csv` containing fields:
`timestamp`, `items_queried`, `available_booleans`, `success`
