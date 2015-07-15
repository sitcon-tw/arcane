from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


@login_required
def dashboard(request):
    # WIP
    return HttpResponse("dashboard")
