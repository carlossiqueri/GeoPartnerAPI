from fastapi import Depends, HTTPException, status

from app.db.repository.partner_repository import PartnerRepository
from app.schemas.partner import PartnerCreate
from app.schemas.user import UserLocation

from haversine import haversine

class PartnerService:
    """
        Service class for managing business partners.
    """
    def __init__(self, partner_repository: PartnerRepository = Depends()) -> None:
        self.partner_repository = partner_repository

    async def create_partner(self, partner: PartnerCreate):
        try:
            new_partner = await self.partner_repository.create_partner(partner)
            return new_partner 

        except Exception as exception:
            # print(exception)
            raise exception

    async def fetch_partner(self, partner_id: int):
        try:
            fetched_partner = await self.partner_repository.fetch_partner(partner_id)
            if not fetched_partner:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No partner was found for the given ID."
                )

            return fetched_partner

        except HTTPException as http_exc:
            raise http_exc
        except Exception as exception:
            print(exception)
            raise exception

    async def closest_available_partner(self, user_loc: UserLocation):
        # try:
        #     all_partner_locations = await self.partner_repository.get_all_locations()
        #     print(all_partner_locations)

        # except Exception as exception:
        #     print(exception)
        #     raise exception

        pass
