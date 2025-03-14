import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from app.utils.mock_utils import partners_mock
from app.db.repository.partner_repository import PartnerRepository
from app.schemas.partner import PartnerCreate
from app.core.config import settings
from app.db.settings.base import Base

engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)


async def create_database():
    """
    Creates the database and tables if they do not exist.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def populate_db():
    """
    Populates the database with a JSON of partners.
    """
    await create_database()

    partners_repository = PartnerRepository()

    for partner in partners_mock["pdvs"]:
        await partners_repository.create_partner(PartnerCreate(**partner))

    print("Finish - populate_db function.")


if __name__ == "__main__":
    asyncio.run(populate_db())
