import sys
import json
from get_holiday_offers import get_holiday_offers
from params import comparison_address
from distance import haversine_distance, geocode_address
from models.offer import OfferWithDistance


def main():
    try:
        comp_lat, comp_lon = geocode_address(comparison_address)
        offers = get_holiday_offers()

        # Process and calculate distances
        offers_with_distance: list[OfferWithDistance] = []

        for offer in offers:
            if offer is not None:
                distance = haversine_distance(
                    comp_lat,
                    comp_lon,
                    offer.coordinates.latitude,
                    offer.coordinates.longitude,
                )
                offer_with_distance = OfferWithDistance(
                    **offer.model_dump(),
                    distance_m=distance,
                )
                offers_with_distance.append(offer_with_distance)

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
