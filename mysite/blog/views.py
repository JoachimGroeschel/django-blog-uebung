from django.shortcuts import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DetailView, 
                                  TemplateView, CreateView, 
                                  UpdateView, DeleteView
                                )
from blog.models import Post, Comment
from forms import PostForm, CommentForm


# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.order_by('-published_date').filter(published_date__isnull=False)
# default template_name = <app_name>/<model_name>_list.html
# default context_object_name = <model_name>_list
# default queryset = <model_name>.objects.all()
# default paginate_by = None
# default ordering = None
        
class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post
    #Achtung: folgende Felder bis return super() sind nicht im Buch, sondern vom Bot
    fields = ['author', 'title', 'text']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post
    
    #Achtung: folgende Felder bis return super() sind nicht im Buch, sondern vom Bot
    fields = ['author', 'title', 'text']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post
    
    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')