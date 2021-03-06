# General idea
* You know the song title.
* You like the song.
* You like to get similar songs.

# How to use recommender project 
1. Go to project main folder `Collaborative Filtering`.
2. `docker-compose build` to build the image of the web app.
3`docker-compose up` to start the containers running locally.
3. Web app available at: 
   * http://localhost:8000/
   * API documentation: http://localhost:8000/docs
4. `docker-compose down` to stop the containers.
5. In web browser go to `http://localhost:8000/recommend/{song_name}` where `{song_name}` is a name of a song you want recommendation for.

## Important!
In current version you can find recommendation only for songs that already on the list of songs in .xlsx data file.
You can find list of songs in file `Data_InCarMusic.xlsx` on the sheet `Music Track`.

# Run tests
1. Go to project main folder `Collaborative Filtering`.
2. Run command `pipenv sync` to synchronise virtual environment with `Pipfile`.
3. Run command `pipenv run pytest`.

# Project file structure
Project structure:
* documentation - containing project documentation 
* src/data - data we will use to train model
* src/model - logic behind creating and training machine learning model
* src/tests - additional tests
* src/main.py - code of the working application that using trained ML model

# Project documentation
After starting service you can find user project documentation under the links:
http://localhost:8000/docs

You can find project requirements documentation in project folder `documentation`.

# Inspiration and credits
Huge inspiration was work of [Eugenia Inzaugarat](https://github.com/ugis22).
In the solution I used and changed part of her code from:
https://github.com/ugis22/music_recommender/tree/master/collaborative_recommender_system