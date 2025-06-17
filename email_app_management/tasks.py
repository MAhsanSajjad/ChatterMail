# import logging
# import calendar
# from django.utils.timezone import now, localtime
# from celery import shared_task
# from django.utils import timezone
# from datetime import timedelta
# from employee_management_app.models import *
# from rest_framework.authtoken.models import Token
# from Attendance_app.models import *
# from payroll_app.models import *
# from decimal import Decimal
# from datetime import date



# logger = logging.getLogger(__name__)
# @shared_task
# def handle_end_of_office_time():
#     current_time = timezone.now()

#     # Fetch office timings
#     office_time = OfficeTime.objects.first()
#     if not office_time:
#         logger.error("No office time found in OfficeTime model.")
#         return "No office time found"

#     # Calculate office end time
#     office_end_time = timezone.make_aware(timezone.datetime.combine(current_time.date(), office_time.end_time))

#     # Process employees
#     employees = Employee.objects.all()

#     for employee in employees:
#         # Get attendance for the day where checkout has not occurred
#         attendance = EmployeeAttendance.objects.filter(
#             employee=employee,
#             check_out_at__isnull=True,
#             check_in_at__date=current_time.date()
#         ).last()

#         # Mark absent only after the office end time
#         if current_time >= office_end_time:
#             if not attendance:
#                 # Check if employee is on leave
#                 is_on_leave = EmployeeAttendance.objects.filter(
#                     employee=employee,
#                     leave_date=current_time.date(),
#                     attendance_status='leave'
#                 ).exists()

#                 if not is_on_leave:
#                     # Mark as absent if no check-in and not on leave
#                     EmployeeAttendance.objects.create(
#                         employee=employee,
#                         attendance_status='A',
#                         check_in_at=None,
#                         check_out_at=None,
#                         description="Employee did not log in by the end of the office day."
#                     )
#                     logger.info(f"Marked employee {employee.user.username} as Absent.")

#             # Process check-out for employees who logged in
#             elif employee.employee_type == "onsite":
#                 if attendance.over_time:
#                     overtime_end_time = office_end_time + timedelta(hours=1)
#                     if current_time >= overtime_end_time:
#                         _logout_employee(employee, attendance, enforced_logout_time=overtime_end_time)
#                 else:
#                     _logout_employee(employee, attendance, enforced_logout_time=office_end_time)

#             # Process remote employees or others
#             else:
#                 check_in_time = attendance.check_in_at
#                 if not check_in_time:
#                     logger.error(f"Check-in time missing for employee {employee.user.username}.")
#                     continue

#                 logout_time = check_in_time + timedelta(hours=9)
#                 if attendance.over_time:
#                     logout_time += timedelta(hours=1)

#                 if current_time >= logout_time:
#                     _logout_employee(employee, attendance, enforced_logout_time=logout_time)

#     return "Office attendance processing complete."


# def _logout_employee(employee, attendance, enforced_logout_time=None):
#     """
#     Helper function to handle employee logout and enforce specific check-out times.
#     """
#     if enforced_logout_time:
#         attendance.check_out_at = enforced_logout_time  # Enforce exact logout time
#     else:
#         attendance.set_check_out()  # Default to current time

#     attendance.save()
#     logger.info(f"Check-out time for {employee.user.username}: {attendance.check_out_at}")

#     # Delete the employee's token
#     token = Token.objects.filter(user=employee.user).first()
#     if token:
#         token.delete()
#         logger.info(f"Token deleted for {employee.user.username}.")
        


# @shared_task
# def calculate_monthly_salary(force_run=False, sync_mode=False):
#     try:
#         today = now().date()
#         _, last_day = calendar.monthrange(today.year, today.month)

#         employees = Employee.objects.all()
#         period_start = today.replace(day=1)
#         first_day_of_current_month = today.replace(day=1)
#         last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)

#         holidays = Holiday.objects.filter(date__month=today.month, date__year=today.year).values_list('date', flat=True)

#         for employee in employees:
#             # Total salary components
#             total_salary = (
#                 employee.basic_salary +
#                 employee.food_allowance +
#                 employee.house_allowance +
#                 employee.transport_allowance
#             )

#             working_days = 26 - len(holidays)
#             total_working_minutes = working_days * 9 * 60
#             salary_per_minute = total_salary / total_working_minutes

#             # Attendance
#             attendances = EmployeeAttendance.objects.filter(
#                 employee=employee,
#                 check_in_at__month=today.month,
#                 check_in_at__year=today.year,
#                 check_out_at__isnull=False
#             )

#             total_worked_minutes = 0
#             holiday_bonus_minutes = 0

#             for attendance in attendances:
#                 check_in = localtime(attendance.check_in_at)
#                 check_out = localtime(attendance.check_out_at)
#                 worked_minutes = (check_out - check_in).total_seconds() / 60
#                 total_worked_minutes += worked_minutes

#                 if attendance.check_in_at.date() in holidays:
#                     holiday_bonus_minutes += worked_minutes

#             # Regular and holiday bonus salaries
#             regular_salary = salary_per_minute * total_worked_minutes
#             holiday_bonus = (salary_per_minute * 1.5) * holiday_bonus_minutes
#             calculated_salary = regular_salary + holiday_bonus

#             # Leave deductions
#             medical_leaves = EmployeeAttendance.objects.filter(
#                 employee=employee,
#                 leave_type='medical_leave',
#                 check_in_at__month=today.month,
#                 check_in_at__year=today.year,
#                 leave_status='accepted'
#             ).count()

#             casual_leaves = EmployeeAttendance.objects.filter(
#                 employee=employee,
#                 leave_type='casual_leave',
#                 check_in_at__month=today.month,
#                 check_in_at__year=today.year,
#                 leave_status='accepted'
#             ).count()

#             total_leaves = medical_leaves + casual_leaves
#             allowed_leaves = 3
#             extra_leaves = max(0, total_leaves - allowed_leaves)

#             # Deduction for extra leaves
#             deduction_per_leave = (total_salary / working_days)
#             leave_deduction = extra_leaves * deduction_per_leave

#             # Final salary calculation with leave deductions
#             final_salary = calculated_salary - leave_deduction
#             deducted_salary = total_salary - final_salary

#             # Save or update salary record
#             salary_obj = Salary.objects.filter(
#                 employee=employee,
#                 period_start__month=today.month,
#                 period_start__year=today.year,
#             ).first()

#             if not salary_obj:
#                 salary_obj = Salary.objects.create(
#                     employee=employee,
#                     period_start=period_start,
#                     period_end=last_day_of_previous_month,
#                     pay_type='Fix',
#                     salary=Decimal(str(final_salary)),
#                     deducted_salary=Decimal(str(deducted_salary)),
#                     salary_status='pending',
#                 )
#             else:
#                 salary_obj.salary = Decimal(str(final_salary))
#                 salary_obj.deducted_salary = Decimal(str(deducted_salary))
#                 salary_obj.save()

#     except Exception as e:
#         if sync_mode:
#             return {"error": str(e)}
#         print(f"Error during salary calculation: {e}")
#         return str(e)
