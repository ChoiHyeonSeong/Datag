import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from dotenv import load_dotenv
import asyncio
import sys
import os

load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'app')))

from main import app
from configs.mariadb import get_database_mariadb, SQLALCHEMY_DATABASE_URL
from configs.mongodb import get_database_mongodb, mongo_url
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="module")
async def test_mongo_db():
    client = AsyncIOMotorClient(os.getenv("TEST_MONGO_URL"))
    db = client["testDB"]
    yield db
    # client.drop_database("testDB")
    client.close()

@pytest.fixture(scope="module")
async def test_real_mongo_db():
    database = await get_database_mongodb()
    return database

@pytest.fixture(scope="module")
def test_maria_db():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_recycle=28000,  # 28000초마다 연결을 재활용
        pool_pre_ping=True,   # Mariadb 연결 확인
        pool_size=5,
        max_overflow=10
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    engine.dispose()
