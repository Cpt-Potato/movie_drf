from django.db import models
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

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


class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод списка фильмов"""
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            user_rating=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(avg_rating=models.Avg('ratings__star'))
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            return MovieListSerializer
        elif self.action == 'retrieve':
            return MovieDetailSerializer


class ReviewCreateViewSet(viewsets.ModelViewSet):
    """Добавление отзыва к фильму"""
    serializer_class = ReviewCreateSerializer


class AddStarRatingViewSet(viewsets.ModelViewSet):
    """Добавление рейтинга к фильму"""
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsViewSet(viewsets.ReadOnlyModelViewSet):
    """Вывод списка актёров и режиссёров"""
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorDirectorListSerializer
        elif self.action == "retrieve":
            return ActorDirectorDetailSerializer

# class MovieListView(generics.ListAPIView):
#     """Вывод списка фильмов"""
#     serializer_class = MovieListSerializer
#     filter_backends = (DjangoFilterBackend,)
#     filterset_class = MovieFilter
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get_queryset(self):
#         movies = Movie.objects.filter(draft=False).annotate(
#             user_rating=models.Count('ratings', filter=models.Q(ratings__ip=get_client_ip(self.request)))
#         ).annotate(avg_rating=models.Avg('ratings__star'))
#         return movies
#
#
# class MovieDetailView(generics.RetrieveAPIView):
#     """Вывод полной информации о фильме"""
#     queryset = Movie.objects.filter(draft=False)
#     serializer_class = MovieDetailSerializer
#
#
# class ReviewCreateView(generics.CreateAPIView):
#     """Добавление отзыва к фильму"""
#     serializer_class = ReviewCreateSerializer
#
#
# class AddStarRatingView(generics.CreateAPIView):
#     """Добавление рейтинга к фильму"""
#     serializer_class = CreateRatingSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(ip=get_client_ip(self.request))
#
#
# class ActorsDirectorsListView(generics.ListAPIView):
#     """Вывод списка актёров и режиссёров"""
#     queryset = Actor.objects.all()
#     serializer_class = ActorDirectorListSerializer
#
#
# class ActorsDirectorsDetailView(generics.RetrieveAPIView):
#     """Вывод информации об актёре или режиссёре"""
#     queryset = Actor.objects.all()
#     serializer_class = ActorDirectorDetailSerializer
