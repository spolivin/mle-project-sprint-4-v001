"""Service for outputing online recommendations (track similarity)."""
import logging
from contextlib import asynccontextmanager

import pandas as pd
from fastapi import FastAPI, Request

# Setting up a logger with uvicorn output stream
logger = logging.getLogger("uvicorn.error")
logging.basicConfig(level=logging.INFO)


class SimilarTracks():
    """Class for displaying online recommendations."""
    def __init__(self) -> None:
        """Initializes a class instance."""
        self._similar_tracks = None

    def load(self, path: str, **kwargs):
        """Loads online recommendatiions."""
        logger.info("Loading similarity data")
        self._similar_tracks = pd.read_parquet(path, **kwargs)
        self._similar_tracks = self._similar_tracks.set_index("track_id_1")
        logger.info("Loaded similarity data")

    def get(self, track_id: int, k: int = 10):
        """Retrieves first k online recommendations."""
        try:
            i2i = self._similar_tracks.loc[track_id].head(k)
            i2i = i2i[["track_id_2", "score"]].to_dict(orient="list")
        except KeyError:
            logger.error("No recommendations found")
            i2i = {"track_id_2": [], "score": []}
        
        return i2i


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Loads data on application start-up."""
    sim_items_store = SimilarTracks()
    sim_items_store.load(path="data/similar.parquet")
    logger.info("Ready for online recommendations")

    yield {"sim_items_store": sim_items_store}


# Creating an app
app = FastAPI(title="features", lifespan=lifespan)

# Adding an endpoint for online recommendations
@app.post("/similar_tracks")
async def similar_tracks(request: Request, track_id: int, k: int):
    """Generates online recommendations."""
    # Getting an object with loaded data
    sim_items_store = request.state.sim_items_store
    # Getting recommendations
    i2i = sim_items_store.get(track_id, k)

    return i2i