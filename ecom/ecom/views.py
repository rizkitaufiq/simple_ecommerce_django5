from django.shortcuts import render, redirect, HttpResponse
from app.models import Category, Product, Contact_us, Order, Brand, Wishlist
from django.contrib.auth.models import User

from app.models import UserCreateForm

# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from cart.cart import Cart

def Master(request):
    return render(request, 'master.html')

def Index(request):
    category   = Category.objects.all()
    brand      = Brand.objects.all()

    categoryID = request.GET.get('category')
    brandID    = request.GET.get('brand')

    if categoryID:
        product     = Product.objects.filter(sub_Category=categoryID).order_by('-id')
    elif brandID:
        product     = Product.objects.filter(brand=brandID).order_by('-id')
    else:
        product     = Product.objects.all() 
    
    bestseller  = Product.objects.filter(status='Best Seller').order_by('-id')
    recommended = Product.objects.filter(status='Recommended').order_by('-id')

    context = {
        'category'   : category,
        'product'    : product,
        'brand'      : brand,
        'bestseller' : bestseller,
        'recommended': recommended,  
    }
    return render(request, 'index.html', context) 

def signup(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'],
            )
            login(request, new_user)
            return redirect('index')
    else:
        form = UserCreateForm()

    context = {
        'form' : form,
    }    
    
    return render(request,'registration/signup.html', context)

def logout_view(request):
    logout(request)
    return redirect('index')


# addtocart
@login_required(login_url="login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("index")


@login_required(login_url="login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id) 
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="login")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')


# contact
def contact_page(request):
    if request.method == "POST":
        contact = Contact_us(
            name    = request.POST.get('name'),
            email   = request.POST.get('email'),
            subject = request.POST.get('subject'),
            message = request.POST.get('message'),
        )
        contact.save()
        
    return render(request, 'contact.html')

# checkout
def checkout_page(request):
    if request.method == "POST":
        address = request.POST.get('address')
        phone   = request.POST.get('phone')
        pincode = request.POST.get('pincode')
        cart    = request.session.get('cart')
        uid     = request.session.get('_auth_user_id')
        user    = User.objects.get(pk = uid)

        for i in cart:
            price       = (int(cart[i]['price']))
            quantity    = cart[i]['quantity']
            total       = price * quantity

            order = Order(
                user    = user,
                product = cart[i]['name'],
                price   = cart[i]['price'],
                quantity= cart[i]['quantity'],
                image   = cart[i]['image'],
                address = address,
                phone   = phone,
                pincode = pincode,
                total   = total,
            )
            order.save()
        request.session['cart'] = {}
        return redirect('index')
        
    return HttpResponse('this is checkout page')

# order
def order_page(request):
    uid     = request.session.get('_auth_user_id')
    user    = User.objects.get(pk = uid)

    order   = Order.objects.filter(user = user).order_by('-date')
    context = {
        'order' : order,
    }
    return render(request,'order.html', context)

# product
def product_page(request):
    category   = Category.objects.all()
    brand      = Brand.objects.all()

    categoryID = request.GET.get('category')
    brandID    = request.GET.get('brand')

    if categoryID:
        product     = Product.objects.filter(sub_Category=categoryID).order_by('-id')
    elif brandID:
        product     = Product.objects.filter(brand=brandID).order_by('-id')
    else:
        product     = Product.objects.all() 

    context = {
        'category': category,
        'product' : product,
        'brand'   : brand,  
    }
    return render(request, 'product.html', context)

def product_detail_page(request,id):
    category   = Category.objects.all()
    brand      = Brand.objects.all()

    product = Product.objects.filter(id = id).first()
   
    context = {
        'category': category,
        'brand'   : brand, 
        'product' : product,
    }
    return render(request,'product_detail.html', context)

def product_detail_index(request,id):
    category   = Category.objects.all()
    brand      = Brand.objects.all()
    
    product = Product.objects.filter(id = id).first()
  
    context = {
        'category': category,
        'brand'   : brand,
        'product' : product,
    }

    if request.method == "POST":
        contact_review = Contact_us(
            name    = request.POST.get('name'),
            email   = request.POST.get('email'),
            subject = request.POST.get('subject'),
            product = request.POST.get('product'),
            message = request.POST.get('message'),
        )
        contact_review.save()
        
    return render(request,'product_detail.html', context)

# wishlist
@login_required(login_url="login")
def wishlist_add(request, id):

    product = Product.objects.filter(id = id)
    uid     = request.session.get('_auth_user_id')
    user    = User.objects.get(pk = uid)

    for i in product:

        wishlist = Wishlist(
            user        = user,
            category    = i.category,
            sub_category= i.sub_category,
            brand       = i.brand,
            image       = i.image,
            name        = i.name,
            price       = i.price,
        )
        wishlist.save()
    
    return redirect("index")

@login_required(login_url="login")
def wishlist_page(request):
    uid     = request.session.get('_auth_user_id')
    user    = User.objects.get(pk = uid)

    wishlist= Wishlist.objects.filter(user = user)
    context = {
        'wishlist' : wishlist,
    }
    return render(request, 'wishlist.html', context)

@login_required(login_url="login")
def wishlistcart_add(request, id):
    cart = Cart(request)
    wishlist = Wishlist.objects.get(id=id)
    cart.add(product=wishlist)
    wishlist.delete()
    return redirect("cart_detail")

# search
def search_page(request):
    search  = request.GET['search']
    product = Product.objects.filter(name__icontains = search)
    context = {
        'product':product,
    }
    return render(request, 'search.html',context)