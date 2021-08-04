import re
import datetime
from django.views.generic import DetailView, View
from django.shortcuts import render
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, forms
from naver_reviews import models as naver_reviews_model
from naver_products.scrapper import get_naver_result


class NaverProductDetail(DetailView):

    """ NaverProduct Detail Definition """

    model = models.NaverProduct


class ScrapeView(View):

    """ ScrapeView Definition """

    def get(self, request):

        search_keywords = request.GET.get("term")
        num_page = request.GET.get("num_page")
        url = f"https://search.shopping.naver.com/search/all?query={search_keywords}&cat_id=&frm=NVSHATC/"
        results = get_naver_result(url, int(num_page))

        for result in results:
            title = result["title"]
            url = result["url"]
            photo = result["photo"]
            price = result["price"]
            over_sea_delivery = result["over_sea_delivery"]
            ankle_height = result["ankle_height"]
            brand = result["brand"]
            manufacturer = result["manufacturer"]
            gender = result["gender"]
            sole_material = result["sole_material"]
            sellers = result["sellers"]
            categories = result["categories"]
            heel_height = result["heel_height"]
            feature = result["feature"]
            main_material = result["main_material"]
            add_ons = result["add_ons"]
            registration = result["registration"]
            dibs = result["dibs"]
            reviews = result["reviews"]

            product = models.NaverProduct(
                name=title,
                url=url,
                price=price,
                over_sea_delivery=over_sea_delivery,
                registration=datetime.date(
                    int(registration[0]), int(registration[1]), 1
                ),
                dibs=dibs,
            )

            if brand:
                try:
                    brand = models.Brand.objects.get(name=brand)
                except Exception:
                    brand = models.Brand.objects.create(name=brand)
                product.brand = brand

            if manufacturer:
                try:
                    manufacturer = models.Manufacturer.objects.get(name=manufacturer)
                except Exception:
                    manufacturer = models.Manufacturer.objects.create(name=manufacturer)
                product.manufacturer = manufacturer

            product.save()

            pk = product.pk
            naver_product = models.NaverProduct.objects.get(pk=pk)

            if reviews:
                for review in reviews:
                    naver_review = review["review"]
                    rating = review["rating"]
                    date_created = review["date_created"]
                    buy = review["buy"]
                    if buy:
                        try:
                            buy = models.Seller.objects.get(name=buy)
                        except Exception:
                            buy = models.Seller.objects.create(name=buy)
                    naver_reviews_model.NaverReview.objects.create(
                        naver_review=naver_review,
                        rating=rating,
                        date_created=datetime.date(
                            2000 + int(date_created[0]),
                            int(date_created[1]),
                            int(date_created[2]),
                        ),
                        buy=buy,
                        naver_product=naver_product,
                    )

            models.NaverPhoto.objects.create(
                file=f"naver_photos/{photo}.png",
                naver_product=naver_product,
            )

            try:
                search_keyword = models.SearchKeyword.objects.get(name=search_keywords)
            except Exception:
                search_keyword = models.SearchKeyword.objects.create(
                    name=search_keywords
                )
            naver_product.search_keywords.add(search_keyword)

            if ankle_height:
                try:
                    ankle_height = models.AnkleHeight.objects.get(name=ankle_height)
                except Exception:
                    ankle_height = models.AnkleHeight.objects.create(name=ankle_height)
                naver_product.ankle_height.add(ankle_height)

            if gender:
                try:
                    gender = models.Gender.objects.get(name=result["gender"])
                except Exception:
                    gender = models.Gender.objects.create(name=result["gender"])
                naver_product.gender.add(gender)

            if sole_material:
                try:
                    sole_material = models.SoleMaterial.objects.get(name=sole_material)
                except Exception:
                    sole_material = models.SoleMaterial.objects.create(
                        name=sole_material
                    )
                naver_product.sole_material.add(sole_material)

            if sellers:
                for seller in sellers:
                    try:
                        seller = models.Seller.objects.get(name=seller)
                    except Exception:
                        seller = models.Seller.objects.create(name=seller)
                    naver_product.sellers.add(seller)

            if categories:
                for category in categories:
                    try:
                        category = models.Category.objects.get(name=category)
                    except Exception:
                        category = models.Category.objects.create(name=category)
                    naver_product.categories.add(category)

            if heel_height:
                for heel_height in heel_height:
                    try:
                        heel_height = models.HeelHeight.objects.get(name=heel_height)
                    except Exception:
                        heel_height = models.HeelHeight.objects.create(name=heel_height)
                    naver_product.heel_height.add(heel_height)

            if feature:
                for feature in feature:
                    try:
                        feature = models.Feature.objects.get(name=feature)
                    except Exception:
                        feature = models.Feature.objects.create(name=feature)
                    naver_product.feature.add(feature)

            if main_material:
                for main_material in main_material:
                    try:
                        main_material = models.MainMaterial.objects.get(
                            name=main_material
                        )
                    except Exception:
                        main_material = models.MainMaterial.objects.create(
                            name=main_material
                        )
                    naver_product.main_material.add(main_material)

            if add_ons:
                for add_ons in add_ons:
                    try:
                        add_ons = models.AddOns.objects.get(name=add_ons)
                    except Exception:
                        add_ons = models.AddOns.objects.create(name=add_ons)
                    naver_product.add_ons.add(add_ons)

        return render(request, "home.html")


