from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import yfinance as yf
from django.db import transaction
from .models import Stock, Transaction, UserProfile, History, BoughtStockTrack
from django.contrib.auth.models import User
import datetime
import requests
from django.utils import timezone
# Create your views here.


@login_required(redirect_field_name="next", login_url="accounts:login")
def portfolio(request):
    user = request.user
    user = User.objects.get(username=user.username)
    transactions = user.transactions.all()
    return render(request, 'dashboard/dashboard.html', context={
        'total': user.userprofile.account_size,
        'balance': user.userprofile.account_balance,
        'transactions':transactions
    })

@transaction.atomic
@login_required(redirect_field_name="next", login_url="accounts:login")
def buy(request):
    if request.method == 'POST':
        symbol = request.POST['symbol']
        shares = request.POST['shares']
        if len(symbol) > 0:
            symbol = symbol.strip().upper()
            try:
                test_it = requests.get(
                    'https://finance.cs50.net/static/favicon.ico', timeout=5.000)
            except:
                messages.error(request, 'No internet connection')
                return render(request, 'dashboard/buy.html')

            user = User.objects.get(username=request.user.username)
            try:
                a_stock = yf.Ticker(symbol)
                stock_info = a_stock.info
                # update this
                stocks = Stock.objects.filter(symbol=symbol)
                # if the stock model exists, we update the price to the currentPrice
                if stocks.exists():
                    stocks[0].price = stock_info['currentPrice']
                    # update this
                    stocks[0].updated = datetime.datetime.now()
                    stocks[0].save();
                    stock = stocks[0]
                    user.bought_stocks.add(stock)
                else:
                    stock = Stock()
                    stock.name = stock_info['shortName']
                    stock.symbol = stock_info['symbol']
                    stock.price = stock_info['currentPrice']
                    stock.website = stock_info['website']
                    stock.sector = stock_info['sector']
                    stock.industry = stock_info['industry']
                    stock.country = stock_info['country']
                    stock.logo_url = stock_info['logo_url']
                    stock.updated = datetime.datetime.now()
                    stock.save();
                    stock.users.add(user)
                total= stock.price * int(shares)
                user_transactions = user.transactions.all()
                one_transaction = [x for x in user_transactions if not x.is_sell and x.stock_symbol == stock.symbol]

                # store history
                history = History(user=user, stock_name=stock.name, stock_symbol=stock.symbol,
                                    stock_price=stock.price,shares=shares, time=datetime.datetime.now())

                # check if a transaction with the same name and type exists
                if len(one_transaction) == 1:                                 # get list of user bought stocks
                    bought_stocks_track = user.bought_stock_tracks.all()
                    if len(bought_stocks_track) >= 1:
                        stock_track = [x for x in bought_stocks_track if x.symbol == stock.symbol][0]
                    one = one_transaction[0]
                    one.updated = datetime.datetime.now()
                    one.shares += int(shares)
                    one.total += total
                    stock_track.shares += int(shares)
                else:
                    one = Transaction(user=user, stock_name=stock.name, stock_symbol=stock.symbol,
                                    stock_price=stock.price, total=total, shares=shares, updated=datetime.datetime.now())
                    stock_track = BoughtStockTrack(user=user,symbol=stock.symbol,shares=shares)
                balance = user.userprofile.account_balance
                if balance < total:
                    messages.error(request,f'Insufficient Cash, you only have ${balance}')
                    return redirect('dashboard:buy')
                balance = balance - int(total)
                userprofile = UserProfile.objects.get(user=user)
                userprofile.account_balance = balance
                # save to db
                stock_track.save();
                userprofile.save();
                one.save();   
                history.save();
                transactions = user.transactions.all()    
                messages.success(request,f'Your Purchase of {one.stock_symbol} was successful')     
                return render(request, 'dashboard/dashboard.html', context={
                    'transactions': transactions,
                    'total':user.userprofile.account_size,
                    'balance':balance
                })
            except:
                messages.error(request,'Invalid inputs')
                redirect('dashboard:buy')
        else:
            messages.error(request, 'Symbol cannot be empty')
    return render(request, 'dashboard/buy.html')


