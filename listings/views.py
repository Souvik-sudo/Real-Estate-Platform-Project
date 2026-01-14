from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Property, ContactForm
from .forms import PropertyForm, ContactFormForm, CustomUserCreationForm

def property_list(request):
    properties = Property.objects.all()
    return render(request, 'listings/property_list.html', {'properties': properties})

# def property_detail(request, pk):
#     property = get_object_or_404(Property, pk=pk)
#     if request.method == 'POST':
#         form = ContactFormForm(request.POST)
#         if form.is_valid():
#             contact_form = form.save(commit=False)
#             contact_form.property = property
#             contact_form.save()
#             return redirect('property_detail', pk=pk)
#     else:
#         form = ContactFormForm()
#     return render(request, 'listings/property_detail.html', {'property': property, 'form': form})


from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from .models import Property
from .forms import ContactFormForm

def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = ContactFormForm(request.POST)
        if form.is_valid():
            contact_form = form.save(commit=False)
            contact_form.property = property
            contact_form.save()
            
            # Construct the email message
            full_message = f"Message regarding {property.title} from {form.cleaned_data['name']} ({form.cleaned_data['email']}):\n\n{form.cleaned_data['message']}"
            
            # Send email to the property owner
            send_mail(
             subject=f"Inquiry about {property.title}",
             message=full_message,
             from_email=settings.DEFAULT_FROM_EMAIL,
             recipient_list=[property.owner.email],
             fail_silently=False,
)
            return redirect('property_detail', pk=pk)
    else:
        form = ContactFormForm()
    return render(request, 'listings/property_detail.html', {'property': property, 'form': form})


@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            return redirect('property_detail', pk=property.pk)
    else:
        form = PropertyForm()
    return render(request, 'listings/property_form.html', {'form': form})

def search_properties(request):
    query = request.GET.get('q')
    properties = Property.objects.filter(title__icontains=query) if query else Property.objects.all()
    return render(request, 'listings/property_list.html', {'properties': properties})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Send email
        send_mail(
            f'New contact from {name}',
            message,
            email,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )
        
        return render(request, 'listings/contact_success.html')
    return render(request, 'listings/contact.html')

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

@login_required
def profile_view(request):
    return render(request, 'listings/property_list.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PropertyForm
from .models import Property, Image

@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property = form.save(commit=False)
            property.owner = request.user
            property.save()
            
            # Handle multiple image uploads
            if 'images' in request.FILES:
                images = request.FILES.getlist('images')
                for image in images:
                    Image.objects.create(property=property, image=image)
            
            return redirect('property_detail', pk=property.pk)
    else:
        form = PropertyForm()
    
    return render(request, 'listings/property_form.html', {'form': form})




from django.shortcuts import render
from .models import Property
from .forms import PropertyFilterForm

def property_list(request):
    properties = Property.objects.all()
    form = PropertyFilterForm(request.GET or None)

    if form.is_valid():
        query = request.GET.get('q')
        location = form.cleaned_data.get('location')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        state = form.cleaned_data.get('state')
        bhk = request.GET.get('bhk')
        
        if query:
            properties = properties.filter(title__icontains=query)

        if location:
            properties = properties.filter(city__icontains=location) | properties.filter(address__icontains=location)
        if min_price:
            properties = properties.filter(price__gte=min_price)
        if max_price:
            properties = properties.filter(price__lte=max_price)
        if state:
            properties = properties.filter(state__icontains=state)
        if bhk:
            properties = properties.filter(bedrooms=bhk)

    return render(request, 'listings/property_list.html', {'properties': properties, 'form': form})

