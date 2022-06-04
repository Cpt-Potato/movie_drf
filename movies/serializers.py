from rest_framework import serializers

from .models import Movie, Review, Rating, Actor


class FilterReviewListSerializer(serializers.ListSerializer):
    """Фильтр только родительских комментариев"""

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Рекурсивный вывод children"""

    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(instance, context=self.context)
        return serializer.data


class ActorDirectorListSerializer(serializers.ModelSerializer):
    """Список актёров и режиссёров"""

    class Meta:
        model = Actor
        fields = ('id', 'name', 'image')


class ActorDirectorDetailSerializer(serializers.ModelSerializer):
    """Полное описание актёра или режиссёра"""

    class Meta:
        model = Actor
        fields = '__all__'


class MovieListSerializer(serializers.ModelSerializer):
    """Список фильмов"""
    user_rating = serializers.BooleanField()
    avg_rating = serializers.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        model = Movie
        fields = ('title', 'tagline', 'category', 'user_rating', 'avg_rating')


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Добавление отзыва"""

    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    """Вывод отзывов"""
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ('name', 'text', 'children')


class MovieDetailSerializer(serializers.ModelSerializer):
    """Полная информация о фильме"""
    category = serializers.SlugRelatedField(slug_field='name', read_only=True)
    directors = ActorDirectorListSerializer(read_only=True, many=True)
    actors = ActorDirectorListSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)


class CreateRatingSerializer(serializers.ModelSerializer):
    """Добавление рейтинга к фильму"""

    class Meta:
        model = Rating
        fields = ('star', 'movie')

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip'),
            movie=validated_data.get('movie'),
            defaults={'star': validated_data.get('star')}
        )
        return rating
