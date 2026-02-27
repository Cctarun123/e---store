from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Category, Order, Product, UserProfile


def seed_sample_data() -> None:
    categories = {
        'Audio': Category.objects.get_or_create(name='Audio', slug='audio')[0],
        'Wearables': Category.objects.get_or_create(name='Wearables', slug='wearables')[0],
        'Computing': Category.objects.get_or_create(name='Computing', slug='computing')[0],
        'Tech Essentials': Category.objects.get_or_create(name='Tech Essentials', slug='tech-essentials')[0],
    }

    sample_products = [
        {
            'category': categories['Audio'],
            'name': 'Pulse One Headphones',
            'slug': 'pulse-one-headphones',
            'description': 'Noise-canceling over-ear headphones tuned for long listening sessions.',
            'price': Decimal('179.00'),
            'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=900&q=80',
            'is_featured': True,
        },
        {
            'category': categories['Wearables'],
            'name': 'Orbit Smartwatch S2',
            'slug': 'orbit-smartwatch-s2',
            'description': 'Fitness and wellness tracking with a week-long battery life.',
            'price': Decimal('229.00'),
            'image_url': 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?auto=format&fit=crop&w=900&q=80',
            'is_featured': True,
        },
        {
            'category': categories['Computing'],
            'name': 'Nova Mechanical Keyboard',
            'slug': 'nova-mechanical-keyboard',
            'description': 'Compact wireless keyboard with tactile switches and RGB backlight.',
            'price': Decimal('119.00'),
            'image_url': 'https://images.unsplash.com/photo-1511467687858-23d96c32e4ae?auto=format&fit=crop&w=900&q=80',
            'is_featured': False,
        },
        {
            'category': categories['Computing'],
            'name': 'Glide Pro Mouse',
            'slug': 'glide-pro-mouse',
            'description': 'Ergonomic high-precision mouse designed for creative workflows.',
            'price': Decimal('79.00'),
            'image_url': 'https://images.unsplash.com/photo-1615663245857-ac93bb7c39e7?auto=format&fit=crop&w=900&q=80',
            'is_featured': False,
        },
        {
            'category': categories['Tech Essentials'],
            'name': 'Volt 65W USB-C Charger',
            'slug': 'volt-65w-usb-c-charger',
            'description': 'Fast multi-device charging brick with foldable plug and compact shell.',
            'price': Decimal('49.00'),
            'image_url': 'https://images.unsplash.com/photo-1583863788434-e58a36330cf0?auto=format&fit=crop&w=900&q=80',
            'is_featured': True,
        },
        {
            'category': categories['Tech Essentials'],
            'name': 'Link 7-in-1 USB-C Hub',
            'slug': 'link-7-in-1-usb-c-hub',
            'description': 'Portable aluminum hub with HDMI, SD, USB-A and pass-through charging.',
            'price': Decimal('69.00'),
            'image_url': 'https://images.unsplash.com/photo-1625842268584-8f3296236761?auto=format&fit=crop&w=900&q=80',
            'is_featured': False,
        },
        {
            'category': categories['Tech Essentials'],
            'name': 'Shield Laptop Sleeve 14"',
            'slug': 'shield-laptop-sleeve-14',
            'description': 'Water-resistant padded sleeve with magnetic closure for daily commute.',
            'price': Decimal('39.00'),
            'image_url': 'https://images.unsplash.com/photo-1511385348-a52b4a160dc2?auto=format&fit=crop&w=900&q=80',
            'is_featured': False,
        },
        {
            'category': categories['Tech Essentials'],
            'name': 'Air Mini Power Bank',
            'slug': 'air-mini-power-bank',
            'description': 'Slim 10,000mAh battery pack with dual USB-C fast charging ports.',
            'price': Decimal('59.00'),
            'image_url': 'https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?auto=format&fit=crop&w=900&q=80',
            'is_featured': False,
        },
    ]

    for product in sample_products:
        Product.objects.get_or_create(slug=product['slug'], defaults=product)


def home(request: HttpRequest) -> HttpResponse:
    seed_sample_data()
    featured = Product.objects.filter(is_featured=True, in_stock=True)[:3]
    latest = Product.objects.filter(in_stock=True)[:8]
    essentials = Product.objects.filter(category__slug='tech-essentials', in_stock=True)[:4]
    total_products = Product.objects.filter(in_stock=True).count()
    return render(
        request,
        'store/home.html',
        {
            'featured_products': featured,
            'products': latest,
            'essentials': essentials,
            'total_products': total_products,
        },
    )


def catalog(request: HttpRequest) -> HttpResponse:
    seed_sample_data()
    category_slug = request.GET.get('category')
    products = Product.objects.select_related('category').filter(in_stock=True)
    if category_slug:
        products = products.filter(category__slug=category_slug)

    categories = Category.objects.all()
    return render(
        request,
        'store/catalog.html',
        {
            'products': products,
            'categories': categories,
            'active_category': category_slug,
        },
    )


def product_detail(request: HttpRequest, slug: str) -> HttpResponse:
    seed_sample_data()
    product = get_object_or_404(Product.objects.select_related('category'), slug=slug)
    related = Product.objects.filter(category=product.category, in_stock=True).exclude(id=product.id)[:4]
    return render(request, 'store/product_detail.html', {'product': product, 'related_products': related})


@login_required
def checkout(request: HttpRequest, slug: str) -> HttpResponse:
    seed_sample_data()
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        payment_method = request.POST.get('payment_method', '').strip()

        if not all([full_name, email, address, payment_method]):
            messages.error(request, 'Please fill all payment details.')
        else:
            order = Order.objects.create(
                customer=request.user,
                product=product,
                full_name=full_name,
                email=email,
                address=address,
                payment_method=payment_method,
                amount=product.price,
            )
            return redirect('store:payment_success', order_id=order.id)

    context = {
        'product': product,
        'initial_full_name': request.user.get_full_name() or request.user.username,
        'initial_email': request.user.email or '',
        'initial_address': profile.full_address,
    }
    return render(request, 'store/checkout.html', context)


@login_required
def payment_success(request: HttpRequest, order_id: int) -> HttpResponse:
    order = get_object_or_404(Order.objects.select_related('product'), id=order_id, customer=request.user)
    return render(request, 'store/payment_success.html', {'order': order})


@login_required
def order_history(request: HttpRequest) -> HttpResponse:
    orders = Order.objects.select_related('product').filter(customer=request.user)
    return render(request, 'store/order_history.html', {'orders': orders})


@login_required
def profile(request: HttpRequest) -> HttpResponse:
    profile_obj, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address_line1 = request.POST.get('address_line1', '').strip()
        address_line2 = request.POST.get('address_line2', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        pincode = request.POST.get('pincode', '').strip()
        country = request.POST.get('country', '').strip() or 'India'

        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.email = email
        request.user.save(update_fields=['first_name', 'last_name', 'email'])

        profile_obj.phone = phone
        profile_obj.address_line1 = address_line1
        profile_obj.address_line2 = address_line2
        profile_obj.city = city
        profile_obj.state = state
        profile_obj.pincode = pincode
        profile_obj.country = country
        profile_obj.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('store:home')

    context = {
        'profile': profile_obj,
    }
    return render(request, 'store/profile.html', context)
