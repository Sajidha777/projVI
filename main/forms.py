from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from .models import ProductReview,UserAddressBook

class SignupForm(UserCreationForm):
    
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        #django by default only asks for username,pass and email in UserCreationForm
        fields =  UserCreationForm.Meta.fields + ('email','first_name','last_name','phone_no',)



#Review add form
class ReviewAdd(forms.ModelForm):
	class Meta:
		model=ProductReview
		fields=('review_text','review_rating')

# AddressBook Add Form
class AddressBookForm(forms.ModelForm):
	class Meta:
		model=UserAddressBook
		fields=('pincode','address','mobile','status')


# ProfileEdit
class ProfileForm(UserChangeForm):
	class Meta:
		model=CustomUser
		fields=('first_name','last_name','email','username')
