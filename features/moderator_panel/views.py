from django.shortcuts import render

def moderator_dashboard(request):
    return render(request, 'moderator_panel/dashboard.html')
