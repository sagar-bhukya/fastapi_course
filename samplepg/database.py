from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote
from .models import Base

password = "Sagar@123"
encoded_password = quote(password, safe='')
DATABASE_URL = f"postgresql://postgres:{encoded_password}@localhost:5432/sagar"


# DATABASE_URL = "postgresql://postgres:Sagar%40123@localhost/sagar"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)