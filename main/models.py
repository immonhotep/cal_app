from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from PIL import Image
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from django.db.models import Avg,Count


class Profile(models.Model):

    bio = HTMLField(blank=True,default="",max_length=3000)
    image = models.ImageField(null=True,blank=True, upload_to="images/avatars")
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    

    
@receiver(post_save, sender=User)
def handler_function(sender, instance, created, **kwargs):
    if  created:
        user_profile = Profile(user=instance)
        user_profile.save()



        
      
class Foods(models.Model):

 
    TYPES = (

        ('Vegetables','Vegetables'),
        ('Meats','Meats'),
        ('Pastas','Pastas'),
        ('Grains','Grains'),
        ('Dairy products','Dairy products'),
        ('Fruits','Fruits'),
        ('Sweets','Sweets'),
        ('Drinks','Drinks'),
        ('Other','Other'),

    )

    name = models.CharField(max_length=250,unique=True)
    description = HTMLField(blank=True,default="",max_length=3000)
    category = models.CharField(max_length=30,choices=TYPES,default='Other')
    image = models.ImageField(null=True,blank=True, upload_to="images/foods")
    calory = models.DecimalField(max_digits=8, decimal_places=2, default=0.0, help_text= " You need to add value/100g ")
    fat = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    protein = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    carbohydrate = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    fiber =  models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    owner = models.ForeignKey(User,on_delete=models.CASCADE, null=True) 
    authorized = models.BooleanField(default=False)
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    class Meta:
        verbose_name_plural = "Foods"
    
    
    def save(self, *args, **kwargs):
        super(Foods, self).save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)


class Dishes(models.Model):

    MEAL = (

        ('Breakfast','Breakfast'),
        ('Lunch','Lunch'),
        ('Dinner','Dinner'),
        ('Other','Other'),
    )
    
    name = models.CharField(max_length=250,unique=True)
    description = HTMLField(blank=True,default="",max_length=3000)
    image = models.ImageField(null=True,blank=True, upload_to="images/dishes")
    type = models.CharField(max_length=30, choices=MEAL,default="Other")
    ingredients = models.ManyToManyField(Foods)
    owner = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    private = models.BooleanField(default=False)
    authorized = models.BooleanField(default=False)
    uploaded = models.DateTimeField(auto_now_add=True)
  

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super(Dishes, self).save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image.path)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    

    @property
    def averagerate(self):
        review = DishRatio.objects.filter(dish=self).aggregate(average=Avg('star_rating'))
        avg=0
        if review["average"] is not None:
            avg=float(review["average"])
        return avg
    
    @property
    def countrate(self):
        reviews = DishRatio.objects.filter(dish=self).aggregate(count=Count('id'))
        cnt=0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

    
    class Meta:
        verbose_name_plural = "Dishes"


class Amount(models.Model):

    food = models.ForeignKey(Foods, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dishes,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    numb = models.PositiveIntegerField(default=100)

    def __str__(self):
        return  self.food.name



class ContactMessage(models.Model):

    title = models.CharField(max_length=250)
    body = HTMLField(blank=False,default="",max_length=3000)
    name = models.CharField(max_length=250)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    answered = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Answer(models.Model):

    title = models.CharField(max_length=250)
    body = HTMLField(blank=False,default="",max_length=3000)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    contact_message = models.ForeignKey(ContactMessage,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class DishRatio(models.Model):

    dish = models.ForeignKey(Dishes, related_name="dish_get_ration", on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, related_name="dish_send_ration", on_delete=models.CASCADE, null=True, blank=True)
    star_rating = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):

        return f'{self.user.last_name}-{self.user.first_name} to - {self.dish.name}'