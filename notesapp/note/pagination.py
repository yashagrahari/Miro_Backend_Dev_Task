
from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10  # Set the desired page size
    page_size_query_param = 'page_size'
    max_page_size = 100