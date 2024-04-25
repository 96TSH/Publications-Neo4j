from django.urls import path
from . import views

urlpatterns = [
    path('api/publication/<str:publication_doi>/', views.get_publication, name='get_publication'),
    path('api/author/<str:author_name>/', views.get_author, name='get_author'),
    path('api/country/<str:country_name>/', views.get_country, name='get_country'),
    path('api/journal/<str:journal_name>/', views.get_journal, name='get_journal'),
    path('api/publication/search/<str:search_term>/', views.search_publications, name='search_publications'),
]