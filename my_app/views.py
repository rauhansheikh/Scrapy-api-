from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .utils import perform_search_and_save
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import render

@method_decorator(csrf_exempt, name='dispatch')
class SearchAPIView(APIView):
    def post(self, request):
        query = request.data.get("query")
        if not query:
            return Response({"error": "Query is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        search_entry = perform_search_and_save(query)
        results = search_entry.results.all().values('title', 'link', 'snippet')
        return Response({"results": list(results)})

def search_page(request):
    return render(request, "my_app/search.html")
