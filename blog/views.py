from django.views.generic import ListView, DetailView
from account.models import User
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from account.mixins import AuthorAccessMixin
# from django.http import Http404
from .models import Article, Category, Ads
from django.db.models import Q
# Create your views here.


class ArticleList(ListView):
    queryset = Article.objects.published()
    paginate_by = 4


class ArticleDetail(DetailView):
    def get_object(self):
        slug = self.kwargs.get('slug')
        article = get_object_or_404(Article.objects.published(), slug=slug)
        ip_address = self.request.user.ip_address

        if ip_address not in article.hits.all():
            article.hits.add(ip_address)

        return article


class ArticlePreview(AuthorAccessMixin, DetailView):
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)


class CategoryList(ListView):
    paginate_by = 4
    template_name = 'blog/category_list.html'

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.articels.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


class AuthorList(ListView):
    paginate_by = 4
    template_name = 'blog/author_list.html'

    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return author.articels.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context


class SearchList(ListView):
    paginate_by = 4
    template_name = 'blog/search_list.html'

    def get_queryset(self):
        search = self.request.GET.get('q')
        return Article.objects.filter(Q(description__icontains=search) | Q(title__icontains=search))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('q')
        return context


def CategoryLists(request):
    return render(request, 'blog/category_lists.html')


def ad(request):
    ads = Ads.adsss.published()
    context = {
        "article_ads": Ads.adsss.all()
    }
    return render(request, 'blog/article_list.html', context)
