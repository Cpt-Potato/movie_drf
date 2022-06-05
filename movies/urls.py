from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = format_suffix_patterns([
    path('movies/', views.MovieViewSet.as_view({'get': 'list'})),
    path('movies/<int:pk>/', views.MovieViewSet.as_view({'get': 'retrieve'})),
    path('reviews/', views.ReviewCreateViewSet.as_view({'post': 'create'})),
    path('ratings/', views.AddStarRatingViewSet.as_view({'post': 'create'})),
    path('actors/', views.ActorsViewSet.as_view({'get': 'list'})),
    path('actors/<int:pk>/', views.ActorsViewSet.as_view({'get': 'retrieve'})),
])

# urlpatterns = [
#     path('movies/', views.MovieListView.as_view()),
#     path('movies/<int:pk>/', views.MovieDetailView.as_view()),
#     path('reviews/', views.ReviewCreateView.as_view()),
#     path('ratings/', views.AddStarRatingView.as_view()),
#     path('actors/', views.ActorsDirectorsListView.as_view()),
#     path('actors/<int:pk>/', views.ActorsDirectorsDetailView.as_view()),
# ]
