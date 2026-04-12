from src.core.config import ADMIN_MAIL
from src.core.permissions import PermissionTags
from src.core.security import generate_password
from src.core.security import hash as pwdlib_hash
from src.database import db
from src.schemas.channels import ChannelCreate
from src.models.users import User as UserModel
from src.services.channels import create_channel


class __Manager:
    def _create_admin_user(self) -> tuple[UserModel, str]:
        random_password = generate_password()
        create_channel(ChannelCreate(channel=""))

        user = UserModel(
            id=0,
            login=ADMIN_MAIL,
            role="Администратор",
            permissions=(
                PermissionTags.ADMIN
                | PermissionTags.MANAGE_CHANNEL
                | PermissionTags.VIEW_CHANNEL
            ),
            password_hashed=pwdlib_hash(random_password),
            channel="",
        )

        return (user, random_password)

    def init_app(self):
        user, random_password = self._create_admin_user()

        with db.Session() as session:
            admin = session.get(UserModel, 0)
            if not admin:
                session.add(user)

            if admin and not admin.initialized:
                session.delete(admin)
                session.add(user)

                print(f"\n\033[33mRoot login --> {ADMIN_MAIL}")
                print(f"\033[33mRoot password --> {random_password}")
                print(
                    "(Pass to sysadmin to enter in the web interface to finish initialization)\033[0m\n",
                    flush=True,
                )

            session.commit()


manager = __Manager()
