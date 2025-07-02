from enum import Enum

DEFAULT_ICON = (
    "https://img.icons8.com/?size=100&id=hJtWtfOfjEsK&format=png&color=000000"
)


class AnimalIcon(str, Enum):
    ELEPHANT = (
        "https://img.icons8.com/?size=100&id=aMvJw65mbqCX&format=png&color=000000"
    )
    GAUR = "https://img.icons8.com/?size=100&id=iByjK44LWaNu&format=png&color=000000"
    LEOPARD = "https://img.icons8.com/?size=100&id=lebmT3Yz7q2Q&format=png&color=000000"
    SUN_BEAR = (
        "https://img.icons8.com/?size=100&id=b9rkD77U9wsN&format=png&color=000000"
    )
    DHOLE = "https://img.icons8.com/?size=100&id=67tg2TQBcKAM&format=png&color=000000"
    PORCUPINE = (
        "https://img.icons8.com/?size=100&id=d2ssoe1zIlGg&format=png&color=000000"
    )
    PANGOLIN = (
        "https://img.icons8.com/?size=100&id=d2ssoe1zIlGg&format=png&color=000000"
    )
    MONITOR_LIZARD = (
        "https://img.icons8.com/?size=100&id=oa2bHbtiJaYF&format=png&color=000000"
    )
    HORNBILL = (
        "https://img.icons8.com/?size=100&id=qTxbyl0tqoKL&format=png&color=000000"
    )
    PEAFOWL = "https://img.icons8.com/?size=100&id=QrhSO3jG3Fgp&format=png&color=000000"
    VULTURE = "https://img.icons8.com/?size=100&id=5ycpDAJhYTbT&format=png&color=000000"
    KINGFISHER = (
        "https://img.icons8.com/?size=100&id=qTxbyl0tqoKL&format=png&color=000000"
    )
    PYTHON = "https://img.icons8.com/?size=100&id=6Tpb4xpmgZk7&format=png&color=000000"
    LANGUR = "https://img.icons8.com/?size=100&id=qLTrKDR4K61i&format=png&color=000000"
    CIVET = "https://img.icons8.com/?size=100&id=l7kbLnDvLZwI&format=png&color=000000"
    WILD_BOAR = (
        "https://img.icons8.com/?size=100&id=HaaDZW8y3oCJ&format=png&color=000000"
    )
    GECKO = "https://img.icons8.com/?size=100&id=oa2bHbtiJaYF&format=png&color=000000"
    EAGLE = "https://img.icons8.com/?size=100&id=FumKjKiTArzQ&format=png&color=000000"
    OWL = "https://img.icons8.com/?size=100&id=lrSRHnxYFj2O&format=png&color=000000"
    TORTOISE = (
        "https://img.icons8.com/?size=100&id=G3uBZC9dmTix&format=png&color=000000"
    )


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
