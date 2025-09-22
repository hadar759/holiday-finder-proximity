import json
from urllib.parse import quote
import urllib.request
from typing import List, Dict, Optional, Any
from datetime import datetime
from params import base_url, data


def fetch_offers_data(url: str) -> List[Dict[str, Any]]:
    """
    Fetch hotel data from the given URL
    Returns list of hotel offers
    """
    try:
        request = urllib.request.Request(url)
        request.add_header(
            "User-Agent",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        )

        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode())

        # Extract offers from the response structure
        if "data" in data and "offers" in data["data"]:
            return data["data"]["offers"]
        elif isinstance(data, list):
            return data
        else:
            raise ValueError("Unexpected data structure")

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


def extract_hotel_info(offer: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Extract relevant hotel information from an offer
    Returns dict with name, coordinates, dates, URL, price, airline, nights_amount, and google_maps_url
    """
    hotel = offer.get("hotel", {})
    offer_data = offer.get("offer", {})
    flight_data = offer.get("flight", {})

    # Extract coordinates
    coords = hotel.get("coordinates", {})
    if not coords or "latitude" not in coords or "longitude" not in coords:
        return None

    hotel_name = hotel.get("name", "Unknown Hotel")
    latitude = float(coords["latitude"])
    longitude = float(coords["longitude"])
    outbound_date = offer_data.get("outboundDate", "")
    inbound_date = offer_data.get("inboundDate", "")

    return {
        "name": hotel_name,
        "latitude": latitude,
        "longitude": longitude,
        "outbound_date": outbound_date,
        "inbound_date": inbound_date,
        "nights_amount": calculate_nights(outbound_date, inbound_date),
        "url": offer_data.get("packageDeeplinkUrl", ""),
        "price": offer_data.get("price", 0),
        "airline": flight_data.get("company_name", "Unknown Airline"),
        "google_maps_url": generate_google_maps_url(latitude, longitude),
    }


def get_holiday_offers():
    offers = fetch_offers_data(f"{base_url}/?data={quote(json.dumps(data))}")
    print("got offers")
    return [extract_hotel_info(offer) for offer in offers]


if __name__ == "__main__":
    get_holiday_offers()
