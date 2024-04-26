from dotenv import load_dotenv
import os


class Settings:
    def __init__(self):
        load_dotenv()

    @property
    def API_TG_BOT_TOKEN(self):
        return os.getenv('API_TG_BOT_TOKEN')

    @property
    def API_TMDB_TOKEN(self):
        return os.getenv('API_TMDB_TOKEN')


settings = Settings()
