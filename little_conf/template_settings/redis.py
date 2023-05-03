from typing import Optional
from urllib.parse import urlsplit, urlunsplit

from pydantic import AnyUrl, BaseSettings, Field


class RedisSettings(BaseSettings):
    password: str = Field(
        None,
        description='Redis password',
    )
    url: AnyUrl = Field(
        ...,
        description='Redis DSN string',
    )
    max_connections: int = Field(
        -1,
        description="Redis connection's max pool size",
    )

    @property
    def dsn(self) -> str:
        return RedisSettings._dsn_reformat(self.url, password=self.password or None)

    @staticmethod
    def _create_netloc(
        hostname: str,
        port: Optional[int] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> str:
        return '{cred}{host}{port}'.format(
            cred='{}:{}@'.format(username or '', password or '')
            if username is not None or password is not None
            else '',
            host=hostname,
            port=f':{port}' if port else '',
        )

    @staticmethod
    def _dsn_reformat(
        dsn: str, username: Optional[str] = None, password: Optional[str] = None
    ) -> str:
        o = urlsplit(dsn)
        new_netloc = RedisSettings._create_netloc(
            hostname=o.hostname or '',
            port=o.port,
            username=username if username is not None else o.username,
            password=password if password is not None else o.password,
        )
        return urlunsplit((o.scheme, new_netloc, o.path, o.query, o.fragment))

    # class Config(BaseSettingsConfig):
    #     env_prefix = 'redis_'
