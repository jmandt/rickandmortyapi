import graphene
import uvicorn
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_graphiql_handler

from config import settings
from schemas import CharacterQuery

app = FastAPI()

schema = graphene.Schema(
    query=CharacterQuery,
)

app.add_route("/", GraphQLApp(schema, on_get=make_graphiql_handler()))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=settings.port)
