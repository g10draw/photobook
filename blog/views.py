from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import PostForm
from .models import Post, Follow
from auth_manager.models import CustomUser

# Create your views here.
def home_page(request):
    return render(request, 'blog/home_page.html')

@login_required
def timeline_page(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            # Read form data from request.POST
            title = form.cleaned_data['title']
            image = form.cleaned_data['image']
            # Create new post
            new_post = Post(title=title, user=request.user)
            if image:
                new_post.image = image
            new_post.save()
            return redirect('timeline_page')
    else:
        form = PostForm()
        following = request.user.following.all()
        followers = request.user.followers.all()
        # Already following users
        following_ids = [obj.following.id for obj in following] + [request.user.id]
        # The new users available to follow
        to_follow = CustomUser.objects.filter(is_superuser=False).exclude(pk__in=following_ids)
    posts = Post.objects.filter(
        user__id__in=following_ids).order_by('-posted_on')
    return render(
        request, 
        'blog/timeline_page.html',
        {
            'form': form,
            'posts': posts,
            'followers': followers,
            'following': following,
            'to_follow': to_follow,
        }
    )

@login_required
def profile_page(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    posts = Post.objects.filter(user=user).order_by('-posted_on')
    already_following = Follow.objects.filter(
        follower=request.user, following=user).exists()
    following = user.following.all()
    followers = user.followers.all()
    return render(
        request, 'blog/profile_page.html', 
        {
            'profile': user,
            'posts': posts,
            'already_following': already_following,
            'followers': followers,
            'following': following,
        }
    )

@login_required
def handle_follow(request, user_id):
    user = CustomUser.objects.get(pk=user_id)
    already_following = Follow.objects.filter(
        follower=request.user, following=user)
    if already_following:
        already_following.delete()
    else:
        follow = Follow.objects.create(
            follower=request.user, following=user
        )
    return redirect('profile_page', user_id=user_id)