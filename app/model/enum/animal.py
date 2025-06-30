from enum import Enum


class AnimalIcon(str, Enum):
    ELEPHANT = "https://img.icons8.com/ios/64/elephant.png"
    GAUR = "https://img.icons8.com/ios/64/bull.png"
    LEOPARD = "https://img.icons8.com/ios/64/leopard.png"
    SUN_BEAR = "https://img.icons8.com/ios/64/bear.png"
    DHOLE = "https://img.icons8.com/ios/64/dog.png"
    PORCUPINE = "https://img.icons8.com/ios/64/hedgehog.png"
    PANGOLIN = "https://img.icons8.com/ios/64/armadillo.png"
    MONITOR_LIZARD = "https://img.icons8.com/ios/64/lizard.png"
    HORNBILL = "https://img.icons8.com/ios/64/bird.png"
    PEAFOWL = "https://img.icons8.com/ios/64/peacock.png"
    VULTURE = "https://img.icons8.com/ios/64/vulture.png"
    KINGFISHER = "https://img.icons8.com/ios/64/kingfisher.png"
    PYTHON = "https://img.icons8.com/ios/64/snake.png"
    LANGUR = "https://img.icons8.com/ios/64/monkey.png"
    CIVET = "https://img.icons8.com/ios/64/cat.png"
    WILD_BOAR = "https://img.icons8.com/ios/64/pig.png"
    GECKO = "https://img.icons8.com/ios/64/gecko.png"
    EAGLE = "https://img.icons8.com/ios/64/eagle.png"
    OWL = "https://img.icons8.com/ios/64/owl.png"
    TORTOISE = "https://img.icons8.com/ios/64/turtle.png"


class AnimalType(str, Enum):
    MAMMAL = "mammal"
    BIRD = "bird"
    REPTILE = "reptile"
    AMPHIBIAN = "amphibian"
    FISH = "fish"
    INSECT = "insect"
    ARACHNID = "arachnid"
    OTHER = "other"


class AnimalStatus(str, Enum):
    """
    Enum for different statuses of an animal.
    """

    ALIVE = "alive"
    DECEASED = "deceased"
