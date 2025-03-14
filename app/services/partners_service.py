from fastapi import Depends, HTTPException, status
from haversine import haversine
from shapely.geometry import Point, MultiPolygon, Polygon

from app.db.repository.partner_repository import PartnerRepository
from app.schemas.partner import PartnerCreate, PartnerResponse
from app.schemas.user import UserLocation


class PartnerService:
    """
    Service class for managing business partners.
    """

    def __init__(self, partner_repository: PartnerRepository = Depends()) -> None:
        self.partner_repository = partner_repository

    async def create_partner(self, partner: PartnerCreate):
        """
        Creates a new business partner and stores it in the database.
        """
        try:
            new_partner = await self.partner_repository.create_partner(partner)
            return new_partner

        except Exception as exception:
            # print(exception)
            raise exception

    async def fetch_partner(self, partner_id: int):
        """
        Fetches a business partner by its ID.
        """
        try:
            fetched_partner = await self.partner_repository.fetch_partner(partner_id)
            if not fetched_partner:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No partner was found for the given ID.",
                )

            return fetched_partner

        except HTTPException as http_exc:
            raise http_exc
        except Exception as exception:
            print(exception)
            raise exception

    async def closest_available_partner(self, user_loc: UserLocation):
        """ "
        Finds the closest business partner whose coverage area includes the user's location.
        """
        try:
            all_partners = await self.partner_repository.get_all_partners()

            if not all_partners:
                raise HTTPException(status_code=404, detail="No partners found")

            serialized_all_partners = [
                PartnerResponse.from_orm(partner) for partner in all_partners
            ]
            user_coords = (user_loc.lon, user_loc.lat)
            user_point_coord = Point(user_coords)

            # Sort all partners by distance
            sorted_partners = sorted(
                serialized_all_partners,
                key=lambda partner: haversine(
                    user_coords, partner.address["coordinates"]
                ),
            )

            for partner in sorted_partners:
                coverage_area = MultiPolygon(
                    [
                        Polygon(rings[0], holes=rings[1:])
                        for rings in partner.coverage_area["coordinates"]
                    ]
                )

                if coverage_area.contains(user_point_coord):
                    return partner

            raise HTTPException(
                status_code=404, detail="No partners cover this location"
            )

        except Exception as exception:
            print(exception)
            raise exception
