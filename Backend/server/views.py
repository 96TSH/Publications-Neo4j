from django.http import JsonResponse
from .models import Publication, Author, Country, Journal

def get_publication(request, publication_doi):
    publication = Publication.nodes.get_or_none(doi=publication_doi)
    if publication:
        data = {
            'doi': publication.doi,
            'title': publication.title,
            'abstract': publication.abstract,
            'citation_count': publication.citation_count,
            'publishDate': publication.publishDate
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Publication not found'}, status=404)

def get_author(request, author_name):
    author = Author.nodes.get_or_none(name=author_name)
    if author:
        data = {
            'name': author.name,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Author not found'}, status=404)

def get_country(request, country_name):
    country = Country.nodes.get_or_none(name=country_name)
    if country:
        data = {
            'name': country.name,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Country not found'}, status=404)

def get_journal(request, journal_name):
    journal = Journal.nodes.get_or_none(name=journal_name)
    if journal:
        data = {
            'name': journal.name,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Journal not found'}, status=404)
    
def search_publications(request, search_term):
    publications = Publication.nodes.filter(title__icontains=search_term)
    data = [{'doi': pub.doi, 'title': pub.title, 'abstract': pub.abstract, 'citation_count': pub.citation_count, 'publishDate': pub.publishDate} for pub in publications]
    return JsonResponse(data, safe=False)