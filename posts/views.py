from django.shortcuts import render

# Create your views here.

def home_page(request):
    return render(request, "posts/home.html")


def new_category(request):
    return render(request, "posts/add_new_category.html")