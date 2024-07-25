from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.search import TrigramSimilarity
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import ListView, DetailView
from taggit.models import Tag

from blog.utils import menu
from blog.models import Posts, Comment
from .forms import EmailPostForm, AddCommentForm, SearchForm, AddPostForm

from django.views.decorators.http import require_POST


# Create your views here.


class PostsListHome(ListView):
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    extra_context = {
        'title': 'Блог Jantric',
        'menu': menu,
        'cat_selected': 0,
        'tag': 0,
        'form_search': SearchForm,
    }
    paginate_by = 4

    def get_queryset(self):
        return Posts.published.all().select_related('cats')


@login_required
def post_share(request, post_slug):
    post = get_object_or_404(Posts, slug=post_slug, is_published=Posts.Status.PUBLISH)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} рекомендует Вам прочесть " \
                      f"{post.title}"
            message = f'Прочитайте {post.title} на {post_url}\n\n' \
                      f"{cd['name']} оставил(-а) вам сообщение: {cd['comments']}"
            send_mail(subject, message, 'eliskarp@yandex.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    data = {
        'title': 'Блог Jantric',
        'menu': menu,
        'post': post,
        'form': form,
        'sent': sent
    }
    return render(request, 'blog/post/share.html', context=data)


class PostDetailView(DetailView):
    template_name = 'blog/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        # self.kwarg = context.view.kwargs
        context['menu'] = menu
        context['cat_selected'] = context['post'].cats.slug if context['post'].cats else 0
        context['comments'] = Comment.objects.filter(active=Comment.Status.PUBLISH, post=context['post'])
        context['form_search'] = SearchForm()
        context['form'] = AddCommentForm()

        # context['tags_selected'] = context['post'].tags

        post_tags_id = context['post'].tags.values_list('id', flat=True)
        similar_posts = Posts.published.filter(tags__in=post_tags_id).exclude(id=context['post'].id)
        similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-date_publish')[:4]
        context['similar_posts'] = similar_posts

        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Posts.published, slug=self.kwargs[self.slug_url_kwarg],
                                 date_publish__year=self.kwargs['year'],
                                 date_publish__month=self.kwargs['month'],
                                 date_publish__day=self.kwargs['day'],
                                 is_published=Posts.Status.PUBLISH
                                 )


class CatShowList(ListView):
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Posts.published.filter(cats__slug=self.kwargs['cat_slug']).select_related('cats')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        cat = context['posts'][0].cats
        context['title'] = cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.slug
        context['form_search'] = SearchForm
        return context


@permission_required(perm='blog.add_posts', raise_exception=True)
def add_post(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('blog:list_post'))
    else:
        form = AddPostForm()
    data = {
        'title': 'Добавить пост',
        'form': form
    }
    return render(request, 'blog/post/add_post.html', context=data)


class TagShowList(ListView):
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False
    tag = None

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        self.tag = tag
        return Posts.published.filter(tags__in=[tag])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['title'] = self.tag.name
        context['tag'] = self.tag
        context['menu'] = menu
        context['tags_selected'] = self.tag.slug
        context['form_search'] = SearchForm
        return context



def posts_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + \
                            SearchVector('content', weight='B')
            search_query = SearchQuery(query)
            # results = Posts.published.annotate(similarity=TrigramSimilarity('title', query)
            #                                    ).filter(similarity__gt=0.1).order_by('-similarity')
            results = Posts.published.annotate(search=search_vector,
                                               rank=SearchRank(search_vector, search_query)
                                               ).filter(rank__gte=0.1).order_by('-rank')

    data = {
        'title': 'Поиск',
        'menu': menu,
        'posts': results,
        'form_search': form,
        'cat_selected': 0,
        'tag': 0
    }
    return render(request, 'blog/search.html', context=data)



@login_required
def add_comment(request, post_slug):
    post = get_object_or_404(Posts.published, slug=post_slug)
    comment = None
    form = AddCommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    data = {
        'menu': menu,
        'post': post,
        'form': form,
        'comment': comment
    }
    return render(request, 'blog/post/add_comment.html', context=data)
