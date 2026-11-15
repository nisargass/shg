# SHG Saathi – Database & Domain Model Specification

## 1. Overview & Engine Configuration

- **Development / Demonstration Engine**: SQLite 3 (`shg_saathi.db`).
- **Production Engine**: PostgreSQL 14+ with Alembic migrations.
- **ORM**: SQLAlchemy 2.0 with pure Python fallback enabled.

The database is pre-seeded with rich operational data representing **Pragati Mahila SHG (NRLM Reg: KA-BLR-2024-0891)**, containing 8 active artisan members, 4 bulk corporate orders, live inventory, quality inspection records, bank payout rolls, and retail products.

---

## 2. Seed Personas & Demo Credentials

All test personas share the same standard demo password: **`Saathi@2026`**.

| Persona / Role | Full Name | Email Address | Portal Route | Primary Capabilities |
|----------------|-----------|---------------|--------------|----------------------|
| **SHG Leader** | Savitribai Shinde | `savitribai@pragati-shg.org` | `/leader` | Work allocation approval, quality review gate, costing, bank payout confirmation |
| **SHG Member** | Sunita Rathod | `sunita.rathod@shg.in` | `/member` | View daily task cards, submit production batches, cast payout quorum votes |
| **Wholesale Buyer** | Amit Deshmukh | `procurement@ecofab.in` | `/buyer` | Place bulk orders, track live milestones, inspect digital inspection certificates |
| **NRLM Federation Officer** | Deepa Narayan | `deepa.narayan@ksrlps.gov.in` | `/federation` | State-level monitoring, SHG performance scorecards, financial anomaly audit |
| **Retail Customer** | Pooja Hegde | `pooja.h@gmail.com` | `/marketplace` | Browse handcrafted catalog, add to cart, place retail orders |

---

## 3. Relational Schema & Entity Relationships

```
+--------------------------------------------------------------------------------------------------+
|                                    ORGANIZATION & USER ENTITIES                                  |
+--------------------------------------------------------------------------------------------------+

  +-----------------------+              +-----------------------+
  |      SHG Group        | 1          * |         User          |
  |-----------------------|------------->|-----------------------|
  | id (PK)               |              | id (PK)               |
  | name                  |              | shg_id (FK)           |
  | registration_number   |              | email (Unique)        |
  | village, district     |              | hashed_password       |
  | bank_account_no       |              | role (Enum)           |
  +-----------------------+              +-----------------------+
              |                                      | 1
              | 1                                    |
              |                                      v 1
              | *                        +-----------------------+
              +------------------------->|     Member Profile    |
                                         |-----------------------|
                                         | id (PK)               |
                                         | user_id (FK)          |
                                         | skills (JSON)         |
                                         | experience_years      |
                                         | quality_score         |
                                         | daily_hours_capacity  |
                                         +-----------------------+

+--------------------------------------------------------------------------------------------------+
|                                       BULK ORDER LIFECYCLE                                       |
+--------------------------------------------------------------------------------------------------+

  +-----------------------+ 1          * +-----------------------+ 1          * +--------------------+
  |      BulkOrder        |------------->|      Allocation       |------------->|  ProductionBatch   |
  |-----------------------|              |-----------------------|              |--------------------|
  | id (PK)               |              | id (PK)               |              | id (PK)            |
  | order_number (Unique) |              | order_id (FK)         |              | allocation_id (FK) |
  | buyer_id (FK)         |              | member_id (FK)        |              | member_id (FK)     |
  | product_name          |              | allocated_quantity    |              | submitted_quantity |
  | total_quantity        |              | completed_quantity    |              | status (Enum)      |
  | agreed_unit_price     |              | completion_likelihood |              | submitted_at       |
  | deadline              |              | status (Enum)         |              +--------------------+
  | status (Enum)         |              +-----------------------+                        | 1
  +-----------------------+                                                               |
                                                                                          v 1
                                                                                +--------------------+
                                                                                | Quality Inspection |
                                                                                |--------------------|
                                                                                | id (PK)            |
                                                                                | batch_id (FK)      |
                                                                                | ai_defect_status   |
                                                                                | ai_confidence      |
                                                                                | human_decision     |
                                                                                | approved_quantity  |
                                                                                | rework_quantity    |
                                                                                | remarks            |
                                                                                +--------------------+

+--------------------------------------------------------------------------------------------------+
|                                    FINANCIAL & PAYOUT ROLL                                       |
+--------------------------------------------------------------------------------------------------+

  +-----------------------+ 1          * +-----------------------+
  |    Payout Approval    |------------->|     Group Approval    |
  |-----------------------|              | (Quorum Voting)       |
  | id (PK)               |              |-----------------------|
  | order_id (FK)         |              | id (PK)               |
  | total_amount          |              | payout_approval_id(FK)|
  | quorum_reached (Bool) |              | member_id (FK)        |
  | disbursed_at          |              | vote (Enum)           |
  +-----------------------+              | voted_at              |
                                         +-----------------------+
```

---

## 4. Model Class Index

- `backend/app/models/user.py`: `User`, `SHG`, `Member`, `Buyer`, `MemberCapacity`
- `backend/app/models/order.py`: `BulkOrder`, `OrderItem`, `Product`, `ProductSpecification`
- `backend/app/models/allocation.py`: `Allocation`, `AllocationStatus`
- `backend/app/models/production.py`: `ProductionBatch`, `BatchStatus`
- `backend/app/models/quality.py`: `QualityInspection`, `InspectionStatus`
- `backend/app/models/pricing.py`: `CostStructure`, `PriceQuote`
- `backend/app/models/inventory.py`: `Inventory`, `MaterialPurchase`
- `backend/app/models/logistics.py`: `Supplier`, `Shipment`
- `backend/app/models/finance.py`: `MemberEarning`, `PayoutApproval`, `GroupApproval`
- `backend/app/models/retail.py`: `RetailProduct`, `RetailOrder`, `RetailOrderItem`
- `backend/app/models/support.py`: `Notification`, `Document`, `AIAnalysisRecord`, `AuditLog`

