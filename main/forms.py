from django import forms
from .models import Profile,Foods,Dishes,Amount,ContactMessage,Answer
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout,HTML
from crispy_forms.bootstrap import InlineCheckboxes

from django.contrib.auth.forms import UserCreationForm,PasswordResetForm


class RegisterForm(UserCreationForm):

    username = forms.CharField(max_length=250)
    email = forms.EmailField(max_length=100)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()
    usable_password = None

    class Meta:
        model = User
        fields=('username','email','first_name','last_name','password1','password2')



class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('bio','image')


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')

    username = forms.CharField(max_length=100,required=True)
    first_name = forms.CharField(max_length=150,required=True)
    last_name = forms.CharField(max_length=150,required=True)
    email = forms.EmailField(max_length=100,required=True)


class UserStatusForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('is_active',)



class ResetPasswordForm(PasswordResetForm):

    def __init__(self,*args,**kwargs):
        super(ResetPasswordForm,self).__init__(*args,**kwargs)
        
    email = forms.EmailField(max_length=100,required=True)



class FoodForm(forms.ModelForm):

    class Meta:
        model = Foods
        fields = ('name','description','category','image','calory','fiber','fat','protein','carbohydrate')
  

    name = forms.CharField(max_length=250,required=True)
    calory = forms.DecimalField(max_digits=8,decimal_places=2)
    fat = forms.DecimalField(max_digits=8,decimal_places=2)
    protein = forms.DecimalField(max_digits=8,decimal_places=2)
    carbohydrate = forms.DecimalField(max_digits=8,decimal_places=2)

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

    category = forms.ChoiceField(
        
        choices=TYPE,
        widget=forms.Select()

    )




class DishForm(forms.ModelForm):

    class Meta:
        model = Dishes
        fields = ('private','name','description','image','type','ingredients')

    MEAL = (

        ('Breakfast','Breakfast'),
        ('Lunch','Lunch'),
        ('Dinner','Dinner'),
        ('Other','Other'),
    )
    
    name = forms.CharField(max_length=250,required=True)
    type = forms.ChoiceField(
        
        choices=MEAL,
        widget=forms.Select()

    )

    ingredients = forms.ModelMultipleChoiceField(required=False,
        queryset=Foods.objects.filter(authorized=True),
        widget=forms.CheckboxSelectMultiple())
    
    
    def __init__(self, *args, **kwargs):
        super(DishForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'POST' 
        self.helper.layout = Layout( 
            'private',
            'name', 
            'description',
            'image',
            'type',
            InlineCheckboxes('ingredients',css_class='ingredients-checkboxes mb-1'),
            Submit('submit', u'Submit', css_class='btn btn-primary'),
            HTML('<a id="user-link" class="btn btn-warning" href="javascript:history.back()">back</a>'),
            
    )
        
    
class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ('title','body','name','email','phone')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('title','body')





    
    

   
