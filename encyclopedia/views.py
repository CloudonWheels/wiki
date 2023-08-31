from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown
import random
from . import util


def index(request):
    try: 
        query = request.GET["q"]
        if util.get_entry(query):
            return HttpResponseRedirect(reverse("entry page", kwargs={'title':request.GET["q"]}))

        return render(request, "encyclopedia/index.html", {
            "heading": "Search Results",
            "entries": list(filter(lambda s: query.upper() in s.upper(), util.list_entries()))
            })
    except:
        return render(request, "encyclopedia/index.html", {
            "heading": "All Pages",
            "entries": util.list_entries()
            })

def entry(request, title):
    markdown_content= util.get_entry(title)   
    if markdown_content:
        rendered_html= markdown.markdown(markdown_content)
    else:
        rendered_html= None

    return render(request, "encyclopedia/entry.html", {
        "data": rendered_html,
        "title": title
   })    
    
    

#for creating new page
def new(request):
    if request.method == 'POST':
        if util.get_entry(request.POST.get('title')):
            return render(request, "encyclopedia/new.html", {"error": True})
        
        util.save_entry(request.POST.get('title'), request.POST.get('content'))
        return HttpResponseRedirect(reverse("entry page", kwargs={'title':request.POST.get('title')}))

    return render(request, "encyclopedia/new.html")
#editing the new page
def edit(request, title):
    return render(request, 'encyclopedia/edit.html', {
        "title": title,
        "content": util.get_entry(title)
    })
#saving the edited page
def confirm_edit(request):
    util.save_entry(request.POST.get('title'), request.POST.get('content'))
    return HttpResponseRedirect(reverse("entry page", kwargs={'title':request.POST.get('title')}))
#for random page to appear
def random_entry(request):
    return HttpResponseRedirect(reverse("entry page", kwargs={
        "title": random.choice(util.list_entries())
    }))