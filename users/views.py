from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm,ProfileUpdateForm, passwordForm

@login_required(login_url='/login')
def add_profile_info(request):
    if request.method == 'POST':
        uform = UserUpdateForm(request.POST, instance=request.user)
        pform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, "Your profile hase been updated")
            return redirect('/add-info')
    else:
        uform = UserUpdateForm(instance=request.user)
        pform = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'form':uform,
        'form1':pform
    }
    return render(request, 'users/prof.html',context)

@login_required(login_url= '/login')
def change_password(request):
    if request.method == 'POST':
        form = passwordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Password Changed You can now log in')
            return redirect('/')
        else:
            messages.error(request, f'You have entered incorect information please try agin carefully')
    else:
        form = passwordForm(request.user)
    context = {
        'form':form
    }
    return render(request, 'users/pwd_change.html', context)


def terms_and_privacy(request):
    return render(request, 'users/privacy_terms.html', {})

def team(request):
    return render(request, 'users/team.html',{})


