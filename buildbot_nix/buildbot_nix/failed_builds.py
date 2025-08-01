import dbm
from datetime import datetime
from pathlib import Path

from pydantic import BaseModel, Field


class FailedBuildsError(Exception):
    pass


def default_url() -> str:
    db_path = Path("failed_builds.dbm").resolve()
    return f"build unknown. Please delete {db_path} to get a build url"


class FailedBuild(BaseModel):
    derivation: str
    time: datetime
    url: str = Field(default_factory=default_url)


class FailedBuildDB:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path

    def add_build(self, derivation: str, time: datetime, url: str) -> None:
        with dbm.open(str(self.db_path), "c") as db:
            db[derivation] = FailedBuild(
                derivation=derivation, time=time, url=url
            ).model_dump_json()

    def check_build(self, derivation: str) -> FailedBuild | None:
        with dbm.open(str(self.db_path), "c") as db:
            if derivation in db:
                return FailedBuild.model_validate_json(db[derivation])
        return None

    def remove_build(self, derivation: str) -> None:
        with dbm.open(str(self.db_path), "c") as db:
            del db[derivation]
