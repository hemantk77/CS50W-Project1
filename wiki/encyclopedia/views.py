from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request):
    return render(request, "encycloppedia/content.html", {
        "content": util.get_entry()
    })