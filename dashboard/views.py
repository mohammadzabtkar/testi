from django.http import HttpResponse
from django.shortcuts import render
import datetime
# Create your views here.
def dashboard(request):
    return render(request , 'dashboard/dashboard.html')
