# External libraries
import pandas

from fuzzywuzzy import fuzz
from loguru import logger
from pandas.core.frame import DataFrame
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors


class Recommender:
    """
    Object for collaborative recommender that use knn algorithm.
    """
    def __init__(self, metric, algorithm, k, data, decode_id_song):
        self.metric = metric
        self.algorithm = algorithm
        self.k = k
        self.data = data
        self.decode_id_song = decode_id_song
        self.data = data
        self.model = self._recommender().fit(data)

    def make_recommendation(self, new_song: str, n_recommendations: int) -> list:
        """
        Make list of recommended songs based on passed song title.

        :param (str) new_song: name of the song on which we base recommendations.
        :param (int) n_recommendations: number of recommendations we want to have

        :return list: list of recommendations based on passed song.
        """
        recommended = self._recommend(new_song=new_song, n_recommendations=n_recommendations)
        logger.debug("Recommendation process status: DONE")

        return recommended

    def _recommender(self) -> NearestNeighbors:
        """
        Get recommender model based on nearest neighbors architecture.

        :return sklearn.neighbors._unsupervised.NearestNeighbors: nearest neighbors model.
        """
        return NearestNeighbors(metric=self.metric, algorithm=self.algorithm, n_neighbors=self.k, n_jobs=-1)

    def _recommend(self, new_song: str, n_recommendations: int) -> list:
        """
        Create list of recommended songs based on passed song title.

        :param (str) new_song: name of the song on which we base recommendations.
        :param (int) n_recommendations: number of recommendations we want to have

        :return list: list of recommendations based on passed song.
        """
        logger.debug("Getting the ID of the recommended songs...")
        recommendations = []
        recommendation_ids = self._get_recommendations(new_song=new_song, n_recommendations=n_recommendations)

        logger.debug("Getting the name of the song using a mapping dictionary...")
        recommendations_map = self._map_indeces_to_song_title()

        logger.debug("Translating this recommendations into the ranking of song titles recommended...")
        for i, (idx, dist) in enumerate(recommendation_ids):
            recommendations.append(recommendations_map[idx])

        return recommendations

    def _get_recommendations(self, new_song: str, n_recommendations: int) -> list:
        """
        Get the list of recommended songs based on passed song title.

        :param (str) new_song: name of the song on which we base recommendations.
        :param (int) n_recommendations: number of recommendations we want to have.

        :return list: list of recommendations based on passed song.
        """
        logger.debug("Getting the ID of the song according to the passed string...")
        recommendation_song_id = self._fuzzy_matching(song=new_song)

        logger.debug(f"Starting the recommendation process for {new_song} ...")
        distances, indices = self.model.kneighbors(self.data[recommendation_song_id], n_neighbors=n_recommendations + 1)

        return sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), key=lambda x: x[1])[:0:-1]

    def _map_indeces_to_song_title(self) -> dict:
        """
        Map songs IDs to songs titles.

        :return dict: map of the song IDs to songs titles.
        """
        logger.debug("Getting reverse mapper...")
        return {song_id: song_title for song_title, song_id in self.decode_id_song.items()}

    def _fuzzy_matching(self, song: str) -> int:
        """
        Match passed song with ID in database.

        :param (str) song: name of the song we want to match.

        :return int: id of the matched song.
        """
        match_tuple = []

        logger.debug("Getting match...")
        for title, idx in self.decode_id_song.items():
            match_tuple.append((title, idx, ratio))

        logger.debug("Sorting results...")
        match_tuple = sorted(match_tuple, key=lambda x: x[2])[::-1]
        if not match_tuple:
            logger.warning(f"The recommendation system could not find a match for {song}")
            return

        return match_tuple[0][1]


def prepare_model(rating, songs) -> Recommender:
    """
    Prepare recommendation model ready to create recommendation based on song name.

    :param (DataFrame) rating: data with user id, song id and rating of songs made by users.
    :param (DataFrame) songs: data of the songs.

    :return Recommender:
    """
    logger.debug("Converting the dataframe into a pivot table...")
    songs_features = pandas.pivot_table(rating, index='ItemID', columns='UserID', values='Rating').fillna(0)

    logger.debug("Obtaining a sparse matrix...")
    songs_features_matrix = csr_matrix(songs_features.values)

    logger.debug("Creating the model...")
    decode_id_song = {
        song: i for i, song in
        enumerate(list(songs.set_index('id').loc[songs_features.index].title))
    }
    model = Recommender(
        metric='cosine',
        algorithm='brute',
        k=20,
        data=songs_features_matrix,
        decode_id_song=decode_id_song
    )

    return model
