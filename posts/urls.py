from django.urls import path

from posts import views

urlpatterns = [
    path('new/', views.new_category, name="new_category"),
    path('<int:id>/', views.category_detail, name="category_detail"),
    path('', views.category_list, name="category_list")
]
