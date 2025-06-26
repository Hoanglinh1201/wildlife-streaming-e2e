from app.model.enum import WolfType
from app.model.location import Location, Range

WOLF_LOCATIONS: list[Location] = [
    Location(
        name="Jasper_National_Park",
        lat_range=Range(min=52.8, max=53.2),
        lon_range=Range(min=-118.1, max=-117.5),
        region="Alberta, Rocky Mountains",
        type=WolfType.NORTHWESTERN,
    ),
    Location(
        name="Algonquin_Provincial_Park",
        lat_range=Range(min=45.3, max=45.9),
        lon_range=Range(min=-78.9, max=-77.5),
        region="Ontario, mixed forest",
        type=WolfType.EASTERN,
    ),
    Location(
        name="Qausuittuq_National_Park",
        lat_range=Range(min=75.0, max=76.0),
        lon_range=Range(min=-100.0, max=-96.0),
        region="Bathurst Island, Nunavut",
        type=WolfType.ARCTIC,
    ),
    Location(
        name="Kluane_National_Park",
        lat_range=Range(min=60.5, max=61.5),
        lon_range=Range(min=-139.0, max=-137.5),
        region="Yukon Territory, boreal forest/mountains",
        type=WolfType.INTERIOR_ALASKAN,
    ),
    Location(
        name="Yellowstone_National_Park",
        lat_range=Range(min=44.4, max=45.0),
        lon_range=Range(min=-110.5, max=-109.0),
        region="Wyoming, Montana, Idaho",
        type=WolfType.NORTHWESTERN,
    ),
    Location(
        name="Denali_National_Park",
        lat_range=Range(min=62.8, max=63.2),
        lon_range=Range(min=-150.0, max=-149.0),
        region="Alaska Range, Alaska",
        type=WolfType.INTERIOR_ALASKAN,
    ),
]
