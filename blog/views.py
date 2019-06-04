from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, DeleteView

from blog.forms import PostForm
from blog.models import Post


class PostList(TemplateView):
    template_name = 'blog/post_list.html'

    def post(self, request, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        post = Post.objects.post = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        context['post'] = post
        return render(request, self.template_name, context)


# def post_list(request):
#    post = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
#    return render(request, 'blog/post_list.html', {'post': posts})


class PostDetail(TemplateView):
    template_name = 'blog/post_detail.html'

    def post(self, request, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        pk = kwargs.get('pk')
        post = get_object_or_404(Post, pk=pk)
        context['post'] = post
        return render(request, self.template_name, context)


# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'blog/post_detail.html', {'post': post})
#


class PostNew(TemplateView):
    form_class = PostForm
    initial = {'key': 'value'}
    template_name = 'blog/post_edit.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST or None)
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


class DetailView(TemplateView):
    form_class = PostForm
    initial = {'key': 'value'}
    template_name = 'blog/post_edit.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
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

    # def post_edit(self, request, pk_):
    #   post = get_object_or_404(Post, pk=pk)
    #   if request.method == "POST":
    #   form = PostForm(request.POST, instance=post)
    #   if form.is_valid():
    #       post = form.save(commit=False)
    #       post.author = request.user
    #       post.published_date = timezone.now()
    #       post.save()
    #       return redirect('post_detail', pk=post.pk)
    # else:
    #       form = PostForm(instance=post)
    # return render(request, 'blog/post_edit.html', context={'form': form})


class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('post-delete')

# Create your views here.e
