# from django import forms
# from . import models


# class SearchForm(forms.Form):

#     search_keywords = forms.CharField(initial="Anywhere", required=False)

#     likes = forms.IntegerField(required=False)

#     instagram_hash_tags = forms.ModelMultipleChoiceField(
#         queryset=models.InstagramHashTag.objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#         required=False,
#     )