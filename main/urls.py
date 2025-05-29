from django.urls import path
from .views import *
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('',HomeView.as_view(),name='home'),
    path('unauthorized-foods',ViewUnathorizedFoods.as_view(),name='unauthorized-foods'),
    path('unauthorized-dishes',ViewUnathorizedDishes.as_view(),name='unauthorized-dishes'),
    path('user-login/',LoginView.as_view(),name='login'),
    path('user-logout/',LogoutView.as_view(),name='logout'),
    path('user-register/',RegisterView.as_view(),name='register'),
    path('profile/',ProfileView.as_view(),name='profile'),
    path('profile/<int:pk>/',ProfileView.as_view(),name='show-profile'),
    path('password-change/',ChangePasswordView.as_view(),name='password-change'),
    path('users/',ListUsers.as_view(),name='users'),
    path('user-status/<int:pk>/',UserStatusView.as_view(),name='user-status'),
    path('account_activation/<uidb64>/<token>', views.account_activation, name='account_activation'),

    path('add-food/',AddFoodView.as_view(),name='add-food'),
    path('update-food/<int:pk>/',UpdateFood.as_view(),name='update-food'),
    path('list-own-foods/',ListOwnFoods.as_view(),name='list-own-foods'),
    path('delete-food/<int:pk>/',DeleteFood.as_view(),name='delete-food'),
    path('detail-food/<int:pk>/',FoodDetail.as_view(),name='detail-food'),
    path('food-chart/<int:pk>/',FoodChart.as_view(),name='food_chart'),
    
    path('dish-chart/<int:pk>/',DishChart.as_view(),name='dish-chart'),
    path('food-category/<str:category>/',FoodCategoryView.as_view(),name='food-category'),
    path('dish-category/<str:category>/',DishCategoryView.as_view(),name='dish-category'),
    path('create-dish/',CreateDish.as_view(),name='create-dish'),
    path('list-user-dish/',ListUserDish.as_view(),name='list-dish'),
    path('list-all-dishes/',ListAllDish.as_view(),name='list-all-dishes'),
    path('update-dish/<int:pk>/',UpdateUserDish.as_view(),name='update-dish'),
    path('delete-dish/<int:pk>/',DeleteDish.as_view(),name='delete-dish'),
    path('dish/<int:pk>/',DishDetail.as_view(),name='dish-detail'),
    path('count-amount/<int:pk>/',CountAmount.as_view(),name='count-amount'),

    path('search/',Search.as_view(),name='search'),
    path('contact/',MakeContactMessage.as_view(),name='contact'),
    path('contact-messages/',ListContactMessages.as_view(),name='contact-messages'),
    path('answers/<int:pk>/',ListAnswers.as_view(),name='answers'),

    path('authorize/<int:pk>/',AuthorizeFoods.as_view(),name='authorize'),
    path('authorize-dish/<int:pk>/',Authorizedishes.as_view(),name='authorize-dish'),


    path('send-answer/<int:pk>/',SendAswer.as_view(),name='send_answer'),

     
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='settings/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='settings/password_reset_complete.html'),name='password_reset_complete'),

    path('send_star_rating/<int:pk>/',SendStarRating.as_view(),name='send_star_rating'),

]