# External libraries
from fastapi import FastAPI
from loguru import logger

# Internal libraries
import model
from data import load_data
from model.recommender import prepare_model


def create_model() -> model.recommender.Recommender:
    """
    Create recommendation model.

    :return model.recommender.Recommender: recommendation model.
    """
    logger.debug("Preparing the data...")
    # TODO: Nice to have: passing name of the xlsx file and rest of the data
    rating, songs = load_data.run("data", "Data_InCarMusic.xlsx")

    logger.debug("Preparing data matrix...")
    recommender_model = prepare_model(rating, songs)

    return recommender_model


# create global model only once
recommendation_model = create_model()
app = FastAPI()


@app.get("/")
def get_root() -> dict:
    return {"STATUS": "Klinesso Recommender API"}


@app.get("/recommend/{song_name}")
def recommend(song_name: str, number_of_recommendations: int = 5) -> dict:
    """
    Get the list of recommended songs based on passed song title from the list of existing song titles.

    :param (str) song_name: name of the song on which we base recommendations.
    :param (int) number_of_recommendations: number of recommendations we want to have.

    :return dict: dict with list of recommendations based on passed song.
    """
    recommendations = recommendation_model.make_recommendation(
        new_song=song_name,
        n_recommendations=number_of_recommendations
    )

    return {"Recommendations": recommendations}
