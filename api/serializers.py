from main.models import Foods,Dishes,Amount,ContactMessage,Answer
from rest_framework import serializers
from rest_framework.reverse import reverse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from django.core.validators import MinValueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer




class UserCreationSerializer(serializers.ModelSerializer):

    username = serializers.CharField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True,style={'input_type': 'password'},validators=[validate_password])
    password2 = serializers.CharField(write_only=True,style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name' ,'password', 'password2')
        extra_kwargs = {"email": {"required": True, "allow_null": False},"first_name":{"required": True, "allow_null": False},"last_name":{"required": True, "allow_null": False}}
        read_only_fields = ('id',)
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "two password fields didn't match"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name','is_active')


class UserUpdateSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name')
        read_only_fields = ('id',)
        extra_kwargs = {"email": {"required": True, "allow_null": False},"first_name":{"required": True, "allow_null": False},"last_name":{"required": True, "allow_null": False}}


class AccountStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name','is_active')
        read_only_fields = ('id','username','email','first_name','last_name')



class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(write_only=True,style={'input_type': 'password'})
    new_password1 = serializers.CharField(write_only=True,style={'input_type': 'password'},validators=[validate_password])
    new_password2 = serializers.CharField(write_only=True,style={'input_type': 'password'})


    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "old password is wrong"})
        return value

    def validate(self, data):
        user = self.context.get("request").user
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({"old_password": "old password is wrong"})
        
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({"new_password2": "two password fields didn't match"})
        return data
    



class FoodSerializer(serializers.ModelSerializer):

    TYPE=[

        ('Vegetables','Vegetables'),
        ('Meats','Meats'),
        ('Pastas','Pastas'),
        ('Grains','Grains'),
        ('Dairy products','Dairy products'),
        ('Fruits','Fruits'),
        ('Sweets','Sweets'),
        ('Drinks','Drinks'),
        ('Other','Other'),
        
    ]

    category = serializers.ChoiceField(choices=TYPE)

    description = serializers.CharField(required=True,max_length=3000)
    image = serializers.ImageField(required=True)
    calory = serializers.DecimalField(required=True,max_digits=8, decimal_places=2)
    fiber = serializers.DecimalField(required=True,max_digits=8, decimal_places=2)
    fat = serializers.DecimalField(required=True,max_digits=8, decimal_places=2)
    protein = serializers.DecimalField(required=True,max_digits=8, decimal_places=2)
    carbohydrate = serializers.DecimalField(required=True,max_digits=8, decimal_places=2)
   

    class Meta:
        model = Foods
        fields = ('id','name','owner','authorized','description','category','image','calory','fiber','fat','protein','carbohydrate')
        read_only_fields = ('id','owner','authorized')


class FoodAuthorizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Foods
        fields = ('id','name','owner','authorized','description','category','image','calory','fiber','fat','protein','carbohydrate')
        read_only_fields = ('id','name','owner','description','category','image','calory','fiber','fat','protein','carbohydrate')


class DishAuthorizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dishes
        fields = ('id','owner','private','name','description','image','type','ingredients','authorized','uploaded')
        read_only_fields = ('id','owner','private','name','description','image','type','ingredients','uploaded')


class AmountSerializer(serializers.ModelSerializer):

    numb = serializers.IntegerField(default=100,validators=[MinValueValidator(0)])

    class Meta:
        model = Amount
        fields = ('id','numb','food')
        read_only_fields = ('id','food')
        


class DishSerializer(serializers.ModelSerializer):

    MEAL = (

        ('Breakfast','Breakfast'),
        ('Lunch','Lunch'),
        ('Dinner','Dinner'),
        ('Other','Other'),
    )

    name = serializers.CharField(max_length=250)
    description = serializers.CharField(max_length=3000)
    image = serializers.ImageField(required=False)
    type = serializers.ChoiceField(choices=MEAL,default="Other")
    ingredients = serializers.PrimaryKeyRelatedField(many = True, queryset = Foods.objects.filter(authorized=True))
   

    class Meta:
        model = Dishes
        fields = ('id','private','authorized','name','description','image','type','ingredients')
        read_only_fields = ('id','authorized')
        depth = 1
    
    

class ContactMessageSerializer(serializers.ModelSerializer):

    title = serializers.CharField(max_length=250)
    body = serializers.CharField(max_length=3000)
    name = serializers.CharField(max_length=250)
    email = serializers.EmailField(max_length=100)
    phone = serializers.CharField(max_length=20)


    class Meta:
        model = ContactMessage
        fields = ('id','title','body','name','email','phone','answered')
        read_only_fields = ('id','answered')


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('id','contact_message','user','title','body','date')
        read_only_fields = ('id','user','date')



