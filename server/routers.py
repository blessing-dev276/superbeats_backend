from rest_framework.routers import SimpleRouter, Route


class CustomRouter(SimpleRouter):
    routes = [
        Route(
            detail=False,
            initkwargs={},
            name="{basename}-url",
            url=r"^{prefix}{trailing_slash}$",
            mapping={
                "put": "update",
                "post": "create",
                "get": "retrieve",
                "delete": "destroy",
                "patch": "partial_update",
            },
        )
    ]

    def get_routes(self, viewset):
        return self.routes
