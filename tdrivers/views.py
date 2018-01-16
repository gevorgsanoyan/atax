from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import tDriver
from .forms import driverForm

# Create your views here.
@login_required
def driversList(request):
    page = request.GET.get('page', 1)
    drivers = tDriver.objects.all()
    paginator = Paginator(drivers, 10)

    try:
        drivers = paginator.page(page)
    except PageNotAnInteger:
        drivers = paginator.page(1)
    except EmptyPage:
        drivers = paginator.page(paginator.num_pages)

    return render(request, 'tdrivers/driversList.html', {'drivers':drivers})

@login_required
def driverInput(request):
    if request.method == "POST":
        form = driverForm(request.POST)
        if form.is_valid():
            s = form.save(commit=False)
            s.iUser = request.user
            s.save()
            return redirect('driverslist')
        else:
            return render(request, 'errorpage.html', {'errT': "Error saving driver"})
    else:
        s = driverForm()
        return render(request, 'tdrivers/driversInput.html', {'driverForm': s})

@login_required
def driverEdit(request, driverId):
    driver = tDriver.objects.get(id=driverId)
    form = driverForm(request.POST or None, instance=driver)
    if form.is_valid():
        driver = form.save(commit=False)
        driver.iUser = request.user
        driver.save()
        return redirect('driverslist')
    #else:
    #    return render(request, 'errorpage.html', {'errT': "Error updateing driver"})

    return render(request, 'tdrivers/driversInput.html', {'driverForm': form})