from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework.decorators import api_view, permission_classes,authentication_classes

from rest_framework import status
from .serializers import *
from .decorators import serializer  # this decorator required to show 'class based views like' html forms, on api page
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist
from main.models import Amount


from django.contrib.auth.views import PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from main.tokens import account_activation_token
#prevent error related force_text not found
from django.utils.encoding import force_str as force_text

from django.core.mail import send_mail


@api_view(['GET'])
@permission_classes([AllowAny])
def api_summary(request):
    if request.method == "GET":
        api_urls = {
        'API summary' :'api/',
        'Session login' : 'api/api-auth/login/',
        'Session logout' : 'api/api-auth/logout/',
        'Obtain JWT auth token' : 'api/token/',
        'Refresh JWT auth token' : 'api/token/refresh/', 
        'Create new user':'api/create-user/',
        'Update user': 'api/update-user/',
        'Change password':'api/change-password/',
        'List accounts' : 'api/list-accounts/',
        'Modify user status' : 'api/account-status/<int:pk>/',
        'List all foods': 'api/foods/', 
        'Food Detail' : 'api/food/<int:pk>/',       
        'List, Create user foods':'api/user-foods/',
        'Detail, update, delete user foods' :'api/user-food/<int:pk>/',
        'List Unauthorized foods' : 'api/unauthorized-foods/',
        'Modify authorization status of foods' : 'api/food-status/<int:pk>/',
        'List, dishes' : 'api/dishes/',
        'Detail dish' : 'api/dish/<int:pk>/',
        'List create user dish' : 'api/user-dishes/',
        'Detail update delete user dish' : 'user-dish/<int:pk>/',
        'List Food Amounts per dish' : 'api/dish/<int:pk>/amounts/',
        'List unathorized dishes' : 'api/unathorized-dishes/',
        'Modify authorization status of dishes' : 'dish-status/<int:pk>/',              
        'List contact messages' : 'api/contact_messages/',
        'Detail contact message' : 'api/contact_message/<int:pk>/',
        'Create contact message' : 'api/create-contact-message/',
        'Create Answer for contact message' : 'api/create-answer/',
        'List answers for contact message' : 'api/contact_message/<int:pk>/answers/',
        

        }        
        return Response(api_urls)
    

