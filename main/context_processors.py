from .models import  Foods,Dishes
from collections import defaultdict

#generate dictionary where for the key (category) will assing two values: first is font awesome specified icon, second is the count 
def navbar_context(request):
    food_categories=[("Vegetables","fa-carrot"),("Meats","fa-drumstick-bite"),("Pastas","fa-pizza-slice"),("Grains","fa-wheat-awn"),("Dairy products","fa-cheese"),("Fruits","fa-lemon"),("Sweets","fa-ice-cream"),("Drinks","fa-wine-glass"),("Other","fa-circle-question")]
    food_cat_dict = defaultdict(list) 
    for key, value in food_categories:
        {food_cat_dict[key].append(value)} 
        count = Foods.objects.filter(category__iexact=key,authorized=True).count()
        food_cat_dict[key].extend([count])
    food_cat_dict=dict(food_cat_dict)

    
    dish_categories=[('Breakfast','fa-mug-saucer'),('Lunch','fa-sun'),('Dinner','fa-moon'),('Other','fa-circle-question')]
    dish_cat_dict = defaultdict(list) 
    for key, value in dish_categories:
        {dish_cat_dict[key].append(value)} 
        count = Dishes.objects.filter(type__iexact=key,authorized=True,private=False).count()
        dish_cat_dict[key].extend([count])
    dish_cat_dict=dict(dish_cat_dict)
    


    return{'food_cat_dict':food_cat_dict,'dish_cat_dict':dish_cat_dict}






"""
('Breakfast','Breakfast'),
        ('Lunch','Lunch'),
        ('Dinner','Dinner'),
        ('Other','Other'),
"""