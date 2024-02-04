from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# from sqlalchemy.pool import NullPool


TEST_DB_URL = 'sqlite+aiosqlite:///./test.db'

# test_engine = create_async_engine(TEST_DB_URL, poolclass=NullPool)
test_engine = create_async_engine(TEST_DB_URL, connect_args={'check_same_thread': False})
TestingSessionLocal = async_sessionmaker(test_engine,
                                         expire_on_commit=False,
                                         autocommit=False,
                                         autoflush=False)
