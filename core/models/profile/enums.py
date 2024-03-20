from enum import Enum


class ProfileRole(str, Enum):
    admin = "admin"
    guest = "guest"
    junior = "junior"
    expert = "expert"
    worker = "worker"
