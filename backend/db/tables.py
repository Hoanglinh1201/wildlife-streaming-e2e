from sqlalchemy import Column, DateTime, Float, ForeignKey, String
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

    animal = relationship("AnimalDB", back_populates="tracker", uselist=False)


class AnimalDB(Base):
    __tablename__ = "animals"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    icon = Column(String, nullable=True)
    species = Column(String, nullable=False)
    animal_type = Column(
        String, nullable=False
    )  # This field is not used in the current implementation
    gender = Column(String, nullable=False)
    age = Column(Float, nullable=False)
    born_at = Column(DateTime, nullable=False)
    deceased_at = Column(DateTime, nullable=True)
    length_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    tracker_id = Column(String, ForeignKey("trackers.id"), nullable=False)

    tracker = relationship("TrackerDB", back_populates="animal")


class EventDB(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True)
    type = Column(String, nullable=False)
    detail = Column(JSONB, nullable=True)
    timestamp = Column(DateTime, nullable=False)
