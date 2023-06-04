import markdown2
import random

from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages
from . import util


class NewSearchForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Search Encyclopedia'}))

class NewCreateForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'The title\'s article'}))
    content = forms.CharField(widget=forms.Textarea(attrs={
                              'style': 'height: 200px;width:1000px'}))

class NewEditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={
                              'style': 'height: 200px;width:1000px'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm()
    })

def searchArticle(request, title):
    content = ""
    flagError = True
    if util.get_entry(title) == None:
        title = "Error"
        content = "<h2> The page does not exist, yet.<h2> <h3>We invite you to create it :)<h3>"
        flagError = False
    else:
        content = markdown2.markdown(util.get_entry(title))
    return render(request, "encyclopedia/article.html", {
        "content": content,
        "title": title,
        "form": NewSearchForm(),
        "flagError": flagError
    })

def searchMatches(request):
    if request.method == "POST":
        form = NewSearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]

            # Full coincidence
            if util.get_entry(title) != None:
                content = markdown2.markdown(util.get_entry(title))
                return render(request, "encyclopedia/article.html", {
                    "content": content,
                    "title": title,
                    "form": NewSearchForm()
                })
            # partial coincidences
            matches = []
            entries = util.list_entries()
            for iter in entries:
                if title.lower() in iter.lower():
                    matches.append(iter)
            return render(request, "encyclopedia/index.html", {
                "entries": entries,
                "results": matches,
                "form": NewSearchForm(),
                "search": True
            })

def createArticle(request):
    if request.method == "POST":
        formCreate = NewCreateForm(request.POST)
        if formCreate.is_valid():
            title = formCreate.cleaned_data["title"]
            content = formCreate.cleaned_data["content"]
            if title not in util.list_entries():
                f = open("entries/"+title+".md", "a")
                f.write(content)
                f.close()
                return redirect('/wiki/'+title)
            else:
                messages.error(request, 'The title already exists.')
                return render(request, "encyclopedia/create.html", {
                    "form": NewSearchForm(),
                    "fromCreate": formCreate
                })
        else:
            return render(request, "encyclopedia/create.html", {
                "form": NewSearchForm(),
                "fromCreate": formCreate
            })
    return render(request, "encyclopedia/create.html", {
        "form": NewSearchForm(),
        "fromCreate": NewCreateForm()
    })

def editArticle(request, title):
    if request.method == "POST":
        formEdit = NewEditForm(request.POST)
        if formEdit.is_valid():
            content = formEdit.cleaned_data["content"]
            try:
                f = open("entries/"+title+".md", "w")
                f.write(content)
                f.close()
                return redirect('/wiki/'+title)
            except:
                messages.error(request, 'There was an error with the file.')
                return render(request, "encyclopedia/edit.html", {
                    "form": NewSearchForm(),
                    "fromEdit": formEdit
                })
        else:
            return render(request, "encyclopedia/edit.html", {
                "form": NewSearchForm(),
                "fromEdit": formEdit
            })
    content = util.get_entry(title)
    initial = {'content': content}
    form = NewEditForm(initial=initial)
    print("title: " + title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "form": NewSearchForm(),
        "fromEdit": form
    })

def randomPage(request):
    articles = util.list_entries()
    article = random.choice(articles)
    return searchArticle(request, article)
