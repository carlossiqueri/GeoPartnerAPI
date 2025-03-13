from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from shapely import MultiPolygon, Point
from shapely.wkb import loads as wkb_loads

class PartnerBase(BaseModel):
    """
        Base schema for a business partner.
    """
    id: Optional[int] = None
    trading_name: str = Field(alias="tradingName")
    owner_name: str = Field(alias="ownerName")
    document: str
    coverage_area: dict = Field(alias="coverageArea")
    address: dict

    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    
class PartnerCreate(PartnerBase):
    """
        Schema for creating a new business partner.

        Mainly for future flexibility and code clarity.

        This class could include validation logic, such as regex validation for the document, since it's a CNPJ field.
    """
    pass

class PartnerResponse(PartnerBase):
    """
        Schema for returning a partner.
    """
    class Config:
        """
            Converts SQLAlchemy models to Pydantic models.
        """
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        """
            Converts an ORM SQLAlchemy object into a Pydantic model.
        """

        def convert_geometry(geometry):
            """
                Converts a Shapely object (MultiPolygon or Point) into a valid GeoJSON dictionary.
            """
            geometry = wkb_loads(bytes(geometry.data))
            if isinstance(geometry, MultiPolygon):
                return {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [[(point[0], point[1]) for point in polygon.exterior.coords]] +
                        [[(point[0], point[1]) for point in ring.coords] for ring in polygon.interiors]
                        for polygon in geometry.geoms
                    ]
                }
            if isinstance(geometry, Point):
                return {
                    "type": "Point",
                    "coordinates": (geometry.x, geometry.y)
                }


        return cls.model_construct(
            id=obj.id,
            trading_name=obj.trading_name,
            owner_name=obj.owner_name,
            document=obj.document,
            coverage_area=convert_geometry(obj.coverage_area),
            address=convert_geometry(obj.address),
        )
