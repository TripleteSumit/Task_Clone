from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register("customers", views.CustomerViewSet)
router.register("products", views.ProductViewSet)
router.register("orders", viewset=views.OrderViewSet, basename="orders")

nested_router = routers.NestedDefaultRouter(router, "products", lookup="product")
nested_router.register(
    "reviews", viewset=views.ReviewViewSet, basename="products-reviews"
)

urlpatterns = router.urls + nested_router.urls
# urlpatterns = [
#     path('customer/', views.CustomerList.as_view()),
#     path('customer/<int:pk>', views.CustomerDetails.as_view())
# ]
