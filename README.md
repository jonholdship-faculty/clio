# clio

Planning Data Hackathon

## Set Up

Install python3.11 and then the package:

```
pip install poetry
poetry install
```

Then run the data set up with poetry

```
poetry run python scripts/summarise_past_apps.py
```

## Run the app

The app is in two parts: a frontend and a backend.

To run the backend:

```
poetry run fastapi dev src/clio/api/api.py
```

This depends on the data processing script above being run first.

Then run the frontend:

```

## Next Steps
- Develop a way to create and maintain a database of summarised applications which the backend can use in place of the in-memory "database" we currently use.
- Dockerise or otherwise prepare for deployment outside of dev
```
