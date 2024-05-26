from multiprocessing import context
from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.core.files.storage import FileSystemStorage #To upload Profile Picture
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.db.models import Q
from .forms import Add_FeedBackStaffs_chat, Add_FeedBackStudent_chat
from django.shortcuts import HttpResponse


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def index(request):
    subjects = Subjects.objects.filter(staff_id=request.user.id)
    all_sutudent_subject = None
    data_char = []
    name_cahr = []
    get_subject_from_courses=[]
    

   
    cources_under_Teacher = []
    all_student_under_Teacher = []
    all_student_ander_to_for_loop = []
    student_by_cource_id = None
    for j in subjects:


        print(j.course_id)
        cources_under_Teacher.append(j.course_id)
    cources_under_Teacher=list(set(cources_under_Teacher))

    #get student hava same cource id
    # student_by_cource_id = Students.objects.filter(course_id=cources_under_Teacher[0].id)
    #for take all student 
   
    print('test', student_by_cource_id)
    for courses_that_teach_have in cources_under_Teacher:
        student_by_cource_id = Students.objects.filter(course_id=courses_that_teach_have.id)
        print(student_by_cource_id)

    for courses_that_teach_have in cources_under_Teacher:

        student_by_cource_id_ = Students.objects.filter(course_id=courses_that_teach_have.id)
        print('len =>', len(student_by_cource_id_))
        if len(student_by_cource_id_)>1:
            for jk in student_by_cource_id_:
                all_student_under_Teacher.append(jk)
        else:
            all_student_under_Teacher.append(student_by_cource_id_)

    print('all studen is ', subjects,all_student_under_Teacher, len(all_student_under_Teacher))

    """# this part particlar for chart.js gender"""

    for j in subjects:
        data_char.append(1)
        name_cahr.append(str(j.subject_name))

    data_char.append(len(subjects))
    name_cahr.append( 'your all Subjects')

    """get list of student gender m or fm"""
    student_m = []
    student_fm = []
    if len(all_student_under_Teacher)==1:
        for student_gender_type in all_student_under_Teacher[0]:
            if student_gender_type.gender == 'Male':
                student_m.append('Male')
            else:
                student_fm.append('Female')
    else:
        for student_gender_type in all_student_under_Teacher:
            try:
                if student_gender_type.gender == 'Male':
                    student_m.append('Male')
                else:
                    student_fm.append('Female')
        
            except:
                pass



    



   
    print(subjects.count(), request.user.first_name, cources_under_Teacher)
    print('tha data that we sended its ', student_m, student_fm)
    context ={
        'all_student_under_Teacher':len(all_student_under_Teacher),
        'cources_under_Teacher':cources_under_Teacher,
        'subjects':subjects,
        'data_char':data_char,
        'name_char': name_cahr,
        'student_m':len(student_m),
        'student_fm' : len(student_fm),


    }

    return render(request, './pages/index.html', context)


def show_student_by_course_id(request, course_id):

    All_Students_by_course_id = Students.objects.filter(course_id=course_id)
    print(All_Students_by_course_id)

    context={
        'All_Students_by_course_id':All_Students_by_course_id
    }

    return render(request, './pages/student_course_id.html', context)



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
def Take_student_Attendance(request, subjects_id):
   """ fun get student_Attendance data from Ajax and trnsfrom it to list or array  """


   id_cuors = None
   all_data = []
   
   

   request.session.set_expiry(0)
   """ fun get string data from Ajax and trnsfrom it to list or array  """
   try:
        if is_ajax(request=request):
            data = request.session['list_s'] = request.POST.get('list_s')
            print(data, 'tesssssssssssssssst')
     
            all_data = retrn_clean_data(data, 3)
            print('alldata is = ', all_data)
        else:
            print('Ajex error fom the fuon ')

       

   except:
        print('Ajex error ')




   subject_id_ = Attendance.objects.filter(id=1)
   Students_id_ = Students.objects.filter(id=1)
   staff = Staffs.objects.filter(id=1)
   subject = Subjects.objects.filter(id=1)
