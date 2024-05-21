from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from .models import Posts
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

# posts = [
#     {
#         "author": "CoreyMS",
#         "title": "Blog Posts 1",
#         "content": "First Post Content",
#         "date_posted": "August 27, 2018"
#     },
#       {
#         "author": "Jane Doe",
#         "title": "Blog Posts 2",
#         "content": "Second Post Content",
#         "date_posted": "August 28, 2018"
#     }
# ]

# Create your views here.
def home(request):
    # return HttpResponse("<h1>Blog Home</h1>")
    context = {
        "posts": Posts.objects.all()
    }
    return render(request, "blog/home.html", context)

class PostListView(ListView):
    model = Posts
    template_name = 'blog/home.html' # <app>/<model>_<viewtype>.html
    context_object_name = "posts"
    ordering = ['-date_posted']
    paginate_by = 3

class UserPostListView(ListView):
    model = Posts
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewtype>.html
    context_object_name = "posts"
    # ordering = ['-date_posted']
    paginate_by = 3    

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Posts.objects.filter(author = user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Posts  

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Posts    
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)  
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Posts    
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)   

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False  
        
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Posts  
    success_url = "/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False         

def about(request):
    # return HttpResponse("<h1>Blog About</h1>")
    return render(request, "blog/about.html", {"title": "About"})