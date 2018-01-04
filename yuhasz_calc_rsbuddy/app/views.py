"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from app.calc_module import *
from app.combinations_module import *

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def home(request):
    """Renders the home page."""
    global_last_update_time = retrieve_db_update_time()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
            'last_update': global_last_update_time,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def raw_materials(request):
    """Renders the calculation page."""
    table_name = ['Logs to Longbow (u)', 'Logs to Shortbow(u)', 'Ores to Bars: No Blast Furnace', 'Ores to Bars: Blast Furnace', 'Logs to Crossbow Stock', 'Grimy to Clean Herbs']
    deploy = deploy_all()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/raw_materials.html',
        {
            'title':'Raw Material To Product',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'table_name': table_name,
            'deploy': deploy,
        }
    )

def by_combination(request):
    """Renders the combination items page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/by_combination.html',
        {
            'title':'Combination Materials',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )

def herblore_combo(request):
    """Renders the combination items page."""
    assert isinstance(request, HttpRequest)
    deploy_herblore = deploy_herbs()
    return render(
        request,
        'app/combinations_secondary/herblore.html',
        {
            'title':'Herblore',
            'message':'Your application description page.',
            'year':datetime.now().year,
            'deploy_herbs': deploy_herblore,
        }
    )

@login_required
def update_me(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    qr = display_entire_db()
    new_db = new_database()
    return render(
        request,
        'app/update_me.html',
        {
            'title':'Updated Database',
            'message':'Your application description page.',
            'year':datetime.now().year,
            #'new_db': new_db,
            'qr': qr,
        }
    )