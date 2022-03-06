from django.shortcuts import redirect, render

# Create your views here.

def home_page(request):
    return render(request, "posts/home.html")


def new_category(request):
    if request.method == "POST":
        return redirect("/categories/")
    return render(request, "posts/add_new_category.html")


def category_list(request):
    return render(request, "posts/category_list.html")