import os


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SERVER_NAME = "127.0.0.1:5000"
    SECRET_KEY = ""


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://dewciu:leclerc0109@localhost:5432/formula1_db"
    )

    DEBUG = True
    SECRET_KEY = "008e2ceb61fee49f68b29afeddd54d49809f232e7c192b6e54fe30a8987159d28b813d3fb0c24598ad88c332bdca5dfcf751"


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://dewciu:leclerc0109@localhost:5432/formula1_db"
    )
    TESTING = True


config: dict[str, Config] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config() -> Config:
    return config.get(os.getenv("FLASK_ENV", "default"))
