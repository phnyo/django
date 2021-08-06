from django.shortcuts import render
from django.http import HttpResponse

def top(request):
    return HttpResponse(b"Hello World")

def snippet_new(request):
    return HttpResponse('Registered snippets')

def snippet_edit(request, snippet_id):
    return HttpResponse('Edit the snippet')

def snippet_detail(request, snippet_id):
    return HttpResponse('Show the snippet details')
