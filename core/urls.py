from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
# from drf_yasg import openapi
# from drf_yasg.views import get_schema_view
# from rest_framework import permissions

from core import settings

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Weekly project CORE API",
#         default_version='v1',
#         description=f"This core functionalities of all Adilbek's projects",
#         contact=openapi.Contact(email="asilbekmirolimov@gmail.com")
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
    # path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
