from django.shortcuts import render,redirect,get_object_or_404
from django.views.decorators.http import require_POST
from pages.models import Course
from .cart import Cart
from .forms import CartAddProductForm

# Create your views here.

@require_POST
def cart_add(request,course_id=None):
    cart = Cart(request)
    course = get_object_or_404(Course,id=course_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        ce =form.cleaned_data
        cart.add(course=course,quantity=ce["quantity"],update_quantity=ce["update"])
    return redirect("cart:cart_detail")

def cart_remove(request,course_id=None):
    cart = Cart(request)
    course = get_object_or_404(Course,id = course_id)
    cart.remove(course)
    return redirect("cart:cart_detail")

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item["update_quantity_form"] = CartAddProductForm(initial={"quantity":item["quantity"],"update":True})
    return render(request,"cart/cart_detail.html",{"cart":cart})


