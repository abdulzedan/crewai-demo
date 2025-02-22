from django.http import JsonResponse


def index(request):
    return JsonResponse({"message": "CrewAI Demo Backend OK"})
