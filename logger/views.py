from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import Http404
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'base.html')

@login_required
def topic(request):
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics':topics}
    return render(request, 'topics.html', context)

@login_required
def add_topic(request):
    if request.method == 'POST':
        topic_form = TopicForm(data=request.POST)
        if topic_form.is_valid():
            new_topic = topic_form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('logger:topic')
    else:
        topic_form = TopicForm()
    context = {'topic_form':topic_form}
    return render(request, 'new_topic.html', context)

@login_required
def entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic,'entries':entries}
    return render(request, 'entries.html', context)

@login_required
def add_entry(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    if request.method == 'POST':
        entry_form = EntryForm(data=request.POST)
        if entry_form.is_valid():
            new_entry = entry_form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('logger:entry', topic_id=topic_id)
    else:
        entry_form = EntryForm()
    context = {'topic':topic, 'entry_form':entry_form}
    return render(request, 'new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise http404

    if request.method == 'POST':
        entry_form = EntryForm(instance=entry, data=request.POST)
        if entry_form.is_valid():
            entry_form.save()
            return redirect('logger:entry', topic_id=topic.id)
    else:
        entry_form = EntryForm(instance=entry)
    context = {'entry':entry, 'topic':topic, 'entry_form':entry_form}
    return render(request, 'edit_entry.html', context)


