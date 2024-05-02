from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserProfile, Product, Cart, Order,OrderItem
from .forms import SignUpForm, LoginForm


# Home Page View
def home(request):
    products = Product.objects.all()  # Get all products
    return render(request, 'home.html', {'products': products})  # Render home page

def about(request):
    return render(request, 'about.html')

# User Sign-Up View
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)  # Use the custom sign-up form
        if form.is_valid():  # If form is valid
            user = form.save()  # Create a new user
            UserProfile.objects.create(user=user, mobile=form.cleaned_data['mobile'])  # Create UserProfile
            login(request, user)  # Automatically log in the new user
            return redirect("home")  # Redirect to home after successful sign-up
    else:
        form = SignUpForm()  # Display the form for GET requests

    return render(request, 'signup.html', {'form': form})  # Render sign-up page


# User Login View
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)  # Use the custom login form
        if form.is_valid():  # Check if form is valid
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)  # Authenticate with username and password
            if user is not None:
                login(request, user)  # Log in the user
                return redirect("home")  # Redirect to home after successful login
            else:
                form.add_error(None, "Invalid username or password.")  # Handle invalid credentials
    else:
        form = LoginForm()  # Display the form for GET requests

    return render(request, 'login.html', {'form': form})  # Render the login page


# User Logout View
def user_logout(request):
    logout(request)  # Log out the user
    return redirect("home")  # Redirect to home after logout


# Use local import to avoid circular import
def products(request):
    from .models import Product  # Local import within function
    products = Product.objects.all()  # Fetch all products
    return render(request, 'products.html', {'products': products})

def about(request):
    return render(request, 'about.html', {'products': products})

@login_required
def user_profile(request):
    # For demonstration, we're just returning a simple profile page.
    # You can customize this to include more details or allow editing.
    return render(request, 'user_profile.html', {'user': request.user})

# Cart Page View
@login_required  # User must be logged in to access the cart
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)  # Fetch all items in the user's cart
    
    total_cost = sum(item.total_price() for item in cart_items)  # Calculate the total cost
    
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_cost': total_cost})  # Render cart page


# Add to Cart View
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Get the product by ID
    
    quantity = int(request.POST.get("quantity", 1))  # Default quantity is 1
    
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)  # Get or create a cart item
    
    if created:
        cart_item.quantity = quantity  # Set the initial quantity
    else:
        cart_item.quantity += quantity  # Increment the quantity

    cart_item.save()  # Save the cart item
    return redirect("cart")  # Redirect to the cart page


# Remove from Cart View
@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)  # Find the cart item
    
    cart_item.delete()  # Delete the cart item
    
    return redirect("cart")  # Redirect to the cart page


# Confirm Order View
@login_required
def confirm_order(request):
    if request.method == 'POST':  # If POST, process order confirmation
        address = request.POST.get('address', "").strip()  # Ensure address is collected
        payment_type = request.POST.get('payment_type', "Credit Card").strip()  # Default payment type
        
        if not address:
            return HttpResponseBadRequest("Address is required.")  # Handle missing address
        
        user_cart = Cart.objects.filter(user=request.user)  # Get all cart items
        
        total_amount = sum(item.total_price() for item in user_cart)  # Calculate total amount
        
        # Create and save the order
        order = Order(
            user=request.user,
            address=address,
            payment_type=payment_type,
            total_amount=total_amount
        )
        order.save()  # Save the order
        
        # Clear the cart after order confirmation
        user_cart.delete()

        return redirect("order_details", order_id=order.id)  # Redirect to order details
    else:
        # If GET, render the confirm order page
        user_cart = Cart.objects.filter(user=request.user)
        return render(request, 'confirm_order.html', {'cart': user_cart})
    

# Order Details View
@login_required
def order_details(request, order_id):
    # Get the specific order
    order = get_object_or_404(Order, id=order_id)
    
    # Get all items related to the order
    order_items = OrderItem.objects.filter(order=order)
    
    # Calculate the total price for each item
    order_items_with_total = []
    for item in order_items:
        total_price = item.quantity * item.product.price
        order_items_with_total.append({
            'product_name': item.product.name,
            'quantity': item.quantity,
            'total_price': total_price,
        })

    # Pass the calculated information to the template
    context = {
        'order': order,
        'order_items': order_items_with_total,
    }
    
    return render(request, 'order_details.html', context)

# Previous Orders View (Order History)
@login_required
def previous_orders(request):
    user_orders = Order.objects.filter(user=request.user)  # Fetch all orders for this user
    
    return render(request, 'history.html', {'orders': user_orders})  # Render order history page
