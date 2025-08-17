from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import perform_search_and_save
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SearchResult,ReScrapedResult
from .utils import scrape_page_with_selenium

@method_decorator(csrf_exempt, name='dispatch')
class SearchAPIView(APIView):
    def post(self, request):
        query = request.data.get("query")
        if not query:
            return Response({"error": "Query is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        search_entry = perform_search_and_save(query)
        results = search_entry.results.all().values('id', 'title', 'link', 'snippet')
        return Response({"results": list(results)})

def search_page(request):
    return render(request, "my_app/search.html")


@csrf_exempt
def rescrape_link(request, result_id):
    if request.method == "POST":
        try:
            result = SearchResult.objects.get(id=result_id)

            # Selenium scrape
            data = scrape_page_with_selenium(result.link)

            # Save in ReScrapedResult
            rescraped = ReScrapedResult.objects.create(
                search_result=result,
                title=data["title"],
                content=data["content"]
            )

            return JsonResponse({
                "status": "success",
                "data": {
                    "title": rescraped.title,
                    "content": rescraped.content,
                    "scraped_at": rescraped.scraped_at.strftime("%Y-%m-%d %H:%M:%S")
                }
            })
        except SearchResult.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Result not found"}, status=404)

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)