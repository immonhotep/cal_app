# Calorie application/api Which also can use as recipe book

 - Application backend:
   
 <p align="center">
  <a href="https://go-skill-icons.vercel.app/">
    <img
      src="https://go-skill-icons.vercel.app/api/icons?i=python,django,djangorestframework"
    />
  </a>
</p>
  
- Application Frontend:

 <p align="center">
  <a href="https://go-skill-icons.vercel.app/">
    <img
      src="https://go-skill-icons.vercel.app/api/icons?i=html,bootstrap,css,javascript"
    />
  </a>
</p>

Simple calory/recipe book application, with fine design for educational purposes. 
Not registered users can view food information, and dish information.
Registered users can create public foods with general calory information, and can create public or private dishes. Dishes contain foods with many-to-many relationship. Users can modify food amount in own dishes, and calculate regular calory data in dishes.
Dishes this way can use as calory tracker, and recipe book as well.
Admin user have permission to authorize both foods, and dishes.
Site visitors can send contant messages, and admin cand send answers about.

Complete crud API with similar functions also included.

Main application functions:

Authentication:

- Registration(email confirmed)
- login
- password reset(email confirmed),
- password change,
- account modification

Food and dish realted functions:

- list all foods and dishes 
- list foods and dishes by category
- list user foods and dishes
- add, update, delete foods and dishes
- views food and dish details
- modify foods amount in dishes to calculate calory and some other data
- chart functions both foods and dishes
- star rating system for dishes

Contact message function:
site visitors can send messages to site admins

Admin functions:

- list unathorized dishes, and foods
- authorize/unathorize dishes and foods 
- list users 
- modify user status to active/inactive
- list contact messages
- send aswers to contact messages with email
- list answers 


API:


| Description                         | URLS                                                        | METHODS                          |  PERMISSIONS                                    |
| ----------------------------------- | ----------------------------------------------------------- | -------------------------------- | ----------------------------------------------- |
| api summary                         | http://127.0.0.1:8000/api/                                  | GET, OPTIONS                     | for anybody                                     |
| api login page                      | http://127.0.0.1:8000/api/api-auth/login/                   | GET, POST, PUT, HEAD, OPTIONS    | for anybody, user and password will require     |
| obtain jwt auth token               | http://127.0.0.1:8000/api/token/                            | POST, OPTIONS                    | for anybody, user and password will require     |
| refresh jwt tokens                  | http://127.0.0.1:8000/api/token/refresh/                    | POST, OPTIONS                    | for anybody, refress token will require         |
| user registration                   | http://127.0.0.1:8000/api/create-user/                      | POST, OPTIONS                    | for anybody                                     |
| update user                         | http://127.0.0.1:8000/api/update-user/                      | GET, OPTIONS, PUT                | authenticated users, token or session required  |
| Change password                     | http://127.0.0.1:8000/api/change-password/                  | PUT, OPTIONS                     | authenticated users, token or session required  |
| list Accounts                       | http://127.0.0.1:8000/api/list-accounts/                    | GET, OPTIONS                     | admin only, token or session required           |
| accout status                       | http://127.0.0.1:8000/api/account-status/{int:pk}/          | GET, OPTIONS, PUT                | admin only, token or session required           |
| list foods                          | http://127.0.0.1:8000/api/foods/                            | GET, OPTIONS                     | for anybody                                     |
| food Detail                         | http://127.0.0.1:8000/api/food/{int:pk}/                    | GET, OPTIONS                     | for anybody                                     |
| list, create, user foods            | http://127.0.0.1:8000/api/user-foods/                       | POST, GET, OPTIONS               | authenticated users, token or session required  |
| detail, update, delete user foods   | http://127.0.0.1:8000/api/user-food/{int:pk}/               | DELETE, PUT, GET, OPTIONS        | authenticated users, token or session required  |
| list unathorized food               | http://127.0.0.1:8000/api/unauthorized-foods/               | GET, OPTIONS                     | admin only, token or session required           |
| update food status                  | http://127.0.0.1:8000/api/food-status/{int:pk}/             | PUT, GET, OPTIONS                | admin only, token or session required           |
| list dishes                         | http://127.0.0.1:8000/api/dishes/                           | GET, HEAD, OPTIONS               | for anybody                                     |
| dish detail                         | http://127.0.0.1:8000/api/dish/{int:pk}/                    | GET, HEAD, OPTIONS               | for anybody                                     |
| list create user dish               | http://127.0.0.1:8000/api/user-dishes/                      | GET, POST, HEAD, OPTIONS         | authenticated users, token or session required  |
| detail, update, delete user dish    | http://127.0.0.1:8000/api/user-dish/{int:pk}/               | GET, PUT, DELETE, HEAD, OPTIONS  | authenticated users, token or session required  |
| food amounts per dish               | http://127.0.0.1:8000/api/dish/{int:pk}/amounts/            | GET, HEAD, OPTIONS               | authenticated users, token or session required  |
| list unathorized dishes             | http://127.0.0.1:8000/api/unathorized-dishes/               | GET, HEAD, OPTIONS               | admin only, token or session required           |
| update dish status                  | http://127.0.0.1:8000/api/dish-status/{int:pk}/             | GET, PUT, HEAD, OPTIONS          | admin only, token or session required           |
| list contact messages               | http://127.0.0.1:8000/api/contact_messages/                 | GET, OPTIONS                     | admin only, token or session required           |
| detail contact message              | http://127.0.0.1:8000/api/contact_message/{int:pk}/         | GET, OPTIONS                     | admin only, token or session required           |
| create contact message              | http://127.0.0.1:8000/api/create-contact-message/           | POST, OPTIONS                    | for anybody                                     |
| create answer                       | http://127.0.0.1:8000/api/create-answer/                    | POST, OPTIONS                    | admin only, token or session required           |
| list answers per contact message    | http://127.0.0.1:8000/api/contact_message/{int:pk}/answers/ | GET, HEAD, OPTIONS               | admin only, token or session required           |




