from django.conf import settings
from pages.models import Course



class Cart(object):

    def __init__(self,request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart

    def add(self,course,quantity =1,update_quantity=False):
        course_id = str(course.pk)
        if course_id not in self.cart:
            self.cart[course_id]= {"quantity":0,"price":str(course.price)}
        if update_quantity:
            self.cart[course_id]["quantity"] = quantity
        else:
            self.cart[course_id]["quantity"] += quantity

        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified  = True

    def remove(self,course):
        course_id = str(course.pk)
        if course_id in self.cart:
            del self.cart[course_id]
            self.save()

    def __iter__(self):
        course_ids = self.cart.keys()
        courses = Course.objects.filter(id__in= course_ids)
        for course in courses:
            self.cart[str(course.pk)]["course"] = course
        for item in self.cart.values():
            item["total_price"] = int(item["price"]) * item["quantity"]
            yield item

    def __len__(self):
        return sum(int(item["quantity"]) for item in self.cart.values())

    def get_total_price(self):
        return sum((int(item["price"])) * int(item["quantity"]) for item in self.cart.values())

    def clear(self):
        self.cart = {}
        self.save()



