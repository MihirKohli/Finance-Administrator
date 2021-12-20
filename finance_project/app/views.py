from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from .forms import *
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from yahoo_fin.stock_info import *
import time
import queue
from threading import Thread


def home(request):
    return render(request, 'app/home.html')


def loan(request):
    return render(request, 'app/loan.html')


def currency(request):
    return render(request, 'app/currency.html')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'app/dashboard.html')


@login_required(login_url='login')
def form(request):
    if request.method == "POST":
        model = formInput
        form = dashboardForm(request.POST)
        # form.save()
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()

        # return redirect('/dashboard/')
    else:
        form = dashboardForm()
    return render(request, 'app/form.html', {"form": form})


@login_required(login_url='login')
def deleteInput(request, pk):

    delete = formInput.objects.get(pk=pk)
    delete.delete()
    return redirect('table')


def resultsData(request):

    data = []
    forms = formInput.objects.filter(user=request.user)
    #forms = formInput.objects.all()

    for i in forms:
        data.append({i.Field: i.Amount})

    return JsonResponse(data, safe=False)


def stockPicker(request):
    stock_picker = tickers_nifty50()
    print(stock_picker)
    return render(request, 'app/stockpicker.html', {'stockpicker': stock_picker})


def stockTracker(request):
    stockpicker = request.GET.getlist('stockpicker')
    print(stockpicker)
    data = {}
    available_stocks = tickers_nifty50()
    for i in stockpicker:
        if i in available_stocks:
            pass
        else:
            return HttpResponse("Error")

    n_threads = len(stockpicker)
    thread_list = []
    que = queue.Queue()
    start = time.time()
    # for i in stockpicker:
    #     result = get_quote_table(i)
    #     data.update({i: result})
    for i in range(n_threads):
        thread = Thread(target=lambda q, arg1: q.put(
            {stockpicker[i]: get_quote_table(arg1)}), args=(que, stockpicker[i]))
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()

    while not que.empty():
        result = que.get()
        data.update(result)
    end = time.time()
    time_taken = end - start
    print(time_taken)

    print(data)
    return render(request, 'app/stocktracker.html', {'data': data})


def registerPage(request):

    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
        context = {'form': form}
        return render(request, 'app/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')

        return render(request, 'app/login.html', {})


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def table(request):
    forms = formInput.objects.filter(user=request.user)
    context = {'forms': forms}
    return render(request, 'app/table.html', context)
