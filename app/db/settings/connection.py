import os
import ssl

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

load_dotenv()

DB_HOST = settings.DB_HOST
DB_PORT = settings.DB_PORT
DB_USER = settings.DB_USER
DB_PASSWORD = settings.DB_PASSWORD
DB_NAME = settings.DB_NAME


class DBConnectionHandler:
    """
    Class responsible for handling the database connection.
    """

    def __init__(self) -> None:
        self.__connection_string = settings.SQLALCHEMY_DATABASE_URL
        self.__engine = self.__create_async_engine()
        self.session = None

    def __create_async_engine(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

        engine = create_async_engine(
            self.__connection_string,
            connect_args={"ssl": ssl_context},
            plugins=["geoalchemy2"],
        )
        return engine

    def get_engine(self):
        return self.__engine

    async def __aenter__(self):
        session_maker = sessionmaker(
            bind=self.__engine, expire_on_commit=False, class_=AsyncSession
        )
        self.session = session_maker()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        await self.__engine.dispose()
