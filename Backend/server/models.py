from neomodel import StructuredNode, StringProperty, IntegerProperty, RelationshipTo, RelationshipFrom

class Article(StructuredNode):
    pmid = IntegerProperty(unique_index=True)
    doi = StringProperty(unique_index=True)
    title = StringProperty()
    citation_count = IntegerProperty()
    published_by = RelationshipTo('Journal', 'PUBLISHED_BY')
    published_in = RelationshipTo('Country', 'PUBLISHED_IN')
    authored_by = RelationshipFrom('Author', 'AUTHORED')

class Author(StructuredNode):
    author = StringProperty(unique_index=True)
    authored_articles = RelationshipTo('Article', 'AUTHORED')

class Country(StructuredNode):
    country = StringProperty(unique_index=True)
    articles_published_in = RelationshipFrom('Article', 'PUBLISHED_IN')

class Journal(StructuredNode):
    journal = StringProperty(unique_index=True)
    articles_published_by = RelationshipFrom('Article', 'PUBLISHED_BY')