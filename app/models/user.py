from dataclasses import asdict, field, dataclass
import json


@dataclass(slots=True)
class User:
    id: int
    username: str
    firstname: str
    lastname: str
    password: str
    email: str
    image: str

    # NOTE: roles: ['admin', 'user', 'curator']
    roles: list[str] = field(default_factory=lambda: ["user"])

    def __post_init__(self):
        self.roles = json.loads(self.roles)

    def todict(self):
        this_dict = asdict(self)
        del this_dict["password"]

        return this_dict

    def todict_simplified(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
        }
