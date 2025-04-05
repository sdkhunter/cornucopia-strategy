from django.http import JsonResponse

def fetch_subscribers(request):
    data = {
        'subscribers': [
            {'id': 1, 'email': 'alice@example.com'},
            {'id': 2, 'email': 'bob@example.com'},
        ]
    }
    return JsonResponse(data)

