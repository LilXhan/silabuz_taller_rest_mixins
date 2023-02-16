from rest_framework.routers import Route, SimpleRouter

class CustomRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}$',
            mapping={'get': 'list'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'} 
        ),
        Route(
            url=r'^{prefix}/{lookup}/$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'} 
        ),
        Route(
            url=r'^{prefix}/add/$',
            mapping={'post': 'create'},
            name='{basename}-post',
            detail=False,
            initkwargs={'suffix': 'Create'}
        ),
        Route(
            url=r'^{prefix}/{lookup}/update/$',
            mapping={'put': 'update'},
            name='{basename}-update',
            detail=False,
            initkwargs={'suffix': 'Update'}
        )
    ]