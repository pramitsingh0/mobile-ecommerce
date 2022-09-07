from django.urls import path

from . import views

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("signup", views.sign_up, name="signup"),
    path("index", views.index, name="index"),
    path('verify', views.verify, name="verify"),
    path('logout', views.logout_view, name="logout"),
    path('infopage/<int:product_id>', views.product_page, name='infopage'),
    path('sell', views.sell_phones, name='sell'),
]
