from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Query
from typing import List
from src.app.offers_distance_sorter import add_distance_to_offers
from src.models.offer import (
    Budget,
    OfferEngineOptions,
    OfferEngineWhoOption,
    OfferOptions,
    OfferWithDistance,
)
from src.app.get_holiday_offers import get_holiday_offers
from src.app.distance import geocode_address
import traceback

router = APIRouter(prefix="/offers")


@router.get("")
async def get_offers(
    comparison_address: str | None = Query(default=None, alias="comparison-address"),
    locale: str = Query(default="he"),
    currency: str = Query(default="USD"),
    fromwhere: List[str] = Query(default=["TLV"], alias="from-where"),
    market: int = Query(default=4),
    whereTxt: List[str] = Query(default=["Rome"], max_length=1, alias="where-txt"),
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
    nights: list[int] = Query(default=[1, 2]),
):
    """
    Get holiday offers based on filters
    """
    print(
        "Starting get_offers with params:",
        {
            "comparison_address": comparison_address,
            "locale": locale,
            "currency": currency,
            "fromwhere": fromwhere,
            "market": market,
            "whereTxt": whereTxt,
            "start_date": start_date,
            "end_date": end_date,
            "who": who,
            "budget_min": budget_min,
            "budget_max": budget_max,
            "flex": flex,
            "nights": nights,
        },
    )

    fallback_to_city_center = False
    if comparison_address is None:
        if len(whereTxt) == 0:
            raise HTTPException(
                status_code=400,
                detail="Comparison address is required unless where-txt param is provided",
            )
        city = whereTxt[0]
        comparison_address = city
        fallback_to_city_center = True

    try:
        comparison_coordinates = geocode_address(
            comparison_address, is_city=fallback_to_city_center
        )
    except Exception:
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Failed to find address: {comparison_address}. {'Try explicitly entering an address' if fallback_to_city_center else 'Try a different address'}",
        )

    try:
        offer_options = OfferOptions(
            locale=locale,
            currency=currency,
            fromwhere=fromwhere,
            engine=OfferEngineOptions(
                market=market,
                when={
                    "flexible": {
                        "start": start_date,
                        "end": end_date,
                        "min": min(nights),
                        "max": max(nights),
                        "nights": nights,
                    },
                },
                who=who,
                whereTxt=whereTxt,
                budget=Budget(min=budget_min, max=budget_max),
                flex=flex,
            ),
        )

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
                "name": offer.hotel.name,
                "url": offer.offer.packageDeeplinkUrl,
                "rating": offer.hotel.rating,
                "image_url": offer.hotel.photos[0]
                if len(offer.hotel.photos) > 0
                else None,
                "google_maps_url": offer.google_maps_url,
                "nights_amount": offer.nights_amount,
                "start_date": offer.offer.outboundDate,
                "end_date": offer.offer.inboundDate,
                "distance_meters": int(offer.distance_m),
                "price": offer.offer.price,
                "airline": offer.flight.company_name,
            }
            for offer in offers_with_distance
        ]

    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Failed to fetch offers: {str(e)}")
