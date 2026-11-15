# Inventory Control and Stockout Prevention SOP

## 1. Inventory Categories
SHGs maintain three distinct inventory classifications:
1. **Raw Materials:** Uncut fabrics, raw jute bundles, yarn, threads, dyes, and buckles.
2. **Work-in-Progress (WIP):** Cut patterns, partially embroidered panels, and unstitched assemblies.
3. **Finished Goods:** Complete, inspected, and packaged products ready for customer delivery.

## 2. Bulk Reservation vs Retail Stock Separation
- When a bulk order is approved, the required raw materials and components are locked under `bulk_reserved_stock`.
- Retail orders placed through consumer channels may **only** reserve freely available stock:
  $$\text{Available Stock} = \text{Physical Stock} - \text{Bulk Reserved} - \text{Retail Reserved} - \text{Damaged Stock}$$
- Retail reservations are prohibited from breaching the bulk reservation threshold.

## 3. Lead Time and Restocking Alerts
- Supplier delivery times from wholesale textile markets typically range between 5 to 10 days.
- Reorder points are determined by daily burn rate and lead times:
  $$\text{Reorder Point} = \text{Daily Burn Rate} \times \text{Lead Time Days} \times 1.25$$
- An automated restock alert is triggered when available stock drops below the reorder point.

