from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from .models import *
from .forms import CarSellersForm



def seller(request):
    seller = CarSellersForm()
    if request.method == 'POST':
        seller = CarSellersForm(request.POST, request.FILES)
        if seller.is_valid():
            seller.save()
            return redirect('index')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        return render(request, 'car_seller.html', {'upload_form': seller})


def update_car(request, car_id):
    car_id = int(car_id)
    try:
        car = CarSeller.objects.get(id=car_id)
    except CarSeller.DoesNotExist:
        return redirect('index')
    car_form = CarSellersForm(request.POST or None, instance=car)
    if car_form.is_valid():
        car_form.save()
        return redirect('index')
    return render(request, 'car_seller.html', {'upload_form': car_form})


def delete_car(request, car_id):    
    car_id = int(car_id)
    try:
        book_sel = CarSeller.objects.get(id=car_id)
    except CarSeller.DoesNotExist:
        return redirect('index')
    book_sel.delete()
    return redirect('index')
