import httpx
from typing import Optional, List, Annotated
from pydantic import Field, ValidationError
from mcp.server.fastmcp import FastMCP
from utils.schemas import *
from dotenv import load_dotenv
import os
from utils.auth import get_mal_access_token

load_dotenv()

MAL_API_URL = "https://api.myanimelist.net/v2"

def register_tools(mcp: FastMCP):

    #Anime
    @mcp.tool()
    async def get_anime(q: str, limit: int = 10, offset: int = 0) -> dict:
        """
        Fetches a list of anime from MyAnimeList based on a search query.
        
        Args:
            q (str): The search query for the anime.
            limit (int): The number of results to return (default is 10 and max 100).
            offset (int): The offset for pagination (default is 0).
        """
        try:
            CLIENT_ID = os.getenv("MAL_CLIENT_ID")
            async with httpx.AsyncClient() as client:
                headers = {"X-MAL-CLIENT-ID": f"{CLIENT_ID}"}
                params = {"q": q, "limit": limit, "offset": offset}
                response = await client.get(
                    f"{MAL_API_URL}/anime",
                    headers=headers,
                    params=params)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "status_code": e.response.status_code}
        except Exception as e:
            return {"error": str(e)}

    @mcp.tool()
    async def get_anime_details(anime_id: int, fields: Optional[List[str]]) -> dict:
        """
        Fetches details of an anime by its ID from MyAnimeList.
        
        Args:
            anime_id (int): The ID of the anime to fetch details for.
            fields (List[str]): List of fields to include in the response. If None, includes common fields:
                id, title, main_pictures.
                Valid fields: id, title, main_picture, alternative_titles, start_date, end_date,
                synopsis, mean, rank, popularity, num_list_users, num_scoring_users, nsfw,
                created_at, updated_at, media_type, status, genres, my_list_status, num_episodes,
                start_season, broadcast, source, average_episode_duration, rating, pictures,
                background, related_anime, related_manga, recommendations, studios, statistics.
        
        Examples:
        - To get the score: get_anime_details(30230, fields=["mean"])
        - To get similar animes: get_anime_details(30230, fields=["recommendations"])
        - To get genres and synopsis: get_anime_details(30230, fields=["genres", "synopsis"])
        """
        try:
            CLIENT_ID = os.getenv("MAL_CLIENT_ID")
            default_fields = ["id", "title", "main_picture"]
            selected_fields = fields if fields else default_fields
            fields_param = ",".join(selected_fields)

            async with httpx.AsyncClient() as client:
                headers = {"X-MAL-CLIENT-ID": f"{CLIENT_ID}"}
                response = await client.get(
                    f"{MAL_API_URL}/anime/{anime_id}?fields={fields_param}",
                    headers=headers)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "status_code": e.response.status_code}
        except Exception as e:
            return {"error": str(e)}
        
    @mcp.tool()
    async def get_anime_ranking(ranking_type: AnimeRanking = AnimeRanking.ALL, limit: int = 10, offset: int = 0) -> dict:
        """
        Fetches anime rankings from MyAnimeList.
        
        Args:
            ranking_type (AnimeRanking): The type of ranking to fetch. Options:
            "all", "airing", "upcoming", "tv", "ova", "movie", "special", "bypopularity", "favorite".
            limit (int): The number of results to return (default is 10 and max 500).
            offset (int): The offset for pagination (default is 0).
        """
        try:
            CLIENT_ID = os.getenv("MAL_CLIENT_ID")
            async with httpx.AsyncClient() as client:
                headers = {"X-MAL-CLIENT-ID": f"{CLIENT_ID}"}
                params = {"limit": limit, "offset": offset}
                response = await client.get(
                    f"{MAL_API_URL}/anime/ranking/{ranking_type.value}",
                    headers=headers,
                    params=params)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "status_code": e.response.status_code}
        except Exception as e:
            return {"error": str(e)}
        
    @mcp.tool()
    async def get_seasonal_anime(season: Season, year: int, sort: Optional[SeasonSort] = None, limit: int = 10, offset: int = 0) -> dict:
        """
        Fetches seasonal anime from MyAnimeList.
        
        Args:
            season (Season): The season to fetch. Options: "winter", "spring", "summer", "fall".
            year (int): The year of the season.
            sort (SeasonSort, optional): Sort order by "anime_score" or "anime_num_list_users". Default is None.
            limit (int): The number of results to return (default is 10 and max 500).
            offset (int): The offset for pagination (default is 0).
        """
        try:
            CLIENT_ID = os.getenv("MAL_CLIENT_ID")
            async with httpx.AsyncClient() as client:
                headers = {"X-MAL-CLIENT-ID": f"{CLIENT_ID}"}
                params = {"limit": limit, "offset": offset}
                if sort:
                    params["sort"] = sort.value
                response = await client.get(
                    f"{MAL_API_URL}/anime/season/{year}/{season.value}",
                    headers=headers,
                    params=params)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "status_code": e.response.status_code}
        except Exception as e:
            return {"error": str(e)}
        

    @mcp.tool()
    async def get_anime_list(username: str, status: AnimeStatus, sort: Optional[AnimeStatusSort] = None, limit: int = 10, offset: int = 0) -> dict:
        """
        Fetches an anime list for a user from MyAnimeList.
        
        Args:
            username (str): The username of the MyAnimeList user.
            status (AnimeStatus): The status of the anime list to fetch. Options: "watching", "completed", "on_hold", "dropped", "plan_to_watch".
            sort (AnimeStatusSort, optional): Sort order by "list_score", "list_updated_at", "anime_title" or "anime_start_date". Default is None.
            limit (int): The number of results to return (default is 10 and max 500).
            offset (int): The offset for pagination (default is 0).
        """
        try:
            CLIENT_ID = os.getenv("MAL_CLIENT_ID")
            async with httpx.AsyncClient() as client:
                headers = {"X-MAL-CLIENT-ID": f"{CLIENT_ID}"}
                params = {"status": status.value, "limit": limit, "offset": offset}
                if sort:
                    params["sort"] = sort.value
                response = await client.get(
                    f"{MAL_API_URL}/users/{username}/animelist",
                    headers=headers,
                    params=params)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "status_code": e.response.status_code}
        except Exception as e:
            return {"error": str(e)}


    #Manga
    @mcp.tool()
    async def get_manga(q: str, limit: int = 10, offset: int = 0) -> dict:
        """
        Fetches a list of manga from MyAnimeList based on a search query.
        
        Args:
            q (str): The search query for the manga.
            limit (int): The number of results to return (default is 10 and max 100).
            offset (int): The offset for pagination (default is 0).
        """
        try:
            CLIENT_ID = os.getenv("MAL_CLIENT_ID")
            async with httpx.AsyncClient() as client:
                headers = {"X-MAL-CLIENT-ID": f"{CLIENT_ID}"}
                params = {"q": q, "limit": limit, "offset": offset}
                response = await client.get(
                    f"{MAL_API_URL}/manga",
                    headers=headers,
                    params=params)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "status_code": e.response.status_code}
        except Exception as e:
            return {"error": str(e)}
        
    @mcp.tool()
    async def get_manga_details(manga_id: int, fields: Optional[List[str]]) -> dict:
        """
        Fetches details of a manga by its ID from MyAnimeList.
        
        Args:
            manga_id (int): The ID of the manga to fetch details for.
            fields (List[str]): List of fields to include in the response. If None, includes common fields:
                id, title, main_picture.
                Valid fields: id, title, main_picture, alternative_titles, start_date, end_date, synopsis, mean,
                rank, popularity, num_list_users, num_scoring_users, nsfw, created_at, updated_at, media_type,
                status, genres, my_list_status, num_volumes, num_chapters, authors, pictures,
                background, related_anime, related_manga, recommendations, serialization
        
        Examples:
        - To get the score: get_manga_details(30230, fields=["mean"])
        - To get similar mangas: get_manga_details(30230, fields=["recommendations"])
        - To get genres and synopsis: get_manga_details(30230, fields=["genres", "synopsis"])
        """
        try:
            CLIENT_ID = os.getenv("MAL_CLIENT_ID")
            default_fields = ["id", "title", "main_picture"]
            selected_fields = fields if fields else default_fields
            fields_param = ",".join(selected_fields)

            async with httpx.AsyncClient() as client:
                headers = {"X-MAL-CLIENT-ID": f"{CLIENT_ID}"}
                response = await client.get(
                    f"{MAL_API_URL}/manga/{manga_id}?fields={fields_param}",
                    headers=headers)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "status_code": e.response.status_code}
        except Exception as e:
            return {"error": str(e)}
        
    @mcp.tool()
    async def get_manga_ranking(ranking_type: MangaRanking, limit: int = 100, offset: int = 0) -> dict:
        """
        Fetches manga rankings from MyAnimeList.
        
        Args:
            ranking_type (MangaRanking): The type of ranking to fetch. Options: 
            "all", "manga", "novels", "oneshot", "doujin", "manhwa", "manhua", "bypopularity", "favorite".
            limit (int): The number of results to return (default is 10 and max 500).
            offset (int): The offset for pagination (default is 0).
        """
        try:
            CLIENT_ID = os.getenv("MAL_CLIENT_ID")
            async with httpx.AsyncClient() as client:
                headers = {"X-MAL-CLIENT-ID": f"{CLIENT_ID}"}
                params = {"limit": limit, "offset": offset}
                response = await client.get(
                    f"{MAL_API_URL}/manga/ranking/{ranking_type.value}",
                    headers=headers,
                    params=params)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "status_code": e.response.status_code}
        except Exception as e:
            return {"error": str(e)}
        
    @mcp.tool()
    async def get_manga_list(username: str, status: MangaStatus, sort: Optional[MangaStatusSort] = None, limit: int = 10, offset: int = 0) -> dict:
        """
        Fetches a manga list for a user from MyAnimeList.
        
        Args:
            username (str): The username of the MyAnimeList user.
            status (MangaStatus): The status of the manga list to fetch. Options: "reading", "completed", "on_hold", "dropped", "plan_to_read".
            sort (MangaStatusSort, optional): Sort order by "list_score", "list_updated_at", "manga_title" or "manga_start_date". Default is None.
            limit (int): The number of results to return (default is 10 and max 500).
            offset (int): The offset for pagination (default is 0).
        """
        try:
            CLIENT_ID = os.getenv("MAL_CLIENT_ID")
            async with httpx.AsyncClient() as client:
                headers = {"X-MAL-CLIENT-ID": f"{CLIENT_ID}"}
                params = {"status": status.value, "limit": limit, "offset": offset}
                if sort:
                    params["sort"] = sort.value
                response = await client.get(
                    f"{MAL_API_URL}/users/{username}/mangalist",
                    headers=headers,
                    params=params)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "status_code": e.response.status_code}
        except Exception as e:
            return {"error": str(e)}

    # User
    # NEEDS OAUTH2 AUTHENTICATION    
    
    @mcp.tool()
    async def get_suggested_anime(limit: int = 10, offset: int = 0) -> dict:
        """
        Fetches suggested anime for the current user from MyAnimeList.
        
        Args:
            limit (int): The number of results to return (default is 10 and max 100).
            offset (int): The offset for pagination (default is 0).
        """
        try:
            token = await get_mal_access_token()
            if not token:
                raise ValueError("No valid access token available")
            headers = {"Authorization": f"Bearer {token}"}
            params = {"limit": limit, "offset": offset}
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{MAL_API_URL}/anime/suggestions",
                    headers = headers,
                    params = params
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "status_code": e.response.status_code}
        except Exception as e:
            return {"error": str(e)}
        
    @mcp.tool()
    async def get_user_profile(fields: Optional[str] = None) -> dict:
        """
        Fetches the profile of the current user from MyAnimeList.
        
        Args:
            fields (str, optional): Set to "anime_statistics" to include anime statistics. Default is None.
        """
        try:
            token = await get_mal_access_token()
            if not token:
                raise ValueError("No valid access token available")
            headers = {"Authorization": f"Bearer {token}"}
            params = {}
            if fields == "anime_statistics":
                params["fields"] = "anime_statistics"
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{MAL_API_URL}/users/@me",
                    headers=headers,
                    params=params
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "status_code": e.response.status_code}
        except Exception as e:
            return {"error": str(e)}
    
    @mcp.tool()
    async def delete_myanimelist_item(anime_id: int) -> dict:
        """
        Deletes an anime from the authenticated user's MyAnimeList.
        
        Args:
            anime_id: The ID of the anime to delete.
        """
        try:
            token = await get_mal_access_token()
            if not token:
                raise ValueError("No valid access token available")
            headers = {"Authorization": f"Bearer {token}"}
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"https://api.myanimelist.net/v2/anime/{anime_id}/my_list_status",
                    headers=headers
                )
                response.raise_for_status()
                return {"message": f"Anime ID {anime_id} deleted successfully"}
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "status_code": e.response.status_code, "response_text": e.response.text}
        except ValueError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
        
    @mcp.tool()
    async def delete_mymangalist_item(manga_id: int) -> dict:
        """
        Deletes an anime from the authenticated user's MyAnimeList.
        
        Args:
            anime_id: The ID of the anime to delete.
        """
        try:
            token = await get_mal_access_token()
            if not token:
                raise ValueError("No valid access token available")
            headers = {"Authorization": f"Bearer {token}"}
            async with httpx.AsyncClient() as client:
                response = await client.delete(
                    f"https://api.myanimelist.net/v2/manga/{manga_id}/my_list_status",
                    headers=headers
                )
                response.raise_for_status()
                return {"message": f"Manga ID {manga_id} deleted successfully"}
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "status_code": e.response.status_code, "response_text": e.response.text}
        except ValueError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
        
    @mcp.tool()
    async def update_myanimelist(
        anime_id: Annotated[int, Field(description="ID of the anime to update", ge=1)],
        status: Annotated[
            Optional[str],
            Field(
                description="Anime list status",
                pattern="^(watching|completed|on_hold|dropped|plan_to_watch)$"
            )
        ] = None,
        score: Annotated[
            Optional[int],
            Field(description="Score for the anime (0-10)", ge=0, le=10)
        ] = None,
        num_watched_episodes: Annotated[
            Optional[int],
            Field(description="Number of episodes watched", ge=0)
        ] = None,
        is_rewatching: Annotated[
            Optional[bool],
            Field(description="Whether the anime is being rewatched")
        ] = None,
        priority: Annotated[
            Optional[int],
            Field(description="Priority (0-2)", ge=0, le=2)
        ] = None,
        num_times_rewatched: Annotated[
            Optional[int],
            Field(description="Number of times rewatched", ge=0)
        ] = None,
        rewatch_value: Annotated[
            Optional[int],
            Field(description="Rewatch value (0-5)", ge=0, le=5)
        ] = None,
        tags: Annotated[
            Optional[str],
            Field(description="Comma-separated tags")
        ] = None,
        comments: Annotated[
            Optional[str],
            Field(description="Comments about the anime", max_length=1000)
        ] = None
    ) -> dict:
        """
        Updates an anime's status in the authenticated user's MyAnimeList.
        
        Args:
            anime_id: The ID of the anime to update.
            status: The watch status (watching, completed, on_hold, dropped, plan_to_watch).
            score: The score given to the anime (0-10).
            num_watched_episodes: Number of episodes watched.
            is_rewatching: Whether the anime is being rewatched.
            priority: Priority of the anime (0-2).
            num_times_rewatched: Number of times the anime was rewatched.
            rewatch_value: Value of rewatching the anime (0-5).
            tags: Comma-separated tags for the anime.
            comments: Comments about the anime.
        
        """
        try:
            fields = {
                "status": status,
                "score": score,
                "num_watched_episodes": num_watched_episodes,
                "is_rewatching": is_rewatching,
                "priority": priority,
                "num_times_rewatched": num_times_rewatched,
                "rewatch_value": rewatch_value,
                "tags": tags,
                "comments": comments
            }
            fields = {k: v for k, v in fields.items() if v is not None}
            if not fields:
                return {"error": "At least one field must be provided to update the anime"}

            token = await get_mal_access_token()
            if not token:
                raise ValueError("No valid access token available")

            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"https://api.myanimelist.net/v2/anime/{anime_id}/my_list_status",
                    headers=headers,
                    data=fields
                )
                response.raise_for_status()
                return response.json()
        except ValidationError as e:
            return {"error": f"Invalid input: {str(e)}"}
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "status_code": e.response.status_code, "response_text": e.response.text}
        except ValueError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
        
    @mcp.tool()
    async def update_mymangalist(
        manga_id: Annotated[int, Field(description="ID of the manga to update", ge=1)],
        status: Annotated[
            Optional[str],
            Field(
                description="Manga list status",
                pattern="^(reading|completed|on_hold|dropped|plan_to_read)$"
            )
        ] = None,
        is_rereading: Annotated[
            Optional[bool],
            Field(description="Whether the manga is being rewatched")
        ] = None,
        score: Annotated[
            Optional[int],
            Field(description="Score for the manga (0-10)", ge=0, le=10)
        ] = None,
        num_volumes_read: Annotated[
            Optional[int],
            Field(description="Number of volumes read", ge=0)
        ] = None,
        num_chapters_read: Annotated[
            Optional[int],
            Field(description="Number of chapters read", ge=0)
        ] = None,
        priority: Annotated[
            Optional[int],
            Field(description="Priority (0-2)", ge=0, le=2)
        ] = None,
        num_times_reread: Annotated[
            Optional[int],
            Field(description="Number of times reread", ge=0)
        ] = None,
        reread_value: Annotated[
            Optional[int],
            Field(description="Reread value (0-5)", ge=0, le=5)
        ] = None,
        tags: Annotated[
            Optional[str],
            Field(description="Comma-separated tags")
        ] = None,
        comments: Annotated[
            Optional[str],
            Field(description="Comments about the manga", max_length=1000)
        ] = None
    ) -> dict:
        """
        Updates a manga's status in the authenticated user's MyAnimeList.
        
        Args:
            manga_id: The ID of the manga to update.
            status: The read status (reading, completed, on_hold, dropped, plan_to_read).
            is_rereading: Whether the manga is being reread.
            score: The score given to the manga (0-10).
            num_volumes_read: Number of volumes read.
            num_chapters_read: Number of chapters read.
            priority: Priority of the manga (0-2).
            num_times_reread: Number of times the manga was reread.
            reread_value: Value of reread the manga (0-5).
            tags: Comma-separated tags for the manga.
            comments: Comments about the manga.
        
        """
        try:
            fields = {
                "status": status,
                "is_rereading": is_rereading,
                "score": score,
                "num_volumes_read": num_volumes_read,
                "num_chapters_read": num_chapters_read,
                "priority": priority,
                "num_times_reread": num_times_reread,
                "reread_value": reread_value,
                "tags": tags,
                "comments": comments
            }
            fields = {k: v for k, v in fields.items() if v is not None}
            if not fields:
                return {"error": "At least one field must be provided to update the manga"}

            token = await get_mal_access_token()
            if not token:
                raise ValueError("No valid access token available")

            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            async with httpx.AsyncClient() as client:
                response = await client.put(
                    f"https://api.myanimelist.net/v2/manga/{manga_id}/my_list_status",
                    headers=headers,
                    data=fields
                )
                response.raise_for_status()
                return response.json()
        except ValidationError as e:
            return {"error": f"Invalid input: {str(e)}"}
        except httpx.HTTPStatusError as e:
            return {"error": str(e), "status_code": e.response.status_code, "response_text": e.response.text}
        except ValueError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
            
        
