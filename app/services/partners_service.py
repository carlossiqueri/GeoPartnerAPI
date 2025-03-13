from fastapi import Depends, HTTPException, status

from app.db.repository.partner_repository import PartnerRepository
from app.schemas.partner import PartnerCreate

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
        except HTTPException as http_exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid request data. Please check your input."
            ) from http_exc
        except Exception as exception:
            print(exception)
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred. Please try again later."
            ) from exception
