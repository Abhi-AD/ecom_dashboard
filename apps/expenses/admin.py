from django.contrib import admin
from apps.expenses.models import Expense, Category

# Register your models here.
admin.site.register(Expense)
admin.site.register(Category)