class SearchView(View):

    """ SearchView Definition """

    def get(self, request):

        global qs
        title = request.GET.get("title")

        page = request.GET.get("page")
        if page:
            url = request.build_absolute_uri()
            url = re.sub(r"&page.*\d", "", url)
        else:
            url = request.build_absolute_uri()

        form = forms.SearchForm(request.GET)

        if form.is_valid():
            title = form.cleaned_data.get("title")
            date_from = form.cleaned_data.get("date_from")
            date_to = form.cleaned_data.get("date_to")
            price_max = form.cleaned_data.get("price_max")
            price_min = form.cleaned_data.get("price_min")
            brands = form.cleaned_data.get("brands")
            manufacturers = form.cleaned_data.get("manufacturers")
            sellers = form.cleaned_data.get("sellers")
            categories = form.cleaned_data.get("categories")
            main_material = form.cleaned_data.get("main_material")
            sole_material = form.cleaned_data.get("sole_material")
            gender = form.cleaned_data.get("gender")
            ankle_height = form.cleaned_data.get("ankle_height")
            heel_height = form.cleaned_data.get("heel_height")

            filter_args = {}
            filter_args_multi = []

            if title:
                filter_args["name__startswith"] = title

            if date_from:
                filter_args["registration__gte"] = date_from

            if date_to:
                filter_args["registration__lte"] = date_to

            if price_max:
                filter_args["price__lte"] = price_max

            if price_min:
                filter_args["price__gte"] = price_min

            if brands:
                for brand in brands:
                    filter_args_multi.append(brand)
                filter_args["brand__in"] = filter_args_multi
                filter_args_multi = []

            if manufacturers:
                for manufacturer in manufacturers:
                    filter_args_multi.append(manufacturer)
                filter_args["manufacturer__in"] = filter_args_multi
                filter_args_multi = []

            if sellers:
                for seller in sellers:
                    filter_args_multi.append(seller)
                filter_args["sellers__in"] = filter_args_multi
                filter_args_multi = []

            if categories:
                for category in categories:
                    filter_args_multi.append(category)
                filter_args["categories__in"] = filter_args_multi
                filter_args_multi = []

            if main_material:
                for main_material in main_material:
                    filter_args_multi.append(main_material)
                filter_args["main_material__in"] = filter_args_multi
                filter_args_multi = []

            if sole_material:
                for sole_material in sole_material:
                    filter_args_multi.append(sole_material)
                filter_args["sole_material__in"] = filter_args_multi
                filter_args_multi = []

            if gender:
                for gender in gender:
                    filter_args_multi.append(gender)
                filter_args["gender__in"] = filter_args_multi
                filter_args_multi = []

            if ankle_height:
                for ankle_height in ankle_height:
                    filter_args_multi.append(ankle_height)
                filter_args["ankle_height__in"] = filter_args_multi
                filter_args_multi = []

            if heel_height:
                for heel_height in heel_height:
                    filter_args_multi.append(heel_height)
                filter_args["heel_height__in"] = filter_args_multi
                filter_args_multi = []

            qs = (
                models.NaverProduct.objects.filter(**filter_args)
                .order_by("-created")
                .distinct()
            )

            paginator = Paginator(qs, 16, orphans=5)

            page_number = request.GET.get("page", 1)

            naver_products = paginator.get_page(page_number)

            return render(
                request,
                "naver_products/naverproduct_search.html",
                {"form": form, "naver_products": naver_products, "url": url},
            )

        qs = models.NaverProduct.objects.all()

        return render(
            request, "naver_products/naverproduct_search.html", {"form": form}
        )


