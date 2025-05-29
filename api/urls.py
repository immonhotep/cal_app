from django.urls import path,include
from . import views
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView




urlpatterns = [

    path('',views.api_summary, name="api-summary"),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('update-user/',views.UserUpdateAPIView,name='list_create_user'),
    path('create-user/',views.CreateUserAPIView,name='create_user'),
    path('list-accounts/',views.ListAccountsApiView,name='list-accounts'),
    path('account-status/<int:pk>/',views.AccountStatusAPIView,name='account-status'),
    path('change-password/',views.ChangePasswordAPIView,name='change_password'),

    path('foods/',views.ListFoodsApiView,name='list_foods'),
    path('food/<int:pk>/',views.FoodDetailApiView,name='food_detail'),
    path('unauthorized-foods/',views.ListUnauthorizedFoodsApiView,name='foods-unathorized'),
    path('food-status/<int:pk>/',views.FoodStatusApiView,name='food-status'),
    path('user-foods/',views.FoodListCreateApiView,name='user_foods_list_create'),
    path('user-food/<int:pk>/',views.FoodDetailUpdateDeleteApiView,name='user_food_detail_update_delete'),
     
    path('dishes/',ListDetailDishApiView.as_view(),name='dishes'),
    path('dish/<int:pk>/',ListDetailDishApiView.as_view(),name='detail-dish'),
    path('user-dishes/',ListCreateUserDishApiView.as_view(),name='user-list_create_dishes'),    
    path('user-dish/<int:pk>/',DetailUpdateDeleteUserDishApiView.as_view(),name='user-dish_detail_update_delete'),
    path('unathorized-dishes/',ListUnathorizedDishesApiView.as_view(),name='dishes-unathorized'),
    path('dish-status/<int:pk>/',DishStatusApiView.as_view(),name='dish-status'),
    path('dish/<int:pk>/amounts/',ListAmountNumberApiView.as_view(),name='list-amounts'),
    path('amount/<int:pk>/',DetailUpdateAmountNumberApiView.as_view(),name='detail-update-amount'),

    path('contact_messages/',views.ContactMessageListDetailApiView,name='list_contact_messages'),
    path('contact_message/<int:pk>/',views.ContactMessageListDetailApiView,name='detail_contact_message'),
    path('create-contact-message/',views.CreateContactMessageApiView,name='create_contact_message'),
    path('create-answer/',views.CreateAnswerApiView,name='create-answer'),
    path('contact_message/<int:pk>/answers/',ViewAnswersApiView.as_view(),name='view_answers')

]