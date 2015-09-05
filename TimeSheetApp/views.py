from django.shortcuts import RequestContext, render_to_response
from TimeSheetApp.models import TimeSheetMain
from TimeSheetApp.models import TimeSheetLine
from TimeSheetApp.models import TimeSheetLineCell
from TimeSheetApp.models import Employee


# Create your views here.
from django.http import Http404


from datetime import timedelta, date
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def time_page(request, result_name):
       records = TimeSheetMain.objects.get(timeSheet_code=result_name)
       empID = Employee.objects.get()

    #Timesheet Date Range filler
       start = records.startDate
       end = records.endDate
       start_Date_as_date = date(int(start.strftime("%Y")), int(start.strftime("%m")), int(start.strftime("%d")))
       end_Date_as_date = date(int(end.strftime("%Y")), int(end.strftime("%m")), int(end.strftime("%d")))
       rangeofdates = daterange(start_Date_as_date, end_Date_as_date)


       req_user = request.user
       recordsUser = records.user

       if req_user == recordsUser:
          timesheet_line = TimeSheetLine.objects.all()
          timesheet_cell = TimeSheetLineCell.objects.all()

          return render_to_response('ts.html', {'records': records,
                                                  'empID': empID,
                                                  'rangeofdates': rangeofdates,
                                                  'timesheet_line': timesheet_line,
                                                  'timesheet_cell': timesheet_cell,
                                                  }, context_instance=RequestContext(request))
       else:
          raise Http404("404 - Not Active User")

