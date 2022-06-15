def get_favorite_genres(collections):
    all_genres = []
    for collection in collections:
        for movie in collection.movies.all():
            all_genres.extend(movie.genres.split(','))

    freq = [(genre, all_genres.count(genre)) for genre in set(all_genres)]
    freq = list(sorted(freq, key=lambda x: x[1], reverse=True))[:3]
    return list(map(lambda x: x[0], freq))
