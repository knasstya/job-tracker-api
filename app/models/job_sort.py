from enum import Enum


class JobSortField(str, Enum):
    CREATED_AT = "created_at"
    COMPANY = "company"
    POSITION = "position"


class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"