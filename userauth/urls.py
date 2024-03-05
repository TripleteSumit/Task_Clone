from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.create_task),
    path('user/delete/<int:id>/', views.delete_task),
    path('user/update/<int:id>/', views.update_task),
    path('user/updating/<int:id>/', views.do_update),
    path('user/com/<int:id>/', views.complete_task)
]
