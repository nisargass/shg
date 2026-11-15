import os
import joblib
import pandas as pd
from typing import Any, Dict, List
from app.schemas.retail import RetailDemandRequest, RetailDemandResponse
from app.utils.calculations import forecast_retail_demand_statistical

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
MODEL_PATH = os.path.join(SAVED_MODELS_DIR, "demand_forecaster.joblib")


class RetailService:
    def __init__(self):
        self.pipeline = None
        self._load_model()

    def _load_model(self):
        try:
            if os.path.exists(MODEL_PATH):
                self.pipeline = joblib.load(MODEL_PATH)
        except Exception:
            self.pipeline = None

    def forecast_demand(self, req: RetailDemandRequest) -> RetailDemandResponse:
        hist_data = [s.model_dump() for s in req.historical_sales]
        res = forecast_retail_demand_statistical(
            product_id=req.product_id,
            historical_sales=hist_data,
            upcoming_festival_season=req.upcoming_festival_season
        )

        factors = []
        if req.upcoming_festival_season:
            factors.append("Festival season surge multiplier (1.4x - 1.8x) applied")
        else:
            factors.append("Standard non-festive sales velocity baseline")

        forecast_val = res["forecasted_monthly_demand"]

        # If ML model is loaded, refine estimate using ML pipeline
        if self.pipeline is not None and hist_data:
            try:
                recent_sales = [h["quantity"] for h in hist_data]
                past_7d = float(recent_sales[-1] * 0.25 if recent_sales else 30.0)
                past_30d = float(recent_sales[-1] if recent_sales else 120.0)
                seasonality = 1.6 if req.upcoming_festival_season else 1.0

                df_in = pd.DataFrame([{
                    "past_7d_sales": past_7d,
                    "past_30d_sales": past_30d,
                    "seasonality_index": seasonality,
                    "lead_time_days": req.lead_time_days or 7,
                    "physical_stock": 50.0,
                    "bulk_reserved_stock": 20.0,
                    "retail_reserved_stock": 10.0,
                    "free_stock": 20.0,
                    "product_category": req.product_category or "Handloom"
                }])
                ml_pred_14d = float(self.pipeline.predict(df_in)[0])
                # Monthly projection
                forecast_val = int(round(ml_pred_14d * 2.1))
                factors.append("Refined via Scikit-learn Demand Forecaster (RandomForestRegressor)")
            except Exception:
                pass

        ci_lower = max(0, int(round(forecast_val * 0.82)))
        ci_upper = int(round(forecast_val * 1.22))

        suggested_action = "RAMP_UP_PRODUCTION" if forecast_val > 150 else "MAINTAIN_STANDARD_REPLENISHMENT"

        return RetailDemandResponse(
            success=True,
            product_id=res["product_id"],
            forecasted_monthly_demand=forecast_val,
            confidence_interval=[ci_lower, ci_upper],
            confidence_score=res.get("confidence_score", 0.85),
            seasonal_factor=res.get("seasonal_factor"),
            explanation=res["explanation"],
            forecast_period="Next 30 Days",
            factors=factors,
            suggested_action=suggested_action
        )


retail_service = RetailService()
