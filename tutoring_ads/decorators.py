from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
def access(request, id):
    if int(request.user.id) != int(id):
        return render(request, 'base_r/home.html')