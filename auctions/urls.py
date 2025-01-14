from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name = "categories"),
    path("categories/<str:category>", views.categories_listings, name="categories_listings"),
    path("<str:user>/create_listing", views.create_listing, name="create_listing"),
    path("<str:listing>/listing/<str:user>", views.listing, name="listing"),
    path("<str:user>/watchlist", views.watchlist, name="watchlist")
]
