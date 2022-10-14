from django.contrib import admin
from .models import Stock, UserProfile, Transaction, History, BoughtStockTrack
# Register your models here.

admin.site.register(Stock)
admin.site.register(UserProfile)
admin.site.register(Transaction)
admin.site.register(History)
admin.site.register(BoughtStockTrack)