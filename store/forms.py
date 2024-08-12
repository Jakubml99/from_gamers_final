from django import forms
from django.contrib.auth.models import User
from .models import Product, Profile, Category, Review, Product, CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'category', 'image_url']  # or 'image' if using ImageField
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
        fields = ['address', 'city', 'state', 'zipcode', 'country', 'phone_number']
        # If you have 'favorites' field in Profile model, include it here
        # fields = ['address', 'city', 'state', 'zipcode', 'country', 'phone_number', 'favorites']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'parent_category']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')