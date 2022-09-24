import datetime
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from home.forms import CreateUser, UserRegistration
from .models import *
from django.http import JsonResponse
import json
from django.forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    #getting all the objects from model.
    products = Product.objects.all()
    context= {'products': products}
    return render (request, 'home.html',context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer 
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitems_set.all()
    else:
        try:
        #getting the cookies 
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart={}

        print(cart)
        items= []
        #passing an empty dictionary for those who are not logged in 
        order={'get_cart_total':0, 'get_cart_total_items':0}
        cartItems =order['get_cart_total_items']


        for i in cart:
            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i)
            total=(product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_total_items'] += cart[i]['quantity']

            item={
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'image':product.image,

                },
                'quantity':cart[i]['quantity'],
                'get_total':total
                
            }
            items.append(item)


    context={'items':items, 'order':order, 'shipping':False}
    return render(request, 'cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer 
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitems_set.all()
    else:
        items= []
        order={'get_cart_total':0, 'get_cart_total_items':0}
    context={'items':items, 'order':order, 'shipping':False}
    
    return render(request, 'checkout.html', context)


def updateItems(request):
    
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']

    print('Action:', action)
    print('ProductID:', productID)

    customer= request.user.customer
    
    product = Product.objects.get(id=productID)
    
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
   
    orderItem, created = OrderItems.objects.get_or_create(order= order, product= product)
    
    if action== 'add':
        orderItem.quantity= (orderItem.quantity+1)
       
    elif action=='remove':
        orderItem.quantity =(orderItem.quantity-1)
     
    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse('item was added', safe=False)
    
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = data['form']['total']
        order.Transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
            print(order.complete)
        order.save()

        if order.shipping == True:
            Shipping_address.objects.create(
                customer=customer,
                order= order,
                address = data['shipping']['address'],
                city= data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],


            )
    else:
        print("user is not logged in")

    return JsonResponse('Payment Complete', safe=False)


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("is this running")
            return redirect('user_registration')
        else:
            messages.warning(request, "The information is not correct")
    
    return render(request,'login.html',context={})


def register(request):
    if request.method =="GET":
        form= CreateUser()
        context={'form':form}
        return render(request, 'register.html', context)

    else:
        form=CreateUser(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('login')
    return render(request, 'register.html', context={'form':form})        


def user_registration(request):
    if request.method == "GET":
        forms=UserRegistration()
        context={'forms':forms}
        return render(request, 'user_details.html', context)

    else:
        forms=UserRegistration(request.POST)
        
        if forms.is_valid():
            forms.save()
           
            return redirect('home')
    return render(request, 'user_details.html', context={'forms':forms})


def user_logout(request):
    logout(request)
    
    return redirect('home')

def bikes(request):
    return render(request, 'bike.html', context={})       
