from pydantic import BaseModel, ConfigDict


class ChannelCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    channel: str
