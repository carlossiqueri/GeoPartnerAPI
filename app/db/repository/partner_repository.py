from geoalchemy2.shape import from_shape
from shapely import MultiPolygon, Point
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

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
                    id= partner.id,
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

            except IntegrityError as error:
                await conn.session.rollback()

                error_message = str(error.orig)

                if "partners_document_key" in error_message:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid partner document. Check your input."
                    ) from error

                print(error)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="An unexpected database error occurred."
                ) from error

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

    async def get_all_partners(self):
        """
            Fetches all partners from the database.
        """
        async with self.db_handler as conn:
            try:
                query = select(
                    Partner
                )
                result = await conn.session.execute(query)
                all_partners = result.scalars().all()
                return all_partners
                
            except KeyError as keye_error:
                print(f"Error accessing dictionary key: {keye_error}")
                raise ValueError(f"Invalid data: missing key {keye_error}") from keye_error

            except AttributeError as attribute_error:
                print(f"Attribute error: {attribute_error}")
                raise TypeError("Error accessing object attributes") from attribute_error

            except Exception as exc:
                print(f"Unexpected error: {exc}")
                raise RuntimeError("Error creating partner in the database") from exc
