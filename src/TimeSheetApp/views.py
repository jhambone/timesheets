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
          # Query for Timesheet Lines
          ts_lines = TimeSheetLine.objects.filter(timeSheet_code=records)
          # Query for Timesheet Line Cells
          ts_cells = [] # Initalize empty list
          for line in ts_lines:
            timesheet_cell = TimeSheetLineCell.objects.filter(timeSheet_line_code=line)
            for c in timesheet_cell:
                ts_cells.append(c)


          class TS_wrangler_line:
              def __init__(self, line):
                  self.timeSheet_line_code = line.timeSheet_line_code
                  self.taskOrder_number = line.taskOrder_number
                  self.cells = [] # To be initalized manually


          class TS_wrangler:
              def __init__(self, header, lines, cells):
                  self.employee     = header.user
                  self.employee_id  = header.employee_id 
                  self.start_dt     = header.startDate
                  self.end_dt       = header.endDate
                  self.signedBy     = header.signedBy
                  self.approvedBy   = header.approvedBy
                  self.status       = header.status
                  # Sort timesheet lines 1-N. Ignore Lambda syntax. Ask me later
                  sorted_lines = sorted(lines, key=lambda x: x.timeSheet_line_code)
                  # Create Empty List to Hold Line Cells
                  self.lines = []
                  for sline in sorted_lines:
                      res = TS_wrangler_line(sline)
                      # Filter to only cells on current line
                      filtered_cells = filter(lambda x: x.timeSheet_line_code == sline, cells)
                      #print filtered_cells,
                      # Sort filtered cells
                      sorted_cells = sorted(filtered_cells, key=lambda x: x.date)
                      #print sorted_cells,
                      res.cells = sorted_cells
                      self.lines.append(res)
                  
          final_result = TS_wrangler(records, ts_lines, ts_cells)


          # final_result contains all of the timesheet information. Return this to the HTML
          print '\n'
          print 'Username    :\t' + str(final_result.employee)
          print 'Employee ID :\t' + str(final_result.employee_id)
          print 'Date Range  :\t' + str(final_result.start_dt) + ' to ' + str(final_result.end_dt)
          for fline in final_result.lines:
              print '\t Line Code: ' + str(fline.timeSheet_line_code) +'\t Task Order ' + str(fline.taskOrder_number)
              print '\t\t Date \t\t Pay Type \t Hours'
              for fcell in fline.cells:
                  print '\t\t ' + str(fcell.date) + ' \t ' + str(fcell.payType) + ' \t\t ' + str(fcell.hours) 
          print '\n'

          


          return render_to_response('ts.html', {'records': records,
                                                  'empID': empID,
                                                  'rangeofdates': rangeofdates,
                                                  'timesheet_line': ts_lines,
                                                  'timesheet_cell': ts_cells,
                                                  }, context_instance=RequestContext(request))
       else:
          raise Http404("404 - Not Active User")

