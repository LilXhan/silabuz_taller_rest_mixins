# Taller

Para recordar que todo este proyecto se está trabajando en el siguiente [repositorio](https://github.com/silabuzinc/DRF)

## Funcionamiento y tipos de router

DRF ofrece soporte para el routing automático para Django, con una forma simple, rápida y consistente forma de conectar nuestra lógica de las vistas en un conjunto de URL's.

Anteriormente ya lo hemos utilizado por ejemplo:

```py
router = routers.DefaultRouter()

router.register('api/v3/todo', TodoViewSetCustom, 'todosCustom')
router.register('api/v4/todo', TodoViewSet, 'todos')
```

Para recordar, las partes que contiene el registro de un router son:

-   `prefix`: URL del prefijo usado para nuestro conjunto de vistas.
    
-   `viewset`: Clase de un viewset.
    

Opcionalmente, podemos especificar un argumento adicional

-   `basename`: La base a usar en el nombre de la URL que es creada. Si no se especifica este nombre se basa en el queryset.

Normalmente no se tiene que especificar el `basename`, pero si tenemos un `viewset` donde hemos definido un custom `get_queryset`(método), si no existe un atributo `.queryset` definido. Obtendríamos un error similar a este:

```shell
'basename' argument not specified, and could not automatically determine the name from the viewset, as it does not have a '.queryset' attribute.
```

Eso indica que se necesita especificar explícitamente el parámetro `basename` dentro del registro del viewset.

### SimpleRouter vs DefaultRouter

`SimpleRouter` incluye rutas para el conjunto estándar de `list`, `create`, `retrieve`, `update`, `partial_update` y `destroy`. Adicionalmente podemos añadir métodos que pueden ser añadidos a las rutas mediante el decorador `@action`.

Por otro lado, `DefaultRouter` es similar a `SimpleRouter`, pero adicionalmente incluye un `API root view`, que retorna un response que contiene los hyperlinks hacia la lista de todas las vistas. Asimismo, genera rutas para sufijos de formato de estilo `.json` opcionales.

## Creación de un router

Dentro de DRF, también podemos crear nuestros propios routers, basados en el `SimpleRouter`.

Para esto, vamos a crear una nueva aplicación que va contener el CRUD de usuarios

### Preparando la aplicación

Primero creamos la aplicación

```shell
python manage.py startapp users
```

Añadimos la aplicación en `settings.py`.

```py
INSTALLED_APPS = [
    # ...
    'users',
]
```

Creamos el modelo `users` y lo migramos.

```py
class Users(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    realname = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
```

```shell
python manage.py makemigrations users

python manage.py migrate
```

Estructuramos nuestra aplicación añadiendo los siguientes archivos:

-   `api.py`
    
-   `urls.py`
    
-   `serializers.py`
    

Luego de haber creado nuestra aplicación vamos a crear un serializador simple y el viewset a utilizar.

-   Creación del serializador
    
    ```py
    from rest_framework import serializers
    from .models import Users
    
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = Users
            fields = '__all__'
            read_only_fields = 'created_at',
    ```
    
-   Creación del viewset
    
    ```py
    from .models import Users
    from rest_framework import viewsets
    from .serializers import UserSerializer
    
    class UserViewSet(viewsets.ModelViewSet):
        serializer_class = UserSerializer
        queryset = Users.objects.all()
    ```
    

Ahora que ya tenemos todo creado, para probar que funciona correctamente vamos a hacer uso del `DefaultRouter` para comprobar el funcionamiento de todo lo que hemos creado.

-   Dentro de `urls.py` añadimos lo siguiente:
    
    ```py
    from rest_framework import routers
    from .api import UserViewSet
    from django.urls import path
    
    router = routers.DefaultRouter()
    
    router.register('api/v1/users', UserViewSet, 'users')
    urlpatterns = router.urls
    ```
    
-   Ahora dentro de las urls de la carpeta principal, incluimos nuestras rutas dentro de la aplicación de DRF.
    
    ```py
    urlpatterns = [
        # ...
        path('users/', include('users.urls')),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    ```
    

Si probamos la ruta en `http://127.0.0.1:8000/users/`, deberíamos obtener la siguiente respuesta.

![User Root](https://photos.silabuz.com/uploads/big/e2a1490b757cdad382f8fe5f8f2fed22.PNG)

Y si accedemos al link que nos muestra, deberíamos obtener el CRUD de nuestro ViewSet.

![CRUD User](https://photos.silabuz.com/uploads/big/e4a5c84940e69df7110d51034af637d2.PNG)

### Creando nuestro router

Ahora que ya vemos que funciona correctamente, podemos empezar a crear nuestro propio router.

Cabe recordar que para nuestro router utilizaremos los siguientes conceptos:

-   `url`
    
    1.  `{prefix}`: El prefijo de la URL a usar en el conjunto de rutas.
        
    2.  `{lookup}`: El campo de búsqueda usado para hacer match en con una sola instancia.
        
    3.  `{trailing_slash}`: Ya sea un '/' o una cadena vacía, según el argumento barra diagonal final.
        
-   `mapping`: Un mapping de los métodos HTTP nombrados en los métodos de nuestras vistas.
    
-   `name`: El nombre de las URL es usado en las llamadas `reverse`. Puede incluir el siguiente formato de la cadena.
    
    1.  `{basename}`: La base a usar en el nombre de la URL que es creada. Si no se especifica este nombre se basa en el queryset.
-   `initkwargs`: Un diccionario de cualquier argumento adicional que se deba pasar al instanciar la vista.
    

Creamos un archivo `routers.py` dentro de nuestra app, y agregamos lo siguiente:

```py
from rest_framework.routers import Route, DynamicRoute, SimpleRouter

class CustomRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}$',
            mapping={'get': 'get'},
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
        Route(
            url=r'^{prefix}/{lookup}$',
            mapping={'get': 'retrieve'},
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Detail'}
        ),
    ]
```

En este caso, las rutas añadidas son las siguientes:

| URL        | HTTP Method           | Action  | URL Name |
| ------------- |:-------------:| -----:| ---------: |
| /users      | GET | list | user-list |
| /users/{username}      | GET      |   retrieve | user-detail|


## Mixins

¿Qué son los mixins? Un mixin permite extender la funcionalidad de nuestra clase principal, pero ¿cómo podemos aplicarlo a nuestro proyecto?

Dentro de nuestras rutas únicamente tenemos implementados dos métodos: List y Retrieve.

Por lo cual, los demás métodos están sin tener un uso. Entonces, crearemos una vista con mixins que solo admita los métodos que disponemos en nuestro router.

Mixins a usar:

-   `ListModelMixin`: Lista un queryset
    
-   `RetrieveModelMixin`: Retorna la instancia de un modelo.
    

Además, para poder hacer uso de nuestro router necesitamos hacer uso de `viewsets.GenericViewSet`.

```py
from .models import Users
from rest_framework import viewsets
from .serializers import UserSerializer
from rest_framework import mixins

class UserViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = UserSerializer
    queryset = Users.objects.all()

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
```

```py
from .models import Users
from rest_framework import viewsets
from .serializers import UserSerializer
from rest_framework import mixins

class UserViewSetOne(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = UserSerializer
    queryset = Users.objects.all()
    lookup_field = "username"

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
```

Para todos los casos usamos `super()` para hacer referencia a nuestro mixin. Por otro lado, lo separamos en dos vista para que no exista conflicto al momento de querer hacer uso de un solo registro o de todo el conjunto.

Ahora que tenemos nuestro ViewSet con Mixins, podemos modificar nuestras rutas.

```py
# ...
from .api import UserViewSet, UserViewSetOne
# ...
router.register('', UserViewSet, 'users')
router.register('', UserViewSetOne, 'oneUser')
# ...
```

¡Tenemos implementado un ViewSet con mixins!

## Versionamiento de API

Ahora, podemos comenzar a versionar nuestra aplicación de TODO's. Por lo que, necesitamos crear una nueva aplicación para trasladas todas nuestras rutas versionadas. Si recordamos, nuestro versionamiento lo manejamos dentro de las url pero DRF nos ofrece otra forma de hacerlo.

Primero, creamos nuestra nueva app.

```shell
python manage.py startapp versionedTodo
```

Ahora que tenemos nuestra aplicación, vamos a utilizar la siguiente estructura como plantilla para versionar nuestra aplicación:

Recordar que estamos haciendo uso de este [repositorio](https://github.com/silabuzinc/DRF)

```sample
DRF/
├── drfcrud
│   └── archivos del proyecto principal (DRF)
├── users
│   └── archivos del app users
├── todos
│   ├── init.py
│   ├── routers.py
|   |── api.py
│   ├── serializers.py
│   ├── pagination.py
│   └── demás archivos de la aplicación que no se van a versionar
├── init.py
└── versionedTodo
    ├── init.py
    ├── v3
    │   ├── init.py
    │   ├── router.py
    |   ├── api.py
    │   ├── serializers.py
    │   └── pagination.py
    └── v4
        ├── init.py
        ├── router.py
        ├── api.py
        ├── serializers.py
        └── pagination.py
```

Entonces, con este ejemplo podemos manejar el versionamiento de dicha forma.

Vamos a crear la v3 y v4 de nuestro proyecto dentro de esta aplicación, por lo que crearemos ambas carpeta que deben contener lo siguiente:

1.  `api.py`
    
2.  `pagination.py`
    
3.  `router.py`
    
4.  `serializer.py`
    

En v3 añadimos las siguientes líneas.

1.  `api.py`
    
    ```py
    from todos.models import Todo
    from rest_framework import viewsets
    from .serializers import TodoSerializer
    from rest_framework import status
    from rest_framework.response import Response
    from django.shortcuts import get_object_or_404
    from .pagination import StandardResultsSetPagination
    from rest_framework import viewsets, filters 
    
    class TodoViewSetCustom(viewsets.ModelViewSet):
        queryset = Todo.objects.all()
        pagination_class = StandardResultsSetPagination
    
        def get_serializer_class(self):
            return TodoSerializer
    
        def list(self, request):
            page = self.paginate_queryset(self.queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
    
            serializer = self.get_serializer(self.queryset, many=True)
            return Response(serializer.data)
    
        def create(self, request):
            if isinstance(request.data, list):
                serializer = TodoSerializer(data=request.data, many = True)
            else:
                serializer = TodoSerializer(data=request.data)
    
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        def retrieve(self, request, pk=None):
            todo = get_object_or_404(self.queryset, pk=pk)
            serializer = TodoSerializer(todo)
            return Response(serializer.data)
    
        def update(self, request, pk=None):
            todo = get_object_or_404(self.queryset, pk=pk)
            serializer = TodoSerializer(todo, data=request.data)
    
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
    
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        def partial_update(self, request, pk=None):
            todo = get_object_or_404(self.queryset, pk=pk)
            serializer = TodoSerializer(todo, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
        def destroy(self, request, pk=None):
            todo = get_object_or_404(self.queryset, pk=pk)
            todo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    ```
    
2.  `pagination.py`
    
    ```py
    from rest_framework.pagination import PageNumberPagination
    
    class StandardResultsSetPagination(PageNumberPagination):
        page_size = 20
        page_size_query_param = 'page_size'
        max_page_size = 1000
    ```
    
3.  `router.py`
    
    ```py
    from . import api
    from rest_framework import routers
    
    router = routers.DefaultRouter()
    router.register(r'todo', api.TodoViewSetCustom, 'todosCustom')
    
    api_urlpatterns = router.urls
    ```
    
4.  `serializer.py`
    

```py
from rest_framework import serializers
from todos.models import Todo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'
        read_only_fields = 'created_at', 'done_at', 'updated_at', 'deleted_at'
```

Para la v4, el único archivo a cambiar es `api,py`, los demás se mantienen como la versión anterior.

1.  `api.py`
    
    ```py
    from todos.models import Todo
    from .serializers import TodoSerializer
    from rest_framework import status
    from rest_framework.response import Response
    from .pagination import StandardResultsSetPagination
    from rest_framework import viewsets, filters 
    
    class TodoViewSet(viewsets.ModelViewSet):
        queryset = Todo.objects.all()
        serializer_class = TodoSerializer
        pagination_class = StandardResultsSetPagination
        filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
        search_fields = ['title', 'body']
        ordering = ('-id')
    ```
    

Ahora que ya tenemos creadas nuestras versiones, necesitamos agregarlas a las rutas.

Dentro de `todos/urls.py` añadimos lo siguiente.

```py
# ...
from django.urls import re_path, include
from versionedTodo.v3.router import api_urlpatterns as api_v3
from versionedTodo.v4.router import api_urlpatterns as api_v4

# ....

urlpatterns = [
    # ...
    re_path(r'^api/v3/', include(api_v3)),
    re_path(r'^api/v4/', include(api_v4)),
]
```

Ahora que ya tenemos registradas nuestras versiones al acceder a las rutas definidas podremos ver lo registrado por el router de cada versión.

Probar las rutas

-   `http://127.0.0.1:8000/api/v3/todo/?search=5`
    
-   `http://127.0.0.1:8000/api/v4/todo/?search=5`
    

Una ruta da respuesta y la otra no.

## Tarea

-   Implementar métodos PUT y POST dentro de:
    
    1.  Router customizado
        
    2.  Mixin de genericviewset
        
    
    Luego de haber implementado ambas rutas y métodos, realizar el ingreso de 5 usuarios.
    
-   Realizar el versionamiento de su proyecto.
    

## Tarea opcional

Crear dos mixin sin hacer uso de Django.

Las clases deben contener lo siguiente.

-   Clase persona(base):
    
    El constructor debe inicializar el nombre
    
-   Clase DictMixin:
    
    Esta clase debe tener el método `to_dict` que convierta todos los atributos de la clase que lo usa a un diccionario.
    
-   Clase JsonMixin:
    
    Esta clase debe tener el método `to_json` que convierta todos los atributos de la clase que lo usa a un json.
    
-   Clase Empleado:
    
    La clase empleado hace uso de Persona, DictMixin y JsonMixin, el constructor debe inicializar el nombre, una lista de skills y un diccionario que contenga los datos de su familia, por ejemplo `{"esposa": "María"}`. Luego de crear la clase hacer uso de `to_dict` y `to_json`.


Links:

[Slide](https://docs.google.com/presentation/d/e/2PACX-1vTVhAMfOCIVe5T9ZnEIFF5Rv365YGW95WpqLprszRxIfkzUl8uYLmpfdGtrkF9FmnJc7JTlz2maQnhh/embed?start=false&loop=false&delayms=3000)

[Teoria](https://www.youtube.com/watch?v=NY49laSW2io&list=PLxI5H7lUXWhgHbHF4bNrZdBHDtf0CbEeH&index=12&ab_channel=Silabuz)
[Practica](https://www.youtube.com/watch?v=MyJoGCLx4bs&list=PLxI5H7lUXWhgHbHF4bNrZdBHDtf0CbEeH&index=13&ab_channel=Silabuz)