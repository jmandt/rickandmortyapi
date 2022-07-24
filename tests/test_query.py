from graphene.test import Client

from app.main import schema

SIMPLE_CHARACTER_FRAGMENT = """
    fragment simpleCharacterValues on Character {
        id
        name
        status
        species
        gender
    }
"""


def test_count_no_filters():
    client = Client(schema)
    query = """
        {
            characters {
                count
            }
        }
    """

    result = client.execute(query)

    assert result == {"data": {"characters": {"count": 20}}}


def test_first_5():
    client = Client(schema)
    query = (
        """
            {
                characters (first: 5) {
                    count
                    edges {
                        node {
                            ...simpleCharacterValues
                        }
                    }
                }
            }
        """
        + SIMPLE_CHARACTER_FRAGMENT
    )
    result = client.execute(query)

    assert result == {
        "data": {
            "characters": {
                "count": 20,
                "edges": [
                    {
                        "node": {
                            "gender": "Male",
                            "id": 1,
                            "name": "Rick Sanchez",
                            "species": "Human",
                            "status": "Alive",
                        }
                    },
                    {"node": {"gender": "Male", "id": 2, "name": "Morty Smith", "species": "Human", "status": "Alive"}},
                    {
                        "node": {
                            "gender": "Female",
                            "id": 3,
                            "name": "Summer Smith",
                            "species": "Human",
                            "status": "Alive",
                        }
                    },
                    {
                        "node": {
                            "gender": "Female",
                            "id": 4,
                            "name": "Beth Smith",
                            "species": "Human",
                            "status": "Alive",
                        }
                    },
                    {"node": {"gender": "Male", "id": 5, "name": "Jerry Smith", "species": "Human", "status": "Alive"}},
                ],
            }
        }
    }


def test_filter():
    client = Client(schema)
    query = (
        """
            {
                characters (filter: {name: "rick"}) {
                    count
                    edges {
                        node {
                            ...simpleCharacterValues
                        }
                    }
                }
            }
        """
        + SIMPLE_CHARACTER_FRAGMENT
    )
    result = client.execute(query)

    assert result == {
        "data": {
            "characters": {
                "count": 4,
                "edges": [
                    {
                        "node": {
                            "" "gender": "Male",
                            "id": 1,
                            "name": "Rick Sanchez",
                            "species": "Human",
                            "status": "Alive",
                        }
                    },
                    {
                        "node": {
                            "gender": "Male",
                            "id": 8,
                            "name": "Adjudicator Rick",
                            "species": "Human",
                            "status": "Dead",
                        }
                    },
                    {
                        "node": {
                            "gender": "Male",
                            "id": 15,
                            "name": "Alien Rick",
                            "species": "Alien",
                            "status": "unknown",
                        }
                    },
                    {
                        "node": {
                            "gender": "Male",
                            "id": 19,
                            "name": "Antenna Rick",
                            "species": "Human",
                            "status": "unknown",
                        }
                    },
                ],
            }
        }
    }


def test_filter_complete_object():
    client = Client(schema)
    query = (
        """
            {
                characters (filter: {name: "Rick Sanchez"}) {
                    count
                    edges {
                        node {
                            ...simpleCharacterValues
                            origin {
                                name
                                url
                            }
                            location {
                                name
                                url
                            }
                            image
                            url
                            created
                        }
                    }
                }
            }
        """
        + SIMPLE_CHARACTER_FRAGMENT
    )
    result = client.execute(query)

    assert result == {
        "data": {
            "characters": {
                "count": 1,
                "edges": [
                    {
                        "node": {
                            "created": "2017-11-04T18:48:46.250000",
                            "gender": "Male",
                            "id": 1,
                            "image": "https://rickandmortyapi.com/api/character/avatar/1.jpeg",
                            "location": {
                                "name": "Citadel of " "Ricks",
                                "url": "https://rickandmortyapi.com/api/location/3",
                            },
                            "name": "Rick Sanchez",
                            "origin": {"name": "Earth (C-137)", "url": "https://rickandmortyapi.com/api/location/1"},
                            "species": "Human",
                            "status": "Alive",
                            "url": "https://rickandmortyapi.com/api/character/1",
                        }
                    },
                ],
            }
        }
    }


def test_no_result():
    client = Client(schema)
    query = (
        """
            {
                characters (filter: {name: "nobody"}) {
                    count
                    edges {
                        node {
                            ...simpleCharacterValues
                        }
                    }
                }
            }
        """
        + SIMPLE_CHARACTER_FRAGMENT
    )
    result = client.execute(query)

    assert result == {"data": {"characters": {"count": 0, "edges": []}}}


def test_wrong_query_params():
    client = Client(schema)
    query = """
        {
            characters (filter: {id: 1}) {
                count
            }
        }
    """
    result = client.execute(query)

    assert result == {
        "data": None,
        "errors": [
            {"locations": [{"column": 34, "line": 3}], "message": "Field 'id' is not defined by type 'Filter'."}
        ],
    }
