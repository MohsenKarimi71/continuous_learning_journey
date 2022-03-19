from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render

import ast

from posts.models import Category

# Create your views here.

def home_page(request):
    return render(request, "posts/home.html")


def new_category(request):
    if request.method == "POST":
        title = request.POST.get('new_category_title', "").strip()
        category = Category(title=title)
        try:
            category.full_clean()
            category.save()
        except ValidationError as e:
            return render(request, "posts/add_new_category.html", {
                "error_messages": ast.literal_eval(str(e))
            })
        return redirect("/categories/")
    return render(request, "posts/add_new_category.html")


def category_list(request):
    categories = Category.objects.all()

    return render(request, "posts/category_list.html", {
        "categories": categories
    })


def category_detail(request, id):
    category = Category.objects.get(id=id)
    return render(request, "posts/category_detail.html", {
        "category": category
    })