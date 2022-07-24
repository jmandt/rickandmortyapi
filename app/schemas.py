from datetime import datetime

from graphene import Connection, ConnectionField, DateTime, Field, InputObjectType, Int, List, ObjectType, String

from data.characters import characters


class BaseType(ObjectType):
    name = String()
    url = String()


class Location(BaseType):
    pass


class Origin(BaseType):
    pass


class Character(ObjectType):
    id = Int()
    name = String()
    status = String()  # should be an Enum
    species = String()  # should be an Enum
    type = String()
    gender = String()  # should be an Enum
    origin = Field(Origin)
    location = Field(Location)
    image = String()
    episode = List(String)
    url = String()
    created = DateTime()

    @staticmethod
    def resolve_created(parent, _):
        created = datetime.strptime(parent.get("created"), "%Y-%m-%dT%H:%M:%S.%fZ")
        return created


class CharacterConnection(Connection):
    count = Int()

    class Meta:
        node = Character

    @staticmethod
    def resolve_count(connection, _):
        return len(connection.iterable)


class Filter(InputObjectType):
    name = String()


class CharacterQuery(ObjectType):
    characters = ConnectionField(CharacterConnection, filter=Filter(description="Field and search query"))

    @staticmethod
    def resolve_characters(
        _,
        __,
        filter=None,  # noqa A002
        *args,
        **kwargs,
    ):
        if not filter:
            return characters

        filtered_result = [
            character for character in characters if filter.name.lower() in character.get("name").lower()
        ]
        return filtered_result
