from django.shortcuts import redirect
from django.contrib import messages

def login_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.warning(request,"you must login first!")
            return redirect("log_view")
        else:
            return fn(request,*args,**kwargs)
    
    return wrapper
         
       
