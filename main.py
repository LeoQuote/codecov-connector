from fastapi import FastAPI, Depends, HTTPException
from pydantic import field_validator, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import Connection
from starlette import status
from sqlalchemy import create_engine, text

app = FastAPI()


class Settings(BaseSettings):
    pg_connection_string: str

    model_config = SettingsConfigDict(env_file='.env.example', env_file_encoding='utf-8')

    @field_validator('pg_connection_string')
    @classmethod
    def sqlalchemy_compact(cls, v: str) -> str:
        if v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://")
        return v


config = Settings()

engine = create_engine(config.pg_connection_string)


async def get_session() -> Connection:
    conn = engine.connect()
    # Open a cursor to perform database operations
    yield conn
    conn.close()


class RepoUploadToken(BaseModel):
    ownerid: int
    owner: str
    name: str
    upload_token: str


@app.get("/{org}/{repo}", response_model=RepoUploadToken)
async def get_upload_token(org: str, repo: str, cursor=Depends(get_session)):
    owner = cursor.execute(text("select ownerid, username from owners where username = :username limit 1"),
                           username=org).first()
    # Retrieve query results
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="no owner with this name found."
        )

    # 取回 token
    result = cursor.execute(text("select ownerid, name, upload_token from repos "
                                 "where ownerid = :ownerid and name= :name limit 1"),
                            ownerid=owner[0],
                            name=repo).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="no repo found with this name")
    return {
        "ownerid": result[0],
        "owner": owner[1],
        "name": result[1],
        "upload_token": result[2]
    }
