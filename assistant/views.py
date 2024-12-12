import json

from llm.llm import chain

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'index.html')

@csrf_exempt
def get_response(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            user_query = body.get('query', '')

            if not user_query:
                return JsonResponse({'error': '질문을 입력해주세요.'}, status=400)
        
            answer = chain.invoke({'question': user_query, 'language': '한국어'})
            return JsonResponse({'response': answer})
        
        except Exception as error:
            return JsonResponse({"error": str(error)}, status=500)
    
    return  JsonResponse({'error': 'Invalid request method. Only POST is allowed.'}, status=405)