# Database schema

This document describes the primary data model for the supply chain optimization system built in Phase 2.

## Core entities

### SKU
- Primary key: `id` (`SKU-000001` format)
- Represents a unique product / stock-keeping unit.
- One-to-many: one SKU can appear in many inventory records, forecasts, and purchase orders.
- Many-to-many: many SKUs can be supplied by many suppliers via `sku_supplier`.

### Location
- Primary key: `id` (`LOC-0001` format)
- Represents a warehouse, distribution center, or plant location.
- One-to-many: one location can host many inventory balances, shortages, production plans, and purchase orders.

### Supplier
- Primary key: `id` (`SUP-0001` format)
- Represents a source vendor or manufacturing partner.
- One-to-many: one supplier can have many purchase orders and capacity entries.
- Many-to-many: many suppliers can cover many SKUs via `sku_supplier`.

### Inventory
- Primary key: `id` (`INV-SKU-...-LOC-...`)
- Stores the current on-hand, reserved, and in-transit stock for a given SKU at a location.
- One-to-many: one inventory record has many historical `inventory_events`.

### ForecastDemand
- Primary key: `id` (`DEM-SKU-LOCATION-2026W01`)
- Stores weekly demand forecasts for a SKU at a location.
- One-to-many from location and SKU.

### PurchaseOrder
- Primary key: `id` (`PO-2026-000001`)
- Tracks planned or historical purchase orders.
- One-to-many from supplier, SKU, and location.

### ProductionPlan
- Primary key: `id` (`PP-SKU-...`)
- Represents a planned production schedule for a SKU at a location.

### Shortage
- Primary key: `id` (`SHORT-2026-000001`)
- Captures projected shortages by SKU and location.
- One-to-many: a shortage can lead to multiple mitigation options.

### MitigationOption
- Primary key: `id` (`MIT-SHORTAGE-ID-01`)
- Contains recommended actions to mitigate a shortage.
- Many-to-one: each mitigation option belongs to a shortage record.

### SupplierCapacity
- Primary key: `id`
- Stores per-SKU capacity and effective-date windows for suppliers.

### LeadTime
- Primary key: `id`
- Tracks supplier lead time by SKU and location over time.

### InventoryEvent
- Primary key: `id`
- Explicit historical event log for inventory changes.
- Supports auditability and change tracking without overwriting prior inventory states.

## Additional bridge table

### SkuSupplier
- Composite primary key: `(sku_id, supplier_id)`
- Captures the many-to-many relationship between SKUs and suppliers.
- Stores contract details such as minimum order quantity and preferred supplier selection.

## Shared fields

Each table keeps the following lifecycle fields when relevant:
- `created_at`
- `updated_at`
- `lifecycle_status`
- `effective_from` / `effective_to` for temporal changes

This ensures that historical purchase orders, forecasts, and allocation decisions can be retained without overwriting the original record.
