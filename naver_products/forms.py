from django import forms
from django.db.models import Count
from . import models


class SearchForm(forms.Form):

    title = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Search"}),
        required=False,
    )

    date_from = forms.DateField(
        widget=forms.TextInput(
            attrs={"placeholder": "Date from", "class": "datepicker"}
        ),
        required=False,
    )

    date_to = forms.DateField(
        widget=forms.TextInput(attrs={"placeholder": "Date to", "class": "datepicker"}),
        required=False,
    )

    price_max = forms.IntegerField(
        widget=forms.NumberInput(attrs={"placeholder": "Maximum price"}),
        required=False,
    )

    price_min = forms.IntegerField(
        widget=forms.NumberInput(attrs={"placeholder": "Minimum price"}),
        required=False,
    )

    brands = forms.ModelMultipleChoiceField(
        queryset=models.Brand.objects.annotate(
            count=Count("naver_products__id")
        ).order_by("-count"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    manufacturers = forms.ModelMultipleChoiceField(
        queryset=models.Manufacturer.objects.annotate(
            count=Count("naver_products__id")
        ).order_by("-count"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    sellers = forms.ModelMultipleChoiceField(
        queryset=models.Seller.objects.annotate(
            count=Count("naver_products__id")
        ).order_by("-count"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=models.Category.objects.annotate(
            count=Count("naver_products__id")
        ).order_by("-count"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    main_material = forms.ModelMultipleChoiceField(
        queryset=models.MainMaterial.objects.annotate(
            count=Count("naver_products__id")
        ).order_by("-count"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    sole_material = forms.ModelMultipleChoiceField(
        queryset=models.SoleMaterial.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    gender = forms.ModelMultipleChoiceField(
        queryset=models.Gender.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    ankle_height = forms.ModelMultipleChoiceField(
        queryset=models.AnkleHeight.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    heel_height = forms.ModelMultipleChoiceField(
        queryset=models.HeelHeight.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
