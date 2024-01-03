from django.shortcuts import reverse_lazy, render, get_object_or_404, redirect
from django.utils import timezone

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (ListView, DetailView, 
                                  TemplateView, CreateView, 
                                  UpdateView, DeleteView
                                )
from blog.models import Post, Comment
from forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required


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
    
#############################################
    #Comments from here
#############################################

@login_required
def psot_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required    
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        #print("request.POST: ", request.POST)
        form = CommentForm(request.POST)
        if form.is_valid():
            #print("form.cleaned_data: ", form.cleaned_data)
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        #print("else")
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment, pk=pk)
    #print("comment: ", comment)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def commetn_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    #print("comment: ", comment)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)

