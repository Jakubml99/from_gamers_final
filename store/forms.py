from django import forms
from .models import Product, Profile, Category
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'stock', 'image', 'slug', 'available']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['favorites']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']


from django import forms
from .models import Category

class CategoryFilterForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, label='Select Category')