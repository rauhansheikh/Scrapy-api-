from django.db import models

class SearchQuery(models.Model):
    query = models.CharField(max_length=255)
    searched_at = models.DateTimeField(auto_now_add=True)

class SearchResult(models.Model):
    query = models.ForeignKey(SearchQuery, on_delete=models.CASCADE, related_name='results')
    title = models.CharField(max_length=500)
    link = models.URLField()
    snippet = models.TextField()

class ReScrapedResult(models.Model):
    search_result = models.ForeignKey(
        SearchResult,
        on_delete=models.CASCADE,
        related_name="rescrapes"
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Re-scrape of {self.search_result.title} at {self.scraped_at}"