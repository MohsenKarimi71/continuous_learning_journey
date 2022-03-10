from django.shortcuts import redirect, render
from posts.models import Category

# Create your views here.

def home_page(request):
    return render(request, "posts/home.html")


def new_category(request):
    if request.method == "POST":
        title = request.POST.get('new_category_title', "default")
        Category.objects.create(title=title)
        return redirect("/categories/")
    return render(request, "posts/add_new_category.html")


def category_list(request):
    categories = Category.objects.all()

    return render(request, "posts/category_list.html", {
        "categories": categories
    })