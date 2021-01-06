from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import *


def home(request):
	#getting all orders from the DB
	orders = Order.objects.all()

	#getting all customers from the DB
	customers = Customer.objects.all()

	#Counting the total number of customers
	total_customers = customers.count()

	#Counting the total number of orders
	total_orders = orders.count()

	#Counting the count for total number of orders delivered
	delivered = orders.filter(status="Delivered").count()

	#Counting the count for total number of orders pending
	pending = orders.filter(status="Pending").count()

	context = {'orders':orders, 'customers':customers, 'total_orders':total_orders, 'total_customers':total_customers, 'delivered':delivered, 'pending':pending}

	return render(request,'accounts/dashboard.html', context)


def products(request):
	products = Product.objects.all()
	
	return render(request,'accounts/products.html', {'products':products})


def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all()
	orders_count = orders.count()

	context = {'customer':customer, 'orders':orders, 'orders_count':orders_count}
	return render(request,'accounts/customer.html', context)
