# Rick and Morty Graphql App

## Getting started
Easily build and start the API using docker-compose file and make commands
```bash
make run-api 
```

You should able to see the GraphQL playground at http://localhost:8080 in your browser.


To test manually using the GraphQL Playground, you can use the queries in the tests or as outlined below:
 ```
 query Characters {
  characters(filter: {name: "rick"}, first: 2) {
    count
    edges {
      node {
        id
        name
        status
        species
        gender
      }
    }
    pageInfo {
      endCursor
      hasPreviousPage
      hasNextPage
    }
  }
}
 ```

### Development

Use [Poetry](https://python-poetry.org/) to install all dependencies with:

```bash
poetry install
```

Enter the poetry virtual env with:
```bash
poetry shell
```

To set up the git hook scripts run:
```bash
pre-commit install
```

You should able to see the GraphQL playground at <http://localhost:8000\> in your browser.

### Testing

You can run the tests that are define in `tests\` with:
```bash
pytest
```

or if you want some additional infos regarding coverage, run 
```bash
make tests
```