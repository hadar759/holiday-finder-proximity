from src.models.holiday_finder_api import Offer
from pydantic import BaseModel, Field


class Budget(BaseModel):
    min: int = Field(default=0)
    max: int = Field(default=1000)


class OfferEngineWhoOption(BaseModel):
    adult: int = Field(default=2)
    child: int = Field(default=0)
    room: int = Field(default=1)
    childAges: list[int] = Field(default=[])


class OfferEngineOptions(BaseModel):
    market: int = Field(default=4)
    where: list[int] | None = Field(default=None)
    when: dict
    who: OfferEngineWhoOption = Field(default=OfferEngineWhoOption())
    whereTxt: list[str]
    budget: Budget = Field(default=Budget())
    flex: bool = Field(default=False)


class OfferOptions(BaseModel):
    locale: str = Field(default="he")
    currency: str = Field(default="USD")
    fromwhere: list[str] = Field(default=["TLV"])
    engine: OfferEngineOptions


class OfferWithCalculatedFields(Offer):
    nights_amount: int
    google_maps_url: str


class OfferWithDistance(OfferWithCalculatedFields):
    distance_m: float
