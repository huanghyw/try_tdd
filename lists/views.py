from django.shortcuts import render, redirect
from django.http import HttpResponse

from lists.models import Item


def home_page(request):
    if 'POST' == request.method:
        new_item_text = request.POST.get('item_text', '')
        Item.objects.create(text=new_item_text)
        return redirect('/')

    return render(request, 'home.html', {'items': Item.objects.all()})
