from pydantic import BaseModel, Field, FutureDatetime, model_validator
from datetime import datetime

class UserSchema(BaseModel):
    login: str = Field(
        min_length=3,
        max_length=20,
        pattern=r"^[a-zA-Z0-9]+$")
    password_hash: str

class TaskSchema(BaseModel):
    title : str = Field(min_length=3, max_length=50)
    description : str | None = Field(max_length=1000)
    start_time :  FutureDatetime
    end_time : FutureDatetime

    @model_validator(mode="after")
    def validate_time(self):
        if self.end_time <= self.start_time:
            raise ValueError("Время окончания задачи должно быть позже времени начала задачи")

        return self

        