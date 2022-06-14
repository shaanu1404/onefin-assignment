from rest_framework import serializers
from .models import Collection, Movie


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = "__all__"


class CollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Collection
        fields = ('uuid', 'title', 'description')


class CreateCollectionSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True)

    class Meta:
        model = Collection
        fields = ('title', 'description', 'movies')

    def create(self, validated_data):
        user = self.context.get('user')
        collection = Collection.objects.create(
            title=validated_data.get('title'),
            description=validated_data.get('description'),
            user=user
        )
        movies = validated_data.get('movies')
        added_movies = []
        for movie in movies:
            new_movie, _ = Movie.objects.get_or_create(**movie)
            added_movies.append(new_movie)
        collection.movies.set(added_movies)
        return collection
