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

## Add MCP Server to Claude

Open the claude desktop app and go to the settings > development > Edit config file.

Add the following to the config file:

```json
{
  "mcpServers": {
    "Clio: Planning Restrictions Checker": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "--with",
        "pandas",
        "--with",
        "fastparquet",
        "--with",
        "pyarrow",
        "--with",
        "sqlmodel",
        "--with",
        "pathlib",
        "mcp",
        "run",
        "/path/to/clio/src/clio/api/mcp.py"
      ],
      "env": {
        "AZURE_OPENAI_MODEL": "gpt-4.1",
        "OPENAI_API_VERSION": "2024-12-01-preview",
        "AZURE_OPENAI_ENDPOINT": "<ENDPOINT_HERE>",
        "AZURE_OPENAI_KEY": "<KEY_HERE>"
      }
    }
  }
}
```

Replace `<ENDPOINT_HERE>` and `<KEY_HERE>` with your Azure OpenAI endpoint and key.

### Demo of how to use the MCP Server

https://www.loom.com/share/fecab7ed072b4de28bc265ae8d2a14da

<div>
  <a href="https://www.loom.com/share/fecab7ed072b4de28bc265ae8d2a14da">
    <p>MCP Server Planning Overview 🚀 - Watch Video</p>
  </a>
  <a href="https://www.loom.com/share/fecab7ed072b4de28bc265ae8d2a14da">
    <img style="max-width:300px;" src="https://cdn.loom.com/sessions/thumbnails/fecab7ed072b4de28bc265ae8d2a14da-349b8a631380e746-full-play.gif">
  </a>
</div>

### Example prompts

**General planning query**

```
My property is Morden Park House, Morden Park Open Space, London Road, Morden, SM4 5QU - what planning considerations should I take into account?
```

**Planning restrictions for a specific postcode**

```
What are the planning restrictions for properties in SM4?
```

**Planning restrictions for a specific town**

```
What are the planning restrictions for properties in Morden?
```

**Planning restrictions for a specific property in a specific format**

```
My property is Morden Park House, Morden Park Open Space, London Road, Morden, SM4 5QU.
I want to build a permanent marquee, give me a summary in the following format:

✅ - for the things I can do
❌ - for the things I can't do
⚠️ - for the things I need permission for

Don't add any other information.
```

## Next Steps
- Develop a way to create and maintain a database of summarised applications which the backend can use in place of the in-memory "database" we currently use.
- Dockerise or otherwise prepare for deployment outside of dev
