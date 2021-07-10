import markdown2

from django.http import HttpResponse
from django.shortcuts import render

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    markdowner = markdown2.Markdown()
    content = markdowner.convert(content)

    if content:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content
        })
    else: 
        return render(request, "encyclopedia/entry_does_not_extist.html", {
            "title": title
        })