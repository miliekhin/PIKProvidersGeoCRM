from django.contrib import admin
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls
from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('partners.urls')),
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='PIK GEO CRM API')),
    path('openapi/', get_schema_view(
        title="PIK GEO CRM",
        description="API",
        version="1.0.0"
    ), name='openapi-schema'),
]
