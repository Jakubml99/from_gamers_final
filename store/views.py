from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Product, OrderItem, Order, Profile, Category
from .forms import ProductForm, UserForm, ProfileForm, CategoryForm

# Function to check if the user is staff
def staff_required(user):
    return user.is_staff

# Existing views
def home(request):
    return render(request, 'store/home.html')

def product_list(request):
    products = Product.objects.all()
    print(f"Number of products: {products.count()}")
    return render(request, 'store/product_list.html', {'products': products})

@login_required
def view_cart(request):
    order = Order.objects.filter(user=request.user, paid=False).first()
    return render(request, 'store/cart.html', {'order': order})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, paid=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product, defaults={'price': product.price})
    if not created:
        order_item.quantity += 1
        order_item.save()
    return redirect('store:view_cart')

@login_required
def update_cart(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user, order__paid=False)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            order_item.quantity = quantity
            order_item.save()
        else:
            order_item.delete()
    return redirect('store:view_cart')

@login_required
def delete_from_cart(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user, order__paid=False)
    order_item.delete()
    return redirect('store:view_cart')

@login_required
def checkout(request):
    order = Order.objects.filter(user=request.user, paid=False).first()
    if request.method == 'POST':
        order.paid = True
        order.save()
        return redirect('store:home')
    return render(request, 'store/checkout.html', {'order': order})

@login_required
@user_passes_test(staff_required)
def admin_panel(request):
    products = Product.objects.all()
    return render(request, 'store/admin_panel.html', {'products': products})

@login_required
@user_passes_test(staff_required)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('store:admin_panel')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})

@login_required
@user_passes_test(staff_required)
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('store:admin_panel')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/edit_product.html', {'form': form, 'product': product})

@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user, role='user')  # Provide a default role

    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=profile)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('store:profile')

    return render(request, 'store/profile.html', {'user_form': user_form, 'profile_form': profile_form})

# New registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('store:home')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

# New login view using Django's built-in LoginView
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

# Category management views

@login_required
@user_passes_test(staff_required)
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store:admin_panel')
    else:
        form = CategoryForm()
    return render(request, 'store/add_category.html', {'form': form})

@login_required
@user_passes_test(staff_required)
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('store:admin_panel')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'store/edit_category.html', {'form': form, 'category': category})

@login_required
@user_passes_test(staff_required)
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('store:admin_panel')
    return render(request, 'store/delete_category.html', {'category': category})
