from django_elasticsearch_dsl import Document, Index
from django_elasticsearch_dsl.registries import registry
from products.models import Product

product_index = Index('products')

@registry.register_document
class ProductDocument(Document):

    class Index:
        name = 'products'

    
    class Django:
        model = Product
        fields = [
            'title',
            'description',
            'category',
            'subcategory'
        ]
