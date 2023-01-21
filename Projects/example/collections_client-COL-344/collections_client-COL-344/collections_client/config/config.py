from pydantic import BaseSettings, PostgresDsn


class AsyncPostgresDsn(PostgresDsn):
    allowed_schemes = list(PostgresDsn.allowed_schemes) + ["postgresql+asyncpg"]


class Setting(BaseSettings):
    PROJECT_NAME: str = "Collections client"

    # COLLECTIONS_CORE
    COLLECTIONS_CORE_URL: str = "http://localhost:8000/api/v1/"
    COLLECTION_CORE_TOKEN: str = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjF9." \
                                 "aug7Ilhl0sCyQKT4L1nyZf39tji_napImkjKtFozYT0"

    # 1C
    URL_1C_ODATA: str = "http://rest1.fdc.kz/test/odata/standard.odata/"
    USERNAME_1C: str = "ws"
    PASSWORD_1C: str = "Fjk32@#$@od83#"

    # 1C service
    URL_1C_SERVICE: str = "http://rest1.fdc.kz/"

    # CACHE EXPIRE TIME
    EXP_TIME: int = 86400

    # DB
    POSTGRES_USER: str = "collections_dev_user"
    POSTGRES_PASSWORD: str = "collections_dev_user"
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_DB: str = "collections_client"
    SQLALCHEMY_DATABASE_URI: str = f"postgresql+asyncpg://" \
                                   f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"

    # TIMEZONE
    USE_TZ: bool = True
    TZ = "Asia/Almaty"

    LIMIT_TO_LOAD_IN_DAYS = 1


settings = Setting()
