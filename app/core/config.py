# from pydantic import BaseSettings

# class Settings(BaseSettings):
#     openai_api_key: str
#     model_temperature: float = 0.7
    
#     class Config:
#         env_file = ".env"

# settings = Settings()

# app/core/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    csv_file_path: str = "./app/policies/cloud_policies.csv"  # Path to the CSV file
    
    class Config:
        env_file = ".env"

settings = Settings()