Installed modules:

- asgiref==3.8.1
- beautifulsoup4==4.13.4
- crispy-bootstrap5==2025.4
- Django==4.2.20-
- django-bootstrap-v5==1.0.11
- django-crispy-forms==2.4
- -django-tinymce==4.1.0 
- djangorestframework==3.16.0
- djangorestframework_simplejwt==5.5.0 
- drf-redesign==0.5.1 
- fontawesomefree==6.6.0 
- pillow==11.2.1
- PyJWT==2.9.0
- six==1.17.0
- soupsieve==2.7
- sqlparse==0.5.3
- typing_extensions==4.13.2


NOTES:

SENDING MAILS:

This site use email validated registration, password change, and other features too.
For the usage need some kind of mail server at least for the testing, or need modify the settings.py to real email providers port, and credentials

very simple pre-installed method for tesing with fake mail server on localhost port 1025:

aiosmtpd version 1.4.6 installed within the virtual environment with the requirements.txt, so just run in a different terminal (in the same virtual environment) the following command to run fake mailserver:

python -m aiosmtpd -n -l localhost:1025

emails will appear in the terminal



INSTALL:

- clone the repository ( git clone https://github.com/immonhotep/cal_app.git )
- Create python virtual environment and activate it ( depends on op system, example on linux: virtualenv venv  and source venv/bin/activate )
- Install the necessary packages and django  ( pip3 install -r requirements.txt ) into the virtual environment
- Create the database:( python3 manage.py makemigrations and then python3 manage.py migrate )
- Create a superuser ( python3 manage.py createsuperuser )
- Run the application ( python3 manage.py runserver )



A Sample example image from dish page: 


  ![sample dish](https://github.com/user-attachments/assets/059c283e-5b71-4a5e-95f0-9b133272826c)

