import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from store.data import cartData
from store.forms import CreateUserForm
from store.models import Customer, Product, Order, OrderItem


def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            name = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            customer = Customer(user=user, email=email, name=name)
            customer.save()
            messages.success(request, 'Account was created for ' + name)

            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def index(request):
    if request.user.is_anonymous:
        return redirect('register')
    else:
        data = cartData(request)

        cartItems = data['cartItems']
        products = Product.objects.all()
        context = {'products': products, 'cartItems': cartItems}

        return render(request, 'store.html', context)


def cart(request):
    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'cart.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']


    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Order updated',safe=False)


def processOrder(request):

    customer = request.user.customer
    order = Order.objects.get(customer=customer, complete= False)
    order.complete = True
    order.save()

    return redirect('store')

def history(request):
    customer = request.user.customer
    orders = Order.objects.filter(customer = customer,complete = True)
    data = cartData(request)
    cartItems = data['cartItems']

    return render(request, 'history.html', {"orders":orders,'cartItems': cartItems})


def detail(request,order_id):
    order = Order.objects.get(id=order_id)
    allItems = order.orderitem_set.all()
    print(allItems[0].product.name)
    data = cartData(request)
    cartItems = data['cartItems']
    return render(request, 'detail.html', {"allItems":allItems,'cartItems': cartItems, "order":order})