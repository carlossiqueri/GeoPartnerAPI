from geoalchemy2.shape import from_shape
from shapely import MultiPolygon, Point
from sqlalchemy import select

from app.db.models.partners import Partner
from app.db.settings.connection import DBConnectionHandler
from app.schemas.partner import PartnerCreate

class PartnerRepository:
    """
        Repository class for handling database operations related to partners.
    """
    def __init__(self):
        self.db_handler = DBConnectionHandler()

    async def create_partner(self, partner: PartnerCreate):
        """
            Creates a new partner in the database.
        """
        async with self.db_handler as conn:
            try:
                coverage_area_shape = MultiPolygon(partner.coverage_area["coordinates"])
                address_shape = Point(
                    partner.address["coordinates"][0],
                    partner.address["coordinates"][1]
                )

                new_partner = Partner(
                    trading_name = partner.trading_name,
                    owner_name = partner.owner_name,
                    document = partner.document,
                    coverage_area = from_shape(coverage_area_shape, srid=4326),
                    address = from_shape(address_shape, srid=4326)
                )

                conn.session.add(new_partner)
                await conn.session.commit()
                await conn.session.refresh(new_partner)

                return new_partner
            except KeyError as keye_error:
                print(f"Error accessing dictionary key: {keye_error}")
                raise ValueError(f"Invalid data: missing key {keye_error}") from keye_error

            except AttributeError as attribute_error:
                print(f"Attribute error: {attribute_error}")
                raise TypeError("Error accessing object attributes") from attribute_error

            except Exception as exc:
                print(f"Unexpected error: {exc}")
                raise RuntimeError("Error creating partner in the database") from exc

    async def fetch_partner(self, partner_id: int):
        """
            Search for a partner in the database for a giver ID.
        """  
        async with self.db_handler as conn:
            try:
                query = select(
                    Partner
                ).where(
                    Partner.id == partner_id
                )

                result = await conn.session.execute(query)
                fetched_partner = result.scalars().first()

                return fetched_partner

            except KeyError as keye_error:
                print(f"Error accessing dictionary key: {keye_error}")
                raise ValueError(f"Invalid data: missing key {keye_error}") from keye_error

            except AttributeError as attribute_error:
                print(f"Attribute error: {attribute_error}")
                raise TypeError("Error accessing object attributes") from attribute_error

            except Exception as exc:
                print(f"Unexpected error: {exc}")
                raise RuntimeError("Error creating partner in the database") from exc
