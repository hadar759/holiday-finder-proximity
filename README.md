# Holiday Finder

A Python tool to find and sort hotels by distance from a given address.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Hotel Distance Sorter

Sort hotels by distance from a specific address:

```bash
python hotel_distance_sorter.py <url> <comparison_address>
```

Example:
```bash
python hotel_distance_sorter.py "https://api.example.com/hotels" "1600 Amphitheatre Parkway, Mountain View, CA"
```

## Development

Install in development mode:

```bash
pip install -e .
```

## Requirements

- Python 3.8+
- nominatim-api

## License

MIT