#    Student_Degree.objects.filter(subject_id=subjects_id).delete()

   for sin_student in all_data:

           subject = Subjects.objects.get(id=int(sin_student[0]))
           Students_id_ = Students.objects.get(id=int(sin_student[1]))
           staff = Subjects.objects.get(id=subjects_id)
           saff_sin = Staffs.objects.filter(admin=staff.staff_id )
           print(' the value that i wont to save it',subject, Students_id_, saff_sin[0] )
           Attendanc_save = My_Attendance(subject_id=subject, student_id=Students_id_, staff_id=saff_sin[0], status=int(sin_student[2]))
           Attendanc_save.save()

   supject_sing = Subjects.objects.get(id=subjects_id)
   print('subject ==', supject_sing.course_id)
   student_by_aubject_id = Students.objects.filter(course_id=supject_sing.course_id)
   print(student_by_aubject_id)
   
   # here to sum all Attendanc for uesh student
   All_Students_by_course_id = Subjects.objects.filter(id=subjects_id)
   
   for subject_id_get in All_Students_by_course_id:
      
       id_cuors = subject_id_get.course_id.id
       print(id_cuors, 'testt======>')


   subject_student = Students.objects.filter(course_id=id_cuors)
   print('###', subject_student)
   student_sum_Atten = []
   for Att_studen in subject_student:
       print(Att_studen.id, '$$$$$$$$$$$')
       Attendance_student = My_Attendance.objects.filter(student_id=Att_studen.id)&My_Attendance.objects.filter(subject_id=subjects_id)
       Att_studen_dict = Attendance_student.aggregate(Sum('status'))
       student_sum_Atten.append(Att_studen_dict['status__sum'])
       print('the sum is === >', Attendance_student.aggregate(Sum('status')))
       print(student_sum_Atten)
   student_names = []


   for cont_Attendsnce in Attendance_student:
        student_names.append(cont_Attendsnce.student_id)
         
        print('Attendance_student =>', cont_Attendsnce.student_id, cont_Attendsnce.status)
   print(list(set(student_names), ))
   all_abute = zip(subject_student, student_sum_Atten)
   

   context={
         'All_Students_by_course_id': student_by_aubject_id,
        'subject_id':subjects_id,
        'all_abute':all_abute,
    }

   return render(request, './pages/Take_student_Attendance.html', context)


@csrf_exempt
def save_Take_Review(request):
   id_cuors = None
   all_data = []
   
   

   request.session.set_expiry(0)
   """ fun get string data from Ajax and trnsfrom it to list or array  """
   if is_ajax(request=request):
       data = request.session['list_s'] = request.POST.get('list_s')
       print(data, 'tesssssssssssssssst')
     
       all_data = retrn_clean_data(data, 3)
   print('alldata is = ', all_data)








      #pass Reviw degree
   Reviw_degree = Student_Review.objects.filter(subject_id=all_data[0][0]).delete()
   print(':::::::::::::::', Reviw_degree)
   for sigle_student in all_data:
        subject = Subjects.objects.get(id=int(sigle_student[0]))
        Students_id_ = Students.objects.get(id=int(sigle_student[1]))
        staff = Staffs.objects.get(admin=request.user.id)

        new_reviw = Student_Review.objects.create(subject_id=subject, student_id=Students_id_, staff_id=staff,  Degree=int(sigle_student[2]))
            # Degree_save = Student_Review(subject_id=subject, student_id=Students_id_, staff_id=staff, Degree=int(2))
        new_reviw.save()
        print(staff, 'see me mouer')
        # new_reviw_old = Student_Review.objects.filter(subject_id=subject, student_id=Students_id_, staff_id=staff)
        # if new_reviw_old:
        #     Degree_save = Student_Review(subject_id=subject, student_id=Students_id_, staff_id=staff, Degree=int(2))
        #     Degree_save.save()
        #     print('oled', new_reviw_old)
        # else:
        #     print('no now')

        #     new_reviw = Student_Review.objects.create(subject_id=subject, student_id=Students_id_, staff_id=staff, Degree=int(2))
        #     # Degree_save = Student_Review(subject_id=subject, student_id=Students_id_, staff_id=staff, Degree=int(2))
        #     new_reviw.save()


   return HttpResponse('Hello')











@csrf_exempt
def Take_Review(request, subjects_id):
   """ fun get student_Attendance data from Ajax and trnsfrom it to list or array  """


   id_cuors = None
   all_data = []
   
   

   request.session.set_expiry(0)
   """ fun get string data from Ajax and trnsfrom it to list or array  """
   if is_ajax(request=request):
       data = request.session['list_s'] = request.POST.get('list_s')
       print(data, 'tesssssssssssssssst')
     
       all_data = retrn_clean_data(data, 3)
   print('alldata is = ', all_data)


   #pass Reviw degree
   Reviw_degree = Student_Review.objects.filter(subject_id=subjects_id)
