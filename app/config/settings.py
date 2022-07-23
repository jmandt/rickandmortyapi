from pydantic import BaseSettings


class Settings(BaseSettings):

    port: int = 8080
