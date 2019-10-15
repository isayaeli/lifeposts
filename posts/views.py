from django.shortcuts import render, redirect, HttpResponseRedirect,get_object_or_404
from django.views.generic import CreateView, UpdateView,DeleteView
from posts.models import Post,Comment
from posts.forms import loginForm, registerForm, VideoForm, commentForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.contrib.auth import get_user_model


@login_required(login_url= '/login')
def home(request,):
    post = Post.objects.all()
    users = get_user_model().objects.all()
    query = request.GET.get('q')
    if query:
        post = Post.objects.filter(
        Q(user__username=query)|
        Q(post_description__icontains=query)|
        Q(updated__icontains=query)
        ).order_by('-id')
    comment = Comment.objects.filter(post=post)
    
    context = {
        'posts':post,
        'comments':comment,
        'users':users
    }
    return render(request, 'posts/home.html', context)

def register(request):
    if request.method == 'POST':
        form = registerForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.info(request, f"Successfully registered as :{username} now Login")
            # login(request, user)
            return redirect('/login')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}:{form.error_messages[msg]}")
                return redirect('/register')
    form = registerForm()
    return render(request, 'posts/register.html', {'form':form})

def login_request(request):
    if request.method == 'POST':
        form = loginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # request.session.set_expiry(1200)
                # messages.success(request, f"Welcome again :{username}")
                return redirect('/')
            else:
                messages.error(request, "Invalid username or password")
                return redirect('/login')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('/login')
    form = loginForm()
    return render(request, 'posts/login.html', {'form':form})
 
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out!! thanks for spending some time on lifebook")
    return redirect('/login')

@login_required(login_url= '/login')
def add_post(request):
    # post = Post(post_description= request.POST['post_description'])
    # post.save()
    # return redirect('/')
    if request.method == 'POST':
        if request.POST.get('post_description'):
            post = Post()
            post.post_description = request.POST.get('post_description')
            post.user = request.user
            post.save()
            return redirect('/')
        else:
            messages.info(request, "You can not add empyt post")
    else:
        return render(request, 'posts/home.html')


# def add_photo(request):
#     # post = Post(post_description= request.POST['post_description'])
#     # post.save()
#     # return redirect('/')
#     if request.method == 'POST':
#         if request.POST.get('post_image') and request.POST.get('post_description'):
#             post = Post()
#             post.post_image = request.POST.get('post_image')
#             post.post_description = request.POST.get('post_description')
#             post.user = request.user
#             post.save()
#             return render(request, 'posts/home.html')
#         else:
#             messages.info(request, "You can not add empyt post")
#     else:
#         return render(request, 'posts/home.html')
 
    
class VideoCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/add_video.html'
    fields = ['post_description', 'post_video']
    

    def form_valid(self, form):
        form.instance.user =self.request.user
        return super().form_valid(form)

class ImageCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts/add_image.html'
    fields = ['post_description', 'post_image']
    

    def form_valid(self, form):
        form.instance.user =self.request.user
        return super().form_valid(form)


class PostUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'posts/update_post.html'
    fields = ['post_description', 'post_video']
    

    def form_valid(self, form):
        form.instance.user =self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post=self.get_object()
        if self.request.user == post.user:
            return True
        return False

class PostDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post=self.get_object()
        if self.request.user == post.user:
            return True
        return False
        
@login_required(login_url= '/login')
def post_likes(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    context={
        'post':post,
        'is_liked':is_liked,
        'total_likes':post.total_likes()
        
    }
    if request.is_ajax():
        html = render_to_string('posts/likes.html', context, request=request)
        return JsonResponse({'form':html})

@login_required(login_url= '/login')
def comment_view(request, id):
    post = Post.objects.get(id=id)
    comment = Comment.objects.filter(post=post).order_by('-id')
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked=True
    
    if request.method == 'POST':
        form = commentForm(request.POST or None)
        if form.is_valid():
            contents = request.POST.get('contents')
            comment = Comment.objects.create(post=post, user=request.user, contents=contents)
            comment.save()
            return redirect('post', id=id)

    form = commentForm()
    context = {
        'post':post,
        'is_liked':is_liked,
        'comment':comment,
        'form':form
    }
    return render(request, 'posts/more.html', context)

class CommentUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'posts/update_comment.html'
    fields = ['contents']
    # success_url = '/'
    
    

    def form_valid(self, form):
        form.instance.user =self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        comment=self.get_object()
        if self.request.user == comment.user:
            return True
        return False

# class CommentDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
#     model = Comment
#     # template_name = 'posts/delete_comments.html'
#     success_url = reverse_lazy('post', kwargs={'id':comment.post_id})

    

#     def test_func(self):
#         comment=self.get_object()
#         if self.request.user == comment.user:
#             return True
#         return False
# def delete_comment(self, id):
#     comment = get_object_or_404(Comment, id=id)
#     comment.delete()
#     return redirect('home')

@login_required
def comment_remove(request, id):
    comment = get_object_or_404(Comment, id=id)
    comment.delete()
    return redirect('post', id=comment.post.id)

@login_required(login_url= '/login')
def user_profile_view(request, id):
    post = Post.objects.get(id=id)
    user = post.user
    post1 = Post.objects.filter(user= user).order_by('-updated')
    context = {
        'post':post,
        'post1':post1
    }
    return render(request, 'posts/profile_details.html', context)

    




