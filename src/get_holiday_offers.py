import json
from urllib.parse import quote
import urllib.request
from typing import List, Optional
from datetime import datetime
from params import base_url, data
from models.holiday_finder_api import ApiResponse, Offer
from models.offer import ProcessedOffer


def fetch_offers_data(url: str) -> List[Offer]:
    """
    Fetch hotel data from the given URL
    Returns list of typed hotel offers
    """
    try:
        request = urllib.request.Request(url)
        request.add_header(
            "User-Agent",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        )

        with urllib.request.urlopen(request) as response:
            raw_data = json.loads(response.read().decode())

        # Parse and validate the response using Pydantic
        api_response = ApiResponse.model_validate(raw_data)
        return api_response.data.offers

    except Exception as e:
        raise Exception(f"Failed to fetch data from URL '{url}': {e}")


def calculate_nights(outbound_date: str, inbound_date: str) -> int:
    """
    Calculate number of nights between outbound and inbound dates
    Expected format: DD/MM/YYYY
    """
    try:
        out_date = datetime.strptime(outbound_date, "%d/%m/%Y")
        in_date = datetime.strptime(inbound_date, "%d/%m/%Y")
        return (in_date - out_date).days
    except (ValueError, TypeError):
        return 0


def generate_google_maps_url(latitude: float, longitude: float) -> str:
    """
    Generate Google Maps link for hotel using coordinates
    """
    return f"https://www.google.com/maps/place/{latitude},{longitude}"


def extract_hotel_info(offer: Offer) -> Optional[ProcessedOffer]:
    """
    Extract relevant hotel information from an offer
    Returns ProcessedOffer with name, coordinates, dates, URL, price, airline, nights_amount, and google_maps_url
    """
    try:
        latitude = offer.hotel.coordinates.latitude
        longitude = offer.hotel.coordinates.longitude
        outbound_date = offer.offer.outboundDate
        inbound_date = offer.offer.inboundDate

        return ProcessedOffer(
            hotel_name=offer.hotel.name,
            image_url=offer.hotel.photos[0],
            coordinates=offer.hotel.coordinates,
            outbound_date=outbound_date,
            inbound_date=inbound_date,
            nights_amount=calculate_nights(outbound_date, inbound_date),
            url=offer.offer.packageDeeplinkUrl,
            price=offer.offer.price,
            airline=offer.flight.company_name,
            google_maps_url=generate_google_maps_url(latitude, longitude),
        )
    except Exception:
        return None


def get_holiday_offers() -> List[Optional[ProcessedOffer]]:
    """
    Fetch and process holiday offers
    Returns list of processed offers (some may be None if processing failed)
    """
    offers = fetch_offers_data(f"{base_url}/?data={quote(json.dumps(data))}")
    return [extract_hotel_info(offer) for offer in offers]


if __name__ == "__main__":
    get_holiday_offers()
