from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        #django by default only asks for username,pass and email in UserCreationForm
        fields =  UserCreationForm.Meta.fields + ('email','first_name','last_name','phone_no',)