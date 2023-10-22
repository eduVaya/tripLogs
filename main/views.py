from django.shortcuts import render, redirect
from .forms import RegisterForm, PostForm, EntryForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import Post, Entry

@login_required(login_url="/login")
def home(request):
    posts = Post.objects.all()
    if request.method == 'POST':
        post_id = request.POST.get('post-id')
        post = Post.objects.filter(id=post_id).first()
        if post and post.author == request.user:
            post.delete()
    return render(request, 'main/home.html', {"posts": posts})

@login_required(login_url="/login")
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/home')
    return render(request, 'main/create_post.html')

@login_required(login_url="/login")
def update_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES, instance=post)
        if post_form.is_valid():
            # post = post_form.save(commit=False)
            # post.author = request.user
            # post.save()
            post_form.save()
            return redirect('/home')
    return render(request, 'main/create_post.html', {"post": post})

@login_required(login_url="/login")
def entries(request, post_id):
    post = Post.objects.get(id=post_id)
    entries = Entry.objects.filter(post_id=post_id)
    return render(request, 'main/entries.html', {"post":post,"entries":entries})

@login_required(login_url="/login")
def create_entry(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        entryForm = EntryForm(request.POST, request.FILES)
        if entryForm.is_valid():
            entry = entryForm.save(commit=False)
            entry.post = post
            entry.author = request.user
            entry.save()
        return redirect(f'/entries/{post_id}')
    else:
        print('here')
        entryForm = EntryForm()
    return render(request, 'main/create_entry.html', { "post": post})

@login_required(login_url="/login")
def delete_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    if entry and entry.author == request.user:
        entry.delete()
    entries = Entry.objects.filter(post_id=entry.post_id)
    post = Post.objects.get(id=entry.post_id)
    return render(request, 'main/entries.html', {"post":post,"entries":entries})

@login_required(login_url="/login")
def update_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    post = Post.objects.get(id=entry.post_id)
    if request.method == 'POST':
        entry_form = EntryForm(request.POST, request.FILES, instance=entry)
        if entry_form.is_valid():
            entry_form.save()
            entries = Entry.objects.filter(post_id=post.id)
            return render(request, 'main/entries.html', {"post":post,"entries":entries})
    return render(request, 'main/create_entry.html', {"post": post, "entry": entry})

@login_required(login_url="/login")
def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'registration/sign_up.html', {"form":form})