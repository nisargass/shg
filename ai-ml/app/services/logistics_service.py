from app.schemas.logistics import CarrierRecommendation, LogisticsRequest, LogisticsResponse
from app.utils.validators import validate_pincode


class LogisticsService:
    def recommend_route(self, req: LogisticsRequest) -> LogisticsResponse:
        origin_pin = validate_pincode(req.origin_pincode, field_name="origin_pincode")
        dest_pin = validate_pincode(req.destination_pincode, field_name="destination_pincode")

        weight = max(1.0, req.weight_kg)

        # Distance estimation based on Indian Postal PIN code circles
        # Karnataka circle: 56xxxx, 57xxxx, 58xxxx, 59xxxx
        karnataka_prefixes = ("56", "57", "58", "59")
        is_intra_karnataka = (origin_pin[:2] in karnataka_prefixes and dest_pin[:2] in karnataka_prefixes)
        same_circle = (origin_pin[:2] == dest_pin[:2]) or is_intra_karnataka
        same_zone = (origin_pin[0] == dest_pin[0])

        carriers = []
        if same_circle:
            # Intra-state transit (e.g. Mysuru 570001 to Bengaluru 560001)
            transit_hours = 18
            rate_per_kg = 10.0
            base_charge = 150.0
            estimated_cost = round(base_charge + (weight * rate_per_kg), 2)

            carrier_name = "KSRTC Cargo Logistics" if is_intra_karnataka else "State Road Transport Express Cargo"
            carriers.append(
                CarrierRecommendation(
                    carrier_name=carrier_name,
                    estimated_cost=estimated_cost,
                    estimated_transit_hours=transit_hours,
                    reliability_rating=4.6,
                    service_type="State Road Transport Express Cargo"
                )
            )
            carriers.append(
                CarrierRecommendation(
                    carrier_name="India Post Registered Parcel",
                    estimated_cost=round(100.0 + (weight * 8.0), 2),
                    estimated_transit_hours=48,
                    reliability_rating=4.3,
                    service_type="Postal Service"
                )
            )
        elif same_zone:
            # Inter-state same zone (e.g. Karnataka to Tamil Nadu)
            transit_hours = 36
            carriers.append(
                CarrierRecommendation(
                    carrier_name="Regional Express Ground Logistics",
                    estimated_cost=round(250.0 + (weight * 14.0), 2),
                    estimated_transit_hours=transit_hours,
                    reliability_rating=4.4,
                    service_type="Surface Cargo"
                )
            )
            carriers.append(
                CarrierRecommendation(
                    carrier_name="India Post Speed Post",
                    estimated_cost=round(200.0 + (weight * 12.0), 2),
                    estimated_transit_hours=72,
                    reliability_rating=4.2,
                    service_type="Speed Post National Network"
                )
            )
        else:
            # National cross-country transit
            carriers.append(
                CarrierRecommendation(
                    carrier_name="National Surface Freight",
                    estimated_cost=round(400.0 + (weight * 18.0), 2),
                    estimated_transit_hours=96,
                    reliability_rating=4.1,
                    service_type="Inter-State Commercial Freight"
                )
            )
            carriers.append(
                CarrierRecommendation(
                    carrier_name="India Post Parcel Service",
                    estimated_cost=round(300.0 + (weight * 15.0), 2),
                    estimated_transit_hours=120,
                    reliability_rating=4.3,
                    service_type="National Parcel Grid"
                )
            )

        explanation = (
            f"Logistics estimates between PIN {origin_pin} and {dest_pin} for {weight}kg parcel. "
            f"Calculated via regional transit matrix. No live commercial tracking carrier is connected."
        )

        return LogisticsResponse(
            success=True,
            recommended_carriers=carriers,
            explanation=explanation
        )


logistics_service = LogisticsService()
