"""Service for outputing offline recommendations (personal and top-popular)."""
import logging
from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI, Request

# Setting up a logger with uvicorn output stream
logger = logging.getLogger("uvicorn.error")
logging.basicConfig(level=logging.INFO)


class Recommender():
    """Class for generating offline recommendations."""
    
    def __init__(self):
        """Initializes a class instance."""
        # Attribute for storing rec-data
        self._recs = {
            "personal": None,
            "default": None,
        }
        # Attribute for storing request counts
        self._stats = {
            "request_personal_count": 0,
            "request_default_count": 0,
        }

    def load(self, type, path, **kwargs):
        """Loads offline recommendations."""
        logger.info(f"Loading recommendations: {type}")
        self._recs[type] = pd.read_parquet(path, **kwargs)
        if type == "personal":
            self._recs[type] = self._recs[type].set_index("user_id")
        logger.info("Recommendations loaded")

    def get(self, user_id: int, k: int = 10):
        """Generates k offline recommendations for user."""
        try:
            recs = self._recs["personal"].loc[user_id]
            recs = recs["track_id"].tolist()[:k]
            self._stats["request_personal_count"] += 1
            logger.info(f"user {user_id} - using personal history")
        except KeyError:
            recs = self._recs["default"]
            recs = recs["track_id"].tolist()[:k]
            self._stats["request_default_count"] += 1
            logger.info(f"user {user_id} - using default")
        except:
            logger.error("No recommendations found")
            recs = []

        return recs
    
    def stats(self) -> None:
        """Logs service statistics."""
        logger.info("Stats for recommendations")

        for name, value in self._stats.items():
            logger.info(f"{name:<30} {value}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Loads data on application start-up."""
    rec_store = Recommender()
    rec_store.load(type="personal", path="data/recommendations.parquet")
    rec_store.load(type="default", path="data/top_popular.parquet")

    yield {"rec_store": rec_store}

    rec_store.stats()


# Creating an app
app = FastAPI(title="recommendations_offline", lifespan=lifespan)

# Endpoint for getting offline recommendations
@app.post("/get_recs")
async def recommendations(request: Request, user_id: int, k: int):
    """Generates offline recommendations."""
    rec_store = request.state.rec_store

    i2i = rec_store.get(user_id, k)

    return i2i
