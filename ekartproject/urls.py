"""
URL configuration for ekartproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ekartApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomeView.as_view(),name="home_view"),
    path('product/<int:id>', views.ProductView.as_view(),name="product_view"),
    path('register', views.UserRegisterView.as_view(),name="reg_view"),
    path('login', views.UserLoginView.as_view(),name="log_view"),
    path('add/cart/<int:id>', views.AddtoCartView.as_view(),name="add_to_cart"),
    path('logout', views.LogoutView.as_view(),name="logout"),
    path('cartlist', views.CartListView.as_view(),name="cartlist_view"),
    path('place/order/<int:id>', views.PlaceOrderView.as_view(),name="place_order"),
    path('order', views.OrderListView.as_view(),name="order_view"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
