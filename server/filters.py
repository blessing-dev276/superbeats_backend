from rest_framework.filters import SearchFilter


class DynamicSearchFilters(SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist("search_fields", getattr(view, "search_fields", []))
