from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
import json
import datetime

from .models import *
from . utils import cookieCart, cartData,guestOrder
# 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout



# Create your views here.
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']
       
    products = Product.objects.all()
    context = { 'products' : products,'cartItems':cartItems}
    return render(request,'store.html',context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
        
    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request,'cart.html',context)

def checkout(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request,'checkout.html',context)

def updateItem(request):
    
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    customer= request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)

    if action== 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action== 'remove':
        orderItem.quantity = (orderItem.quantity - 1)    
    
    orderItem.save()

    if orderItem.quantity <=0:
       orderItem.delete()
    print('Action:', action)
    print('productId:',productId)
    return JsonResponse('Item was added',safe=False)

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    if total == order.get_cart_total:
            order.complete = True
    order.save() 

    if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode']
            )       
    return JsonResponse('Payment completed!',safe=False)


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def LoginPage(request):
      if request.method=='POST':
          username=request.POST.get('username')
          pass1=request.POST.get('pass')
          user=authenticate(request,username=username,password=pass1)
          if user is not None:
               login(request,user)
               return redirect('store')
          else:
               return HttpResponse("Username or Password is incorrect !")
      return render(request, 'login.html')

def SignupPage (request):
     if request.method=='POST':
          uname=request.POST.get('username')
        #   fname=request.POST.get('firstname')
        #   lname=request.POST.get('lastname')
          email1=request.POST.get('email')
          pass1=request.POST.get('password1')
          pass2=request.POST.get('password2')  
          if pass1!=pass2:
                return HttpResponse("your password and confirm password are not same!!!")
          else:
                my_user = User.objects.create_user(username=uname,email=email1,password=pass1)
                my_user.save()
                r=Customer(user=my_user,name=uname,email=email1)
                r.save()
                return redirect('log_in')
     context = {}
     
     return render (request,'signup.html',context)



def LogoutPage(request):
     logout(request)
     return redirect('store')