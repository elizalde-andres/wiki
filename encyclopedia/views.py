import random
from logging import disable
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2

from django.http import HttpResponse
from django.shortcuts import render

from . import util
import encyclopedia

class NewPageForm(forms.Form):
    title = forms.CharField(label="Entry title")
    content = forms.CharField(label="", widget=forms.Textarea)


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
#If the query matches one of the items redirects to the correspondant entry
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
                suggested_search_results.append(entry_title)
                print(suggested_search_results)
        return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "suggested_search_results": suggested_search_results
        })


def create_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data["title"]
            if entry_title in util.list_entries():
                return render(request, "encyclopedia/create_page.html", {
                            "form": NewPageForm(request.POST),
                            "entry_already_exists": True,
                            "form_is_not_valid": False
                        })            
            page_content = form.cleaned_data["content"]
            page_content = f"# {entry_title}\n\n {page_content}"
            util.save_entry(entry_title, page_content)
            return HttpResponseRedirect(reverse("entry", args=(entry_title,)))
        else:
            return render(request, "encyclopedia/create_page.html", {
            "form": NewPageForm(request.POST),
            "entry_already_exists": False,
            "form_is_not_valid": True
        })
    else:
        return render(request, "encyclopedia/create_page.html", {
            "form": NewPageForm(),
            "entry_already_exists": False,
            "form_is_not_valid": False
        })


def edit_page(request, title):
    if request.method == "POST":
        print(f"REQUEST POSTTTT {request.POST}")
        print(f"TITLEEEEEEEEE {title}")
        form = NewPageForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data["title"]            
            page_content = form.cleaned_data["content"]
            util.save_entry(entry_title, page_content)
            return HttpResponseRedirect(reverse("entry", args=(entry_title,)))
        else:
            return render(request, "encyclopedia/edit_page.html", {
            "form": NewPageForm(request.POST),
            "form_is_not_valid": True
        })
    form = NewPageForm({
                        "title": title,
                        "content": util.get_entry(title)
                    })
    form.fields['title'].widget.attrs['readonly'] = True
    return render(request, "encyclopedia/edit_page.html", {
            "form": form
        })
    

def random_page(request):
    random_page_title = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse("entry", args=(random_page_title,)))


    