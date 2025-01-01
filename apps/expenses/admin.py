from django.contrib import admin
from apps.expenses.models import Expense, Category


# Register your models here.
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("amount", "description", "owner", "date")
    search_fields = ("amount", "description", "date")
    list_per_page = 2


admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Category)
