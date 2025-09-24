from pydantic import BaseModel

from models.common import Coordinates


class ProcessedOffer(BaseModel):
    hotel_name: str
    image_url: str | None
    coordinates: Coordinates
    outbound_date: str
    inbound_date: str
    nights_amount: int
    url: str
    price: int
    airline: str
    google_maps_url: str

class OfferWithDistance(ProcessedOffer):
    distance_m: float