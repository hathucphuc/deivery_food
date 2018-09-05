from django.shortcuts import render
from orders.models import OrderItem
from orders.forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth.models import User
from pages.forms import UserForm, UserProfileInfoForm
from pages.models import UserProfileInfo
from django.core.mail import EmailMessage, send_mail
from django.template.loader import get_template
from django.template import Context
# Create your views here.

def order_create(request):
	cart = Cart(request)
	#form = OrderCreateForm()

	if request.method == "POST":
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			order = form.save()
			for item in cart:
				OrderItem.objects.create(order = order,course = item["course"],price = item["price"],quantity = item["quantity"])

			#cart.clear()

			# send email to confirm
			subject = "Email xac nhan da nhan don hang"
			to = [order.email]
			from_email = "haphuc.testing@gmail.com"
			message = get_template("orders/send_email.html").render({"cart":cart})
			msg = EmailMessage(subject,message,to=to,from_email=from_email)
			msg.content_subtype = "html"
			msg.send()

			cart.clear()
			return render(request,"orders/created.html",context= {"order":order})

	else:
		if request.user.is_authenticated:
			user = request.user
			userprofile = UserProfileInfo.objects.get(user=user)
			form = OrderCreateForm(initial={"first_name":user.first_name,"last_name":user.last_name,"phone":userprofile.phone,"email":user.email,"address":userprofile.address,"postal_code":"","city":""})
		else:
			form = OrderCreateForm()

	

	return render(request,"orders/create.html",context={"form":form})