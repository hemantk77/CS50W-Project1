from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title_open(request, title):
    return render(request, "entries/{title}.md", {
        "content": util.get_entry(title)
    })