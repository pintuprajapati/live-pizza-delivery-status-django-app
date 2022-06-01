from unicodedata import name
from wsgiref.util import request_uri
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pyparsing import Or
from .models import *

# Create your views here.
def home(request):
    pizza = Pizza.objects.all() ## all the objects
    orders = Order.objects.filter(user = request.user)
    print(pizza)
    context = {'pizza': pizza, 'orders': orders}
    return render(request, 'home/index.html', context)

def order(request, order_id):
    order = Order.objects.filter(order_id = order_id).first()
    # name = Pizza.objects.filter(name = Pizza.name).first()
    # print('pizza name is:', name)
    if order is None:
        return redirect('/')
    
    # context = {'order': order, 'pizza_name': name}
    context = {'order': order}
    return render(request, 'home/order.html', context)

@csrf_exempt
def order_pizza(request):
    user = request.user
    data = json.loads(request.body)

    try:
        pizza = Pizza.objects.get(id=data.get('id'))
        order = Order(user=user, pizza=pizza, amount=pizza.price)
        order.save()
        return JsonResponse({'message': 'Success', 'status': True})
    
    except Pizza.DoesNotExist:
        return JsonResponse({'error': 'Something went wrong', 'status': False})