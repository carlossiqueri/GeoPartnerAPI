from fastapi import APIRouter, Depends, status
from app.schemas.partner import PartnerResponse, PartnerCreate
from app.services.partners_service import PartnerService

router = APIRouter(prefix="/partners", tags=["partners"])

@router.post("/create_partner", response_model=PartnerResponse, status_code=status.HTTP_201_CREATED)
async def create_partner(partner: PartnerCreate, partner_service: PartnerService = Depends(PartnerService)):
    """
        Endpoint to create a new partner.
    """
    new_partner = await partner_service.create_partner(partner)
    return PartnerResponse.from_orm(new_partner)
