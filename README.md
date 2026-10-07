# Employee Management API

## Run with Docker

Build the image and start the API with a persistent SQLite database:

```sh
docker compose up --build
```

The API is available at <http://localhost:8000>; interactive documentation is
at <http://localhost:8000/docs>. Compose stores the database in the
`employee-data` volume so employee records survive container recreation.

To build and run the image without Compose:

```sh
docker build -t employee-db-api .
docker run --rm -p 8000:8000 employee-db-api
```

The standalone container stores its database in the container filesystem.
Use Compose if you need the database to persist across container removal.

## Run locally

```sh
pip install -r requirements.txt
uvicorn main:app --reload
```

By default, the local server stores data in `employees.db` in the project
directory. Set `DATABASE_URL` to use a different SQLAlchemy database URL.
