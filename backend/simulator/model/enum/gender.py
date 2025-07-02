from enum import Enum


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"


class TravelMode(str, Enum):
    IDLE = "idle"
    TROT = "trot"
    LOPE = "lope"
    SPRINT = "sprint"


class TrackerType(str, Enum):
    COLLAR = "collar"
    GPS = "gps"
    RFID = "rfid"


class AnimalType(str, Enum):
    MAMMAL = "mammal"
    BIRD = "bird"
    REPTILE = "reptile"
    AMPHIBIAN = "amphibian"
    FISH = "fish"
    INSECT = "insect"
    ARACHNID = "arachnid"
    OTHER = "other"


class Species(str, Enum):
    ELEPHANT = "Elephant"
    GAUR = "Gaur"
    LEOPARD = "Leopard"
    SUN_BEAR = "Sun Bear"
    DHOLE = "Dhole"
    PORCUPINE = "Porcupine"
    PANGOLIN = "Pangolin"
    MONITOR_LIZARD = "Monitor Lizard"
    HORNBILL = "Hornbill"
    PEAFOWL = "Peafowl"
    VULTURE = "Vulture"
    KINGFISHER = "Kingfisher"
    PYTHON = "Python"
    LANGUR = "Langur"
    CIVET = "Civet"
    WILD_BOAR = "Wild Boar"
    GECKO = "Gecko"
    EAGLE = "Eagle"
    OWL = "Owl"
    TORTOISE = "Tortoise"
