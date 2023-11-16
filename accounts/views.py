from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm


# Create your views here.
def pre_index(request):
    return render(request, 'pre_index.html')


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('accounts:pre_index')
    else:
        form = CustomUserCreationForm()
    context ={
        'form': form,
    }
    return render(request, 'accounts_form.html', context)