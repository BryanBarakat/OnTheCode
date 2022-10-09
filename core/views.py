from hmac import new
import re
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile,Post,LikePost,FollowersCount
from itertools import chain
import random

# Create your views here.

@login_required(login_url="signin")
def index(request):
    user_object = User.objects.get(username= request.user.username)
    user_profile = Profile.objects.get(user = user_object)
    image = user_profile.profile_image
    
    user_following_list = []
    feed = []
    
    user_following = FollowersCount.objects.filter(follower = request.user.username)
    
    for user in user_following:
        user_following_list.append(user)
        
    for username in user_following_list:
        feed_lists = Post.objects.filter(user = username)
        feed.append(feed_lists)
        
    #transforming queryset objects to list
    feed_list = list(chain(*feed))
    
    # user suggestions
    all_users = User.objects.all()
    user_following_all = []
    
    for user in user_following:
        user_list = User.objects.get(username=user.user)
        user_following_all.append(user_list)
        
    new_suggestions_list = [x for x in list(all_users) if(x not in list(user_following_all))]
    current_user = User.objects.filter(username=request.user.username)
    final_suggestions_list = [x for x in list(new_suggestions_list) if(x not in list(current_user))]
    random.shuffle(final_suggestions_list)
    
    username_profile = []
    username_profile_list = []
    
    for users in final_suggestions_list:
        username_profile.append(users.id)
        
    for ids in username_profile:
        profile_lists = Profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_lists)
        
    suggestions_username_profile_list = list(chain(*username_profile_list))
    
    return render(request,'index.html',{'image':image,'posts':feed_list,'suggestions_username_profile_list':suggestions_username_profile_list[:4]})

def signUp(request):
    if(request.method == "POST"):
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        
        if password == password2:
            if (User.objects.filter(email = email).exists()):
                messages.info(request, 'Email already exists')
                return redirect('signup')
            elif (User.objects.filter(username = username).exists()):
                messages.info(request, 'Username already exists')
                return redirect('signup')
            else:
                user = User.objects.create_user(username = username, email = email,password = password)
                user.save()
                
                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request,user_login)
                
                #create a Profile object for the new user
                user_model = User.objects.get(username = username)
                new_profile = Profile.objects.create(user = user_model,id_user = user_model.id)
                new_profile.save()
                return redirect("settings")
        else:
            messages.info(request, "Passwords do not much")
            return redirect("signup")
    else:
        return render(request,'signup.html')
    
def signIn(request):
    if(request.method == "POST"):
        username = request.POST["username-login"]
        password = request.POST["password-login"]
        
        user = auth.authenticate(username = username,password = password)
        
        if(user is not None):
            auth.login(request,user)
            return redirect('index')
        else: 
            messages.info(request,'Credentials Invalid')
            return redirect("signin")
    else:
        return render(request,'signin.html')
    
    
@login_required(login_url="signin") 
def logOut(request):
    auth.logout(request)
    return redirect("signin")

@login_required(login_url="signin") 
def settings(request):
    user_profile = Profile.objects.get(user = request.user)
    
    if(request.method == "POST"):
        if(request.FILES.get('image') == None):
            bio = request.POST["bio"]
            location = request.POST["location"]
            website = request.POST["website"]
            name = request.POST["name"]
            
            image = user_profile.profile_image
            
            user_profile.website = website
            user_profile.sur_name = name
            user_profile.profile_image = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            return redirect('/settings')
        if(request.FILES.get("image") != None):
            bio = request.POST["bio"]
            location = request.POST["location"]
            website = request.POST["website"]
            name = request.POST["name"]
            
            image = request.FILES.get("image")
            
            user_profile.profile_image = image
            user_profile.website = website
            user_profile.sur_name = name
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            return redirect('/settings')
    return render(request,"settings.html",{'user_profile':user_profile})


@login_required(login_url="signin") 
def upload(request):    
    if(request.method == "POST"):
        user = request.user.username
        file = request.FILES.get('file-post')
        description = request.POST["desc-post"]
            
        new_post = Post.objects.create(user=user,image=file,caption=description)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')
    

@login_required(login_url="signin") 
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    
    post = Post.objects.get(id=post_id)
    
    like_filter = LikePost.objects.filter(post_id=post_id,username = username).first()
    
    if(like_filter == None):
        new_like = LikePost.objects.create(post_id=post_id,username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')
    
    
@login_required(login_url="signin")
def profile(request,pk):
    user = User.objects.get(username = pk)
    user_image = Profile.objects.get(user=user)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)
    current_user = user_image.user
    image = user_image.profile_image
    user_name = user_image.sur_name
    website = user_image.website
    bio = user_image.bio
    
    follower = request.user.username
    user = pk
    
    if(FollowersCount.objects.filter(follower= follower,user=user).first()):
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
        
    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))
    
    context = {
        'current_user':current_user,
        'user_name':user_name,
        'website':website,
        'bio':bio,
        'image':image,
        'user_posts':user_posts,
        'user_post_length':user_post_length,
        'button_text':button_text,
        'user_followers':user_followers,
        'user_following':user_following,
    }
    
    return render(request,'profile.html',context)


@login_required(login_url="signin")
def follow(request):
    if(request.method == "POST"):
        follower = request.POST['follower']
        user = request.POST['user']
        
        if(FollowersCount.objects.filter(follower=follower,user=user).first()):
            delete_follower = FollowersCount.objects.get(follower=follower,user=user)
            delete_follower.delete()
            return redirect(('/profile/' + user))
        else:
            new_follower = FollowersCount.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect(('/profile/' + user))
    else:
        return redirect("/")
    

@login_required(login_url="signin")
def search(request):
    if(request.method == 'POST'):
        username = request.POST["username"]
        username_object = User.objects.filter(username__icontains = username)
        
        username_profile = []
        username_profile_list = []
        
        for user in username_object:
            username_profile.append(user.id)
            
        for id in username_profile:
            profile_lists = Profile.objects.filter(id_user=id)
            username_profile_list.append(profile_lists)
            
        username_profile_list = list(chain(*username_profile_list))
    return render(request,'search.html',{'username_profile_list':username_profile_list,'username':username})