from enum import Enum

class AnimeRanking(Enum):
    ALL = "all"
    AIRING = "airing"
    UPCOMING = "upcoming"
    TV = "tv"
    OVA = "ova"
    MOVIE = "movie"
    SPECIAL = "special"
    BYPOPULARITY = "bypopularity"
    FAVORITE = "favorite"

class Season(Enum):
    WINTER = "winter"
    SPRING = "spring"
    SUMMER = "summer"
    FALL = "fall"

class SeasonSort(Enum):
    SCORE = "anime_score"
    NUM_LIST_USERS = "anime_num_list_users"

class AnimeStatus(Enum):
    WATCHING = "watching"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    DROPPED = "dropped"
    PLANNING = "plan_to_watch"

class AnimeStatusSort(Enum):
    LIST_SCORE = "list_score"
    LIST_UPDATED_AT = "list_updated_at"
    ANIME_TITLE = "anime_title"
    ANIME_START_DATE = "anime_start_date"

class MangaRanking(Enum):
    ALL = "all"
    MANGA = "manga"
    NOVEL = "novels"
    ONE_SHOT = "oneshots"
    DOUJIN = "doujin"
    MANHWA = "manhwa"
    MANHUA = "manhua"
    BYPOPULARITY = "bypopularity"
    FAVORITE = "favorite"

class MangaStatus(Enum):
    READING = "reading"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"
    DROPPED = "dropped"
    PLANNING = "plan_to_read"

class MangaStatusSort(Enum):
    LIST_SCORE = "list_score"
    LIST_UPDATED_AT = "list_updated_at"
    MANGA_TITLE = "manga_title"
    MANGA_START_DATE = "manga_start_date"