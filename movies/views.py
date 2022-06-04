from django.db import models
from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor
from .serializers import (
    MovieDetailSerializer,
    MovieListSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorDirectorListSerializer,
    ActorDirectorDetailSerializer
)
from .services import get_client_ip, MovieFilter


class MovieListView(generics.ListAPIView):
    """Вывод списка фильмов"""
    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            user_rating=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(avg_rating=models.Avg('ratings__star'))
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    """Вывод полной информации о фильме"""
    serializer_class = MovieDetailSerializer
    queryset = Movie.objects.filter(draft=False)


class ReviewCreateView(generics.CreateAPIView):
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializer


class AddStarRatingView(generics.CreateAPIView):
    """Добавление рейтинга к фильму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsDirectorsListView(generics.ListAPIView):
    """Вывод списка актёров и режиссёров"""
    queryset = Actor.objects.all()
    serializer_class = ActorDirectorListSerializer


class ActorsDirectorsDetailView(generics.RetrieveAPIView):
    """Вывод информации об актёре или режиссёре"""
    queryset = Actor.objects.all()
    serializer_class = ActorDirectorDetailSerializer
