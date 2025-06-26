from enum import Enum


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    SICK = "sick"
    INJURED = "injured"


class TravelMode(str, Enum):
    IDLE = "idle"
    TROT = "trot"
    LOPE = "lope"
    SPRINT = "sprint"


class WolfType(str, Enum):
    ARCTIC = "arctic"
    EASTERN = "eastern"
    NORTHWESTERN = "northwestern"
    INTERIOR_ALASKAN = "interior_alaskan"


class PackName(str, Enum):
    ANDROMEDA = "Andromeda"
    ORION = "Orion"
    SIRIUS = "Sirius"
    VEGA = "Vega"
    POLARIS = "Polaris"
    CASSIOPEIA = "Cassiopeia"
    LYRA = "Lyra"
    NEBULA = "Nebula"
    ALTAIR = "Altair"
    DRACO = "Draco"
    BETELGEUSE = "Betelgeuse"
    RIGEL = "Rigel"
    ARCTURUS = "Arcturus"
    PROXIMA_CENTAURI = "Proxima Centauri"
    TAURUS = "Taurus"
    SAGITTARIUS = "Sagittarius"
    ANTARES = "Antares"
    QUASAR = "Quasar"
    PHOENIX = "Phoenix"
    HYDRAMERCURY = "HydraMercury"
    VENUS = "Venus"
    EARTH = "Earth"
    MARS = "Mars"
    JUPITER = "Jupiter"
    SATURN = "Saturn"
    URANUS = "Uranus"
    NEPTUNE = "Neptune"
    PLUTO = "Pluto"
    CERES = "Ceres"
    ERIS = "Eris"
    HAUMEA = "Haumea"
    MAKEMAKE = "Makemake"
    KEPLER_22B = "Kepler-22b"
    PROXIMA_B = "Proxima b"
    GLIESE_581G = "Gliese 581g"
    TAU_CETI_E = "Tau Ceti e"
    VULCAN = "Vulcan"
    KRYPTON = "Krypton"
    GALLIFREY = "Gallifrey"
