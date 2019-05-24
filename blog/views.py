from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.utils import timezone

from blog.forms import PostForm
from blog.models import Post
from django.views.generic import TemplateView


class PostDetail(TemplateView):
    def post(self, request, **kwargs):
        pk = kwargs.get('pk')
        post = get_object_or_404(Post, pk=pk)
        return render(request, 'blog/post_detail.html', context={'post': post})

# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'blog/post_detail.html', {'post': post})
#


class PostNew(TemplateView):
    form_class = PostForm
    initial = {'key': 'value'}
    template_name = 'blog/post_edit.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(inital = self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
        return render(request, self.template_name, {'form': form})


    # def post_new(self, request, **kwargs):
    #     if request.method == "POST":
    #     form = PostForm(request.POST)
    #     if form.is_valid():
    #         post = form.save(commit=False)
    #         post.author = request.user
    #         post.published_date = timezone.now()
    #         post.save()
    #         return redirect('post_detail', pk=post.pk)
    # else:
    #     form = PostForm()
    # return render(request, 'blog/post_edit.html', context={'form': form})




class Detail(TemplateView):
    form_class = PostNew
    inital = {'key': 'value'}
    template_name = 'blog/post_edit.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(inital = self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = self.form_class(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
        return render(request, self.template_name, {'form': form})


    #def post_edit(self, request, pk_):
    #post = get_object_or_404(Post, pk=pk)
    #if request.method == "POST":
        #form = PostForm(request.POST, instance=post)
        #if form.is_valid():
            #post = form.save(commit=False)
            #post.author = request.user
            #post.published_date = timezone.now()
            #post.save()
            #return redirect('post_detail', pk=post.pk)
    #else:
        #form = PostForm(instance=post)
    #return render(request, 'blog/post_edit.html', context={'form': form})

# Create your views here.
