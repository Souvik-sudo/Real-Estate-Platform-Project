from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Property, ContactForm, CustomUser

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ['owner', 'created_at', 'updated_at']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }

class ContactFormForm(forms.ModelForm):
    class Meta:
        model = ContactForm
        fields = ['name', 'email', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('email', 'phone_number')
        widgets = {
            'phone_number': forms.TextInput(attrs={'type': 'tel'}),
        }


class PropertyFilterForm(forms.Form):
    location = forms.CharField(required=False, label='Location')
    min_price = forms.DecimalField(required=False, min_value=0, decimal_places=2, label='Min Price')
    max_price = forms.DecimalField(required=False, min_value=0, decimal_places=2, label='Max Price')
    state = forms.CharField(required=False, label='State')


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)