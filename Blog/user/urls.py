from django.urls import path
from . import views
# ,RegisterView, UserListView

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('users/', views.UserListView.as_view(), name='user-list'),
    
    path('category/', views.CategoryListView.as_view(), name='category-list'),
    path('category/<int:id>/', views.CategoryListView.as_view(), name='category-list'),

    path('blogs/', views.BlogListView.as_view(), name='blog-list'),
    path('blogs/<int:id>/', views.BlogListView.as_view(), name='blog-list'),
]