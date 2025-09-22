base_url = "https://www.holidayfinder.co.il/api_no_auth/holiday_finder/offers"

comparison_address = "Dorotheergasse 13"
city = "Vienna"
min_budget = 505
max_budget = 665
min_nights = 4
max_nights = 5
data = {
    "locale": "he",
    "currency": "USD",
    "fromwhere": ["TLV"],
    "engine": {
        "market": 4,
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
