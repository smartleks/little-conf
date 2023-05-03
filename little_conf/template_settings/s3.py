from pydantic import BaseSettings, Field


class S3Settings(BaseSettings):
    endpoint_url: str = Field(..., description='S3 Endpoint url')
    access_key: str = Field(..., description='S3 Access Key')
    secret_key: str = Field(..., description='S3 Secret Key')
    bucket: str = Field(..., description='S3 Bucket name')

    # class Config(BaseSettingsConfig):
    #     env_prefix = 's3_'
