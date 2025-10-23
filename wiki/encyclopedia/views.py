from django.shortcuts import render
import markdown
import os
from django.conf import settings
from django.http import Http404
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title_open(request, title):
    return render(request, f"entries/{title}.md", {
        "content": util.get_entry(title)
    })