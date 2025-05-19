from dataclasses import asdict, field, dataclass
import json


@dataclass(slots=True)
class User:
    id: int
    image: str
    password: str
    username: str
    roles: list[str]
    extra: dict[str, str] = field(default_factory=dict)

    # NOTE: roles: ['admin', 'user', 'curator']
    roles: list[str] = field(default_factory=lambda: ["user"])

    def todict(self):
        this_dict = asdict(self)
        del this_dict["password"]

        return this_dict

    def todict_simplified(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.extra["firstname"] if self.extra else "",
        }
