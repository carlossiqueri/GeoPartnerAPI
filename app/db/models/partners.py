from geoalchemy2 import Geometry
from sqlalchemy import Column, Integer, String
from app.db.settings.base import Base


class Partner(Base):
    """
    Represents a business partner entity in the database.
    """

    __tablename__ = "partners"

    id = Column(String, primary_key=True, index=True, nullable=False)
    trading_name = Column(String, nullable=False)
    owner_name = Column(String, nullable=False)
    document = Column(String, unique=True, nullable=False)
    coverage_area = Column(Geometry("MULTIPOLYGON"), nullable=False)
    address = Column(Geometry("POINT"), nullable=False)
