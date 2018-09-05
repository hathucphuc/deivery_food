from django.conf.urls import url
from cart import views
from django.conf.urls.static import static
from django.conf import settings

app_name = "cart"
urlpatterns = [
    url(r"^cart_add/(\d+)/$",views.cart_add,name="cart_add"),
    url(r"^cart_remove/(\d+)/$",views.cart_remove,name="cart_remove"),
    url(r"^cart_detail/",views.cart_detail,name="cart_detail"),
]