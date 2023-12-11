from django.http import Http404
from django.shortcuts import render, redirect
from .models import Topic, Entry
from . import forms
from django.contrib.auth.decorators import login_required


# Create your views here.
def verify_user(request_user, owner):
    if request_user.user == owner.owner:
        return True
    else:
        return False


def index(request):
    """ a home page """
    return render(request, 'learning_logs/index.html')


@login_required(login_url='users:login')
def topics(request):
    """a topics page"""
    my_topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': my_topics}
    return render(request, "learning_logs/topics.html", context=context)


@login_required(login_url='users:login')
def topic_entries(request, topic_id):
    """ a topic view/page"""
    wanted_topic = Topic.objects.get(id=topic_id)
    gate_pass = verify_user(request, wanted_topic)
    if not gate_pass:
        raise Http404

    wanted_topic_entries = wanted_topic.entry_set.order_by('date_added')
    context = {"topic": wanted_topic, "entries": wanted_topic_entries}
    return render(request, "learning_logs/topic.html", context=context)


@login_required(login_url='users:login')
def add_new_topic(request):
    if request.method != "POST":
        form = forms.TopicForm()
    else:
        form = forms.TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect("learning_logs:topics")
    context = {"form": form}
    return render(request, "learning_logs/add_topic.html", context)


@login_required(login_url='users:login')
def add_new_entry(request, topic_id):
    current_topic = Topic.objects.get(id=topic_id)
    gate_pass = verify_user(request,current_topic)

    if not gate_pass:
        raise Http404

    if request.method != 'POST':
        form = forms.EntryForm()
    else:
        form = forms.EntryForm(data=request.POST)
        if form.is_valid():
            this_entry = form.save(commit=False)
            this_entry.topic = current_topic
            this_entry.save()
            return redirect("learning_logs:topic", topic_id=topic_id)
    context = {"form": form, "c_topic": current_topic}
    return render(request, "learning_logs/add_entries.html", context)


@login_required(login_url='users:login')
def edit_entry(request, entry_id):
    to_be_edited = Entry.objects.get(id=entry_id)
    topic = to_be_edited.topic

    if request.method != "POST":
        form = forms.EntryForm(instance=to_be_edited)
    else:
        form = forms.EntryForm(instance=to_be_edited, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("learning_logs:topic", topic.id)
    context = {"form": form, "topic": topic, "entry": to_be_edited}
    return render(request, "learning_logs/edit_entries.html", context)
