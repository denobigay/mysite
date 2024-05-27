from django.shortcuts import render, redirect
from .models import Gender, User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from datetime import datetime

# Create your views here.

def index_gender(request):
    genders = Gender.objects.all() # SELECT * FROM genders

    context = {
        'genders': genders
    }

    return render(request, 'gender/index.html', context)
    
def create_gender(request):
    return render(request, 'gender/create.html')

def store_gender(request):
    gender = request.POST.get('gender')
    Gender.objects.create(gender=gender) # INSERT INTO genders(gender) VALUES(gender)
    messages.success(request, 'Gender successfully saved.')
    return redirect('/genders')

def show_gender(request, gender_id):
    gender = Gender.objects.get(pk=gender_id) # SELECT * FROM genders WHERE  gender_id = gender_id

    context = {
        'gender': gender, 
    }

    return render(request, 'gender/show.html', context)

def edit_gender(request, gender_id):
    gender = Gender.objects.get(pk=gender_id) # SELECT * FROM genders WHERE  gender_id = gender_id

    context = {
        'gender': gender, 
    }

    return render(request, 'gender/edit.html', context)

def update_gender(request, gender_id):
    gender = request.POST.get('gender')
    
    Gender.objects.filter(pk=gender_id).update(gender=gender) # UPDATE genders SET gender = gender WHERE gender_id = gender_id 
    messages.success(request, 'Gender succesfully updated.')

    return redirect('/genders')

def delete_gender(request, gender_id):
    gender = Gender.objects.get(pk=gender_id) # SELECT * FROM genders WHERE  gender_id = gender_id

    context = {
        'gender': gender, 
    }

    return render(request, 'gender/delete.html', context)

def destroy_gender(request, gender_id):
    Gender.objects.filter(pk=gender_id).delete() # DELETE FROME genders WHERE gender_id = gender_id
    messages.error(request, 'Gender succesfully deleted.')

    return redirect('/genders')


   # USERS 
    # INDEX USER
def index_user(request):
    users = User.objects.select_related('gender') # SELECT * FROM users LEFT JOIN genders ON users.gender_id = genders.gender_id

    context =  {
        'users': users, 
    }

    return render(request, 'user/index.html', context)

# CREATE USER

def create_user(request):
    genders = Gender.objects.all() # Select * FROM genders

    context = {
        'genders': genders
    }

    return render(request, 'user/create.html', context)


def store_user(request):
    firstName = request.POST.get('first_name')
    middleName =  request.POST.get('middle_name')
    lastName =  request.POST.get('last_name')
    age = request.POST.get('age')
    birtDate = request.POST.get('birth_date')
    genderId = request.POST.get('gender_id')
    usermame = request.POST.get('username')
    password = request.POST.get('password')
    confirmPassword = request.POST.get('confirm_password')
    encryptedPassword = make_password(password)

    if password == confirmPassword:
        User.objects.create(first_name=firstName, middle_name=middleName, last_name=lastName, age=age, birth_date=birtDate, 
        gender_id=genderId, username=usermame, password=encryptedPassword)

        messages.success(request, 'User successfully saved.')

        return redirect('/users')
    else:
        messages.error(request, 'Password do not match.')
        return redirect('/user/create')
    
    
    # VIEW USER

def show_user(request, user_id):
    user = User.objects.get(pk=user_id) # SELECT * FROM users WHERE  user_id = user_id

    context = {
        'user': user, 
    }

    return render(request, 'user/show.html', context)

    # EDIT USER

def edit_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    context = {
        'user': user,
    }

    return render(request, 'user/edit.html', context)

def update_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        birth_date_str = request.POST.get('birth_date')
        gender_name = request.POST.get('gender')

        # Convert the birth_date to the correct format
        try:
            birth_date = datetime.strptime(birth_date_str, '%B %d, %Y').strftime('%Y-%m-%d')
        except ValueError:
            messages.error(request, 'Invalid date format. Please use "Month day, Year" format.')
            return redirect(f'/user/edit/{user_id}')

        try:
            gender = Gender.objects.get(gender=gender_name)
        except Gender.DoesNotExist:
            messages.error(request, 'Invalid gender provided.')
            return redirect(f'/user/edit/{user_id}')

        # Update user fields
        user.username = username
        user.first_name = first_name
        user.middle_name = middle_name
        user.last_name = last_name
        user.age = age
        user.birth_date = birth_date
        user.gender = gender

        user.save()

        messages.success(request, 'User successfully updated.')
        return redirect('/users')
    else:
        messages.error(request, 'Invalid request method.')
        return redirect(f'/user/edit/{user_id}')
    
# DELETE USERS
    
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    context = {
        'user': user, 
    }

    return render(request, 'user/delete.html', context)

def destroy_user(request, user_id):
    User.objects.filter(pk=user_id).delete() # DELETE FROME genders WHERE gender_id = gender_id
    messages.error(request, 'User succesfully deleted.')

    return redirect('/users')