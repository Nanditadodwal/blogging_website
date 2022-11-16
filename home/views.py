from django.shortcuts import render, redirect
from .form import *
from django.contrib.auth import logout
from django.core.paginator import Paginator
import time

def logout_view(request):
    logout(request)
    return redirect('/')

def home(request):
    context = {'blogs' :BlogModel.objects.all()}
    return render(request, 'home.html', context)


def login_view(request):
    return render(request, 'login.html')

def blog_detail(request, slug):
    # blog_object = BlogModel.objects.get(slug = slug)
    # blog_object.post_views = blog_object.post_views +1 
    # blog_object.save()
    # time.sleep()
    context={}
    try:
        blog_obj= BlogModel.objects.filter(slug = slug).first()
        context['content'] =blog_obj.content
        context['image'] =blog_obj.image

        
        # blog_obj.post_views = 0
        context['post_views'] =blog_obj.post_views + 1
        blog_obj.post_views.save()
    except Exception as e:
        print(e)
  

    return render(request, 'blog_detail.html', context)
    
    

def see_blog(request):
    
    context={}
    try:
        blog_objs = BlogModel.objects.filter(user = request.user)
        context['blog_objs'] = blog_objs
    except Exception as e:
        print(e)
    return render(request, 'see_blog.html', context)


def blog_delete(request, id):
    try:
        blog_obj = BlogModel.objects.get(id=id)

        if blog_obj.user == request.user:
            blog_obj.delete()


    except Exception as e:
        print(e) 

    return redirect('/see-blog/')

def blog_update(request, slug):
    context={}
    try:
        
        blog_obj = BlogModel.objects.get(slug = slug)
       
        if blog_obj.user != request.user:
            return redirect('/')
        
        initial_dict={'content' : blog_obj.content}
        form = BlogForm(initial=initial_dict)
        if request.method == 'POST' :
            form = BlogForm(request.POST)
            image = request.FILE['image']
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']
            BlogModel.objects.create(
                user=user, title = title,
                content = content, image = image
            )

        context['blog_obj'] = blog_obj
        context['form'] = form
    except Exception as e:
        print(e)

    return render(request, 'update_blog.html')

def register_view(request):
    return render(request, 'register.html')

def add_blog(request):
   context = {'form': BlogForm}
   try:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            print(request.FILES)
            image = request.FILES.get('image', '')
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                print('Valid')
                content = form.cleaned_data['content']

            blog_obj = BlogModel.objects.create(
                user=user, title=title,
                content=content, image=image
            )
            print(blog_obj)
            return redirect('/add-blog/')
   except Exception as e:
        print(e)

   return render(request, 'add_blog.html', context)

def verify(request, token):
    try:
        profile_obj = Profile.objects.filter(token=token).first()

        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
        return redirect('/login/')

    except Exception as e:
        print(e)

    return redirect('/')



# from django.core.paginator import Paginator
# def index(request):
# 	posts = BlogModel.objects.all() # fetching all post objects from database
# 	p = Paginator(posts, 5) # creating a paginator object
# 	# getting the desired page number from url
# 	page_number = request.GET.get('page')
# 	try:
# 		page_obj = p.get_page(page_number) # returns the desired page object
# 	except PageNotAnInteger:
# 		# if page_number is not an integer then assign the first page
# 		page_obj = p.page(1)
# 	except EmptyPage:
# 		# if page is empty then return last page
# 		page_obj = p.page(p.num_pages)
# 	context = {'page_obj': page_obj}
# 	# sending the page object to index.html
# 	return render(request, 'home.html', context)
