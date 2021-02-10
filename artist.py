import requests

auth = 'BQDFor9bIBD-ugP3Ma2qnpYWeb1wvgWHIUc1FEqNf4R1XQu5URXkjadpXgjJJeLBYnSeUvL2gDwHwUVvl7EMWsfmkZOpXMmjiHBP9mbzZdMStnBvM_5ZPP9Ms27gMrblNrGYKRkxIAw0x7tIsXlXp2sS3uUuimS53PH7Aum-W4WlF4dajee5OsGnZkxrV5gPTrQgMmIilVDgHiAEz6ZvehP4YzR-T5sB_s29mewsxxS9zN-BMZlxUx9lHg0NR_r8gCgkzTlYjTtWL6wjONiDS5DzujKR'

base_url = 'https://api.spotify.com/v1/'

artists_url = base_url + 'artists'

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {auth}'
}


def get_artist_genres(artist_id):
    params = (('ids', f'{artist_id}'),)

    genres: list = []

    with requests.get(artists_url, headers=headers, params=params) as response:
        if not response.ok:
            return genres

        json_response = response.json()
        genres = json_response.get('artists')[0].get('genres')

    return genres


def get_common_genre(genres: list):
    try:
        previous_genre: str = genres[0]
        common_genre: str = ''

        for index in range(1, len(genres) - 1):

            genre_1 = previous_genre.split(" ")
            genre_2 = genres[index].lower().split(" ")

            common_word_index = len(list(set(genre_1) & set(genre_2)))

            if common_word_index > 0:
                common_genre = genre_1[common_word_index]
                break

        print(f"common genre is : {common_genre}")
    except Exception as e:
        return ""    

if __name__ == '__main__':
    get_common_genre(get_artist_genres('0oSGxfWSnnOXhD2fKuz2Gy'))
