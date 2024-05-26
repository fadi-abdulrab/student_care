import imp
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
import datetime # To Parse input DateTime into Python Date Time Object
from django.db.models import Sum
from django.db.models import Q
from .models import Courses_Fees, CustomUser, FeedBackStudent_chat, My_Attendance, Staffs, Courses, Student_Review, Subjects, Students, Attendance, AttendanceReport, LeaveReportStudent, FeedBackStudent, StudentResult
from .forms import Form_Courses_Fees
from django.views.decorators.csrf import csrf_exempt

# from .models import FeedBackStudent_chat
from django.shortcuts import HttpResponse


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'





def student_home(request):

    student_obj = Students.objects.get(admin=request.user.id)
    print(student_obj, student_obj.id, 'test22')
    total_attendance_to_sing = My_Attendance.objects.filter(student_id=student_obj.id)
    print('total_atendens is', total_attendance_to_sing.count())
    #attendance_present
    attendance_present =  My_Attendance.objects.filter(student_id=student_obj.id, status=1).count()
    total_attendance = AttendanceReport.objects.filter(student_id=student_obj).count()
    # attendance_present = AttendanceReport.objects.filter(student_id=student_obj, status=True).count()
    attendance_absent = My_Attendance.objects.filter(student_id=student_obj, status=0).count()

    course_obj = Courses.objects.get(id=student_obj.course_id.id)
    total_subjects = Subjects.objects.filter(course_id=course_obj)

    subject_name = Subjects.objects.filter(course_id=course_obj)
    subject_name_sin = []
    for get_subject_name in subject_name:
        subject_name_sin.append(get_subject_name.subject_name)


    get__cuorses = Subjects.objects.filter(staff_id=student_obj.id)
    Student_Review_sin = Student_Review.objects.filter(student_id=student_obj)

    attendance_present_To_each_subject =  My_Attendance.objects.filter(student_id=student_obj.id, status=1)
    print(' Att each', attendance_present_To_each_subject, 'my_test is here',Student_Review_sin,'courses', subject_name)

    all_att = []
    for each_studen in subject_name:
        attendance =  My_Attendance.objects.filter(subject_id=each_studen.id)&My_Attendance.objects.filter(status=1)
        if attendance.aggregate(Sum('status'))['status__sum'] == None:
            
            all_att.append(0)
        else:
            all_att.append(int(attendance.aggregate(Sum('status'))['status__sum']))

        print(all_att, total_subjects)


    data_absent = []
    # subject_data = Subjects.objects.filter(course_id=student_obj.course_id)
    # for subject in subject_data:
    #     attendance = My_Attendance.objects.filter(subject_id=subject.id)
    #     # attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True, student_id=student_obj.id).count()
    #     # attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=False, student_id=student_obj.id).count()
    #     subject_name.append(subject.subject_name)
    #     # data_present.append(attendance_present_count)
    #     # data_absent.append(attendance_absent_count)
    stars = zip(subject_name_sin, Student_Review_sin)
    r = Student_Review_sin
    context={
        "total_attendance": total_attendance_to_sing.count(),
        "attendance_present": attendance_present,
        "attendance_absent": attendance_absent,
        "total_subjects": total_subjects.count(),
        "subject_name": subject_name_sin,
        'stars':stars,
        'all_subject_attendance':all_att,
        "data_present": attendance_present,
        "data_absent": attendance_absent,
        'r':r,
        'course_obj':course_obj
    }

    print(total_subjects)

    return render(request, "student_template/student_home_template.html", context)