#    for sigle_student in all_data:
#         subject = Subjects.objects.get(id=int(sigle_student[0]))
#         Students_id_ = Students.objects.get(id=int(sigle_student[1]))
#         staff = Staffs.objects.get(admin=request.user.id)
#         print(staff, 'see me mouer')
#         new_reviw_old = Student_Review.objects.filter(subject_id=subject, student_id=Students_id_, staff_id=staff)
#         if new_reviw_old:
#             Degree_save = Student_Review(subject_id=subject, student_id=Students_id_, staff_id=staff, Degree=int(2))
#             Degree_save.save()
#             print('oled', new_reviw_old)
#         else:
#             print('no now')

#             new_reviw = Student_Review.objects.create(subject_id=subject, student_id=Students_id_, staff_id=staff, Degree=int(2))
#             # Degree_save = Student_Review(subject_id=subject, student_id=Students_id_, staff_id=staff, Degree=int(2))
#             new_reviw.save()

#    Student_Review.objects.filter(subject_id=subjects_id).delete()

#    for sin_student in all_data:


#        if len(all_data) == 1:
#            if not Reviw_degree:

#                 subject = Subjects.objects.get(id=int(sin_student[0]))
#                 Students_id_ = Students.objects.get(id=int(sin_student[1]))
#                 staff = Staffs.objects.get(admin=request.user.id)
#                 print(staff, 'see me mouer')
#                 Degree_save = Student_Review(subject_id=subject, student_id=Students_id_, staff_id=staff, Degree=int(sin_student[2]))
#                 Degree_save.save()
#            else:

#            #crzy thing is there

#                 subject = Subjects.objects.get(id=int(sin_student[0]))
#                 Students_id_ = Students.objects.get(id=int(sin_student[1]))
#                 staff = Staffs.objects.get(admin=request.user.id)
#                 Reviw_degree[all_data.index(sin_student)].subject_id=subject
#                 Reviw_degree[all_data.index(sin_student)].student_id=Students_id_
#                 Reviw_degree[all_data.index(sin_student)].staff_id=staff
#                 Reviw_degree[all_data.index(sin_student)].Degree = int(sin_student[2])
#                 Reviw_degree[all_data.index(sin_student)].save()

           
#        else:

#            if not Reviw_degree:

#             subject = Subjects.objects.filter(id=int(sin_student[0]))
#             Students_id_ = Students.objects.filter(id=int(sin_student[1]))
#             staff = Staffs.objects.filter(id=request.user.id)

#             Degree_save = Student_Review(subject_id=subject[0], student_id=Students_id_[0], staff_id=staff[0], Degree=int(sin_student[2]))
#             Degree_save.save()



#            else:

#            #crzy thing is there

#             subject = Subjects.objects.filter(id=int(sin_student[0]))
#             Students_id_ = Students.objects.filter(id=int(sin_student[1]))
#             staff = Staffs.objects.filter(id=request.user.id)
#             Reviw_degree[all_data.index(sin_student)].subject_id=subject[0]
#             Reviw_degree[all_data.index(sin_student)].student_id=Students_id_[0]
#             Reviw_degree[all_data.index(sin_student)].staff_id=staff[0]
#             Reviw_degree[all_data.index(sin_student)].Degree = int(sin_student[2])
#             Reviw_degree[all_data.index(sin_student)].save()



       
 


            #    Degree_save = Student_Review(subject_id=subject[0], student_id=Students_id_[0], staff_id=staff[0], Degree=int(sin_student[2]))
            #    Degree_save.save()
   Reviw_degrees_list = []
   Reviw_degrees = Student_Review.objects.filter(subject_id=subjects_id)
   print('here the Reviw_degrees', Reviw_degrees)
   supject_sing = Subjects.objects.get(id=subjects_id)
   print('subject ==', supject_sing.course_id)
   student_by_aubject_id = Students.objects.filter(course_id=supject_sing.course_id)
   print(student_by_aubject_id)
   
   # here to sum all Attendanc for uesh student
   All_Students_by_course_id = Subjects.objects.filter(id=subjects_id)
   print('testmy_here ', All_Students_by_course_id)
   for subject_id_get in All_Students_by_course_id:
      
       id_cuors = subject_id_get.course_id.id
       print(id_cuors, 'testt======>')


   subject_student = Students.objects.filter(course_id=id_cuors)
   print('###', subject_student, '$$$$$')
   student_sum_Atten = []
   for reviw, Att_studen in enumerate(subject_student) :

        if len(Reviw_degrees) == len(subject_student) :
            Reviw_degrees_list = Reviw_degrees
            print('yes')
        else:
            try:
                Reviw_degrees_list.append(Reviw_degrees[reviw])
                
            except:
                  Reviw_degrees_list.append(0)

            print('no')
       
        
        print(reviw)
        print(Att_studen.id, '$$$$$$$$$$$')
        Attendance_student = My_Attendance.objects.filter(student_id=Att_studen.id, subject_id=subjects_id)
        #&My_Attendance.objects.filter(subject_id=subjects_id)
        Att_studen_dict = Attendance_student.aggregate(Sum('status'))
        student_sum_Atten.append(Att_studen_dict['status__sum'])
        print('the sum is === >', Attendance_student.aggregate(Sum('status')))
        print(student_sum_Atten)
   student_names = []
   print(Reviw_degrees_list, 'Reviw_degrees_list')
    

   for cont_Attendsnce in Attendance_student:
        student_names.append(cont_Attendsnce.student_id)
         
        print('Attendance_student =>',Reviw_degree, cont_Attendsnce.student_id, cont_Attendsnce.status)
   print(list(set(student_names), ))
   all_abute = zip(subject_student, student_sum_Atten, Reviw_degrees_list)
   

   context={
         'All_Students_by_course_id': student_by_aubject_id,
        'subject_id':subjects_id,
        'all_abute':all_abute,
    }
    

   return render(request, './pages/Take_Review.html', context)






