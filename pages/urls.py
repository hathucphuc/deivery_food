from django.conf.urls import url
from . import views

app_name = "pages"
urlpatterns = [
    url(r"^$", views.index, name="index"),
    url(r"^korean_food.html/$", views.korean_food, name="korean_food"),
    url(r"^pizza.html/$", views.pizza, name="pizza"),
    url(r"^course_detail/(\d+)/$", views.course_detail, name="course_detail"),
    url(r"^register/$",views.register,name="register"),
    url(r"^registered/$",views.registered,name="registered"),
    url(r"^logout/$",views.user_logout,name="logout"),
    url(r"^login/$",views.user_login,name="login"),

]
