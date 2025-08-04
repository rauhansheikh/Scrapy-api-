from django.db import models

class SearchQuery(models.Model):
    query = models.CharField(max_length=255)
    searched_at = models.DateTimeField(auto_now_add=True)

class SearchResult(models.Model):
    query = models.ForeignKey(SearchQuery, on_delete=models.CASCADE, related_name='results')
    title = models.CharField(max_length=500)
    link = models.URLField()
    snippet = models.TextField()
