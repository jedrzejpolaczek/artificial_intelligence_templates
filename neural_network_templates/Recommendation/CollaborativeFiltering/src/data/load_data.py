# External libraries
import pandas

from loguru import logger
from pandas.core.frame import DataFrame


def convert_xlsx_to_csv(source_file: str, sheet_name: str, csv_name: str) -> None:
    """
    Create csv file from converting sheet from xlsx file.

    :param (str) source_file: path to the source xlsx file.
    :param (str) sheet_name : name of the excel sheet we want convert to csv file.
    :param (str) csv_name: name of csv that will be created.
    """
    contextual_rating = pandas.read_excel(source_file, sheet_name, index_col=None)
    contextual_rating.to_csv(csv_name, index=None)


def run(base_path: str, excel_name: str) -> (DataFrame, DataFrame):
    """
    Load input data of user contextual rating and songs from xlsx file.

    :param (str) base_path : path to data.
    :param (str) excel_name: name of excel file.

    :return (pandas.core.frame.DataFrame, pandas.core.frame.DataFrame): dataframe of user contextual rating and songs.
    """
    contextual_rating_csv_name = "Data_InCarMusic_ContextualRating.csv"
    music_track_csv_name = "Data_InCarMusic_MusicTrack.csv"

    # logger.info("Downloading xlsx data...")
    # TODO: Nice to have: downloading and extracting zip xlsx file

    logger.debug("Creating csv files from xlsx...")
    convert_xlsx_to_csv(f"{base_path}/{excel_name}", "ContextualRating", f"{base_path}/{contextual_rating_csv_name}")
    convert_xlsx_to_csv(f"{base_path}/{excel_name}", "Music Track", f"{base_path}/{music_track_csv_name}")

    logger.debug("Loading csv data to memory as dataframes...")
    user_contextual_rating = pandas.read_csv(f"{base_path}/{contextual_rating_csv_name}", delimiter=",")
    songs = pandas.read_csv(f"{base_path}/{music_track_csv_name}", delimiter=",")

    user_contextual_rating = user_contextual_rating.rename(columns={" Rating": "Rating"})
    songs = songs.rename(columns={" title": "title"})

    return user_contextual_rating, songs
