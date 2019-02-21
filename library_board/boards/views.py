from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Board, Topic, Post
from .forms import NewTopicForm,PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView,ListView, DeleteView
from django.utils import timezone
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.urls import reverse
"""
--old method--
def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})
"""
class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'

"""
--old method--

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    queryset = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    page = request.GET.get('page', 1)

    #no of posts in each page(3)
    paginator = Paginator(queryset, 3)

    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        # fallback to the first page
        topics = paginator.page(1)
    except EmptyPage:
        # probably the user tried to add a page number
        # in the url, so we fallback to the last page
        topics = paginator.page(paginator.num_pages)

    return render(request, 'topics.html', {'board': board, 'topics': topics})
   """



class TopicUpdateView(UpdateView):
    model = Topic
    fields = ('subject','message')
    template_name = 'edit_topic.html'
    pk_url_kwarg = 'topic_pk'
    context_object_name = 'topic'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        topic = form.save(commit=False)
        topic.updated_by = self.request.user
        topic.updated_at = timezone.now()
        topic.save()
        return redirect('topic', pk=topic.board.pk, topic_pk=topic.pk)






class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-created_at').annotate(replies=Count('posts')-1)
        return queryset



class TopicDeleteView(DeleteView):
    model = Topic
    template_name = 'delete_topic.html'
    pk_url_kwarg = 'topic_pk'
    def get_success_url(self): 
        return reverse_lazy('home')
    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)
"""
    def form_valid(self, form):
        topic = form.save(commit=False)
        topic.delete()
        topic.save()
        return redirect('topics', pk=topic.board.pk, topic_pk=topic.pk)
"""

@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.created_by = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=pk,topic_pk=topic.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views +=1 
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})

"""
--old method--
@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            topic.last_updated = timezone.now() 
            topic.save()   
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})
"""




@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            topic.created_time = timezone.now()
            topic.save()

            topic_url = reverse('topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )

            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})







@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        """
        self.topic.views += 1
        self.topic.save()
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)
        """

        session_key = 'viewed_topic_{}'.format(self.topic.pk)  # <-- here
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True           # <-- until here

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)


    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    pk_url_kwarg = 'post_pk'
    def get_success_url(self): 
        return reverse_lazy('topics')
    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.delete()
        post.save()
        return redirect('topics', pk=post.topic.board.pk, topic_pk=post.topic.pk)