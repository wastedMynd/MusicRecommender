from recommender.api import Recommender
import os
from artist import get_artist_genres, get_common_genre

# This is a Music Recommender Python script.

# Press Shift+F10 to execute it.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

client_id = os.environ.get("CLIENT_ID")
client_secret =  os.environ.get("CLIENT_SECRET")


env_path = os.environ.get("MP3JUICES_DOWNLOAD_PATH")
base_path = os.path.join(os.environ.get("HOME"), "Downloads/mp3juices")
download_dir = base_path if env_path is None else env_path
query_path = os.path.join(download_dir, "query.txt")


def recommend(artist_like):

    recommender = Recommender(client_id=client_id, client_secret=client_secret)
    recommender.artists = artist_like
    recommender.track_attributes = {
        'danceability': 1.0
    }

    try:

        recommendations = recommender.find_recommendations()



        artists: list = []

        for recommendation in recommendations['tracks']:
            

            artist = recommendation["artists"][0]["name"]
            artist_id = recommendation["artists"][0]["id"]
            song = recommendation["name"]
            popularity = recommendation["popularity"]

            if any((artist.strip() == artist_like.strip()), (artist.strip() in artists)):
                continue

            artists.append(
                {
                    "id": artist_id,
                    "name": artist,
                    "song": song,
                    "popularity": popularity,
                }
            )

    
        return artists

    except Exception as e:
        return []


def mp3juices_query_reader() -> list:
    with open(query_path, "r") as reader:
        lines = reader.readlines()
    query_artists: list = []
    for line in lines:
        if (skip_line_comment:=line.startswith("#")) or (present := line in query_artists):
            continue
        query_artists.append(line)
    return query_artists


def get_new_recommendations():
    present_mp3juices_queries = mp3juices_query_reader()
    new_recommendations: list = []

    for mp3juices_query in present_mp3juices_queries:

        try:
            recommendations = recommend(mp3juices_query)
        except Exception:
            continue

        for recommendation in recommendations:
            found = False
            for new_recommendation in new_recommendations:

                recommendation_name = recommendation.get("name").strip()
                new_recommendation_name = new_recommendation.get("name").strip()
                
                if recommendation_name == new_recommendation_name:
                    found = True
                    break
                
                if recommendation_name == mp3juices_query.strip():
                    found = True
                    break

            if found:
                continue

            new_recommendations.append(recommendation)

    return new_recommendations


def append_new_recommendations():
    print("Started recommendations...")

    if  (recommendation_count := len(new_recommendations := get_new_recommendations())) == 0:
        print('sorry... no new recommendation(s) found!')
        return

    print(f"found {recommendation_count} recommendation(s).")


    with open(query_path, "a") as appender:
        
        print('writing to query.txt')
    
        for recommendation in new_recommendations:

            artist = recommendation.get("name")
            artist_id = recommendation.get("id")
            genre = ""

            try:
                genre = get_common_genre(get_artist_genres(artist_id=artist_id))
            finally:
                if genre:
                    appender.write(f"#@ {genre}\n")
                    appender.write(f"{artist}\n")
                    appender.write("##\n")
                else:
                    appender.write(f"{artist}\n")
        
        print("done")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    append_new_recommendations()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