def student_show_more_student_detile(request):

    student_obj = Students.objects.get(admin=request.user.id)
    print(student_obj, student_obj.id, 'test22')
    total_attendance_to_sing = My_Attendance.objects.filter(student_id=student_obj.id)
    print('total_atendens is', total_attendance_to_sing.count())
    #attendance_present
    attendance_present =  My_Attendance.objects.filter(student_id=student_obj.id, status=1).count()
    total_attendance = AttendanceReport.objects.filter(student_id=student_obj).count()
    # attendance_present = AttendanceReport.objects.filter(student_id=student_obj, status=True).count()
    attendance_absent = My_Attendance.objects.filter(student_id=student_obj, status=0).count()

    course_obj = Courses.objects.get(id=student_obj.course_id.id)
    total_subjects = Subjects.objects.filter(course_id=course_obj)

    subject_name = Subjects.objects.filter(course_id=course_obj)
    subject_name_sin = []
    for get_subject_name in subject_name:
        subject_name_sin.append(get_subject_name.subject_name)


    get__cuorses = Subjects.objects.filter(staff_id=student_obj.id)
    Student_Review_sin = Student_Review.objects.filter(student_id=student_obj)

    attendance_present_To_each_subject =  My_Attendance.objects.filter(student_id=student_obj.id, status=1)
    print(' Att each', attendance_present_To_each_subject, 'my_test is here',Student_Review_sin,'courses', subject_name)

    all_att = []
    for each_studen in subject_name:
        attendance =  My_Attendance.objects.filter(subject_id=each_studen.id)&My_Attendance.objects.filter(status=1)
        if attendance.aggregate(Sum('status'))['status__sum'] == None:
            
            all_att.append(0)
        else:
            all_att.append(int(attendance.aggregate(Sum('status'))['status__sum']))

        print(all_att, total_subjects)

    at = []
    for single_subject in total_subjects:
        print('hi', single_subject)
        attendance_2 =  My_Attendance.objects.filter(subject_id=single_subject, student_id=student_obj)
        print(attendance_2)
        print(attendance_2.aggregate(Sum('status'))['status__sum'])
        at.append(attendance_2.aggregate(Sum('status'))['status__sum'])
        for k in attendance_2:
            print(k.status)


    data_absent = []
    # subject_data = Subjects.objects.filter(course_id=student_obj.course_id)
    # for subject in subject_data:
    #     attendance = My_Attendance.objects.filter(subject_id=subject.id)
    #     # attendance_present_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=True, student_id=student_obj.id).count()
    #     # attendance_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendance, status=False, student_id=student_obj.id).count()
    #     subject_name.append(subject.subject_name)
    #     # data_present.append(attendance_present_count)
    #     # data_absent.append(attendance_absent_count)
    stars = zip(subject_name_sin, Student_Review_sin)
    r = Student_Review_sin
    context={

        "total_attendance": total_attendance_to_sing.count(),
        "attendance_present": attendance_present,
        "attendance_absent": attendance_absent,
        "total_subjects": zip(total_subjects, at),
        "total_subject_num": total_subjects.count(),

        "subject_name": subject_name_sin,
        'stars':stars,
        'all_subject_attendance':all_att,
        "data_present": attendance_present,
        "data_absent": attendance_absent,
        'r':r,
        'course_obj':course_obj
    }

    print(at)

    return render(request, "student_template/student_show_more_student_detile.html", context)


















def student_view_attendance(request):
    student = Students.objects.get(admin=request.user.id) # Getting Logged in Student Data
    course = student.course_id # Getting Course Enrolled of LoggedIn Student
    # course = Courses.objects.get(id=student.course_id.id) # Getting Course Enrolled of LoggedIn Student
    subjects = Subjects.objects.filter(course_id=course) # Getting the Subjects of Course Enrolled
    context = {
        "subjects": subjects
    }
    return render(request, "student_template/student_view_attendance.html", context)


def student_view_attendance_post(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('student_view_attendance')
    else:
        # Getting all the Input Data
        subject_id = request.POST.get('subject')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Parsing the date data into Python object
        start_date_parse = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_parse = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        # Getting all the Subject Data based on Selected Subject
        subject_obj = Subjects.objects.get(id=subject_id)
        # Getting Logged In User Data
        user_obj = CustomUser.objects.get(id=request.user.id)
        # Getting Student Data Based on Logged in Data
        stud_obj = Students.objects.get(admin=user_obj)

        # Now Accessing Attendance Data based on the Range of Date Selected and Subject Selected
        attendance = Attendance.objects.filter(attendance_date__range=(start_date_parse, end_date_parse), subject_id=subject_obj)
        # Getting Attendance Report based on the attendance details obtained above
        attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance, student_id=stud_obj)

        # for attendance_report in attendance_reports:
        #     print("Date: "+ str(attendance_report.attendance_id.attendance_date), "Status: "+ str(attendance_report.status))

        # messages.success(request, "Attendacne View Success")

        context = {
            "subject_obj": subject_obj,
            "attendance_reports": attendance_reports
        }

        return render(request, 'student_template/student_attendance_data.html', context)
       


def student_feedback(request):
    student_obj = Students.objects.get(admin=request.user.id)
    feedback_data = FeedBackStudent.objects.filter(student_id=student_obj)
    context = {
        "feedback_data": feedback_data
    }
    return render(request, 'student_template/student_feedback.html', context)


def student_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('student_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        student_obj = Students.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStudent(student_id=student_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('student_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('student_feedback')


def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)

    context={
        "user": user,
        "student": student
    }
    return render(request, 'student_template/student_profile.html', context)


