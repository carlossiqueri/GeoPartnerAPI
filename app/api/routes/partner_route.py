from fastapi import APIRouter, Depends, status
from app.schemas.partner import PartnerResponse, PartnerCreate
from app.schemas.user import UserLocation
from app.services.partners_service import PartnerService

router = APIRouter(prefix="/partners", tags=["partners"])


@router.post(
    "/create_partner",
    response_model=PartnerResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_partner(
    partner: PartnerCreate, partner_service: PartnerService = Depends(PartnerService)
):
    """
    Endpoint to create a new partner.
    """
    new_partner = await partner_service.create_partner(partner)
    return PartnerResponse.from_orm(new_partner)


@router.get("/fetch_partner/{partner_id}", response_model=PartnerResponse)
async def fetch_partner_by_id(
    partner_id: int, partner_service: PartnerService = Depends(PartnerService)
):
    """
    Endpoint to fetch a partner using its ID.
    """
    fetched_partner = await partner_service.fetch_partner(partner_id)
    return PartnerResponse.from_orm(fetched_partner)


@router.post("/closest_available_partner", response_model=PartnerResponse)
async def closest_available_partner(
    user_loc: UserLocation, partner_service: PartnerService = Depends(PartnerService)
):
    """
    Endpoint to search for the closest partner to the user's input location.
    The user's input must be a location within the partner's coverage area.
    """
    closest_partner = await partner_service.closest_available_partner(user_loc)
    return closest_partner
