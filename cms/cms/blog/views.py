from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Post, Category
from blog.forms import ContactUsForm, RegisterForm, PostForm
from django.views import View, generic
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin

# Create your views here.
def index(request):
    posts = Post.objects.all()
    category = Category.objects.all()
    return render(request, "blog/stories.html", context = {"posts":posts, "category":category})

class HomeView(View):

    def get(self, request):
        posts = Post.objects.all()
        category = Category.objects.all()
        return render(request, 'blog/stories.html', context= {"posts":posts})

class PostListView(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status = "p")
    context_object_name = 'posts'
    template_name = "blog/stories.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['categories'] = categories
        return context

#def index2(request):
 #   return render(request, "temp1.html")

def categories(request, id):
    if Category.objects.filter(id = id)[0].name == "All":
        posts = Post.objects.all()
        category = Category.objects.all()
    else:
        posts = Post.objects.filter(category__id = id)
        category = Category.objects.filter(id = id)
    return render(request, "blog/stories.html", context = {"posts":posts, "category":category})


def post_details(request,id):
    try:
        post = Post.objects.get(id = id)
        return render(request,"blog/blog-post.html",{"post":post})
    except:
        return HttpResponse("Page not found!!")

class PostView(View):
    def get(self, request, id):
        try:
            post = Post.objects.get(id = id)
            return render(request,"blog/blog-post.html",{"post":post})
        except:
            return HttpResponse("welcome to my blog!!")

class PostDetailView(LoginRequiredMixin, generic.DetailView):
    model = Post
    queryset = Post.objects.filter(status="p")
    template_name = "blog/blog-post.html"
    #pk_url_kwarg = "id"
    login_url = reverse_lazy('login')
    

def contact_form_view(request):
    #print(request.method)
    if request.method == "GET":
        form = ContactUsForm()
        return render(request, "blog/contact-us.html", context = {"form":form})
    else:
        print(request.POST)
        form = ContactUsForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            return render(request,"blog/thanks.html")
        else:
            print(form.errors)
            return render(request, "blog/contact-us.html", context = {"form":form})

def register_form_view(request):
    #print(request.method)
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "blog/register.html", context = {"form":form})
    else:
        print(request.POST)
        form = RegisterForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            return render(request,"blog/thanks.html")
        else:
            print(form.errors)
            return render(request, "blog/register.html", context = {"form":form})
            
def post_form_view(request):
    #print(request.method)
    if request.method == "GET":
        form = PostForm()
        return render(request, "blog/post.html", context = {"form":form})
    else:
        print(request.POST)
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request,"blog/thanks.html")
        else:
            print(form.errors)
            return render(request, "blog/post.html", context = {"form":form})

# class PostCreateView(View):
#     def get(self, request):
#         form = PostForm()
#         return render(request, 'blog/post.html', context={"form":form})

#     def post(self, request):
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return render(request,"blog/thanks.html")
#         else:
#             print(form.errors)
#             return render(request, "blog/post.html", context = {"form":form})

class PostCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    permission_required = 'blog.add_post'
    login_url = reverse_lazy('login')
    model = Post
    #fields = ['title', 'content', 'status', 'category', 'image', 'author']
    template_name = "blog/post.html"
    form_class = PostForm
    #success_url = reverse_lazy("post-details")

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # def get_form_kwargs(self):
    #     kwargs = {
    #         'initial': self.get_initial(),
    #         'prefix': self.get_prefix(),
    #     }
    #     kwargs['initial']['author'] = self.request.user.profile
    #     if self.request.method in ('POST', 'PUT'):
    #         kwargs.update({
    #             'data': self.request.POST,
    #             'files': self.request.FILES,
    #         })
    #         #data = kwargs.get('data').dict()
    #         #data['author'] = self.request.user.profile.id
    #     return kwargs

class AboutUs(generic.TemplateView):
    template_name = "404.html"

# class RedirectPost(generic.RedirectView):
#     url = reverse_lazy("home")


def post_update_form_view(request, id):
    #print(request.method)
    post = Post.objects.get(id = id)
    if request.method == "GET":
        form = PostForm(instance = post)
        return render(request, "blog/post.html", context = {"form":form})
    else:
        print(request.POST)
        form = PostForm(request.POST, request.FILES, instance = post)
        if form.is_valid():
            form.save()
            return render(request,"blog/thanks.html")
        else:
            print(form.errors)
            return render(request, "blog/post.html", context = {"form":form})

# class PostUpdateView(generic.UpdateView):
#     model = Post
#     form_class = PostForm
#     template_name = "blog/post.html"

class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    permission_required = 'blog.change_post'
    login_url = reverse_lazy('login')
    model = Post
    #fields = ['title', 'content', 'status', 'category', 'image', 'author']
    template_name = "blog/post.html"
    form_class = PostForm
    #success_url = reverse_lazy("post-details")

    def form_valid(self,form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self, *args, **kwargs):
        post = Post.objects.get(slug = self.kwargs.get('slug'))
        if post.author == self.request.user:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    permission_required = 'blog.delete_post'
    model = Post
    success_url = reverse_lazy('home')
    template_name = "blog/delete_post.html"
    context_object_name = "post"

    def test_func(self):
        return self.request.user == Post.objects.get(slug=self.kwargs["slug"]).author
