import re
from django.views.generic import DetailView, View
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models, forms


class InstagramProductDetail(DetailView):

    """ NaverProduct Detail Definition """

    model = models.InstagramProduct


class ScrapeView(View):

    """ ScrapeView Definition """

    pass


class SearchView(View):

    """ SearchView Definition """

    def get(self, request):

        search_keywords = request.GET.get("search_keywords")

        page = request.GET.get("page")
        if page:
            url = request.build_absolute_uri()
            url = re.sub(r"&page.*\d", "", url)
        else:
            url = request.build_absolute_uri()

        if search_keywords:

            form = forms.SearchForm(request.GET)

            if form.is_valid():
                search_keywords = form.cleaned_data.get("search_keywords")
                instagram_hash_tags = form.cleaned_data.get("instagram_hash_tags")
                likes = form.cleaned_data.get("likes")

                filter_args = {}
                filter_args_multi = []

                if search_keywords != "Anywhere":
                    filter_args["search_keywords"] = search_keywords

                if likes is not None:
                    filter_args["likes__gte"] = likes

                if instagram_hash_tags:
                    for instagram_hash_tag in instagram_hash_tags:
                        filter_args_multi.append(instagram_hash_tag)
                    filter_args["all_hash_tags__in"] = filter_args_multi
                    filter_args_multi = []

                qs = (
                    models.InstagramProduct.objects.filter(**filter_args)
                    .order_by("-created")
                    .distinct()
                )

                paginator = Paginator(qs, 12, orphans=5)

                page_number = request.GET.get("page", 1)

                instagram_products = paginator.get_page(page_number)

                return render(
                    request,
                    "instagram_products/instagramproduct_search.html",
                    {
                        "form": form,
                        "instagram_products": instagram_products,
                        "url": url,
                    },
                )
        else:

            form = forms.SearchForm()

        return render(
            request, "instagram_products/instagramproduct_search.html", {"form": form}
        )
