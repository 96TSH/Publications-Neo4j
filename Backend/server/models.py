from neomodel import StructuredNode, StringProperty, IntegerProperty, DateProperty
    
class Publication(StructuredNode):
    doi = StringProperty(unique_index=True)
    title = StringProperty()
    abstract = StringProperty()
    citation_count = IntegerProperty()
    publishDate = DateProperty()

class Author(StructuredNode):
    name = StringProperty(unique_index=True)

class Country(StructuredNode):
    name = StringProperty(unique_index=True)

class Journal(StructuredNode):
    name = StringProperty(unique_index=True)