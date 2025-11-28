import json
from urllib.parse import quote
import urllib.request
from typing import List, Optional
from datetime import datetime
from src.models.holiday_finder_api import ApiResponse, Offer
from src.models.offer import OfferOptions, OfferWithCalculatedFields

base_url = "https://www.holidayfinder.co.il/api_no_auth/holiday_finder/offers"
CITY_NUMBERS = {"Prague": 28, "Rome": 19}


def fetch_offers_data(offer_options: OfferOptions) -> List[Offer]:
    """
    Fetch hotel data from the given URL
    Returns list of typed hotel offers
    """
    try:
        data = {
            **offer_options.model_dump(),
            "sort": {"best": -1},
            "limit": 1000,
            "offset": 0,
        }
        if data["engine"]["where"] is None and data["engine"]["whereTxt"] is not None:
            maybe_city_number = CITY_NUMBERS.get(data["engine"]["whereTxt"][0])
            if maybe_city_number is not None:
                data["engine"]["where"] = [maybe_city_number]

        url = f"{base_url}/?data={quote(json.dumps(data))}"
        request = urllib.request.Request(url)

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


def add_calculated_fields(offer: Offer) -> Optional[OfferWithCalculatedFields]:
    """
    Extract relevant hotel information from an offer
    Returns ProcessedOffer with name, coordinates, dates, URL, price, airline, nights_amount, and google_maps_url
    """
    try:
        latitude = offer.hotel.coordinates.latitude
        longitude = offer.hotel.coordinates.longitude
        outbound_date = offer.offer.outboundDate
        inbound_date = offer.offer.inboundDate

        return OfferWithCalculatedFields(
            **offer.model_dump(),
            nights_amount=calculate_nights(outbound_date, inbound_date),
            google_maps_url=generate_google_maps_url(latitude, longitude),
        )
    except Exception:
        return None


def get_holiday_offers(
    offer_options: OfferOptions,
) -> List[Optional[OfferWithCalculatedFields]]:
    """
    Fetch and process holiday offers
    Returns list of processed offers (some may be None if processing failed)
    """
    offers = fetch_offers_data(offer_options)

    destination_names = (
        [where_txt.lower() for where_txt in offer_options.engine.whereTxt]
        if offer_options.engine.whereTxt is not None
        else []
    )
    destination_ids = (
        offer_options.engine.where if offer_options.engine.where is not None else []
    )
    city_offers = [
        offer
        for offer in offers
        if offer.destinationData.name_en.lower() in destination_names
        or offer.destinationData.destinationId in destination_ids
    ]
    return [add_calculated_fields(offer) for offer in city_offers]
