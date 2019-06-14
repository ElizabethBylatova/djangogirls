from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DeleteView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


from blog.forms import PostForm
from blog.models import Post


class PostList(TemplateView):
    template_name = 'blog/post_list.html'

    def get(self, request, *args, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
        context['posts'] = posts
        return render(request, self.template_name, context)


# def post_list(request):
#    post = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
#    return render(request, 'blog/post_list.html', {'post': posts})


class PostDetail(LoginRequiredMixin,TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    template_name = 'blog/post_detail.html'

    def get(self, request, *args, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        pk = kwargs.get('pk')
        post = get_object_or_404(Post, pk=pk)
        context['post'] = post
        return render(request, self.template_name, context)


# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'blog/post_detail.html', {'post': post})
#


class PostNew(LoginRequiredMixin,TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
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


class PostEdit(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
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


class LoginView(TemplateView):
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        context = {}
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                context['error'] = "Логин или пароль неправильные"
        return render(request, self.template_name, context)


class ProfilePage(TemplateView):
    template_name = 'registration/profile.html'


class RegisterView(TemplateView):
    template_name = "registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password == password2:
                User.objects.create_user(username, email, password)
                return redirect(reverse("login"))

        return render(request, self.template_name)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    model = Post
    success_url = '/'

# Create your views here.e
