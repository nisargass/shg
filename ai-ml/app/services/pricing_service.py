from app.schemas.pricing import MarketBenchmarkRange, PricingRequest, PricingResponse
from app.utils.calculations import calculate_pricing_breakdown


class PricingService:
    def recommend_pricing(self, req: PricingRequest) -> PricingResponse:
        res = calculate_pricing_breakdown(
            material_cost=req.material_cost,
            labor_cost=req.labor_cost,
            packaging_cost=req.packaging_cost,
            transport_cost=req.transport_cost,
            operational_expenses=req.operational_expenses,
            quantity=req.quantity,
            target_margin_percentage=req.target_margin_percentage
        )

        benchmark = None
        if res.get("market_benchmark_range"):
            bm = res["market_benchmark_range"]
            benchmark = MarketBenchmarkRange(
                min_unit_price=bm["min_unit_price"],
                max_unit_price=bm["max_unit_price"],
                source=bm.get("source")
            )

        return PricingResponse(
            success=True,
            recommended_selling_price_per_unit=res["recommended_selling_price_per_unit"],
            recommended_total_order_value=res["recommended_total_order_value"],
            estimated_profit=res["estimated_profit"],
            margin_percentage=res["margin_percentage"],
            missing_cost_warnings=res["missing_cost_warnings"],
            market_benchmark_range=benchmark
        )


pricing_service = PricingService()

