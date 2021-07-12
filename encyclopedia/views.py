from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2

from django.http import HttpResponse
from django.shortcuts import render

from . import util
import encyclopedia

class NewSearchForm(forms.Form):
    q = forms.CharField(label="Search Encyclopedia")


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

#Searches for title query in list_entries
#If the query matches one of the items calls entry method that redirects to the correspondant entry
#If the query does not match one of the items returns the query string and a list of entries containing the query search
def search(request):
    if request.method == "POST":
        entries = util.list_entries()
        suggested_search_results = []
        query = request.POST.get('query')

        for entry_title in entries:
            if entry_title.lower() == query.lower():
                return HttpResponseRedirect(reverse("entry", args=(entry_title,)))
            elif query.lower() in entry_title.lower():
                print("MATCHHHHHHHHHHHHHHHHHH")
                print(f"query.lower() {query.lower()} in entry_title.lower() {entry_title.lower()}")
                suggested_search_results.append(entry_title)
                print(suggested_search_results)
        return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "suggested_search_results": suggested_search_results
        })


# def search(request):
#     if request.method == "POST":
#         search = NewSearchForm(request.POST)
#         if search.is_valid():
#             query = search.cleaned_data["q"]
            
#             entries = util.list_entries()
#             suggested_search_results = []

#             for entry_title in entries:
#                 if entry_title.lower == query.lower:
#                     return HttpResponseRedirect(reverse("encyclopedia:entry_title"))
#                     # entry(request, entry_title)
#                 elif entry_title.lower.find(query.lower) >= 0:
#                     suggested_search_results.append(entry_title)
#             return render(request, "encyclopedia/search_results.html", {
#                 "query": query,
#                 "title": suggested_search_results
#                 })
#         else:
#             #TODO: redirect to an error page
#             return HttpResponseRedirect(reverse("encyclopedia:index"))
#     else:
#         #TODO: I don't know!!!!
#         return HttpResponseRedirect(reverse("encyclopedia:index"))
#         # return render(request, "tasks/add.html", {
#         #     "form": NewTaskForm()
#         # })