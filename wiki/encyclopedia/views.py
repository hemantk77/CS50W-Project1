from django.shortcuts import render, redirect
import markdown #This library help to translate the md file into a html one
import os #opens the md file and reads all the data in it
from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from . import util
from django.urls import reverse
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title_open(request, title):
    # This builds the full address: /your/project/folder/entries/CSS.md
    md_file_path = os.path.join(settings.BASE_DIR, 'entries', f'{title}.md')
    
    try:
        with open(md_file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        html_content = markdown.markdown(markdown_content)
        
    except FileNotFoundError:
        # If the file isn't there, this shows the standard "Page Not Found" page
        raise Http404(f"Sorry, the page for '{title}' doesn't exist.")    
    
    context = {
        'title': title,
        'content_html': html_content  # The converted HTML is stored here
    }
    
    # We send the converted HTML to a *real* HTML template file:
    return render(request, 'encyclopedia/entry_display.html', context)

def search_results(request):
    user_query = request.GET.get('q') #from data comes from request.GET
    all_entries = util.list_entries()
    substring_matches = []
    exact_match = None
    
    for entry in all_entries:
        
        if user_query.lower() == entry.lower():
            exact_match = entry
            break
        
        elif user_query.lower() in entry.lower():
            substring_matches.append(entry)
            
    if exact_match:
        entry_title = exact_match
        redirect_url = reverse('title_open', kwargs={'title':entry_title})
        return HttpResponseRedirect(redirect_url)
    else:
        results_list = substring_matches
        
        return render(request, "encyclopedia/search_results.html", {
            "results": results_list,
            "query": user_query
        })
        
def create_new_page(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new_page.html")
    
    elif request.method == "POST":
        print(f"FORM DATA RECEIVED: {request.POST}")
        
        title = request.POST['title']
        content = request.POST['content']
        all_entries = util.list_entries()
        
        for entry in all_entries:
            if entry.lower() == title.lower():
                return render(request, "encyclopedia/new_page.html", {
                    "error": "This Title already exists."
                    })
            
        util.save_entry(title, content)
        return redirect('title_open', title=title)
    
def edit_page(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        
        if content is None:
            raise Http404("Entry for '{title}' not found.")
        
        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "content": content
        })
        
    elif request.method == "POST":
        new_content = request.POST['content']
        util.save_entry(title, new_content)
        
        return redirect('title_open', title=title)
    
def random_page(request):
    all_entries = util.list_entries()
    title = random.choice(all_entries)
    
    return redirect('title_open', title=title)
    