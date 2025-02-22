from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	DATABASE_URL: str
	SECRET_KEY: str
	ALGORITHM: str
	ACCESS_TOKEN_EXPIRE_MINUTES: int

	SMTP_HOST: str
	SMTP_PORT: int
	SMTP_USERNAME: str
	SMTP_PASSWORD: str

	class Config:
		env_file = ".env"


settings = Settings()
