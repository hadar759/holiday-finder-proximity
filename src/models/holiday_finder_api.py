from typing import Any
from pydantic import BaseModel, Field

from src.models.common import Coordinates


class DestinationData(BaseModel):
    small_photo: str
    about: str
    advices: list[str]
    commute: str
    destinationId: int
    locationType: str
    coordinates: Coordinates
    name: str
    name_en: str
    big_photo: str
    atlas_top: str
    atlas_top_en: str
    atlas_top_id: int
    haul_type: str
    priority: int
    market_id: int


class Capacity(BaseModel):
    adult: int
    child: int
    infant: int | None


class Stickers(BaseModel):
    lastMinute: bool | None = Field(default=None)
    weekend: bool | None = Field(default=None)
    nightFlight: bool | None = Field(default=None)
    allInclusive: bool | None = Field(default=None)
    breakfast: bool | None = Field(default=None)
    boardType: str | None = Field(default=None)
    partiallyRefundable: bool | None = Field(default=None)
    non_refundable: bool | None = Field(default=None)
    highlyRefundable: bool | None = Field(default=None)
    isGroupBooking: bool | None = Field(default=None)
    changeForFree: bool | None = Field(default=None)
    direct: bool | None = Field(default=None)
    haulType: str | None = Field(default=None)
    splitType: int | None = Field(default=None)
    whatStickerToShow: str | None = Field(default=None)
    luggageIncluded: bool | None = Field(default=None)
    carryOnTrolleyIncluded: bool | None = Field(default=None)
    hotelBookingStats: dict[str, Any] | None = Field(default=None)
    BARComparison: dict[str, float | None] | None = Field(default=None)
    hotelPreferencesMet: list[Any] | None = Field(default=None)
    includeTransfer: Any | None = Field(default=None)
    alpClosedPackage: bool | None = Field(default=None)
    kosher: bool | None = Field(default=None)
    closeToChabad: bool | None = Field(default=None)


class OfferData(BaseModel):
    offerId: str
    hfOfferId: str
    outboundDate: str
    inboundDate: str
    price: int
    packageDeeplinkUrl: str
    capacity: Capacity
    duration: int
    leadTime: str
    currency: str
    debug_info: dict[str, Any]
    # Not important
    # stickers: Stickers
    capacity_from_filter: dict[str, Any]
    created_at: str


class Facility(BaseModel):
    name: str
    slug: str | None
    name_en: str


class HotelData(BaseModel):
    last_updated: str
    name: str
    board: str
    refundable: bool
    allInclusive: bool | None = Field(default=None)
    rating: int
    photos: list[str]
    coordinates: Coordinates
    facilities: dict[str, Facility] | list[Facility] | None = Field(default=None)
    packageHighlightOnCard: str | None = Field(default=None)
    packageTitleOnCard: str | None = Field(default=None)
    packageTitleOnDetails: str | None = Field(default=None)
    specialDealLabel: str | None = Field(default=None)
    addedToCacheDate: str | None = Field(default=None)
    addedBy: str | None = Field(default=None)
    featureCharacteristics: list[str] | None = Field(default=None)
    packageLabelOnDetails: str | None = Field(default=None)
    hotelQuotesOnDetails: str | None = Field(default=None)
    tags: list[str] | None = Field(default=None)
    provider_hotel_id: str | None = Field(default=None)
    directConnectedHotel: bool | None = Field(default=None)
    directConnectedHotelProviders: list[str] | None = Field(default=None)
    isPromoterSuperstar: bool | None = Field(default=None)
    isOnlyForSpecificDestination: bool | None = Field(default=None)
    roomName: str | None = Field(default=None)
    # bestSellerHotelInDestination: list[Any] | None = Field(default=None)
    # topTrendingHotelInDestination: list[Any] | None = Field(default=None)
    # bestSellerHotelInTheme: list[Any] | None = Field(default=None)
    location: dict[str, Any] | None = Field(default=None)


class FlightData(BaseModel):
    takeoff_hour: str
    landing_hour: str
    travel_duration_format: str
    travel_duration_minutes: int
    nb_escales: int
    city_from_airport_code: str
    city_to_airport_code: str
    company_code: str
    public_flight_id: str
    provider_code: str
    provider_source_code: str
    price: int
    flight_number: list[str]
    number_of_available_seats: int
    inbound: dict[str, Any] | None
    base_price: float
    comp_path: str
    comp_logo: str
    company_name: str
    last_updated_outbound: str | None = None
    last_updated_inbound: str | None = None
    flightsInUse: list[str] | None


class Offer(BaseModel):
    destinationData: DestinationData
    offer: OfferData
    hotel: HotelData
    flight: FlightData
    optionsToAdd: Any | None
    differentBoardTypePrices: list[Any]
    luggageAddon: list[Any]
    extraFlightInfo: list[Any]
    extraTermsInfo: list[Any]


class Pagination(BaseModel):
    total_offers_count: int
    total_offers_pages: int
    current_offers_page: int
    limit: int
    offset: int
    allFinalOffersByBucketWithoutSplit: list[Any]
    bucketNamesWithCount: list[Any]
    doWeNeedAggregate: Any | None


class ApiData(BaseModel):
    pagination: Pagination
    offers: list[Offer]


class ApiResponse(BaseModel):
    data: ApiData
