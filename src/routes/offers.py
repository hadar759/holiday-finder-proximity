from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from src.app.offers_distance_sorter import add_distance_to_offers
from src.app.params import CITY_CENTERS
from src.models.offer import (
    Budget,
    OfferEngineOptions,
    OfferEngineWhoOption,
    OfferOptions,
    OfferWithDistance,
)
from src.app.get_holiday_offers import get_holiday_offers
from src.app.distance import geocode_address

router = APIRouter(prefix="/offers")


@router.get("")
async def get_offers(
    comparison_address: str | None = Query(default=None, alias="comparison-address"),
    locale: str = Query(default="he"),
    currency: str = Query(default="USD"),
    fromwhere: List[str] = Query(default=["TLV"], alias="from-where"),
    market: int = Query(default=4),
    where: Optional[List[int]] = Query(default=None),
    whereTxt: List[str] = Query(default=["Rome"], alias="where-txt"),
    start_date: str = Query(
        default=datetime.now().strftime("%d/%m/%Y"), alias="start-date"
    ),
    end_date: str = Query(
        default=(datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y"),
        alias="end-date",
    ),
    who: OfferEngineWhoOption = Query(default=OfferEngineWhoOption()),
    budget_min: int = Query(default=0, ge=0, alias="budget-min"),
    budget_max: int = Query(default=1000, ge=1, alias="budget-max"),
    flex: bool = Query(default=False),
    min_nights: int = Query(default=1, alias="min-nights"),
    max_nights: int = Query(default=7, alias="max-nights"),
):
    """
    Get holiday offers based on filters
    """
    comparison_address = (
        comparison_address
        if comparison_address is not None
        else CITY_CENTERS[whereTxt[0]]
    )
    comparison_coordinates = geocode_address(comparison_address)
    try:
        offer_options = OfferOptions(
            locale=locale,
            currency=currency,
            fromwhere=fromwhere,
            engine=OfferEngineOptions(
                market=market,
                where=where,
                when={
                    "months": {
                        "periods": [],
                        "from": start_date,
                        "to": end_date,
                        "min": min_nights,
                        "max": max_nights,
                        "nights": [i for i in range(min_nights, max_nights + 1)],
                    },
                },
                who=who,
                whereTxt=whereTxt,
                budget=Budget(min=budget_min, max=budget_max),
                flex=flex,
            ),
        )

        print(f"offer_options: {offer_options}")
        offers = get_holiday_offers(offer_options)
        valid_offers = [offer for offer in offers if offer is not None]

        offers_with_distance: list[OfferWithDistance] = add_distance_to_offers(
            valid_offers, comparison_coordinates
        )
        if not offers_with_distance:
            return []

        offers_with_distance.sort(key=lambda x: x.distance_m)

        return [
            {
                "name": offer.hotel_name,
                "url": offer.url,
                "google_maps_url": offer.google_maps_url,
                "nights_amount": offer.nights_amount,
                "start_date": offer.outbound_date,
                "end_date": offer.inbound_date,
                "distance_meters": int(offer.distance_m),
                "price": offer.price,
                "airline": offer.airline,
            }
            for offer in offers_with_distance
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch offers: {str(e)}")
