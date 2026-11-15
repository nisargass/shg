from typing import List, Optional
from pydantic import BaseModel, Field, model_validator


class CarrierRecommendation(BaseModel):
    carrier_name: str
    estimated_cost: float = Field(..., description="Estimated shipping charge in INR")
    estimated_transit_hours: int = Field(..., description="Estimated delivery turnaround time in hours")
    reliability_rating: float = Field(..., description="Carrier track record rating out of 5.0")
    service_type: Optional[str] = "Standard Ground Parcel"


class LogisticsRequest(BaseModel):
    origin_pincode: Optional[str] = Field(None, description="6-digit Indian PIN code of pickup origin")
    origin: Optional[str] = Field(None, description="Origin alias for backwards compatibility")
    destination_pincode: Optional[str] = Field(None, description="6-digit Indian PIN code of destination")
    destination: Optional[str] = Field(None, description="Destination alias for backwards compatibility")
    weight_kg: float = Field(..., gt=0.0, description="Total parcel weight in kg")
    target_delivery_date: Optional[str] = Field(None, description="Optional required delivery deadline")

    @model_validator(mode="after")
    def unify_pincode_fields(self):
        # Resolve aliases
        if not self.origin_pincode and self.origin:
            self.origin_pincode = self.origin
        if not self.destination_pincode and self.destination:
            self.destination_pincode = self.destination

        if not self.origin_pincode:
            raise ValueError("Either 'origin_pincode' or 'origin' must be provided")
        if not self.destination_pincode:
            raise ValueError("Either 'destination_pincode' or 'destination' must be provided")
        return self


class LogisticsResponse(BaseModel):
    success: bool = True
    recommended_carriers: List[CarrierRecommendation] = []
    explanation: Optional[str] = None

