from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import TemplateView
from ekartApp.models import Product,Cart,Order
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from ekartApp.forms import UserRegisterForm,UserLoginForm,CartForm,OrderForm
from django.utils.decorators import method_decorator
from ekartApp.authentication import login_required
from django.core.mail import send_mail,settings

# Create your views here.

# class HomeView(TemplateView):
#     template_name="index.html"

class HomeView(View):
    def get(self,request):
        products=Product.objects.all()
        return render(request,"index.html",{'products':products})
    
class ProductView(View):
    def get(self,request,**kwargs):
        id=kwargs.get("id")
        prod=Product.objects.get(id=id)
        return render(request,"product_view.html",{'product':prod})
    
class UserRegisterView(View):
    def get(self,request):
        form=UserRegisterForm()
        return render(request,'register.html',{'form':form})
    
    def post(self,request):
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"registration successful")
            return redirect("log_view")
        else:
            messages.warning(request,"user already exists")
            return redirect("reg_view")
        
class UserLoginView(View):
    def get(self,request):
        form=UserLoginForm()
        return render(request,'login.html',{'form':form})
    def post(self,request):
        usrnm=request.POST.get("username")
        pswrd=request.POST.get("password")
        res=authenticate(request,username=usrnm,password=pswrd)
        if res:
            login(request,res)
            messages.success(request,"login successfully")
            return redirect("home_view")
            
        else:
            messages.warning(request,"invalid username or password")
            return redirect("log_view")
        
@method_decorator(login_required,name="dispatch")
class AddtoCartView(View):
    def get(self,request,*args,**kwargs):
        form=CartForm()
        return render(request,'add_to_cart.html',{'form':form})
    
    def post(self,request,*args,**kwargs):
        product=Product.objects.get(id=kwargs.get("id"))
        user=request.user
        quantity=request.POST.get("quantity")
        cart_instance=Cart.objects.filter(user=user,products=product).exclude(status="order-placed")
        if cart_instance:
            cart_instance[0].quantity+=int(quantity)
            cart_instance[0].save()
            messages.success(request,'Item added to cart')
            return redirect("home_view")
        else:
            Cart.objects.create(user=user,products=product,quantity=quantity)
            messages.success(request,'item added to cart')
            return redirect("home_view")
    
class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect("log_view")


class CartListView(View):
    def get(self,request):
        cart_list=Cart.objects.filter(user=request.user,status='in-cart')
        return render(request,'cart_list.html',{'cartlist':cart_list})
    
class PlaceOrderView(View):
    def get(self,request,**kwargs):
        form=OrderForm()
        return  render(request,'add_to_cart.html',{'form':form})
    
    def post(self,request,**kwargs):
        user=request.user
        email=user.email
        cart_instance=Cart.objects.get(id=kwargs.get("id"))
        address=request.POST.get("address")
        Order.objects.create(address=address,user=user,cart=cart_instance)
        cart_instance.status="order-placed"
        cart_instance.save()

        subject = "Order Placed Successfully!"
        message = f"""
        Hi {user.username},

        Thank you for your order! 🎉

        Your order has been successfully placed.
        Shipping Address: {address}

        We will notify you when your order is shipped.

        Best regards,
        Ekart Team
        """
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
        except Exception as e:
            print("Email sending failed:", e)

        return render(request, 'order_success.html', {'user': user})
    

class OrderListView(View):
    def get(self,request):
        orders=Order.objects.filter(user=request.user,status='order-placed')
        return render(request,'order_placed.html',{'orders':orders})
    
    


    

    
    