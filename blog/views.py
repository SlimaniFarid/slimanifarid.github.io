from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView

from .models import Article, Category


class ArticleListView(ListView):
    model = Article
    template_name = "blog/article_list.html"
    context_object_name = "articles"
    paginate_by = 6

    def get_queryset(self):
        qs = Article.objects.filter(published=True)
        self.category_slug = self.kwargs.get("category_slug")
        if self.category_slug:
            qs = qs.filter(category__slug=self.category_slug)
        return qs.select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(articles__published=True).distinct()
        if self.category_slug:
            context["active_category"] = get_object_or_404(Category, slug=self.category_slug)
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/article_detail.html"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Article.objects.filter(published=True).select_related("category")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(articles__published=True).distinct()
        context["related"] = (
            Article.objects.filter(published=True, category=self.object.category)
            .exclude(pk=self.object.pk)
            .order_by("-created_at")[:3]
        )
        return context


def home_redirect(request):
    return HttpResponseRedirect(reverse("article_list"))