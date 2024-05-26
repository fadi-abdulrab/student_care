from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.



admin.site.register(AdminHOD)
admin.site.register(Staffs)
admin.site.register(Courses)
admin.site.register(Subjects)
admin.site.register(Students)
# admin.site.register(Attendance)
admin.site.register(My_Attendance)
admin.site.register(FeedBackStudent_chat)
admin.site.register(FeedBackStaffs_chat)

#
# admin.site.register(AttendanceReport)
# admin.site.register(LeaveReportStudent)
# admin.site.register(LeaveReportStaff)
# admin.site.register(FeedBackStudent)
# admin.site.register(FeedBackStaffs)
# admin.site.register(NotificationStudent)
# admin.site.register(NotificationStaffs)
