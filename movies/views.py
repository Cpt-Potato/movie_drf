from django.db import models
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie
from .serializers import MovieDetailSerializer, MovieListSerializer, ReviewCreateSerializer, CreateRatingSerializer
from .services import get_client_ip


class MovieListView(APIView):
    """Вывод списка фильмов"""

    def get(self, request):
        movies = Movie.objects.filter(draft=False).annotate(
            user_rating=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(request)))
        ).annotate(
            avg_rating=models.Avg('ratings__star')
        )
        serializer = MovieListSerializer(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    """Вывод полной информации о фильме"""

    def get(self, request, pk):
        movie = Movie.objects.get(pk=pk, draft=False)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)


class ReviewCreateView(APIView):
    """Добавление отзыва к фильму"""

    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class AddStarRatingView(APIView):
    """Добавление рейтинга к фильму"""

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        return Response(status=400)
