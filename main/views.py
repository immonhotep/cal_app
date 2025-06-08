from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .mixins import UserIsAnonymous,SuperUserRequiredMixin
from .forms import RegisterForm,ProfileForm,UserForm,FoodForm,DishForm,ResetPasswordForm,ContactMessageForm,AnswerForm
from .models import Foods,Dishes,Amount,ContactMessage,Answer,DishRatio
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect,JsonResponse
from django.db.models import Q

from django.contrib.auth.views import PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
#prevent error related force_text not found
from django.utils.encoding import force_str as force_text

from django.core.mail import send_mail
from itertools import chain


class HomeView(View):
    def get(self,request):
        foods = Foods.objects.filter(authorized=True).order_by('-name')
        p = Paginator(foods,2)
        page = self.request.GET.get('page')

        try:
            foods = p.page(page)
        except PageNotAnInteger:
            foods = p.page(1)
        except EmptyPage:
            foods = p.page(p.num_pages)

        context = {'foods':foods}
        return render(request,'main/home.html',context)
    

class ViewUnathorizedFoods(SuperUserRequiredMixin,View):
       
       def get(self,request):
        foods = Foods.objects.filter(authorized=False).order_by('-uploaded')
        p = Paginator(foods,2)
        page = self.request.GET.get('page')

        try:
            foods = p.page(page)
        except PageNotAnInteger:
            foods = p.page(1)
        except EmptyPage:
            foods = p.page(p.num_pages)

        context = {'foods':foods}
        return render(request,'main/home.html',context)
       

class ViewUnathorizedDishes(SuperUserRequiredMixin,View):
       
       def get(self,request):
        dishes = Dishes.objects.filter(authorized=False).order_by('-uploaded')
        p = Paginator(dishes,2)
        page = self.request.GET.get('page')

        try:
            dishes = p.page(page)
        except PageNotAnInteger:
            dishes = p.page(1)
        except EmptyPage:
            dishes = p.page(p.num_pages)

        context = {'dishes':dishes}
        return render(request,'main/dishes.html',context)





    
class LoginView(View):
    def get(self,request):

        if request.user.is_authenticated:
            return redirect('home')

        form = AuthenticationForm()
        context = {'form':form,'header':'login'}
        return render(request,'main/auth.html',context)
    
    def post(self,request):
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request,f'Welcome {user.username}')
        else:    
            for error in list(form.errors.values()):
                messages.error(request,error)  
                return redirect('login')   
        return redirect('home')
    
class LogoutView(LoginRequiredMixin,View):

    def post(self,request):
        logout(request)
        messages.success(request,'You have been logged out')
        return redirect('home')
    
class RegisterView(View):

    def get(self,request):

        if request.user.is_authenticated:
            return redirect('home')
        
        form = RegisterForm()
        context = {'form':form,'header':'register'}
        return render(request,'main/auth.html',context)

    def post(self,request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            current_site = get_current_site(self.request)

            subject = 'Activate Your Account'
            message = render_to_string('settings/account_activation_email.html', {
            'user':user,
            'domain':current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),})
           
            try:
                user.email_user(subject=subject, message=message)              
                messages.success(self.request,'To finish registration please check your mailbox including spam folder and follow instructions')
            except:
                messages.error(self.request,'Mail Server Connection problem, please turn to website admin')

        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
                return redirect('register')
        return redirect('home')


def account_activation(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)    
    except():
        pass

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Your registration finished now please login')
        return redirect('login')

    else:
        return render(request, 'settings/activation_invalid.html')


class ProfileView(LoginRequiredMixin,View):

    def get(self,request,pk=None):

        if pk is None:
            user = request.user
            profile = request.user.profile
            profile_form = ProfileForm(instance=profile)
            user_form = UserForm(instance=user)
            context = {'profile_form':profile_form,'user_form':user_form,'user':user,'profile':profile}
        else:
            user = get_object_or_404(User,pk=pk)
            profile = user.profile
            context = {'profile':profile,'user':user}

        return render(request,'main/profile.html',context)
        
    def post(self,request):
        user = request.user
        
        profile_form = ProfileForm(request.POST,request.FILES,instance=user.profile)
        user_form = UserForm(request.POST,instance=user)

        if profile_form.is_valid and user_form.is_valid:
            profile_form.save()
            user_form.save()
            messages.success(request,'Your profile has been updated')
        else:
            for error in list(profile_form.errors.values()):
                messages.error(request,error)
            for error in list(user_form.errors.values()):
                messages.error(request,error)
        return redirect('profile')
    


