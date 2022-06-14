def get_favorite_genres(collections):
    all_genres = []
    for collection in collections:
        for movie in collection.movies.all():
            all_genres.extend(movie.genres.split(','))

    freq = {}
    for genre in set(all_genres):
        freq[genre] = all_genres.count(genre)

    print(freq)
