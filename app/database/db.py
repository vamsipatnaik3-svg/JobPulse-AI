'''
What is happening here?
- engine: establishes the connection to SQLite.
- SessionLocal: creates database sessions for reading and writing.
- Base: the parent class for our database models.
- init_db(): creates the database tables.
'''


import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


load_dotenv()

# Use PostgreSQL in the cloud and SQLite locally.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./jobpulse.db"
)

# SQLite requires a special connection argument.
connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def init_db():

    from app.database import models

    Base.metadata.create_all(bind=engine)

    print("JobPulse database initialized successfully!")
