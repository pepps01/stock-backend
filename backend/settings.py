# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     SECRET_KEY = os.getenv("SECRET_KEY", "defaultsecret")
#     SQLALCHEMY_DATABASE_URI = (
#         f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
#         f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
#     )
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     REDIS_URL = os.getenv("REDIS_URL")
#     RABBITMQ_URL = os.getenv("RABBITMQ_URL")