class ChangePasswordView(LoginRequiredMixin,View):

    def get(self,request):
        form = PasswordChangeForm(request.user)
        context = {'form':form}
        return render(request,'main/password-form.html',context)
    
    def post(self,request):
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request,'Your password has been changed')
            return redirect('home')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
                return redirect('password-change')
            

class ResetPasswordView(UserIsAnonymous,SuccessMessageMixin, PasswordResetView):

    form_class = ResetPasswordForm
    template_name = 'settings/password_reset.html'
    email_template_name = 'settings/password_reset_email.html'
    subject_template_name = 'settings/password_reset_subject.txt'

    success_message = "We sent email for you with instructions to change your password." \
                      " if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    
    success_url = reverse_lazy('home')


    def form_invalid(self, form):     
        for key, error in list(form.errors.values()):
            messages.error(self.request, error)      
        return redirect('home')


              
       
class AddFoodView(LoginRequiredMixin,View):

    def get(self, request):
        form = FoodForm()
        context = {'form':form,'header':'Add food'}
        return render(request,'main/food-form.html',context)
    
    def post(self,request):
        form = FoodForm(request.POST,request.FILES)
        if form.is_valid():
            food = form.save(commit=False)
            food.owner = request.user
            food.save()
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
                return redirect('add-food')
        messages.success(request,f'{food.name} created')
        return redirect('add-food')
    

class UpdateFood(LoginRequiredMixin,View):

    def get(self,request,pk):
        food = get_object_or_404(Foods,pk=pk,owner=request.user)
        form = FoodForm(instance=food)
        context = {'form':form,'header':f'Update: {food.name}'}
        return render(request,'main/food-form.html',context)
    
    def post(self,request,pk):
        prev = request.GET.get('prev')
        food = get_object_or_404(Foods,pk=pk,owner=request.user)
        form = FoodForm(request.POST,request.FILES,instance=food)
        if form.is_valid():
            form.save()
            messages.success(request,f'{food.name} updated')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
        return HttpResponseRedirect(prev)
    

class ListOwnFoods(LoginRequiredMixin,View):
    def get(self,request):
        foods = Foods.objects.filter(owner=request.user).order_by('-name')
        p = Paginator(foods,2)
        page = self.request.GET.get('page')

        try:
            foods = p.page(page)
        except PageNotAnInteger:
            foods = p.page(1)
        except EmptyPage:
            foods = p.page(p.num_pages)
        context = {'foods':foods}
        return render(request,'main/home.html',context)
    

class DeleteFood(LoginRequiredMixin,View):

    def post(self,request,pk):
        food = get_object_or_404(Foods,pk=pk,owner=request.user)
        if food:
            dishes = Dishes.objects.filter(ingredients__in=[food.id]).exclude(owner=request.user)
            if dishes.count() == 0:
                food.delete()
                messages.success(request,'Food deleted')
                return redirect(request.META.get('HTTP_REFERER')) 
            else:
                messages.warning(request,'This food unable to delete, other users already used it on their dishes ')
                return redirect(request.META.get('HTTP_REFERER')) 



class FoodDetail(View):

    def get(self,request,pk):
        food = get_object_or_404(Foods,pk=pk)
        if request.user.is_superuser:
            food = food
        elif food.owner == request.user:
            food = food 
        else:
            food = get_object_or_404(Foods,pk=pk,authorized=True)

        same_category = Foods.objects.filter(category__iexact=food.category).exclude(pk=pk).exclude(authorized=False)
        context={'food':food,'same_category':same_category}
        return render(request,'main/food.html',context)


class FoodChart(View):

    def get(self,request,pk):
               
        fat = Foods.objects.values_list('fat', flat=True).get(pk=pk)
        protein = Foods.objects.values_list('protein', flat=True).get(pk=pk)
        fiber = Foods.objects.values_list('fiber', flat=True).get(pk=pk)
        carbohydrate = Foods.objects.values_list('carbohydrate', flat=True).get(pk=pk)
 
        data = [fat,protein,fiber,carbohydrate]
        labels = ['Fat','Protein','Fiber','carbohydrate',]
    
        return JsonResponse(data={
            'labels': labels,
            'data': data,})
    
