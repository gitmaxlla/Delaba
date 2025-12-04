from pydantic import BaseModel
import datetime


class News(BaseModel):
    id: int
    section: str

    by: int
    postedAt: datetime.datetime
    message: str
