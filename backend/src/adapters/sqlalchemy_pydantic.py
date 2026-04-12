from src.models.users import User as UserModel
from src.schemas.users import User as UserSchema


def to_user_schema(user: UserModel) -> UserSchema:
    user_fields = user.__dict__.copy()
    user_fields["permissions"] = int(user_fields["permissions"], 2)
    return UserSchema.model_validate(user_fields)
