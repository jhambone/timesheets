from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Department(models.Model):
    dept_id = models.CharField(max_length=15, blank=False, unique=True)
    dept_name = models.CharField(max_length=100, blank=False, unique=False)

    def __unicode__(self):
        return "{0}".format(
                self.dept_name)

class LaborType(models.Model):
    labortype_id   = models.CharField(max_length=15, blank=False, unique=True)
    labortype_desc = models.CharField(max_length=100, blank=False, unique=False)

    def __unicode__(self):
        return "Labor Type: {0}".format(
                self.labortype_id)

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department)    # CharField(max_length=100)
    employeeID = models.CharField(max_length=100,
            validators=[RegexValidator('^[0-9]{6}',
            message="Employee ID must be 6 numeric digits")])
    laborType = models.ForeignKey(LaborType)  #CharField(max_length=30)

    def __unicode__(self):
        return "User: {0}".format(
            self.user)

class TimeSheetMain(models.Model):
    timeSheet_code = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)
    user = models.ForeignKey(User)
    employee_id = models.CharField(max_length=20)
    startDate = models.DateField()
    endDate = models.DateField()
    signedBy = models.CharField(max_length=20)
    approvedBy = models.CharField(max_length=20)
    status = models.CharField(max_length=10)

    def __unicode__(self):
        return "User: {0}, Date: {1}-{2}, Status: {3}".format(
            self.user, self.startDate, self.endDate, self.status)

class TimeSheetLine(models.Model):
    timeSheet_line_code = models.CharField(max_length=20)
    timeSheet_code = models.ForeignKey('TimeSheetMain')
    taskOrder_number = models.CharField(max_length=20)
    unit = models.CharField(max_length=20)

    def __unicode__(self):
        return "{0}, {1}, {2}".format(
            self.pk, self.timeSheet_line_code, self.taskOrder_number)


class TimeSheetLineCell(models.Model):
    timeSheet_line_cell_ID = models.IntegerField(max_length=20)
    timeSheet_line_code = models.ForeignKey('TimeSheetLine')
    payType = models.CharField(max_length=20)
    workComp_cd = models.DecimalField(max_digits=3, decimal_places=2)
    hours = models.DecimalField(max_digits=3, decimal_places=2)
    date = models.DateField()

    def __unicode__(self):
        return "{0}, timeSheet_line_code_ID: {1}, timeSheet_line_code: {2}".format(
            self.pk, self.timeSheet_line_cell_ID, self.timeSheet_line_code)




