from django.urls import path

from posts import views

urlpatterns = [
    path('<int:category_id>/new/', views.new_subject, name="new_subject"),
    path('new/', views.new_category, name="new_category"),
    path('<int:category_id>/', views.category_detail, name="category_detail"),
    path('', views.category_list, name="category_list")
]
