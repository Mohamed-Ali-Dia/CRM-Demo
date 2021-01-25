from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm, CustomerForm

#Dashboard home page
def home(request):
	#Retrieving all orders
	orders = Order.objects.all()

	#Retrieving all customers
	customers = Customer.objects.all()

	#The total number of customers
	total_customers = customers.count()

	#The total number of orders
	total_orders = orders.count()

	#The total number of orders delivered
	delivered = orders.filter(status="Delivered").count()

	#The total number of orders pending
	pending = orders.filter(status="Pending").count()

	context = {'orders':orders, 'customers':customers, 'total_orders':total_orders, 'total_customers':total_customers, 'delivered':delivered, 'pending':pending}

	return render(request,'accounts/dashboard.html', context)

#Retrieve all products
def products(request):
	#getting all products from the DB
	products = Product.objects.all()
	
	return render(request,'accounts/products.html', {'products':products})

#Retrieve all orders for a specific customer 
def customer(request, pk_test):
	#getting the customer with id=pk_test
	customer = Customer.objects.get(id=pk_test)

	#getting all orders ordered by the customer
	orders = customer.order_set.all()

	#Counting all orders ordered by the customer
	orders_count = orders.count()

	#The total number of orders pending
	orders_pending = orders.filter(status="Pending").count()

	#The total number of orders out for delivery
	orders_outdelivery = orders.filter(status="Out for delivery").count()

	context = {'customer':customer, 'orders':orders, 'orders_count':orders_count, 'orders_pending':orders_pending, 'orders_outdelivery':orders_outdelivery}
	return render(request,'accounts/customer.html', context)


#Place order for a customer
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
	#form = OrderForm(initial={'customer': customer})
	if request.method == 'POST':
		#form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'formset': formset}
	return render(request, 'accounts/order_form.html', context)

#delete order
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'accounts/delete_form.html', context)


#Update an Order
def updateOrder(request, pk):
	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form': form}

	return render(request, 'accounts/order_form.html', context) 


#Create new customer
def createCustomer(request):
	form = CustomerForm()
	if request.method == 'POST':
		form = CustomerForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
			
	context = {'form':form}
	return render(request, 'accounts/customer_form.html', context)

#delete customer
def deleteCustomer(request, pk):
	customer = Customer.objects.get(id=pk)
	if request.method == "POST":
		customer.delete()
		return redirect('/')

	context= {'item':customer}
	return render(request, 'accounts/delete_form.html', context)


#Update customer
def updateCustomer(request, pk):
	customer = Customer.objects.get(id=pk)
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, instance=customer)
		if form.is_valid():
			form.save()
			return redirect('/')
	context = {'form': form}

	return render(request, 'accounts/customer_form.html', context) 
