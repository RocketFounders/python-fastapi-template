from typing import Optional, Iterable

from core.models.profile.db import ProfileDB
from core.models.profile.domains import UpdateProfile
from core.storage.db.postgres import DB
from core.utils import throw_not_found, throw_bad_request
from asyncpg import Record


class ProfileStorage:
    def __init__(self, db: DB) -> None:
        self.db = db

    @classmethod
    def row_to_profile(cls, row: Record) -> ProfileDB:
        return ProfileDB.model_validate(
            {key: val for key, val in zip(row.keys(), row.values())}
        )

    async def get_all(
            self, throw_error: bool = False
    ) -> list[ProfileDB]:
        sql = "SELECT * FROM api_profile"
        rows = await self.db.fetch(sql)
        if not rows and throw_error:
            throw_not_found("No active users!")

        profiles: list[ProfileDB] = []
        for row in rows:
            profiles.append(self.row_to_profile(row))

        return profiles

    async def get_by_id(
            self, profile_id: str, throw_error: bool = False
    ) -> Optional[ProfileDB]:
        sql = "SELECT * FROM api_profile WHERE (id = $1)"
        row = await self.db.fetch_row(sql, profile_id)
        if not row and throw_error:
            throw_not_found("No user with this id!")
        profile = self.row_to_profile(row)
        return profile

    async def get_by_email(self, email: str, throw_error: bool = True) -> ProfileDB:
        sql = "SELECT * FROM api_profile WHERE (email = $1)"
        row = await self.db.fetch_row(sql, email)
        if not row and throw_error:
            throw_not_found("No user with this id!")

        return self.row_to_profile(row)

    async def get_by_username(
            self, username: str, throw_error: bool = True
    ) -> ProfileDB:
        sql = "SELECT * FROM api_profile WHERE (username = $1)"
        row = await self.db.fetch_row(sql, username)
        if not row and throw_error:
            throw_not_found("No user with this id!")
        return self.row_to_profile(row)

    async def create(
            self,
            username: str,
            password: str,
            email: str,
            phone_number: str,
            first_name: str,
            last_name: str,
            photo_url: str,
            role: str,
    ) -> ProfileDB:
        sql = """
        INSERT INTO api_profile
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8::role)
        RETURNING *
        """
        try:
            row = await self.db.fetch_val(
                sql,
                username,
                password,
                email,
                phone_number,
                first_name,
                last_name,
                photo_url,
                role,
            )
            profile = self.row_to_profile(row)
            return profile
        except:  # TODO handle specific error
            throw_bad_request("User with this email already exists!")

    async def update(self, profile: UpdateProfile, email: str) -> ProfileDB:
        sql = (
            "UPDATE api_profile "
            "SET first_name = $2,"
            "last_name = $3,"
            "phone_number = $4"
            "WHERE email = $1 "
            "RETURNING *"
        )
        profile = await self.db.fetch_row(
            sql,
            email,
            profile.first_name,
            profile.last_name,
            profile.phone_number,
        )
        return ProfileDB.model_validate(dict(profile))
