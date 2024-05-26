from django.shortcuts import render
from . models import *
# Create your views here.

def index(request):
    all_class = class_type.objects.all()

    return render(request, './pages_wib/index.html', {'all_class':all_class,'active_link': 'wibside_index' ,
})



def Blogs(request):
    all_blog = Blog.objects.all()
    return render(request, './pages_wib/blog.html', {'all_blog':all_blog,'active_link': 'Blog' ,
})



def Contact(request):
    return render(request, './pages_wib/contact.html', {'active_link': 'Contact' ,
})