
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.
class Stock(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=31)
    price = models.DecimalField( decimal_places=2, max_digits=8)
    website = models.URLField()
    sector = models.CharField(max_length=100)
    industry = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    logo_url = models.URLField()
    updated = models.DateTimeField()
    users = models.ManyToManyField(User,related_name='bought_stocks')

    def __str__(self):
        return f'{self.symbol} -> {self.updated.ctime()}'
    class Meta:
        ordering = ['-updated']

class BoughtStockTrack(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='bought_stock_tracks')
    symbol = models.CharField(max_length=31)
    shares = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} -> {self.symbol} -> {self.shares}'

class Transaction(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='transactions')
    stock_name = models.CharField(max_length=100)
    stock_symbol = models.CharField(max_length=31)
    stock_price = models.DecimalField(decimal_places=2, max_digits=10)
    shares = models.PositiveIntegerField()
    is_sell = models.BooleanField(default=False)
    total = models.DecimalField(decimal_places=2,max_digits=10)
    updated = models.DateTimeField()
    
    def __str__(self):
        return f'{self.user.username} -> {self.stock_symbol} -> {self.updated.ctime()}'

    class Meta:
        ordering = ['-updated']

class History(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name='historys')
    stock_name = models.CharField(max_length=100)
    stock_symbol = models.CharField(max_length=31)
    stock_price = models.DecimalField(decimal_places=2, max_digits=10)
    shares = models.PositiveIntegerField()
    is_sell = models.BooleanField(default=False)
    time = models.DateTimeField()

    class Meta:
        ordering = ['-time']

    def __str__(self):
        return f'{self.user.username} -> {self.shares}'

class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    account_size = models.DecimalField(decimal_places=2, max_digits=10)
    account_balance = models.DecimalField(decimal_places=2, max_digits=10)
    def __str__(self):
        return f'{self.user.username} -> ${self.account_balance}'