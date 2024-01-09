from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from urllib.parse import urlencode

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    base_url = 'http://127.0.0.1:8000/api/timeline/'

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data
        })

    def get_next_link(self):
        if not self.page.has_next():
            return None
        page_number = self.page.next_page_number()
        url = f"{self.base_url}?{urlencode({self.page_query_param: page_number})}"
        return url

    def get_previous_link(self):
        if not self.page.has_previous():
            return None
        page_number = self.page.previous_page_number()
        url = f"{self.base_url}?{urlencode({self.page_query_param: page_number})}"
        return url
