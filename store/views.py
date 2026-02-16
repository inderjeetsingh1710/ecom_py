from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order, OrderItem, Category, Carriage, PaymentMethod, Country
from django.http import JsonResponse
import sys
import json
from .models import StoreSetting
from decimal import Decimal
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

def get_store_settings():
    return StoreSetting.objects.first()

def home(request):
    # products = Product.objects.all()
    products = Product.objects.order_by("?")[:3]  # 3 random products
    return render(request, 'store/home.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, 'store/product_detail.html', {'product': product})

def cart(request):
    return render(request, 'store/cart.html')

def shop(request):
    category_id = request.GET.get("category")
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    
    categories = Category.objects.all()
    return render(request, 'store/shop.html',{'products': products,'categories': categories,'selected_category':category_id})


def add_to_cart_ajax11(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        cart = request.session.get('cart', {})
        print("Cart Debug:", cart)
        sys.exit("Debug stop!")  

        
        if product_id in cart:
            cart[product_id] += 1
        else:
            cart[product_id] = 1

        request.session['cart'] = cart
        total_items = sum(cart.values())

        return JsonResponse({'success': True, 'total_items': total_items})
    
    return JsonResponse({'success': False}, status=400)

def add_to_cart_ajax(request):
    try:
        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            cart = request.session.get('cart', {})
            cart[product_id] = cart.get(product_id, 0) + 1
            request.session['cart'] = cart
            return JsonResponse({'success': True, 'total_items': sum(cart.values())})
        return JsonResponse({'success': False}, status=400)
    except Exception as e:
        import traceback
        print("Add to cart error:", e)
        traceback.print_exc()
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def cart_view(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    settings = get_store_settings()
    shipping_charge = settings.shipping_charge
    

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=product_id)
            price = product.get_price()
            subtotal = price * quantity
            total += subtotal

            cart_items.append({
                'id': product.id,
                'name': product.name,
                'image': product.image.url,
                'price': price,
                'quantity': quantity,
                'subtotal': subtotal,
                'shipping_charge': shipping_charge
            })
        except Product.DoesNotExist:
            continue  # skip if product no longer exists

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'subtotal': total,
        'total': total + float(shipping_charge)
    })


def checkout111(request):
    cart = request.session.get('cart', {})  # cart is dict {product_id: qty}
    items = []
    total = 0
    settings = get_store_settings()
    shipping_charge = settings.shipping_charge
    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        subtotal = product.get_price() * qty
        total += subtotal
        items.append({
            'product': product,
            'qty': qty,
            'subtotal': subtotal,
            'image': product.image.url
        })

    shipping_charge = float(shipping_charge)
    grand_total = total + shipping_charge

    context = {
        'items': items,
        'total': total,
        'shipping': shipping_charge,
        'grand_total': grand_total
    }
    return render(request, 'store/checkout.html', context)


def checkout(request):
    cart = request.session.get('cart', {})  # cart is dict {product_id: qty}
    items = []
    subtotal = Decimal("0.00")

    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        line_total = Decimal(str(product.get_price())) * qty
        subtotal += line_total
        items.append({
            "product": product,
            "qty": qty,
            "subtotal": line_total,
            "image": product.image.url if product.image else None
        })

    # Load active carriages and other selections
    carriages = Carriage.objects.filter(is_active=True).order_by('name')
    payment_methods = PaymentMethod.objects.filter(is_active=True).order_by('name')
    countries = Country.objects.order_by('name')

    # Default shipping uses the first active carriage (or 0 if none)
    default_carriage = carriages.first()
    shipping_charge = default_carriage.price if default_carriage else Decimal("0.00")

    # If submitting the form, use the selected carriage price
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        customer_name = f"{first_name} {last_name}".strip()
        email = request.POST.get("email")
        address = request.POST.get("address")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip_code = request.POST.get("zip_code")
        selected_carriage_id = request.POST.get("carriage_id")
        country_id = request.POST.get("country")
        payment_method_id = request.POST.get("payment_method_id")

        country = Country.objects.get(id=country_id) if country_id else None
        carriage = Carriage.objects.get(id=selected_carriage_id) if selected_carriage_id else default_carriage
        payment_method = PaymentMethod.objects.get(id=payment_method_id) if payment_method_id else None

        # Calculate totals with selected carriage
        shipping_charge = carriage.price if carriage else Decimal("0.00")
        grand_total = subtotal + shipping_charge

        # Create order
        order = Order.objects.create(
            customer_name=customer_name,
            email=email,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            subtotal=subtotal,
            shipping_charge=shipping_charge,
            total=grand_total,
            country=country,
            carriage=carriage,
            payment_method=payment_method,
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item["product"],
                quantity=item["qty"],
                price=item["product"].get_price(),
            )

        request.session["cart"] = {}
        return redirect("order_confirmation", order_id=order.id)

    # For initial render, compute grand total with default carriage
    grand_total = subtotal + shipping_charge

    context = {
        "items": items,
        "total": subtotal,
        "shipping": shipping_charge,
        "grand_total": grand_total,
        "carriages": carriages,
        "payment_methods": payment_methods,
        "countries": countries,
    }
    return render(request, "store/checkout.html", context)



def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, "store/order_confirmation.html", {"order": order})


# ----------------------------
# Auth: Signup, Login, Logout
# ----------------------------
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', { 'form': form })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    next_url = request.GET.get('next') or request.POST.get('next')
    # Normalize cases where the hidden input posts the literal string 'None'
    if next_url in (None, '', 'None'):
        next_url = None
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # Only redirect to next_url if it's a safe local URL
            if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect('home')
    else:
        form = AuthenticationForm(request)
    return render(request, 'store/login.html', { 'form': form, 'next': next_url })


def logout_view(request):
    auth_logout(request)
    return redirect('home')