class DishChart(View):

    def get(self,request,pk):

        dish = get_object_or_404(Dishes,pk=pk)
        amounts = Amount.objects.filter(dish=dish)

        calory = {}
        for amount in amounts:
            val = (amount.food.calory/100 * amount.numb)
            calory.update({amount.food:float(val)})
        fat = {}
        for amount in amounts:
            val = (amount.food.fat/100 * amount.numb)
            fat.update({amount.food:float(val)})
        protein = {}
        for amount in amounts:
            val = (amount.food.protein/100 * amount.numb)
            protein.update({amount.food:float(val)})
        carbohydrate = {}
        for amount in amounts:
            val = (amount.food.carbohydrate/100 * amount.numb)
            carbohydrate.update({amount.food:float(val)})
        fiber = {}
        for amount in amounts:
            val = (amount.food.fiber/100 * amount.numb)
            fiber.update({amount.food:float(val)})
        
        cal_sum = sum(calory.values())
        fat_sum = sum(fat.values())
        prot_sum = sum(protein.values())
        car_sum = sum(carbohydrate.values())
        fib_sum = sum(fiber.values())
        summary = sum(amounts.values_list('numb',flat=True))
                 
        data = [round(fat_sum,3),round(prot_sum,3),round(fib_sum,3),round(car_sum,3)]
        labels = ['Fat','Protein','Fiber','carbohydrate',]
    
        return JsonResponse(data={
            'labels': labels,
            'data': data,
            'sum:':summary,})


class FoodCategoryView(View):

    def get(self,request,category):
        foods = Foods.objects.filter(category__iexact=category,authorized=True).order_by('-name')

        p = Paginator(foods,2)
        page = self.request.GET.get('page')

        try:
            foods = p.page(page)
        except PageNotAnInteger:
            foods = p.page(1)
        except EmptyPage:
            foods = p.page(p.num_pages)
        context = {'foods':foods}
        return render(request,'main/home.html',context)
    

class DishCategoryView(View):

    def get(self,request,category):
        dishes = Dishes.objects.filter(type__iexact=category,authorized=True,private=False).order_by('-name')

        p = Paginator(dishes,2)
        page = self.request.GET.get('page')

        try:
            dishes = p.page(page)
        except PageNotAnInteger:
            dishes = p.page(1)
        except EmptyPage:
            dishes = p.page(p.num_pages)
        context = {'dishes':dishes}
        return render(request,'main/dishes.html',context)
    

class CreateDish(LoginRequiredMixin,View):

    def get(self,request):
        form = DishForm()
        context = {'form':form,'header':'Create dish'}
        return render(request,'main/dish-form.html',context)

    def post(self,request):

        form = DishForm(request.POST,request.FILES)
        if form.is_valid():
            dish = form.save(commit=True)
            dish.owner = request.user
            dish.save()
            for food in dish.ingredients.all():
                amount, created = Amount.objects.get_or_create(dish=dish,food=food,user=request.user)               
            messages.success(request,f'New dish:{dish}  created')
            return redirect('home')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
                return redirect('create-dish')


class ListUserDish(LoginRequiredMixin,View):

    def get(self,request):

        dishes = Dishes.objects.filter(owner=request.user).order_by('-name')
        p = Paginator(dishes,2)
        page = self.request.GET.get('page')

        try:
            dishes = p.page(page)
        except PageNotAnInteger:
            dishes = p.page(1)
        except EmptyPage:
            dishes = p.page(p.num_pages)

        
        context = {'dishes':dishes}
        return render(request,'main/dishes.html',context)
    


class ListAllDish(View):

    def get(self,request):

        dishes = Dishes.objects.filter(private=False,authorized=True).order_by('-name')
        p = Paginator(dishes,2)
        page = self.request.GET.get('page')

        try:
            dishes = p.page(page)
        except PageNotAnInteger:
            dishes = p.page(1)
        except EmptyPage:
            dishes = p.page(p.num_pages)

        
        context = {'dishes':dishes}
        return render(request,'main/dishes.html',context)    
    

class UpdateUserDish(LoginRequiredMixin,View):

    def get(self,request,pk):

        dish = get_object_or_404(Dishes,pk=pk,owner=request.user)
        form = DishForm(instance=dish)  
        context = {'form':form,'header':'Update Dish'}
        return render(request,'main/dish-form.html',context)
    

    def post(self,request,pk):
        prev = request.GET.get('prev')
        dish = get_object_or_404(Dishes,pk=pk,owner=request.user)
        amounts = Amount.objects.filter(user=request.user,dish=dish)
        form = DishForm(request.POST,request.FILES,instance=dish)
        if form.is_valid():
            form.save()       
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
            messages.success(request,f'{dish.name} updated')           
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
        return HttpResponseRedirect(prev)        
        