@serializer(UserCreationSerializer)
@api_view(['POST'])
@permission_classes([AllowAny])
def CreateUserAPIView(request):
    if request.method == "POST":
        serializer = UserCreationSerializer(data=request.data)
        if serializer.is_valid():   

            user = serializer.save()
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your Account'
            message = render_to_string('settings/account_activation_email.html', {
            'user':user,
            'domain':current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),})
           
            try:
                user.email_user(subject=subject, message=message)              
                return Response({"detail": "To finish registration please check your mailbox including spam folder and follow instructions"},status=status.HTTP_204_NO_CONTENT)
            except:
                return Response({'error': 'mail server connection problem, turn to side administration'},status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@serializer(UserListSerializer)  
@api_view(['GET'])
@permission_classes([IsAdminUser])
@authentication_classes([SessionAuthentication,JWTAuthentication])
def ListAccountsApiView(request):
    if request.method == "GET":
        users = User.objects.all().exclude(is_superuser=True)
        serializer = UserListSerializer(users,many=True)
        return Response(serializer.data)
    

@serializer(AccountStatusSerializer)  
@api_view(['GET','PUT'])
@permission_classes([IsAdminUser])
@authentication_classes([SessionAuthentication,JWTAuthentication])
def AccountStatusAPIView(request,pk):
    try:
        user = User.objects.get(pk=pk)
        if user.is_superuser:
            return Response({"error": "forbidden"},status=403)

    except ObjectDoesNotExist:
        return Response({'error': 'user not found'},status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = AccountStatusSerializer(user)
        return Response(serializer.data)
    
    if request.method == "PUT":
        serializer = AccountStatusSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@serializer(UserUpdateSerializer)  
@api_view(['GET','PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication,JWTAuthentication])
def UserUpdateAPIView(request):
    if request.method == "GET":
        user = request.user
        serializer = UserUpdateSerializer(user)
        return Response(serializer.data)
    
    if request.method == "PUT":
        user = request.user
        serializer = UserUpdateSerializer(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@serializer(ChangePasswordSerializer)  
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication,JWTAuthentication])
def ChangePasswordAPIView(request):
    if request.method == "PUT":
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            new_password1 = serializer.validated_data['new_password1']     
            user.set_password(new_password1)
            user.save()
            update_session_auth_hash(request, user)
            return Response({"detail": "Password updated successfully"},status=status.HTTP_204_NO_CONTENT)        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@serializer(FoodSerializer)  
@api_view(['GET'])
@permission_classes([AllowAny])
def ListFoodsApiView(request):
    if request.method == "GET":
        foods = Foods.objects.filter(authorized=True)
        serializer = FoodSerializer(foods,many=True)
        return Response(serializer.data)
    


@serializer(FoodSerializer)  
@api_view(['GET'])
@permission_classes([IsAdminUser])
@authentication_classes([SessionAuthentication,JWTAuthentication])
def ListUnauthorizedFoodsApiView(request):
    if request.method == "GET":
        foods = Foods.objects.filter(authorized=False)
        serializer = FoodSerializer(foods,many=True)
        return Response(serializer.data)
    


@serializer(FoodAuthorizeSerializer)  
@api_view(['GET','PUT'])
@permission_classes([IsAdminUser])
@authentication_classes([SessionAuthentication,JWTAuthentication])
def FoodStatusApiView(request,pk):
    try:
        food = Foods.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response({'error': 'food not found'},status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = FoodAuthorizeSerializer(food)
        return Response(serializer.data)
    
    if request.method == "PUT":
        serializer = FoodAuthorizeSerializer(food,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  

@serializer(FoodSerializer)  
@api_view(['GET'])
@permission_classes([AllowAny])
def FoodDetailApiView(request,pk):
    try:
        food = Foods.objects.get(pk=pk,authorized=True)
    except ObjectDoesNotExist:
        return Response({'error': 'food not found'},status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = FoodSerializer(food)
        return Response(serializer.data)
    

       
@serializer(FoodSerializer)  
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication,JWTAuthentication])
def FoodListCreateApiView(request):
    if request.method == "GET":
        foods = Foods.objects.filter(owner=request.user)
        serializer = FoodSerializer(foods,many=True)
        return Response(serializer.data)
    
    if request.method == "POST":
        serializer = FoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['owner'] = request.user
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)     


@serializer(FoodSerializer)
@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([SessionAuthentication,JWTAuthentication])
def FoodDetailUpdateDeleteApiView(request,pk):
    try:
        food = Foods.objects.get(pk=pk,owner=request.user)
    except ObjectDoesNotExist:
        return Response({'error': 'food not found'},status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = FoodSerializer(food)
        return Response(serializer.data)
    
    if request.method == "PUT":
        serializer = FoodSerializer(food,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
               
    if request.method == "DELETE":
        dishes = Dishes.objects.filter(ingredients__in=[food.id]).exclude(owner=request.user)
        if dishes.count() == 0:
            food.delete()
            return Response({'success': 'food deleted'},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'This food unable to delete, other users already used it on their dishes'},status=status.HTTP_400_BAD_REQUEST)

        

@serializer(ContactMessageSerializer)  
@api_view(['GET'])
@permission_classes([IsAdminUser])
@authentication_classes([SessionAuthentication,JWTAuthentication])
def ContactMessageListDetailApiView(request,pk=None):

    if pk is not None:
        try:
            message = ContactMessage.objects.get(pk=pk)
            messages={}
        except ObjectDoesNotExist:
            return Response({'error': 'food not found'},status=status.HTTP_404_NOT_FOUND)
    else:
        messages = ContactMessage.objects.all()
        message = {}
    
    if request.method == 'GET':
        if messages:
            serializer = ContactMessageSerializer(messages,many=True)
        if message:
             serializer = ContactMessageSerializer(message,many=False)
        return Response(serializer.data)
    
@serializer(ContactMessageSerializer)  
@api_view(['POST'])
@permission_classes([AllowAny])
def CreateContactMessageApiView(request):

    if request.method == "POST":
        serializer = ContactMessageSerializer(data = request.POST)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@serializer(AnswerSerializer)  
@api_view(['POST'])
@permission_classes([IsAdminUser])
@authentication_classes([SessionAuthentication,JWTAuthentication])
def CreateAnswerApiView(request):
    if request.method == "POST":
        serializer = AnswerSerializer(data = request.POST)
        if serializer.is_valid():
            contact_message = serializer.validated_data['contact_message']
            serializer.validated_data['user'] = request.user
            contact_message.answered = True
            contact_message.save()
            data = serializer.save()

            current_site = get_current_site(request)
            subject = data.title
            message = data.body
            from_email = request.user.email
            email_to = contact_message.email
            notice_html = render_to_string('settings/emails.html',{ "message": message })

            try:
                send_mail(
                    subject=subject, 
                    message=message, 
                    recipient_list=[email_to], 
                    from_email=from_email, 
                    fail_silently=False,
                    html_message=notice_html 
                    )
            except:
                return Response({'error': 'Mail server connection problems'},status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListCreateUserDishApiView(APIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DishSerializer

    def get(self, request):
        dishes = Dishes.objects.filter(owner=request.user)  
        serializer = DishSerializer(dishes, many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer = DishSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['owner'] = request.user
            dish = serializer.save()
            for food in serializer.validated_data['ingredients']:       
                amount, created = Amount.objects.get_or_create(dish=dish,food=food,user=request.user)           
            return Response(serializer.data)
        return Response(serializer.errors,status=400)
    

class DetailUpdateDeleteUserDishApiView(APIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DishSerializer

    def get(self, request,pk):
        try:
            dish = Dishes.objects.get(pk=pk,owner=request.user)
        except ObjectDoesNotExist:
            return Response({'error': 'dish not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = DishSerializer(dish, many=False)
        return Response(serializer.data)
    
    def put(self,request,pk):
        try:
            dish = Dishes.objects.get(pk=pk,owner=request.user)
        except ObjectDoesNotExist:
            return Response({'error': 'dish not found'}, status=400)
        
        serializer = DishSerializer(dish, data=request.data)
        if serializer.is_valid():
            dish=serializer.save()
            amounts = Amount.objects.filter(user=request.user,dish=dish)
            for food in dish.ingredients.all():
                if amounts.exists():
                    for amount in amounts:
                        if amount.food == food:
                                pass
                        else:
                            data, created = Amount.objects.get_or_create(dish=dish,food=food,user=request.user)
                else:
                    data, created = Amount.objects.get_or_create(dish=dish,food=food,user=request.user)
           
            for amount in amounts:
                if amount.food in dish.ingredients.all():
                    pass
                else:
                    amount.delete()
            return Response(serializer.data)
        return Response(serializer.errors,status=400)

    def delete(self,request,pk):
        try:
            dish = Dishes.objects.get(pk=pk,owner=request.user)
            dish.delete()
            return Response({'success': 'dish deleted'}, status=200)
        except ObjectDoesNotExist:
            return Response({'error': 'dish not found'}, status=400)
        

class ListDetailDishApiView(APIView):

    permission_classes = [AllowAny]
    serializer_class = DishSerializer

    def get(self, request,pk=None):
        if pk is not None:
            try:
                dish = Dishes.objects.get(pk=pk,private=False,authorized=True)
            except ObjectDoesNotExist:
                 return Response({'error': 'dish not found'}, status=400)
            serializer = DishSerializer(dish, many=False)
            return Response(serializer.data)  
        else:
            dishes = Dishes.objects.filter(private=False,authorized=True)  
            serializer = DishSerializer(dishes, many=True)
            return Response(serializer.data)

        

class ListAmountNumberApiView(APIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AmountSerializer

    def get(self,request,pk):
        try:
            dish = Dishes.objects.get(pk=pk,owner=request.user)
            amounts = Amount.objects.filter(user=request.user,dish=dish)
            serializer = AmountSerializer(amounts,many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({'error': 'dish not found'}, status=400)



class DetailUpdateAmountNumberApiView(APIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AmountSerializer

    def get(self,request,pk):
        try:
            amount = Amount.objects.get(pk=pk,user=request.user)
            serializer = AmountSerializer(amount,many=False)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({'error': 'amount not found'}, status=400)

    def put(self,request,pk):
        try:
            amount = Amount.objects.get(pk=pk,user=request.user)
            serializer = AmountSerializer(amount, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors,status=400)
        except ObjectDoesNotExist:
            return Response({'error': 'object does not exist'}, status=400)
        


class ListUnathorizedDishesApiView(APIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = DishSerializer


    def get(self,request):

        dishes = Dishes.objects.filter(authorized=False)
        serializer = DishSerializer(dishes,many=True)
        return Response(serializer.data)
 


class DishStatusApiView(APIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = DishAuthorizeSerializer

    def get(self,request,pk):
        try:
            dish = Dishes.objects.get(pk=pk)
            serializer = DishAuthorizeSerializer(dish,many=False)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            return Response({'error': 'dish not found'}, status=400)

    def put(self,request,pk):
        try:
            dish = Dishes.objects.get(pk=pk)
            serializer = DishAuthorizeSerializer(dish, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors,status=400)
        except ObjectDoesNotExist:
            return Response({'error': 'dish not found'}, status=400)
        
        

class ViewAnswersApiView(APIView):

    authentication_classes = [SessionAuthentication,JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = AnswerSerializer

    def get(self,request,pk):
        try:
            contact_message = ContactMessage.objects.get(pk=pk)
            answers = Answer.objects.filter(contact_message = contact_message)
            if answers:
                serializer = AnswerSerializer(answers,many=True)
                return Response(serializer.data) 
            return Response({'error': 'no answers'}, status=400)          
        except ObjectDoesNotExist:
             return Response({'error': 'contact message not found'}, status=400)














      

        
                

        









