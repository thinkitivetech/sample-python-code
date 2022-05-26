from django.urls import path
from . import views
# from userAuth.views import CustomTokenObtainPairView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [ 
    path('register/user', views.register_user),
    path('register/admin', views.register_admin),
    path('user',views.UserView.as_view()),
    path('user/<int:id>',views.UserViewById.as_view()),
    path('password/update', views.update_password),
    path('verify-email', views.verify_email, name="verify-email"),
    path('password/reset', views.reset_password_request),
    path('reset-password', views.reset_password, name="reset-password"),
    path('reset-password1', views.reset_password1, name="reset-password1"),
    path('login/', jwt_views.TokenObtainPairView.as_view()),
    path('login/refresh', jwt_views.TokenRefreshView.as_view() ),
    path('logout', views.logout),
    
         
]

