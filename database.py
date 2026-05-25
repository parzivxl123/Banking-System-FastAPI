from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = (
    "mysql+pymysql://root:bankingsys123@localhost/banking_system"
)

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(
    autocommit = False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

print(engine)


try:

    connection = engine.connect()

    print(
        "Database connected successfully"
    )

    connection.close()

except Exception as e:

    print(
        "Database connection failed:"
    )

    print(e)