@csrf_exempt
def Edit_student_Attendance(request,student_id, subject_id, ):
    """ this fun for Edit_student_Attendance use Ajax to update the data  """

    all_data = []
    update_data_index = None
    frist_data = ''
    clean_data_1 = []
    clean_data_2 = []
    data_form_fun = []
    get_data_string = ''
    stud = Students.objects.filter(id=student_id)
    subj = Subjects.objects.filter(id=subject_id)
    edit_student_Attenedance = My_Attendance.objects.filter(Q(subject_id=subject_id) & Q(student_id=student_id))
    print(edit_student_Attenedance)
    print(stud, subj, edit_student_Attenedance.aggregate(Sum('status')))

    request.session.set_expiry(0)
    if is_ajax(request=request):

       data = request.session['list_s'] = request.POST.get('list_s')
       print(data, 'tesssssssssssssssst')

       for upate_data in data:
           print(upate_data)

       """ fun get string data from Ajax and trnsfrom it to list or array  """

       frist_data = data
       clean_data_1 = frist_data.split('"]')

       for j in clean_data_1:
           for h in j:
               if h == '['  or h == ']' or h == "'" or h == '"':
                   h = ''
               else:
                   get_data_string += h


       clean_data_2 = get_data_string.split(',')

       all_data = list(list_split(clean_data_2, 1))



       """ end the fun """

    print('end_or_list_data', all_data)
    Attendance_edit = My_Attendance.objects.filter(subject_id=subject_id)
    for update_data_index in range(len(all_data)):

        print(int(all_data[update_data_index][0]), edit_student_Attenedance[update_data_index])
        print(edit_student_Attenedance[update_data_index].id)
        update_obj = edit_student_Attenedance.get(id=edit_student_Attenedance[update_data_index].id)
        update_obj.status = int(all_data[update_data_index][0])
        update_obj.save()
        print('its done')


            # Degree_save = My_Attendance(status=int(upate_data[0]))
            # Degree_save.save()






    context={
        'edit_student_Attenedance':edit_student_Attenedance,
        'student_id':student_id,
        'subject_id':subject_id,

    }

    return render(request, './pages/Edit_student_Attendance.html', context)





