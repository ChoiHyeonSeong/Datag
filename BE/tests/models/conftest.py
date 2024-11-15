from motor.motor_asyncio import AsyncIOMotorClient
import pytest

@pytest.fixture(scope="session")
def event_loop():
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="class")
def db_client(event_loop):
    client = MongoDBClient()
    motor_client = AsyncIOMotorClient(f"mongodb://{SETTINGS.mongodb_host}:{SETTINGS.mongodb_port}", io_loop=event_loop)
    client._client = motor_client
    client._db_name = "testDB"
    client._db = motor_client["testDB"]
    yield client
    event_loop.run_until_complete(client.drop_database())
    client.close()