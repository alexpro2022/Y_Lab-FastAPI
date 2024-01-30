from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

TEST_DB_URL = 'postgresql+asyncpg://postgres:test_password@test_db:5432'

test_engine = create_async_engine(TEST_DB_URL, poolclass=NullPool)
TestingSessionLocal = async_sessionmaker(test_engine,
                                         expire_on_commit=False,
                                         autocommit=False,
                                         autoflush=False)