class ChartView(APIView):

    """ Chart View Definition """

    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        sellers_pk_dup = qs.values_list("sellers", flat=True)
        sellers_pk = list(dict.fromkeys(sellers_pk_dup))
        seller_dict = {}
        for pk in sellers_pk:
            if pk is not None:
                seller = models.Seller.objects.values_list("name", flat=True).get(pk=pk)
                seller_item = list(sellers_pk_dup).count(pk)
                seller_dict[seller] = seller_item
        seller_dict = dict(
            reversed(sorted(seller_dict.items(), key=lambda item: item[1]))
        )
        seller_labels = list(seller_dict.keys())[:30]
        seller_items = list(seller_dict.values())[:30]

        heel_height_pk_dup = qs.values_list("heel_height", flat=True)
        heel_height_pk = list(dict.fromkeys(heel_height_pk_dup))
        heel_height_dict = {}
        for pk in heel_height_pk:
            if pk is not None:
                heel_height = models.HeelHeight.objects.values_list(
                    "name", flat=True
                ).get(pk=pk)
                heel_height_item = list(heel_height_pk_dup).count(pk)
                heel_height_dict[heel_height] = heel_height_item

        heel_height_labels = list(heel_height_dict.keys())[:30]
        heel_height_items = list(heel_height_dict.values())[:30]

        gender_pk_dup = qs.values_list("gender", flat=True)
        gender_pk = list(dict.fromkeys(gender_pk_dup))
        gender_dict = {}
        for pk in gender_pk:
            if pk is not None:
                gender = models.Gender.objects.values_list("name", flat=True).get(pk=pk)
                gender_item = list(gender_pk_dup).count(pk)
                gender_dict[gender] = gender_item
        gender_dict = dict(
            reversed(sorted(gender_dict.items(), key=lambda item: item[1]))
        )
        gender_labels = list(gender_dict.keys())[:30]
        gender_items = list(gender_dict.values())[:30]

        main_material_pk_dup = qs.values_list("main_material", flat=True)
        main_material_pk = list(dict.fromkeys(main_material_pk_dup))
        main_material_dict = {}
        for pk in main_material_pk:
            if pk is not None:
                main_material = models.MainMaterial.objects.values_list(
                    "name", flat=True
                ).get(pk=pk)
                main_material_item = list(main_material_pk_dup).count(pk)
                main_material_dict[main_material] = main_material_item
        main_material_dict = dict(
            reversed(sorted(main_material_dict.items(), key=lambda item: item[1]))
        )
        main_material_labels = list(main_material_dict.keys())[:30]
        main_material_items = list(main_material_dict.values())[:30]

        add_ons_pk_dup = qs.values_list("add_ons", flat=True)
        add_ons_pk = list(dict.fromkeys(add_ons_pk_dup))
        add_ons_dict = {}
        for pk in add_ons_pk:
            if pk is not None:
                add_ons = models.AddOns.objects.values_list("name", flat=True).get(
                    pk=pk
                )
                add_ons_item = list(add_ons_pk_dup).count(pk)
                add_ons_dict[add_ons] = add_ons_item
        add_ons_dict = dict(
            reversed(sorted(add_ons_dict.items(), key=lambda item: item[1]))
        )
        add_ons_labels = list(add_ons_dict.keys())[:30]
        add_ons_items = list(add_ons_dict.values())[:30]

        price_list = qs.values_list("price", flat=True)
        price_dict = {}
        price_keys = {
            "5만원이하": 0,
            "5만원~10만원": 0,
            "10만원~15만원": 0,
            "15만원~20만원": 0,
            "20만원~30만원": 0,
            "30만원~50만원": 0,
            "50만원~70만원": 0,
            "70만원~100만원": 0,
            "100만원이상": 0,
        }
        price_dict.update(price_keys)
        p1 = 0
        p2 = 0
        p3 = 0
        p4 = 0
        p5 = 0
        p6 = 0
        p7 = 0
        p8 = 0
        p9 = 0
        for pl in price_list:
            if pl is not None:
                if pl <= 50000:
                    p1 = p1 + 1
                    price_dict["5만원이하"] = p1
                if pl > 50000 and pl <= 100000:
                    p2 = p2 + 1
                    price_dict["5만원~10만원"] = p2
                if pl > 100000 and pl <= 150000:
                    p3 = p3 + 1
                    price_dict["10만원~15만원"] = p3
                if pl > 150000 and pl <= 200000:
                    p4 = p4 + 1
                    price_dict["15만원~20만원"] = p4
                if pl > 200000 and pl <= 300000:
                    p5 = p5 + 1
                    price_dict["20만원~30만원"] = p5
                if pl > 300000 and pl <= 500000:
                    p6 = p6 + 1
                    price_dict["30만원~50만원"] = p6
                if pl > 500000 and pl <= 700000:
                    p7 = p7 + 1
                    price_dict["50만원~70만원"] = p7
                if pl > 700000 and pl <= 1000000:
                    p8 = p8 + 1
                    price_dict["70만원~100만원"] = p8
                if pl > 1000000:
                    p9 = p9 + 1
                    price_dict["100만원이상"] = p9
        price_labels = list(price_dict.keys())
        price_items = list(price_dict.values())

        data = {
            "seller_labels": seller_labels,
            "seller_data": seller_items,
            "heel_height_labels": heel_height_labels,
            "heel_height_data": heel_height_items,
            "gender_labels": gender_labels,
            "gender_data": gender_items,
            "price_labels": price_labels,
            "price_data": price_items,
            "main_material_labels": main_material_labels,
            "main_material_data": main_material_items,
            "add_ons_labels": add_ons_labels,
            "add_ons_data": add_ons_items,
        }
        return Response(data)
