from django.urls import path, include
from blog.views import index, post_details, contact_form_view, categories, register_form_view, post_form_view, post_update_form_view
from blog.views import HomeView, PostView, PostCreateView, PostListView, PostDetailView, AboutUs, PostUpdateView, PostDeleteView
urlpatterns = [
    path('', PostListView.as_view(), name="home"),
    path('blogs/<slug:slug>', PostDetailView.as_view(), name="post-details"),
    #path('blogs/<slug:slug>', RedirectPost.as_view(), name="post-details"),
    path('contact', contact_form_view, name="contact"),
    path('category/<int:id>', categories, name = "category"),
    path('register', register_form_view, name="sign-up"),
    path('post', PostCreateView.as_view(), name="create-blog"),
    path('post/<slug:slug>/update',  PostUpdateView.as_view(), name="post-update"),
    path('post/<slug:slug>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('about-us', AboutUs.as_view()),
]