from django.shortcuts import render

# Create your views here.

def textinput(request):
    """
    View function for the text input page of the site.
    """
    return render(
        request,
        'textinput.html',
        context={},
    )

def featureoutput(request):
    """
    View function for the feature output page of the site.
    """
    return render(
        request,
        'featureoutput.html',
        context={},
    )

from .models import User

def account(request):
    """
    View function for user accounts.
    """
    username = User._meta.get_field('username')
    return render(
        request,
        "account.html",
        context={'username':username}
    )