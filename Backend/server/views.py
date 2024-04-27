from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from .models import Article, Author, Country, Journal


def get_article(request, article_pmid):
    article = Article.nodes.get_or_none(pmid=article_pmid)
    if article:
        data = {
            "pmid": article.pmid,
            "doi": article.doi,
            "title": article.title,
            "citation_count": article.citation_count,
            "published_by": [journal.journal for journal in article.published_by],
            "published_in": [country.country for country in article.published_in],
            "authored_by": [author.author for author in article.authored_by],
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Article not found"}, status=404)


def get_all_articles(request):
    page_number = int(
        request.GET.get("page", 1)
    )  # Get the page number from the query parameters
    page_size = int(
        request.GET.get("size", 10)
    )  # Get the page size from the query parameters

    articles = Article.nodes.all()
    paginator = Paginator(articles, page_size)

    try:
        articles_page = paginator.page(
            page_number
        )  # Get the articles on the current page
    except (EmptyPage, InvalidPage):
        articles_page = paginator.page(
            paginator.num_pages
        )  # If the page is out of range, deliver the last page of results

    data = []
    for article in articles_page:
        data.append(
            {
                "pmid": article.pmid,
                "doi": article.doi,
                "title": article.title,
                "citation_count": article.citation_count,
                "published_by": [journal.journal for journal in article.published_by],
                "published_in": [country.country for country in article.published_in],
                "authored_by": [author.author for author in article.authored_by],
            }
        )

    return JsonResponse(
        {
            "total_pages": paginator.num_pages,
            "current_page": page_number,
            "page_size": page_size,
            "articles": data,
        }
    )


def get_author(request, author_name):
    author = Author.nodes.get_or_none(author=author_name)
    if author:
        data = {
            "author": author.author,
            "authored_articles": [article.pmid for article in author.authored_articles],
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Author not found"}, status=404)


def get_country(request, country_name):
    country = Country.nodes.get_or_none(country=country_name)
    if country:
        data = {
            "country": country.country,
            "articles_published_in": [
                article.pmid for article in country.articles_published_in
            ],
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Country not found"}, status=404)


def get_journal(request, journal_name):
    journal = Journal.nodes.get_or_none(journal=journal_name)
    if journal:
        data = {
            "journal": journal.journal,
            "articles_published_by": [
                article.pmid for article in journal.articles_published_by
            ],
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"error": "Journal not found"}, status=404)


def search_articles(request, search_term):
    page_number = int(
        request.GET.get("page", 1)
    )  # Get the page number from the query parameters
    page_size = int(
        request.GET.get("size", 10)
    )  # Get the page size from the query parameters

    # Search for articles that match the search term
    articles = Article.nodes.filter(title__icontains=search_term)

    # Create a Paginator object
    paginator = Paginator(articles, page_size)

    try:
        articles_page = paginator.page(
            page_number
        )  # Get the articles on the current page
    except (EmptyPage, InvalidPage):
        articles_page = paginator.page(
            paginator.num_pages
        )  # If the page is out of range, deliver the last page of results

    data = []
    for article in articles_page:
        data.append(
            {
                "pmid": article.pmid,
                "doi": article.doi,
                "title": article.title,
                "citation_count": article.citation_count,
                "published_by": [journal.journal for journal in article.published_by],
                "published_in": [country.country for country in article.published_in],
                "authored_by": [author.author for author in article.authored_by],
            }
        )

    return JsonResponse(
        {
            "total_pages": paginator.num_pages,
            "current_page": page_number,
            "page_size": page_size,
            "articles": data,
        }
    )
