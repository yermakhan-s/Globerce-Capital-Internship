from pydantic import BaseSettings


class Setting(BaseSettings):

    # COLLECTRION_CORE
    COLLECTIONS_CORE_URL = "http://0.0.0.0:8000/api/v1/"
    COLLECTION_CORE_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjF9.aug7Ilhl0sCyQKT4L1nyZf39tji_napImkjKtFozYT0"

    # 1C
    URL_1C = "http://rest1.fdc.kz/test/odata/standard.odata/"
    USERNAME_1C = "ws"
    PASSWORD_1C = "Fjk32@#$@od83#"

    # RABBITMQ
    RABBITMQ_URL = "amqp://rabbit:rabbit@rabbitmq:5672/celery"


settings = Setting()
