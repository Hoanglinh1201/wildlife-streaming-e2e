from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    """
    Base class for all database models.
    This class is used to define the base for SQLAlchemy ORM models.
    """

    pass


class TrackerDB(Base):
    __tablename__ = "trackers"

    id = Column(String, primary_key=True)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False)

    coordinates = relationship("CoordinateDB", back_populates="trackers")
    animals = relationship("AnimalDB", back_populates="trackers", uselist=False)


class AnimalDB(Base):
    __tablename__ = "animals"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    icon = Column(String, nullable=True)
    species = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    age = Column(Float, nullable=False)
    born_at = Column(DateTime, nullable=False)
    deceased_at = Column(DateTime, nullable=True)
    length_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    tracker_id = Column(String, ForeignKey("trackers.id"), nullable=False, unique=True)

    trackers = relationship("TrackerDB", back_populates="animals")


class CoordinateDB(Base):
    __tablename__ = "coordinates"

    id = Column(String, primary_key=True)
    tracker_id = Column(String, ForeignKey("trackers.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    battery_level = Column(Float, nullable=False)
    timestamp = Column(BigInteger, nullable=False)

    trackers = relationship("TrackerDB", back_populates="coordinates")


class EventDB(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True)
    event_type = Column(String, nullable=False)
    event_data = Column(JSONB, nullable=True)
