from typing import Optional, Iterable


from core.models.profile.db import ProfileDB
from core.storage.db.postgres import DB
from core.utils import throw_not_found, throw_bad_request
from asyncpg import Record


class ProfileStorage:
    def __init__(self, db: DB) -> None:
        self.db = db

    @classmethod
    async def row_to_profile(cls, row: Record) -> ProfileDB:
        return ProfileDB.model_validate({key: val
                                         for key, val in zip(row.keys(), row.values())})

    async def get_by_id(
            self, profile_id: str, throw_error: bool = False
    ) -> Optional[ProfileDB]:
        sql = "SELECT * FROM api_profile WHERE (id = $1)"
        row = await self.db.fetch_row(sql, profile_id)
        if not row and throw_error:
            throw_not_found("No user with this id!")
        profile = await self.row_to_profile(row)
        return profile

    async def get_by_email(self, email: str, throw_error: bool = True) -> ProfileDB:
        sql = "SELECT * FROM api_profile WHERE (email = $1)"
        row = await self.db.fetch_row(sql, email)
        if not row and throw_error:
            throw_not_found("No user with this id!")

        return await self.row_to_profile(row)

    async def get_by_username(self, username: str, throw_error: bool = True) -> ProfileDB:
        sql = "SELECT * FROM api_profile WHERE (username = $1)"
        row = await self.db.fetch_row(sql, username)
        if not row and throw_error:
            throw_not_found("No user with this id!")
        return await self.row_to_profile(row)

    async def create(self,
                     username: str,
                     password: str,
                     email: str,
                     phone_number: str,
                     first_name: str,
                     last_name: str,
                     photo_url: str,
                     role: str) -> ProfileDB:
        sql = "INSERT INTO api_profile VALUES (DEFAULT, $1, crypt($2, gen_salt('bf', 8)), $3, $4, $5, $6, $7, $8::role, FALSE) RETURNING id"
        try:
            idx = await self.db.fetch_val(sql, username, password, email, phone_number, first_name, last_name,
                                          photo_url,
                                          role)
            return await self.get_by_id(idx)
        except:  # TODO handle specific error
            throw_bad_request("User with this email already exists!")
