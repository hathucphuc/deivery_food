from django.shortcuts import render,redirect
from .models import Course
from cart.forms import CartAddProductForm
from .forms import UserForm, UserProfileInfoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout



# Create your views here.


def index(request):
    return render(request, "pages/index.html")


def korean_food(request):
    '''Korean food'''
    course_list_korean= Course.objects.filter(restaurant=2).order_by("name")
    part1 = int(len(course_list_korean)/2)
    list1 = []
    for i in range(0,part1,1):
        list1.append(course_list_korean[i])

    list2 = []
    for i in range(part1,len(course_list_korean),1):
        list2.append(course_list_korean[i])
    
    course_dic = {"courses":course_list_korean,"course1":list1,"course2":list2}
    return render(request,"pages/korean_food.html",context=course_dic)

def pizza(request):
    '''pizza'''
    course_list_pizza=Course.objects.filter(restaurant=3).order_by("name")
    part1 = int(len(course_list_pizza)/2)
    list1 = []
    for i in range(0,part1,1):
        list1.append(course_list_pizza[i])

    list2 = []
    for i in range(part1,len(course_list_pizza),1):
        list2.append(course_list_pizza[i])

    course_dic = {"courses_pizza":course_list_pizza,"course1":list1,"course2":list2}
    return render(request,"pages/pizza.html",context=course_dic)

def course_detail(request,id_numb=None):
    course=Course.objects.get(pk=id_numb)
    cart_product_form = CartAddProductForm()
    return render(request,"pages/course_detail.html",context={"course":course,"cart_product_form":cart_product_form})



# Register user:

def register(request):
    registered = False
    if request.method == "POST":
        form_user = UserForm(data=request.POST)
        form_por = UserProfileInfoForm(data=request.POST)
        if form_user.is_valid() and form_por.is_valid():
            user = form_user.save()
            user.set_password(user.password)
            user.save()

            profile = form_por.save(commit=False)
            profile.user = user

            if "picture" in request.FILES:
                profile.picture = request.FILES["picture"]

            profile.save()

            registered = True
            return redirect("pages:registered")
    
    else:
        form_user =UserForm()
        form_por = UserProfileInfoForm()
    return render(request,"pages/registration.html",{"form_user":form_user,"form_por":form_por,"registered":registered})
                
def registered(request):
    return render(request,"pages/registered.html")

# Login user

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect("pages:index")

        else:
            login_result = "Username và password không hợp lệ"
            return render(request,"pages/login.html",{"login_result":login_result})
    else:
        return render(request,"pages/login.html")
@login_required
def user_logout(request):
    logout(request)
    return redirect("pages:index")
    