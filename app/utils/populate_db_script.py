import asyncio
from app.utils.mock_utils import partners_mock
from app.db.repository.partner_repository import PartnerRepository
from app.schemas.partner import PartnerCreate

async def populate_db():
    """
        Script for populating the database with a previously created JSON of partners.
    """
    partners_repository = PartnerRepository()
    
    for partner in partners_mock['pdvs']:
        await partners_repository.create_partner(PartnerCreate(**partner))

if __name__ == "__main__":
    asyncio.run(populate_db())