class DeleteDish(LoginRequiredMixin,View):

    def post(self,request,pk):
        dish = get_object_or_404(Dishes,pk=pk,owner=request.user)
        if dish:
            dish.delete()
            messages.success(request,'Dish deleted')
            return redirect(request.META.get('HTTP_REFERER')) 



class DishDetail(View):

    def get(self,request,pk):
        dish = get_object_or_404(Dishes,pk=pk)

        try:
            ratio = DishRatio.objects.filter(dish=dish,user=request.user)
        except:
            ratio = {}

    
        if request.user.is_superuser:
            dish = dish 
        elif dish.owner == request.user:
            dish = dish 
        else:
            dish = get_object_or_404(Dishes,pk=pk,private=False,authorized=True)

    
        amounts = Amount.objects.filter(dish=dish)
    
        calory = {}
        for amount in amounts:
            val = (amount.food.calory/100 * amount.numb)
            calory.update({amount.food:float(val)})
        fat = {}
        for amount in amounts:
            val = (amount.food.fat/100 * amount.numb)
            fat.update({amount.food:float(val)})
        protein = {}
        for amount in amounts:
            val = (amount.food.protein/100 * amount.numb)
            protein.update({amount.food:float(val)})
        carbohydrate = {}
        for amount in amounts:
            val = (amount.food.carbohydrate/100 * amount.numb)
            carbohydrate.update({amount.food:float(val)})
        fiber = {}
        for amount in amounts:
            val = (amount.food.fiber/100 * amount.numb)
            fiber.update({amount.food:float(val)})

        cal_sum = sum(calory.values())
        fat_sum = sum(fat.values())
        prot_sum = sum(protein.values())
        car_sum = sum(carbohydrate.values())
        fib_sum = sum(fiber.values()) 
        summary = sum(amounts.values_list('numb',flat=True))
        sum_list = [cal_sum,fat_sum,prot_sum,car_sum,fib_sum]

        context = {'dish':dish,
                   'amounts':amounts,
                   'calory':calory,
                   'fat':fat,
                   'protein':protein,
                   'carbohydrate':carbohydrate,
                   'fiber':fiber,
                   'sum_list':sum_list,
                   'summary':summary,
                   'ratio':ratio,     
                   }
        return render(request,'main/dish.html',context)
    


class CountAmount(LoginRequiredMixin,View):

    def post(self,request,pk):

        dish = get_object_or_404(Dishes,pk=pk,owner=request.user)
        counts = request.POST.getlist('count')    
        food_num = 0
        for food in dish.ingredients.all():
            amount, created = Amount.objects.get_or_create(dish=dish,food=food,user=request.user) 
            if created:
                amount.numb = counts[food_num]
                amount.save()
            else:
                amount.numb = counts[food_num]
                amount.save()
            food_num += 1                
        return redirect('dish-detail',dish.pk)

     
class Search(View):

    def get(self,request):
        
        search = request.GET.get('search',None)
        if search is not None:
            foods = Foods.objects.filter(authorized=True).filter(Q(name__icontains=search)|Q(description__icontains=search)).order_by('-name')
        else:
           foods = Foods.objects.all()

        p = Paginator(foods,2)
        page = self.request.GET.get('page')

        try:
            foods = p.page(page)
        except PageNotAnInteger:
            foods = p.page(1)
        except EmptyPage:
            foods = p.page(p.num_pages)

        context = {'foods':foods}
        return render(request,'main/home.html',context)

    
class AuthorizeFoods(SuperUserRequiredMixin,View):
    
    def post(self,request,pk):
        food = get_object_or_404(Foods,pk=pk)
        status = request.POST.get('food-status')
        if status is not None:
            food.authorized = True
            messages.success(request,f'{food} status modified to authorized')
        else:
            food.authorized = False
            dishes = Dishes.objects.filter(ingredients__in=[food.id])
            for dish in dishes:
                if dish.authorized:
                    dish.authorized = False
                    dish.save()

            messages.error(request,f'{food} status modified to unauthorized, dishes status witch contain this food also modified to unauthorized')        
        food.save()
        return redirect('detail-food',pk)
    

