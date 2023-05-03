from pydantic import AnyUrl, BaseSettings, Field


class DatabaseSettings(BaseSettings):
    username: str = Field(
        ...,
        description='Database user name',
    )
    password: str = Field(
        ...,
        description='Database password',
    )
    url: AnyUrl = Field(
        ...,
        description='Database DSN string',
    )
    db_schema: str = Field(
        'public',
        description='Database schema',
    )
    max_pool_size: int = Field(
        30,
        description="Database connection's max pool size",
    )

    @property
    def dsn(self) -> str:
        from sqlalchemy.engine.url import make_url  # noqa

        url = make_url(self.url)
        url = url.set(
            drivername='postgresql',
            username=self.username,
            password=self.password,
        )
        return str(url)

    # class Config(BaseSettingsConfig):
    #     env_prefix = 'database_'
