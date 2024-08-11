from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Product, OrderItem, Order, Profile, Category, Review
from .forms import ProductForm, UserForm, ProfileForm, CategoryForm, ReviewForm

# Custom decorator to check if the user is staff
def staff_required(user):
    return user.is_staff

# Home view
def home(request):
    return render(request, 'store/home.html')

# Product listing view
def product_list(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    if selected_category:
        products = Product.objects.filter(category__id=selected_category)
    else:
        products = Product.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'store/product_list.html', context)

# View cart
@login_required
def view_cart(request):
    order = Order.objects.filter(user=request.user, paid=False).first()
    return render(request, 'store/cart.html', {'order': order})

# Add product to cart
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    order, created = Order.objects.get_or_create(user=request.user, paid=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product, defaults={'price': product.price})
    if not created:
        order_item.quantity += 1
        order_item.save()
    return redirect('store:view_cart')

# Update cart item quantity
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

# Delete item from cart
@login_required
def delete_from_cart(request, item_id):
    order_item = get_object_or_404(OrderItem, id=item_id, order__user=request.user, order__paid=False)
    order_item.delete()
    return redirect('store:view_cart')

# Checkout view
@login_required
def checkout(request):
    order = Order.objects.filter(user=request.user, paid=False).first()
    if request.method == 'POST':
        order.paid = True
        order.save()
        return redirect('store:home')
    return render(request, 'store/checkout.html', {'order': order})

# Admin panel view (staff only)
@login_required
@user_passes_test(staff_required)
def admin_panel(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        category_id = request.POST.get('category_id')
        product = get_object_or_404(Product, id=product_id)
        category = get_object_or_404(Category, id=category_id)
        product.category = category
        product.save()
        return redirect('store:admin_panel')
    return render(request, 'store/admin_panel.html', {'products': products, 'categories': categories})

# Add product view (staff only)
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

# Edit product view (staff only)
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

# User profile view
@login_required
def profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user, role='user')

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

# Custom login view
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

# User registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('store:home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Add category view (staff only)
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

# Edit category view (staff only)
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

# Delete category view (staff only)
@login_required
@user_passes_test(staff_required)
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('store:admin_panel')
    return render(request, 'store/delete_category.html', {'category': category})
