from django import forms
from rango.models import Category, Page





class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, min_length=2, required=True,
                           help_text="Please enter the category name")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ("name",)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=Category.MAX_LENGTH,
                            help_text="Please enter the page title")
    url = forms.URLField(max_length=20,
                         help_text="Please enter the URL")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category',)