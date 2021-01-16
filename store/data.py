from store.models import Order


def prepareCartData(request):

    customer=request.user.customer

    if Order.objects.filter(customer=customer, complete= False).exists():
        order = Order.objects.get(customer=customer, complete= False)
    else:
        order = Order.objects.create(customer= customer,complete= False)

    cartItems= order.get_cart_items
    items = order.orderitem_set.all()

    return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):

    preparedData = prepareCartData(request)

    cartItems = preparedData['cartItems']
    order = preparedData['order']
    items = preparedData['items']

    return {'cartItems': cartItems, 'order': order, 'items': items}