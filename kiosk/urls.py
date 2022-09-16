"""kiosk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from controller import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^api/jwt', views.jwt),
    url(r'^api/ads', views.ads),
    url(r'^api/checkNumber', views.checkNumber),
    url(r'^api/order', views.order),
    url(r'^api/charge', views.charge),
    url(r'^api/prefix', views.prefix),
    url(r'^api/searchNumber', views.searchNumber),
    url(r'^api/blockUnblock', views.blockUnblock),
    url(r'^api/userConfirmation', views.userConfirmation),
    url(r'^api/hur', views.hur),
    url(r'^api/createNumber', views.createNumber),
    url(r'^api/payment', views.payment),
    url(r'^api/checkPayment', views.checkPayment),
    url(r'^api/barimt', views.barimt),
    url(r'^api/baiguullagaRegister', views.baiguullagaRegister),
    url(r'^api/callBackUrl', views.callBackUrl),
]
