"""
URL configuration for demoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from demoproject import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    path('',views.base,name='base'),
    path('user/',views.user,name='user'),
    path('login/',views.login_view,name='login'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('user_register/',views.user_register,name='user_register'),
    path('user_home/',views.user_home,name='user_home'),
    path('user_addblog/',views.user_addblog,name='user_addblog'),
    path('myblog/',views.myblog,name='myblog'),
    path('viewblogs_admin/',views.viewblogs_admin,name='viewblogs_admin'),
     path('view_users/',views.view_users,name='view_users'),
    path('edit_blog/<int:id>/',views.edit_blog,name='edit_blog'),
   path('delete_blog/<int:id>/',views.delete_blog,name='delete_blog'),
   path('logout/',views.logout_view,name='logout'),
   path('', views.home, name='home'),
   path('about/', views.about, name='about'),
   path('user_profile/',views.user_profile,name='user_profile'),
   path('update_profile_pic/',views.update_profile_pic, name='update_profile_pic'),
   path('like_blog/<int:id>/',views.like_blog,name='like_blog'),
   path('add_comment/<int:id>/', views.add_comment,name='add_comment'),
   path('admin_delete_blog/<int:id>/',views.admin_delete_blog, name='admin_delete_blog'),
   path('explore/',views.explore,name='explore'),
   path('edit_profile/',views.edit_profile,name='edit_profile'),
   path('blog_detail/<int:id>/',views.blog_detail,name='blog_detail'),
   path('save_blog/<int:id>/',views.save_blog,name='save_blog'),
   path('saved_blogs/', views.saved_blogs,name='saved_blogs'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
