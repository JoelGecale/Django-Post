from typing import Any
from django import http
from django.contrib.auth.models import User
from django.views.generic import DetailView, View, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.db.models import Count, Q
from django.db.models import Subquery, OuterRef, IntegerField, BooleanField
from django.db.models.functions import Cast

from feed.models import Post
from followers.models import Follower
from profiles.models import Profile


class ProfileDetailView(DetailView):
    http_method_names=["get"]
    template_name="profile/detail.html"
    model = User
    context_object_name="user"
    slug_field="username"
    slug_url_kwarg="username"

    def dispatch(self, request, *args, **kwargs):
        self.request=request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user=self.get_object()
        context=super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.filter(author=user).count
        context['total_followers'] = Follower.objects.filter(following=user).count

        if self.request.user.is_authenticated:
            context['you_follow'] = Follower.objects.filter(following=user, followed_by=self.request.user).exists
        return context

class FollowView(LoginRequiredMixin, View):
    http_method_names=["post"]

    def post(self, request, *args, **kwargs):
        data=request.POST.dict()

        if "action" not in data or "username" not in data:
            return HttpResponseBadRequest("Missing Data")
    
        try:
            other_user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return HttpResponseBadRequest("Missing user")
        
        if data['action'] == "follow":
            follower, created = Follower.objects.get_or_create(
                followed_by=request.user,
                following=other_user
            )
        else:
            try:
                follower = Follower.objects.get(
                    followed_by=request.user,
                    following=other_user,                    
                )
            except Follower.DoesNotExist:
                follower=None
            
            if follower:
                follower.delete()
                
        return JsonResponse({
            'success': True,
            'wording': "Unfollow" if data['action'] == "follow" else "Follow"
        })


class MyProfileView(LoginRequiredMixin, UpdateView):
    http_method_names=["get","put","post"]
    template_name="profile/myprofile.html"
    model = Profile
    fields=['name', 'tagline', 'id', 'image', 'cover']
    context_object_name="myprofile"
    slug_field="id"
    slug_url_kwarg="id"
    success_url="/"

    def dispatch(self, request, *args, **kwargs):
        self.request=request
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        user=self.get_object()
        context=super().get_context_data(**kwargs)
        context['total_posts'] = Post.objects.filter(author=user.user).count
        context['total_followers'] = Follower.objects.filter(following=user.user).count
        return context

class UsersView(ListView):
    http_method_names = ["get"]
    template_name="profile/users.html"
    model = Profile
    context_object_name = "users"
    queryset = Profile.objects.all().order_by('user')[0:60]
    
    def dispatch(self, request, *args, **kwargs):
        self.request=request
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        context =  super().get_context_data(*args, **kwargs)
        users = Profile.objects.filter(~Q(user=self.request.user)).order_by('user')[0:80]                
        posts = Post.objects.values("author").annotate(total_posts=Count("author"))
        followers = Follower.objects.values("following").annotate(total_followers=Count("following"))
        you_follow_qs = Follower.objects.values("following").annotate(you_follow=Count("following", filter=Q(followed_by=self.request.user)))
       # you_follow_sub= you_follow_qs.filter(followed_by=self.request.user)
        #you_follow = Follower.objects.filter(followed_by=self.request.user)
        #print(you_follow_qs)

        subquery_qs_posts = posts.filter(author=OuterRef('id'))
        subquery_qs_followers = followers.filter(following=OuterRef('id'))
        subquery_qs_you_follow = you_follow_qs.filter(following=OuterRef('id'))

       # print(subquery_qs_followers)
        #print(subquery_qs_you_follow)

        context['users'] = users.annotate(total_posts = Cast(Subquery(subquery_qs_posts.values('total_posts')[:1]), output_field=IntegerField()),
                                        total_followers = Cast(Subquery(subquery_qs_followers.values('total_followers')[:1]), output_field=IntegerField()),
                                        you_follow = Cast(Subquery(subquery_qs_you_follow.values('you_follow')[:1]), output_field=IntegerField()))
    
        return context

    