@login_required(redirect_field_name="next", login_url="accounts:login")
def sell(request):
    name = request.user.username
    user = User.objects.get(username=name)
    if request.method == 'POST':
        symbol = request.POST['symbol']
        shares = request.POST['shares']
        if len(symbol) > 0:
            symbol = symbol.strip().upper()
            try:
                test_it = requests.get(
                    'https://finance.cs50.net/static/favicon.ico', timeout=5.000)
            except:
                messages.error(request, 'No internet connection')
                return redirect('dashboard:sell')
            bought_stocks = user.bought_stocks.all()
            sell_stock = [x for x in bought_stocks if x.symbol == symbol]
            if len(sell_stock) < 1 :
                messages.error(request,f"you don't have {symbol}")
                return redirect('dashboard:sell')
            stock = sell_stock[0]
            try:
                a_stock = yf.Ticker(stock.symbol)
                stock_info = a_stock.info
                stock.price = stock_info['currentPrice']
                updated = datetime.datetime.now()
                stock.updated = updated
                stock.save();
                # get the stock tracker list
                bought_stocks_track = user.bought_stock_tracks.all()
                stock_track = [x for x in bought_stocks_track if x.symbol == stock.symbol][0]
                shares = int(shares)
                if stock_track.shares >= shares:
                    total = int(stock.price * shares)
                    # instantiate a transaction and history
                    history = History(user=user, stock_name=stock.name, stock_symbol=stock.symbol,
                                    stock_price=stock.price,shares=shares, time=updated, is_sell=True)

                    # check if a transaction with the same name and type(as in buy/sell ) exists
                    user_transactions = user.transactions.all()
                    one_transaction = [x for x in user_transactions if x.is_sell and x.stock_symbol == stock.symbol]
                    if len(one_transaction) == 1:
                        one = one_transaction[0]
                        one.updated = updated
                        one.shares += shares
                        one.total += total
                    else:
                        one = Transaction(user=user, stock_name=stock.name, stock_symbol=stock.symbol,
                                        stock_price=stock.price, total=total, shares=shares, updated=updated, is_sell=True)
                    stock_track.shares -= shares
                    balance = user.userprofile.account_balance
                    balance += total
                    user.userprofile.account_balance = balance
                    # save
                    stock_track.save();
                    user.userprofile.save();
                    one.save();
                    history.save();
                    transactions = user.transactions.all()  
                    messages.success(request,f'Sale of {stock.symbol} was successful !!') 
                    return render(request, 'dashboard/dashboard.html', context={
                    'transactions': transactions,
                    'total':user.userprofile.account_size,
                    'balance':balance
                    })
                else:
                    messages.error(request,f'{shares} >  amount of {stock.symbol} You have Ole')
                    return redirect('dashboard:sell')
            except:
                bought_stocks = user.bought_stock_tracks.all()
                bought_stocks = [x for x in bought_stocks if not x.shares == 0]
                messages.error(request,'Invalid Inputs')
                return render(request, 'dashboard/sell.html',context={
                    'stocks':bought_stocks,
                })
    else:
        bought_stocks = user.bought_stock_tracks.all()
        bought_stocks = [x for x in bought_stocks if not x.shares == 0]
        return render(request, 'dashboard/sell.html',context={
            'stocks':bought_stocks,
        })


@login_required(redirect_field_name="next", login_url="accounts:login")
def history(request):
    user = request.user
    user = User.objects.get(username=user.username)
    transactions = user.historys.all()
    num = len(transactions)
    if request.method == "POST":
        choice = request.POST['choice']
        if choice == 'yes':
            user.historys.all().delete()
            transactions = user.historys.all()
            num = len(transactions)
    return render(request, 'dashboard/history.html', context={
        'transactions':transactions,
        'num':num
    })


@transaction.atomic
@login_required(redirect_field_name="next", login_url="accounts:login")
def quotes(request):
    if request.method == 'POST':
        symbol = request.POST['symbol']
        if len(symbol) > 0:
            symbol = symbol.strip().upper()
            try:
                test_it = requests.get(
                    'https://finance.cs50.net/static/favicon.ico', timeout=5.000)
            except:
                messages.error(request, 'No internet connection')
                return redirect('dashboard:quotes')
            try:
                a_stock = yf.Ticker(symbol)
                stock_info = a_stock.info
                stock = Stock.objects.filter(symbol=symbol)
                # if the stock model exists, we update the price to the currentPrice
                if stock.exists():
                    stock[0].price = stock_info['currentPrice']
                    stock[0].updated = datetime.datetime.now()
                    stock[0].save()
                    return render(request, 'dashboard/quote.html', context={
                        'stock': stock[0],
                        'stock_exists': Stock.objects.filter(symbol=symbol),
                    })
                else:
                    stock = Stock()
                    stock.name = stock_info['shortName']
                    stock.symbol = stock_info['symbol']
                    stock.price = stock_info['currentPrice']
                    stock.website = stock_info['website']
                    stock.sector = stock_info['sector']
                    stock.industry = stock_info['industry']
                    stock.country = stock_info['country']
                    stock.logo_url = stock_info['logo_url']
                    stock.updated = datetime.datetime.now()
                    name = request.user.username
                    user = User.objects.get(username=name)
                    stock.save();
                    stock.users.add(user)
                    return render(request, 'dashboard/quote.html', context={
                        'stock': stock,
                        'stock_exists': Stock.objects.filter(symbol=symbol),
                    })
            except:
                messages.error(request, f'The stock {symbol} doesnt exist')
                return redirect('dashboard:quotes')
        else:
            messages.error(request, 'Symbol cannot be empty')
    return render(request, 'dashboard/quote.html')


