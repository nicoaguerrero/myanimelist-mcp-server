[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/nicoaguerrero-myanimelist-mcp-server-badge.png)](https://mseep.ai/app/nicoaguerrero-myanimelist-mcp-server)

# MyAnimeList MCP Server

[![smithery badge](https://smithery.ai/badge/@nicoaguerrero/myanimelist-mcp-server)](https://smithery.ai/server/@nicoaguerrero/myanimelist-mcp-server)

MCP Server for interacting with the MyAnimeList API, allowing LLM clients to access and interact with anime, manga and more.

## Using with Claude Desktop (or other MCP clients)

### Installing via Smithery

To install myanimelist-mcp-server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@nicoaguerrero/myanimelist-mcp-server):

```bash
npx -y @smithery/cli install @nicoaguerrero/myanimelist-mcp-server --client claude
```

### Manual Installation

1. Add this server to your `claude_desktop_config.json`:

```json
{
    "mcpServers": {
        "myanimelist": {
            "command": "uv",
            "args": [
                "--directory",
                "<path to your project>",
                "run",
                "main.py"
            ]
        }
    }
}
```

2. Restart Claude Desktop
3. Use the tools to interact with MyAnimeList

## Available Tools

### Anime
- **get_anime**: Get a list of anime based on a search query and filters
- **get_anime_details**: Get details of an anime by its ID, like recommendations, studios, broadcasting, etc.
- **get_anime_ranking**: Get anime rankings
- **get_seasonal_anime**: Get seasonal anime based on year and season
- **get_anime_list**: Get an user's anime list based on it's username
- **get_suggested_anime**: [Requires Auth] Get anime recommendations for a logged user
- **update_myanimelist**: [Requires Auth] Update an anime from the logged user's anime list
- **delete_myanimelist_item**: [Requires Auth] Delete an anime from the logged user's anime list

### Manga
- **get_manga**: Get a list of manga based on a search query and filters
- **get_manga_details**: Get details of a manga by its ID
- **get_manga_ranking**: Get manga rankings
- **get_manga_list**:  Get an user's manga list based on it's username
- **update_mymangalist**: [Requires Auth] Update a manga from the logged user's manga list
- **delete_mymangalist_item**: [Requires Auth] Delete a manga from the logged user's manga list

### User
- **get_user_profile**: [Requires Auth] Get details about the logged user

### Get an MyAnimeList API Token for Auth

To get an API token, follow these steps:

1. Go to [API](https://myanimelist.net/apiconfig) in profile settings.
2. Click on "Create ID" and select app type web.
3. Use this URL as your client's "Redirect URL":
```
http://localhost:8080/callback
```

4. Click "Submit"
5. Then click "Edit" in your generated client and you will see the the client_ID and client_secret.
6. Copy them in your `.env` file or environment variables (see .env_example).


#### Useful resources
https://myanimelist.net/apiconfig/references/authorization
https://myanimelist.net/forum/?topicid=1850649&show=150#msg69272815
https://myanimelist.net/apiconfig/references/api/v2
