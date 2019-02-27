from haystack import indexes
from pages.models import Book


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.EdgeNgramField(document=True, use_template=True, template_name='search/book_text.txt')
   
    bCode = indexes.IntegerField(model_attr='bCode')
    bName = indexes.EdgeNgramField(model_attr='bName')
    author = indexes.EdgeNgramField(model_attr='author')
    publisher = indexes.EdgeNgramField(model_attr='publisher')
    publication_year = indexes.IntegerField(model_attr='publication_year')
    classno = indexes.IntegerField(model_attr='classno')
    loanCnt = indexes.IntegerField(model_attr='loanCnt')
    bImage = indexes.CharField(model_attr='bImage')


    def get_model(self):
        return Book

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()