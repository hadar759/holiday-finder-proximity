import sys
import json
from .get_holiday_offers import get_holiday_offers
from .params import CITY_CENTERS
from .distance import haversine_distance, geocode_address
from src.models.common import Coordinates
from src.models.offer import (
    Budget,
    OfferOptions,
    OfferEngineOptions,
    OfferWithDistance,
    ParsedOffer,
)


def add_distance_to_offers(
    offers: list[ParsedOffer], comp_coordinates: Coordinates
) -> list[OfferWithDistance]:
    offers_with_distance = []
    for offer in offers:
        distance = haversine_distance(
            comp_coordinates.latitude,
            comp_coordinates.longitude,
            offer.coordinates.latitude,
            offer.coordinates.longitude,
        )
        offers_with_distance.append(
            OfferWithDistance(
                **offer.model_dump(),
                distance_m=distance,
            )
        )
    offers_with_distance.sort(key=lambda x: x.distance_m)
    return offers_with_distance


def main():
    min_nights = 5
    max_nights = 6
    min_budget = 0
    max_budget = 550
    city = "Rome"

    offer_options = OfferOptions(
        engine=OfferEngineOptions(
            market=4,
            when={
                "months": {
                    "periods": [
                        {"start": "01/10/2025", "end": "31/10/2025"},
                        {"start": "01/11/2025", "end": "30/11/2025"},
                    ],
                    "min": min_nights,
                    "max": max_nights,
                    "nights": [min_nights, max_nights],
                }
            },
            whereTxt=[city],
            budget=Budget(min=min_budget, max=max_budget),
            flex=False,
        ),
        sort={"best": -1},
        limit=1000,
        offset=0,
    )
    comparison_address = CITY_CENTERS[city]

    try:
        comp_coordinates = geocode_address(comparison_address)
        offers = get_holiday_offers(offer_options)

        # Process and calculate distances
        offers_with_distance: list[OfferWithDistance] = add_distance_to_offers(
            offers, comp_coordinates
        )
        if not offers_with_distance:
            return

        offers_with_distance.sort(key=lambda x: x.distance_m)

        output_data = []
        for offer in offers_with_distance:
            output_data.append(
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
            )

        print(f"got {len(output_data)} offers")
        print(
            f"Closest offer: {json.dumps(output_data[0], indent=2, ensure_ascii=False)}"
        )
        # Write results to JSON file
        with open("output/hotels_output.json", "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
