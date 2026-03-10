import os

class Config:
    # Use Railway DATABASE_URL if set, otherwise fallback to local DB
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:Rakshu%40123@localhost:5432/rental-portal"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "super-secret"