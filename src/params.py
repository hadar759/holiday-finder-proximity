base_url = "https://www.holidayfinder.co.il/api_no_auth/holiday_finder/offers"

CITY_CENTERS = {
    "Budapest": "St. Stephen's Basilica",
    "Vienna": "Dorotheergasse 13",
    "Prague": "Staroměstské nám.",
    "Rome": "Trevi Fountain",
}
CITY_NUMBERS = {"Prague": 28, "Rome": 19}

city = "Rome"
min_budget = 0
max_budget = 550
min_nights = 5
max_nights = 6
data = {
    "locale": "he",
    "currency": "USD",
    "fromwhere": ["TLV"],
    "engine": {
        "market": 4,
        "where": None if CITY_NUMBERS.get(city) is None else [CITY_NUMBERS[city]],
        "when": {
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
        "who": {"adult": 2, "child": 0, "room": 1, "childAges": []},
        "whereTxt": [city],
        "budget": {"min": min_budget, "max": max_budget},
        "flex": False,
    },
    "sort": {"best": -1},
    "limit": 1000,
    "offset": 0,
}

comparison_address = CITY_CENTERS[city]
