from typing import Any
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.core.mail import send_mail
from django.db.models import Count
from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, FormView
from taggit.models import Tag
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from common.utils import unique_slugify



from .serializers import PostsSerializer
 
from .models import Posts, Comment
from .forms import EmailPostForm, AddCommentForm, SearchForm, AddPostForm

from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class PostsAPIView(APIView):

    def get(self, request):
        lst = Posts.objects.all().values()
        return Response({'posts': list(lst)})

    def post(self, request):
        post_new = Posts.objects.create(
            title=request.data['title'],
            content=request.data['content'],
            cats_id=request.data['cats_id']
        )
        return Response({'post': post_new.get_absolute_url()})
# class PostsAPIView(generics.ListAPIView):
#     queryset = Posts.objects.all()
#     serializer_class = PostsSerializer


class PostsListHome(ListView):
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    paginate_by = 4
    form_search = SearchForm()

        
    def get_queryset(self):
        if 'query' in self.request.GET:
            form = SearchForm(self.request.GET)
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
                self.form_search = form
                
                return results.select_related('cats')

        # return render(request, 'blog/search.html', context=data)

        return Posts.published.all().select_related('cats')

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Поиск' if self.form_search else 'Блог Jantric'
        context['cat_selected'] = 0
        context['tag'] = 0
        context['form_search'] = self.form_search
        return context
        

class PostShareView(LoginRequiredMixin, FormView):
    form_class = EmailPostForm
    template_name = 'blog/post/share.html'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.post_object = get_object_or_404(Posts, slug=self.kwargs['post_slug'], is_published=Posts.Status.PUBLISH)
        
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        
        self.post_object = get_object_or_404(Posts, slug=self.kwargs['post_slug'], is_published=Posts.Status.PUBLISH)
        form = self.get_form()
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(self.post_object.get_absolute_url())
            subject = f"{cd['name']} рекомендует Вам прочесть " \
                      f"{self.post_object.title}"
            message = f'Прочитайте {self.post_object.title} на {post_url}\n\n' \
                      f"{cd['name']} оставил(-а) вам сообщение: {cd['comments']}"
            send_mail(subject, message, 'eliskarp@yandex.com', [cd['to']])
            
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Блог Jantric'
        context['post'] = self.post_object
        return context
    
    def get_success_url(self) -> str:

        return reverse_lazy('blog:detail_post', kwargs={
                                                        'year': self.post_object.date_publish.year,
                                                        'month': self.post_object.date_publish.month,
                                                        'day': self.post_object.date_publish.day,
                                                        'post_slug': self.post_object.slug
                                                        })

# @login_required
# def post_share(request, post_slug):
#     post = get_object_or_404(Posts, slug=post_slug, is_published=Posts.Status.PUBLISH)
#     sent = False

#     if request.method == 'POST':
#         form = EmailPostForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             post_url = request.build_absolute_uri(post.get_absolute_url())
#             subject = f"{cd['name']} рекомендует Вам прочесть " \
#                       f"{post.title}"
#             message = f'Прочитайте {post.title} на {post_url}\n\n' \
#                       f"{cd['name']} оставил(-а) вам сообщение: {cd['comments']}"
#             send_mail(subject, message, 'eliskarp@yandex.com', [cd['to']])
#             sent = True
#     else:
#         form = EmailPostForm()
#     data = {
#         'title': 'Блог Jantric',
#         'post': post,
#         'form': form,
#         'sent': sent
#     }
#     return render(request, 'blog/post/share.html', context=data)


class PostDetailView(DetailView):
    template_name = 'blog/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['post'].title
        # self.kwarg = context.view.kwargs
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
        context['cat_selected'] = cat.slug
        context['form_search'] = SearchForm
        return context


class AddPostView(PermissionRequiredMixin, CreateView):
    permission_required = 'blog.add_posts'
    raise_exception = True

    model = Posts
    form_class = AddPostForm
    template_name = 'blog/post/add_post.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs: any) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить пост'
        return context

# @permission_required(perm='blog.add_posts', raise_exception=True)
# def add_post(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return HttpResponseRedirect(reverse('blog:list_post'))
#     else:
#         form = AddPostForm()
#     data = {
#         'title': 'Добавить пост',
#         'form': form
#     }
#     return render(request, 'blog/post/add_post.html', context=data)


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
        context['tags_selected'] = self.tag.slug
        context['form_search'] = SearchForm
        return context


# def posts_search(request):
#     form = SearchForm()
#     query = None
#     results = []

#     if 'query' in request.GET:
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             search_vector = SearchVector('title', weight='A') + \
#                             SearchVector('content', weight='B')
#             search_query = SearchQuery(query)
#             # results = Posts.published.annotate(similarity=TrigramSimilarity('title', query)
#             #                                    ).filter(similarity__gt=0.1).order_by('-similarity')
#             results = Posts.published.annotate(search=search_vector,
#                                                rank=SearchRank(search_vector, search_query)
#                                                ).filter(rank__gte=0.1).order_by('-rank')

#     data = {
#         'title': 'Поиск',
#         'posts': results,
#         'form_search': form,
#         'cat_selected': 0,
#         'tag': 0
#     }
#     return render(request, 'blog/search.html', context=data)


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = AddCommentForm
    template_name = "blog/post/add_comment.html"
    comment = None

    def post(self, request, *args, **kwargs):
        post_object = get_object_or_404(Posts.published, slug=kwargs['post_slug'])
        self.post_object = post_object
        form = self.get_form()
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.post = self.post_object
            self.comment = self.object
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['post'] = self.post_object
        context['comment'] = self.get_object()
        return context
    
    def get_success_url(self) -> str:
        return self.post_object.get_absolute_url()



# @login_required
# def add_comment(request, post_slug):
#     post = get_object_or_404(Posts.published, slug=post_slug)
#     comment = None
#     form = AddCommentForm(request.POST)
#     if form.is_valid():
#         comment = form.save(commit=False)
#         comment.post = post
#         comment.save()
#     data = {
#         'post': post,
#         'form': form,
#         'comment': comment
#     }
#     return render(request, 'blog/post/add_comment.html', context=data)
