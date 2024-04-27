from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.get_all_articles, name='get_all_articles'),
    path('article/<str:article_pmid>/', views.get_article, name='get_article'),
    path('author/<str:author_name>/', views.get_author, name='get_author'),
    path('country/<str:country_name>/', views.get_country, name='get_country'),
    path('journal/<str:journal_name>/', views.get_journal, name='get_journal'),
    path('articles/search/<str:search_term>/', views.search_articles, name='search_articles'),
]