def student_profile_update(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('student_profile')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        address = request.POST.get('address')

        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            student = Students.objects.get(admin=customuser.id)
            student.address = address
            student.save()
            
            messages.success(request, "Profile Updated Successfully")
            return redirect('student_profile')
        except:
            messages.error(request, "Failed to Update Profile")
            return redirect('student_profile')


# def student_view_result(request):
#     student = Students.objects.get(admin=request.user.id)
#     student_result = StudentResult.objects.filter(student_id=student.id)
#     context = {
#         "student_result": student_result,
#     }
#     return render(request, "student_template/student_view_result.html", context)


def student_Payment_Feest(request, courses_id):
    fee_cuorses = Courses_Fees.objects.get(courses=courses_id)

    print('fee is', fee_cuorses.fee)
 
    context = {
        'fee_cuorses':fee_cuorses
       
    }
    return render(request, "student_template/student_Payment_Fees.html", context)





def student_feedback_my_chat(request):
    
    context = {
        "staff": 'from_Subjects_to_get_staff'
    }
    return render(request, 'student_template/s.html', context)


def list_split(listA, n):


    for x in range(0, len(listA), n):
        every_chunk = listA[x: n+x]

        if len(every_chunk) < n:
            every_chunk = every_chunk + \
                [None for y in range(n-len(every_chunk))]
        yield every_chunk

def retrn_clean_data(data, number):
   frist_data = ''
   clean_data_1 = []
   clean_data_2 = []
   get_data_string = ''

   frist_data = data
   clean_data_1 = frist_data.split('"]')
   for j in clean_data_1:
       for h in j:
           if h == '['  or h == ']' or h == "'" or h == '"':
               h = ''
           else:
               get_data_string += h
   clean_data_2 = get_data_string.split(',')
   clean_Data = list(list_split(clean_data_2, number))
   """ end the fun """
#    print('end_or_list_data', clean_Data)
#    print(':::::::::::my own function:::::::::::::')
   return clean_Data

@csrf_exempt
def student_single_student_chat(request, id):
    all_data = None
    staff_messag_after_fillter = None
    staffs_our = []
    student_obj = Students.objects.get(admin=request.user)
    course_obj = Courses.objects.get(id=student_obj.course_id.id)
    from_Subjects_to_get_staff = Subjects.objects.filter(course_id=student_obj.course_id)
    print(student_obj.id, 'user student', request.user.id , 'requeststudent', from_Subjects_to_get_staff)
    for single_staff in from_Subjects_to_get_staff:
        staff_end = Staffs.objects.get(admin=single_staff.staff_id)
        print(single_staff.staff_id, staff_end.id, 'id ===>', id)
        staffs_our.append(staff_end)
    staff_without_repet = set(staffs_our)




    all_masseg_from_staff = FeedBackStudent_chat.objects.filter(staff_resver=id, student_sender=student_obj.id)
    print(all_masseg_from_staff, 'all messages')


    request.session.set_expiry(0)
    """ fun get string data from Ajax and trnsfrom it to list or array  """
    if is_ajax(request=request):
       student_reple = request.session['list_student_reple'] = request.POST.get('list_student_reple')
       staff_messag = request.session['list_staff_messa'] = request.POST.get('list_staff_messa')

       print(student_reple, 'tesssssssssssssssst')
       staff_messag_after_fillter = retrn_clean_data(staff_messag, 4)
       all_data=retrn_clean_data(student_reple, 4)

       if staff_messag_after_fillter[0][1] == "":
            pass
       else:
            staf = Subjects.objects.filter(staff_id=id)
            staff_and_student = FeedBackStudent_chat.objects.filter(staff_resver=int(staff_messag_after_fillter[0][2]), student_sender=int(staff_messag_after_fillter[0][3]),)
            print(staff_and_student, 'chet')
            satfa_id = Staffs.objects.get(id=int(staff_messag_after_fillter[0][2]))
            # print(satfa_id)
            edit_reple_to_student = FeedBackStudent_chat.objects.create(staff_resver=satfa_id,
                                                       student_sender=student_obj,
                                                        feedback=staff_messag_after_fillter[0][1], feedback_reply="")
            # edit_reple_to_student.feedback_reply = all_data[0][1]
            edit_reple_to_student.save()

            # print(edit_reple_to_student, 'the student reple', staff_messag_after_fillter)





















    context = {
        'student_id':student_obj.id,
        'staff_id':id,
        "staff": staff_without_repet,
        "all_masseg_from_staff":all_masseg_from_staff,
    }
    return render(request, 'student_template/student_chat.html', context)

