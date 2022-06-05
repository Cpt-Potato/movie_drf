from django_filters import rest_framework as filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from movies.models import Movie


def get_client_ip(request):
    """Получение IP пользователя"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class MovieFilter(filters.FilterSet):
    genres = CharFilterInFilter(field_name='genres__name', lookup_expr='in')
    years = filters.RangeFilter()

    class Meta:
        model = Movie
        fields = ['genres', 'years']


class PaginationMovie(PageNumberPagination):
    page_size = 1
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })
