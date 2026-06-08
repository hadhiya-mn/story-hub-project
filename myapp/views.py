from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from myapp.models import (
    Blog,
    UserProfile,
    Like,
    Comment,
    Save
)


# =========================
# PUBLIC PAGES
# =========================

def base(request):

    return render(request, 'index.html')


def home(request):

    return render(request, 'index.html')


def user(request):

    return render(request, 'user.html')


def about(request):

    return render(request, 'about.html')


# =========================
# LOGIN / LOGOUT
# =========================

def login_view(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.is_superuser:

                return redirect('admin_home')

            else:

                return redirect('user_home')

        else:

            messages.error(
                request,
                "Incorrect username or password"
            )

            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):

    logout(request)

    return redirect('login')


# =========================
# USER REGISTRATION
# =========================

def user_register(request):

    if request.method == "POST":

        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        place = request.POST['place']
        username = request.POST['username']
        password = request.POST['password']

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        UserProfile.objects.create(
            USER=user,
            name=name,
            email=email,
            phone=phone,
            place=place
        )

        return redirect('login')

    return render(request, 'user_register.html')


# =========================
# ADMIN SECTION
# =========================

@login_required
def admin_home(request):

    total_users = User.objects.filter(
        is_superuser=False
    ).count()

    total_blogs = Blog.objects.count()

    context = {
        'total_users': total_users,
        'total_blogs': total_blogs
    }

    return render(request, 'admin_home.html', context)


@login_required
def viewblogs_admin(request):

    blogs = Blog.objects.all().order_by('-created_at')

    return render(
        request,
        'viewblogs_admin.html',
        {'blogs': blogs}
    )


@login_required
def view_users(request):

    users = UserProfile.objects.all()

    return render(
        request,
        'view_users.html',
        {'users': users}
    )


@login_required
def admin_delete_blog(request, id):

    blog = Blog.objects.get(id=id)

    blog.delete()

    return redirect('viewblogs_admin')


# =========================
# USER HOME
# =========================

@login_required
def user_home(request):

    blogs = Blog.objects.filter(USER=request.user)

    total_likes = 0
    total_comments = 0

    for blog in blogs:

        total_likes += blog.like_set.count()
        total_comments += blog.comment_set.count()

    context = {
        'blogs': blogs,
        'total_blogs': blogs.count(),
        'total_likes': total_likes,
        'total_comments': total_comments
    }

    return render(request, 'user_home.html', context)


# =========================
# BLOG SECTION
# =========================

@login_required
def user_addblog(request):

    if request.method == "POST":

        title = request.POST['title']
        content = request.POST['content']

        image = None

        if 'image' in request.FILES:

            image = request.FILES['image']

        Blog.objects.create(
            USER=request.user,
            title=title,
            content=content,
            image=image
        )

        return redirect('myblog')

    return render(request, 'user_addblog.html')


@login_required
def myblog(request):

    search = request.GET.get('search')

    blogs = Blog.objects.filter(
        USER=request.user
    ).order_by('-id')

    if search:

        blogs = blogs.filter(
            title__icontains=search
        )

    return render(
        request,
        'myblog.html',
        {'blogs': blogs}
    )


@login_required
def edit_blog(request, id):

    blog = Blog.objects.get(id=id)

    if request.method == "POST":

        blog.title = request.POST['title']
        blog.content = request.POST['content']

        if 'image' in request.FILES:

            blog.image = request.FILES['image']

        blog.save()

        return redirect('myblog')

    return render(
        request,
        'edit_blog.html',
        {'blog': blog}
    )


@login_required
def delete_blog(request, id):

    blog = Blog.objects.get(id=id)

    blog.delete()

    return redirect('myblog')


@login_required
def blog_detail(request, id):

    blog = Blog.objects.get(id=id)

    return render(
        request,
        'blog_detail.html',
        {'blog': blog}
    )


# =========================
# LIKE SECTION
# =========================

@login_required
def like_blog(request, id):

    blog = Blog.objects.get(id=id)

    like = Like.objects.filter(
        USER=request.user,
        BLOG=blog
    ).first()

    if like:

        like.delete()

    else:

        Like.objects.create(
            USER=request.user,
            BLOG=blog
        )

    return redirect(
        request.META.get(
            'HTTP_REFERER',
            'myblog'
        )
    )


# =========================
# COMMENT SECTION
# =========================

@login_required
def add_comment(request, id):

    blog = Blog.objects.get(id=id)

    if request.method == "POST":

        comment = request.POST['comment']

        Comment.objects.create(
            USER=request.user,
            BLOG=blog,
            comment=comment
        )

    return redirect(
        request.META.get(
            'HTTP_REFERER',
            'myblog'
        )
    )


# =========================
# EXPLORE PAGE
# =========================

@login_required
def explore(request):

    blogs = Blog.objects.all().order_by('-id')

    return render(
        request,
        'explore.html',
        {'blogs': blogs}
    )


# =========================
# PROFILE SECTION
# =========================

@login_required
def user_profile(request):

    profile = UserProfile.objects.get(
        USER=request.user
    )

    return render(
        request,
        'user_profile.html',
        {'profile': profile}
    )


@login_required
def update_profile_pic(request):

    profile = UserProfile.objects.get(
        USER=request.user
    )

    if request.method == "POST":

        if 'profile_pic' in request.FILES:

            profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            return redirect('user_profile')

    return render(
        request,
        'update_profile_pic.html'
    )


@login_required
def edit_profile(request):

    profile = UserProfile.objects.get(
        USER=request.user
    )

    if request.method == "POST":

        profile.name = request.POST['name']
        profile.phone = request.POST['phone']
        profile.place = request.POST['place']

        if 'bio' in request.POST:

            profile.bio = request.POST['bio']

        if 'profile_pic' in request.FILES:

            profile.profile_pic = request.FILES['profile_pic']

        profile.save()

        return redirect('user_profile')

    return render(
        request,
        'edit_profile.html',
        {'profile': profile}
    )


# =========================
# SAVE BLOGS
# =========================

@login_required
def save_blog(request, id):

    blog = Blog.objects.get(id=id)

    saved = Save.objects.filter(
        USER=request.user,
        BLOG=blog
    )

    if saved.exists():

        saved.delete()

    else:

        Save.objects.create(
            USER=request.user,
            BLOG=blog
        )

    return redirect(
        request.META.get(
            'HTTP_REFERER'
        )
    )


@login_required
def saved_blogs(request):

    saved = Save.objects.filter(
        USER=request.user
    )

    return render(
        request,
        'saved_blogs.html',
        {'saved': saved}
    )