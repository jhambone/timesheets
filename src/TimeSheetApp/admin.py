from django.contrib import admin
from .models import TimeSheetMain, TimeSheetLine, TimeSheetLineCell, Employee, Department, LaborType
# Register your models here.


admin.site.register([TimeSheetMain, TimeSheetLine, TimeSheetLineCell, Employee, Department, LaborType])
