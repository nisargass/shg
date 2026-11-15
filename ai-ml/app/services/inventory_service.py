from app.schemas.inventory import InventoryRestockRequest, InventoryRestockResponse
from app.utils.calculations import calculate_inventory_stockout


class InventoryService:
    def forecast_restock(self, req: InventoryRestockRequest) -> InventoryRestockResponse:
        retail_res = req.retail_reserved_stock or 0.0
        # Total committed = bulk + retail reserved
        total_committed = req.bulk_committed_stock + retail_res
        free_stock = max(0.0, req.current_physical_stock - total_committed)

        res = calculate_inventory_stockout(
            current_physical_stock=req.current_physical_stock,
            bulk_committed_stock=total_committed,
            lead_time_days=req.lead_time_days,
            daily_burn_rate=req.daily_burn_rate
        )

        urgency = res["urgency"]
        if urgency == "CRITICAL":
            suggested_action = "EXPEDITE_EMERGENCY_REPLENISHMENT"
        elif urgency == "HIGH":
            suggested_action = "PLACE_PURCHASE_ORDER_IMMEDIATELY"
        elif urgency == "MEDIUM":
            suggested_action = "PLAN_WEEKLY_RESTOCK"
        else:
            suggested_action = "INVENTORY_LEVELS_HEALTHY"

        return InventoryRestockResponse(
            success=True,
            inventory_id=req.inventory_id,
            physical_stock=req.current_physical_stock,
            bulk_reserved_stock=req.bulk_committed_stock,
            retail_reserved_stock=retail_res,
            free_stock=free_stock,
            days_until_stockout=res["days_until_stockout"],
            restock_recommended=res["restock_recommended"],
            recommended_order_quantity=res["recommended_order_quantity"],
            urgency=urgency,
            suggested_action=suggested_action,
            explanation=res["explanation"]
        )


inventory_service = InventoryService()
