from django.urls import path

from posts import views

urlpatterns = [
    path('new/', views.new_category, name="new_category"),
    path('', views.category_list, name="category_list")
]