def staff_feedback(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    feedback_data = FeedBackStaffs.objects.filter(staff_id=staff_obj)
    context = {
        "feedback_data":feedback_data
    }
    return render(request, "pages/staff_feedback_template.html", context)





def staff_feedback(request):
    staff_obj = Staffs.objects.get(admin=request.user.id)
    feedback_data = FeedBackStaffs.objects.filter(staff_id=staff_obj)
    context = {
        "feedback_data":feedback_data
    }
    return render(request, "pages/staff_feedback_template.html", context)


def staff_feedback_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method.")
        return redirect('staff_feedback')
    else:
        feedback = request.POST.get('feedback_message')
        staff_obj = Staffs.objects.get(admin=request.user.id)

        try:
            add_feedback = FeedBackStaffs(staff_id=staff_obj, feedback=feedback, feedback_reply="")
            add_feedback.save()
            messages.success(request, "Feedback Sent.")
            return redirect('staff_feedback')
        except:
            messages.error(request, "Failed to Send Feedback.")
            return redirect('staff_feedback')


@csrf_exempt
def staff_feedback_chat(request, id):
    all_data = None
    staff_messag_after_fillter = None
    courses = []
    All_student = []
    student_obj = Staffs.objects.get(admin=request.user.id)
    # course_obj = Courses.objects.get(id=student_obj.course_id.id)
    get_Subjects = Subjects.objects.filter(staff_id=student_obj.admin)
    # total_subjects = Subjects.objects.filter(course_id=course_obj).count()
    print(student_obj.admin, 'course', get_Subjects[0].course_id)
    for course in get_Subjects:
            courses.append(course.course_id)

    all_masseg_from_student = FeedBackStudent_chat.objects.filter(student_sender=id)
    print(all_masseg_from_student, 'here i am')
    print(courses)
    courses = list(set(courses))
    print(courses)

    for course_id in courses:
        
        Get_Students = Students.objects.filter(course_id=course_id)
        All_student.append(Get_Students)

    print(All_student)




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
            staff_and_student = FeedBackStudent_chat.objects.filter(staff_resver=int(staff_messag_after_fillter[0][2]),student_sender =int(staff_messag_after_fillter[0][3]),)
            print(staff_and_student, 'chet')
            try:
                edit_reple_to_student = FeedBackStudent_chat.objects.create(staff_resver=staff_and_student[0].staff_resver,
                                                       student_sender=staff_and_student[0].student_sender,
                                                        feedback="", feedback_reply=staff_messag_after_fillter[0][1])
                # edit_reple_to_student.feedback_reply = all_data[0][1]
                edit_reple_to_student.save()

                print(edit_reple_to_student, 'the student reple', staff_messag_after_fillter)
            except:

                staff_and_student = Staffs.objects.get(id=int(staff_messag_after_fillter[0][2]))
                print(staff_and_student, 'chet')
                student_opj = Students.objects.get(id=id)
                print(student_opj, 'i am here my mpra')
                edit_reple_to_student = FeedBackStudent_chat.objects.create(staff_resver=staff_and_student,
                                                       student_sender=student_opj,
                                                        feedback=" ", feedback_reply=staff_messag_after_fillter[0][1])
                # edit_reple_to_student.feedback_reply = all_data[0][1]
                edit_reple_to_student.save()

                print(edit_reple_to_student, 'the student reple', staff_messag_after_fillter)


       if all_data[0][1] == "":
            pass
       else:
            edit_reple_to_student = FeedBackStudent_chat.objects.get(id=all_data[0][0])
            edit_reple_to_student.feedback_reply = all_data[0][1]
            edit_reple_to_student.save()

            print(edit_reple_to_student, 'the student reple', staff_messag_after_fillter)

    print('alldata is = ', all_data, all_data)
    # d = FeedBackStudent_chat.objects.all()
    # d.delete()
 
    all_mess = []
    #ather way to get the data from tow table
    messages_chat = FeedBackStudent_chat.objects.filter(staff_resver=student_obj.id, student_sender=id)
    #.union(FeedBackStudent_chat.objects.filter(student_sender=id))
    # messages_chat2 = FeedBackStudent_chat.objects.filter(student_sender=id)
    # from itertools import chain
    # all_mess = list(chain(messages_chat, messages_chat2.order_by('created_at')))
    # #
    print(messages_chat.order_by('created_at'), 'here is all messaes', len(all_mess))








    if request.method == 'POST':
        # Donors_to_Company = Donors_to_Company_Form(request.POST, request.FILES)
        # Donors_to_Company_Dress_ = Add_FeedBackStaffs_chat(request.POST, request.FILES)
        Donors_to_Company_Dress_2 = Add_FeedBackStudent_chat(request.POST, request.FILES)

        # company = Profile_company.objects.get(user=request.user)
        # print('ok', company,  request.user, company.company_name)
        #print('companyname' ,company[0].user, company[0].company_name)
        if Donors_to_Company_Dress_2.is_valid():
            
            # Donors_to_Company_Dress_.save()
            Donors_to_Company_Dress_2.save()
            print('ok2')
        else:
            print('thamething wrong1')
    else:
        # Donors_to_Company_Dress_ = Add_FeedBackStaffs_chat()
        Donors_to_Company_Dress_2 = Add_FeedBackStudent_chat()

    print(student_obj.id, 'id')
    context = {
        "student": All_student[0],
        # 'form' :Donors_to_Company_Dress_,
        'form2':Donors_to_Company_Dress_2,
        'student_mass':all_masseg_from_student,
        'staff_id':student_obj.id,
        'student_id':id,
        'messages_chat':messages_chat.order_by('created_at'),
    }
    return render(request, "staff_template/staff_chat.html", context)