class Authorizedishes(SuperUserRequiredMixin,View):
    
    def post(self,request,pk):
        dish = get_object_or_404(Dishes,pk=pk)
        status = request.POST.get('dish-status')
        if status is not None:
            dish.authorized = True
            messages.success(request,f'{dish} status modified to authorized')
        else:
            dish.authorized = False
            messages.error(request,f'{dish} status modified to unathorized')        
        dish.save()
        return redirect('dish-detail',pk)

                
        
class MakeContactMessage(View):

    def get(self,request):
        form = ContactMessageForm()
        context = {'form':form}
        return render(request,'main/message-form.html',context)    
    def post(self,request):
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your message saved, we will soon contact with you')
        else:
            for error in list(form.errors.values()):
                messages.error(request,error)
        return redirect('home')
    

class ListContactMessages(SuperUserRequiredMixin,View):

    def get(self,request):

        answer_form = AnswerForm()
        order_answer = request.GET.get('RadioSelect')
    
        if not order_answer:
            order_answer = "all"

        request.session['order_checked'] = order_answer

        if order_answer == "all":
            contact_messages = ContactMessage.objects.all().order_by('-date')
        elif order_answer == "answered":
            contact_messages = ContactMessage.objects.filter(answered=True).order_by('-date')
        else:
            contact_messages = ContactMessage.objects.filter(answered=False).order_by('-date')


        p = Paginator(contact_messages,1)
        page = self.request.GET.get('page')

        try:
            contact_messages = p.page(page)
        except PageNotAnInteger:
            contact_messages = p.page(1)
        except EmptyPage:
            contact_messages = p.page(p.num_pages)

        context = {'contact_messages':contact_messages,'answer_form':answer_form}
        return render(request,'main/contact_messages.html',context)
    

class SendAswer(SuperUserRequiredMixin,View):

    def post(self,request,pk):

        contact_message = get_object_or_404(ContactMessage,pk=pk)
        answer_form = AnswerForm(request.POST)
    
        if answer_form.is_valid():
            data = answer_form.save(commit=False)
            data.user = request.user
            data.contact_message = contact_message
            data.save()
            contact_message.answered = True
            contact_message.save()

            
            current_site = get_current_site(self.request)
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
                                  
                messages.success(request,f'You sent answer to {contact_message.name}')                    
            except:
                messages.error(self.request,'Mail Server Connection problem, please turn to website admin')
           
        else:
            for error in list(answer_form.errors.values()):
                messages.error(request,error)

        return redirect('contact-messages')

class ListAnswers(SuperUserRequiredMixin,View):

    def get(self,request,pk):
        contact_message = get_object_or_404(ContactMessage,pk=pk)
        answers = Answer.objects.filter(contact_message=contact_message)
        context = {'answers':answers}
        return render(request,'main/contact_messages.html',context)
    

class ListUsers(SuperUserRequiredMixin,View):

    def get(self,request):

        users = User.objects.all().exclude(is_superuser=True).order_by('-date_joined')
        p = Paginator(users,8)
        page = self.request.GET.get('page')

        try:
            users = p.page(page)
        except PageNotAnInteger:
            users = p.page(1)
        except EmptyPage:
            users = p.page(p.num_pages)
        context = {'users':users}
        return render(request,'main/users.html',context)
 
class UserStatusView(SuperUserRequiredMixin,View):
    
    def post(self,request,pk):
        user = get_object_or_404(User,pk=pk)
        status = request.POST.get('user-status')
        if status is not None:
            user.is_active = True
            messages.success(request,f'{user} status modified to active')
        else:
            user.is_active = False
            messages.error(request,f'{user} status modified to inactive')        
        user.save()
        return redirect('users')


class SendStarRating(LoginRequiredMixin,View):

    def post(self,request,pk):

        dish = get_object_or_404(Dishes,pk=pk)
        user = request.user
        rating = DishRatio.objects.filter(dish=dish,user=user)

        if not rating:
            
            star = self.request.POST.get('star')
            if star:
                rate_range, created = DishRatio.objects.get_or_create(dish=dish,user=user,star_rating=star)
            
                if  created:
                    messages.success(self.request,'Your rating has been saved')
            else:
                messages.error(request,'You must select start rating')
                
        return redirect('dish-detail',dish.pk)
