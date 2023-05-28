from django.utils import timezone
import json

from django.shortcuts import render, HttpResponse
from index.models import *
from utils import *


# Create your views here.
def index(request):
    # return HttpResponse("this is a test")
    return render(request, 'teacher/index.html')


def courseTable(request):
    return render(request, 'teacher/courseTable.html')


def applyTable(request):
    return render(request, 'teacher/applyTable.html')


def studentTable(request):
    return render(request, 'teacher/studentTable.html')


def homepage(request):
    return render(request, 'teacher/homepage.html')


def homework(request):
    return render(request, 'teacher/homework.html')


def booking_select(request):
    """
    查看学员申请（预约功能）
    @param request:
    @return:
    """
    # GET请求, 进入学员申请审核页面
    if request.method == 'GET':
        return render(request, 'temp_学员申请审核')

    # POST请求, 业务实现
    elif request.method == 'POST':
        temp_tid = request.POST.get('temp_teacher_id')
        temp_sid = request.POST.get('temp_student_id')
        temp_time = request.POST.get('temp_time')
        # print(temp_condition_1)
        # print(temp_condition_2)

        # 列表存储查询结果
        temp_json_data = []

        # 参数都为空, 查询全部申请信息
        if not temp_tid:

            # 执行中间表的查询操作，获取数据
            booking_data = Booking.objects.all()
        elif temp_sid and temp_time:
            print('2')
            booking_data = Booking.objects.filter(teacherid=temp_tid, studentid=temp_sid, bookingtime=temp_time)
        elif temp_sid:
            booking_data = Booking.objects.filter(teacherid=temp_tid, studentid=temp_sid)
        elif temp_time:
            booking_data = Booking.objects.filter(teacherid=temp_tid,
                                                  bookingtime=temp_time)
        else:
            booking_data = Booking.objects.filter(teacherid=temp_tid)
            # 构建结果列表
        result = []
        for st_data in booking_data:
            student_name = st_data.studentid.realname
            teacher_name = st_data.teacherid.realname
            bookdescription = st_data.bookdescription
            time = st_data.booktime
            if time:
                time = time.strftime('%Y-%m-%d %X')
            result.append({
                'student_name': student_name,
                'teacher_name': teacher_name,
                'bookdescription': bookdescription,
                'time': time

            })

        # 将结果列表转换为JSON字符串
        temp_json_data = json.dumps(result)

        # else:
        #     多条件动态查询
        #     temp_data 保存
        #     数组转为 json 格式

        return HttpResponse(temp_json_data, content_type='application/json')

    # return HttpResponse('预约查询')


def booking_examine(request):
    """
    审核学员申请（预约功能）
    @param request:
    @return:
    """
    # POST请求, 业务实现
    if request.method == 'POST':
        temp_tid = request.POST.get('temp_tid')
        temp_sid = request.POST.get('temp_sid')
        temp_choose = request.POST.get('temp_choose')

        # 参数不全, 错误
        if not all([temp_sid, temp_tid]):
            return HttpResponse('参数不全')

        if temp_choose == '1':
            Booking.objects.filter(studentid=temp_sid, teacherid=temp_tid).update(booksuccess=1)
        else:
            Booking.objects.filter(studentid=temp_sid, teacherid=temp_tid).update(booksuccess=0)

        return HttpResponse('ok')

    # return HttpResponse('预约审核')


def evaluate(request):
    """
    给予学员评价
    @param request:
    @return:
    """
    # POST请求, 业务实现
    if request.method == 'POST':
        temp_studentid = request.POST.get('temp_sid')
        temp_tid = request.POST.get('temp_tid')
        temp_comment = request.POST.get('temp_comment')
        temp_star = request.POST.get('temp_star')
        time = timezone.now()

        #  参数不全, 错误
        if not all([temp_studentid, temp_tid]):
            return HttpResponse('参数不全')

        # 添加数据到相应表
        Teachertostudentcomment.objects.create(
            studentid=Student.objects.filter(studentid=temp_studentid).first(),
            teacherid=Teacher.objects.filter(teacherid=temp_tid).first(),
            t2scomment=temp_comment,
            t2sstar=temp_star,
            t2scommenttime=time
        )

        return HttpResponse('ok')

    # return HttpResponse('评价')


def timetable(request):
    """
    查看课表
    @param request:
    @return:
    """
    # GET请求, 进入课表查看页面
    if request.method == 'GET':
        return render(request, 'temp_课表查看')

    # POST请求, 业务实现
    elif request.method == 'POST':
        temp_tid = request.POST.get('temp_tid')

        # 列表存储查询结果
        temp_json_data = []

        # 参数都为空, 查询全部信息
        if not temp_tid:
            # 执行中间表的查询操作，获取数据
            timetable_data = Teach.objects.all()
        else:
            timetable_data = Teach.objects.filter(teacherid=temp_tid)

        # 构建结果列表
        result = []
        for time_data in timetable_data:
            course_name = time_data.courseid.coursename
            class_set = Class.objects.filter(courseid=time_data.courseid)
            course_time = []
            for class_data in class_set:
                class_date = class_data.classdate
                class_date = translateDateId2Date(class_date)
                class_time = class_data.classtime
                course_time.append({'class_date': class_date, 'class_time': class_time})
            stime = time_data.courseid.coursestarttime
            if stime:
                stime = stime.strftime('%Y-%m-%d %X')
            etime = time_data.courseid.courseendtime
            if etime:
                etime = etime.strftime('%Y-%m-%d %X')
            course_type = time_data.courseid.coursetype
            course_type = translateTypeId2Type(course_type)
            result.append({
                'course_name': course_name,
                'course_time': course_time,
                'course_start_time': stime,
                'course_end_time': etime,
                'course_type': course_type
            })

        # 将结果列表转换为JSON字符串
        temp_json_data = json.dumps(result)

        return HttpResponse(temp_json_data, content_type='application/json')

    return HttpResponse('课表')


def course_start(request):
    """
    课程开设
    @param request:
    @return:
    """
    # GET请求, 进入课程开设页面
    if request.method == 'GET':
        return render(request, 'temp_课程开设')

    # POST请求, 业务实现
    elif request.method == 'POST':
        # temp_cid = request.POST.get('temp_cid')
        temp_stime = request.POST.get('temp_start_time')
        temp_etime = request.POST.get('temp_end_time')
        temp_type = request.POST.get('temp_type')
        temp_type = translateType2TypeId(temp_type)
        temp_name = request.POST.get('temp_name')
        temp_intro = request.POST.get('temp_intro')
        temp_state = 'reviewing'
        # 参数不全, 错误
        if not all([temp_type]):
            return HttpResponse('参数不全')

        course = Course.objects.create(coursestarttime=temp_stime, courseendtime=temp_etime, coursetype=temp_type,
                                       coursename=temp_name, courseintro=temp_intro, coursestate=temp_state)

        coursereview = Coursereview.objects.create(courseid=course, adminid=Admin.objects.order_by('?').first(),
                                                   reviewstate=temp_state)
        # print(course.courseid)
        # 加入相应表中

        # 返回成功信息。
        return HttpResponse('ok')

    return HttpResponse('开设课程')


def course_change(request):
    """
    课程更改
    @param request:
    @return:
    """
    # GET请求, 进入课程开设页面
    if request.method == 'GET':
        return render(request, 'temp_课程开设')

    # POST请求, 业务实现
    elif request.method == 'POST':
        temp_cid = request.POST.get('temp_course_id')
        temp_stime = request.POST.get('temp_start_time')
        temp_etime = request.POST.get('temp_end_time')
        temp_type = request.POST.get('temp_type')
        temp_type = translateType2TypeId(temp_type)
        temp_name = request.POST.get('temp_name')
        temp_num = request.POST.get('temp_register_num')
        temp_favor = request.POST.get('temp_favor_degree')
        temp_intro = request.POST.get('temp_intro')

        # 参数不全, 错误
        if not all([temp_cid]):
            return HttpResponse('参数不全')

        # 更改到相应表中
        course = Course.objects.filter(courseid=temp_cid)
        if course is not None:
            if temp_stime:
                course.update(coursestarttime=temp_stime)
            if temp_etime:
                course.update(courseendtime=temp_etime)
            if temp_type:
                course.update(coursetype=temp_type)
            if temp_name:
                course.update(cousrename=temp_name)
            if temp_num:
                course.update(courseregisternum=temp_num)
            if temp_favor:
                course.update(coursefavordeg=temp_favor)
            if temp_intro:
                course.update(courseintro=temp_intro)

        # 返回成功信息。
        return HttpResponse('ok')

    return HttpResponse('课程更改')


def course_delete(request):
    """
    课程删除
    @param request:
    @return:
    """
    # GET请求, 进入课程删除页面
    if request.method == 'GET':
        return render(request, 'temp_课程删除')

    # POST请求, 业务实现
    elif request.method == 'POST':
        temp_cid = request.POST.get('temp_course_id')

        # 参数不全, 错误
        if not all([temp_cid]):
            return HttpResponse('参数不全')
        Course.objects.get(courseid=temp_cid).delete()
        # 返回成功信息。
        return HttpResponse('ok')

    return HttpResponse('删除课程')


def homework_assign(request):
    """
       作业发布
       @param request:
       @return:
    """
    # GET请求, 进入作业发布页面
    if request.method == 'GET':
        return render(request, 'temp_作业发布')

    # POST请求, 业务实现
    elif request.method == 'POST':
        temp_cid = request.POST.get('temp_class_id')
        temp_tid = request.POST.get('temp_teacher_id')
        temp_stime = request.POST.get('temp_start_time')
        temp_etime = request.POST.get('temp_end_time')
        temp_content = request.POST.get('temp_content')

        if not all([temp_cid, temp_tid]):
            return HttpResponse('参数不全')

        homework = Homework.objects.create(classid=Class.objects.get(classid=temp_cid),
                                           teacherid=Teacher.objects.get(teacherid=temp_tid),
                                           homeworkstarttime=temp_stime,
                                           homeworkendtime=temp_etime, homeworkcontent=temp_content)
        return HttpResponse('ok')

    return HttpResponse('发布作业')


def homework_change(request):
    """
           作业修改
           @param request:
           @return:
        """
    # GET请求, 进入作业发布页面
    if request.method == 'GET':
        return render(request, 'temp_作业发布')

    # POST请求, 业务实现
    elif request.method == 'POST':
        temp_hid = request.POST.get('temp_homework_id')

        temp_stime = request.POST.get('temp_start_time')
        temp_etime = request.POST.get('temp_end_time')
        temp_content = request.POST.get('temp_content')

        if not all([temp_hid]):
            return HttpResponse('参数不全')
        print('1')
        # 更改到相应表中
        homework = Homework.objects.filter(homeworkid=temp_hid)
        print('2')
        if homework is not None:
            if temp_stime:
                homework.update(homeworkstarttime=temp_stime)
            if temp_etime:
                homework.update(homeworkendtime=temp_etime)
            if temp_content:
                homework.update(homeworkcontent=temp_content)
            # 返回成功信息。
        return HttpResponse('ok')

    return HttpResponse('课程修改')


def homework_delete(request):
    """
    作业删除
    @param request:
    @return:
    """
    # GET请求, 进入课程删除页面
    if request.method == 'GET':
        return render(request, 'temp_作业删除')

    # POST请求, 业务实现
    elif request.method == 'POST':
        temp_hid = request.POST.get('temp_homework_id')

        # 参数不全, 错误
        if not all([temp_hid]):
            return HttpResponse('参数不全')
        Homework.objects.get(homeworkid=temp_hid).delete()
        # 返回成功信息。
        return HttpResponse('ok')

    return HttpResponse('删除作业')


def homework_select(request):
    """
     查看发布的作业
     @param request:
     @return:
     """
    # GET请求, 进入作业发布
    if request.method == 'GET':
        return render(request, 'temp_作业发布')

    # POST请求, 业务实现
    elif request.method == 'POST':
        temp_hid = request.POST.get('temp_homework_id')
        temp_cid = request.POST.get('temp_class_id')
        temp_tid = request.POST.get('temp_teacher_id')

        # print(temp_condition_1)
        # print(temp_condition_2)

        # 列表存储查询结果
        temp_json_data = []

        # 参数都为空, 查询全部申请信息
        if not temp_tid:
            # 执行中间表的查询操作，获取数据
            homework_data = Homework.objects.all()
        elif temp_hid and temp_cid:
            homework_data = Homework.objects.filter(teacherid=temp_tid, homeworkid=temp_hid, classid=temp_cid)
        elif temp_hid:
            homework_data = Homework.objects.filter(teacherid=temp_tid, homeworkid=temp_hid)
        elif temp_cid:
            homework_data = Homework.objects.filter(teacherid=temp_tid, classid=temp_cid)
        else:
            homework_data = Homework.objects.filter(teacherid=temp_tid)

            # 构建结果列表
        result = []
        for hw_data in homework_data:
            class_id = hw_data.classid

            homework_id = hw_data.homeworkid

            course_name = hw_data.classid.courseid.coursename
            stime = hw_data.homeworkstarttime
            if stime:
                stime = stime.strftime('%Y-%m-%d %X')
            etime = hw_data.homeworkendtime.strftime('%Y-%m-%d %X')
            if etime:
                etime = etime.strftime('%Y-%m-%d %X')
            content = hw_data.homeworkcontent
            result.append({
                'homework_id': homework_id,
                'class_id': class_id.classid,
                'course_name': course_name,
                'start_time': stime,
                'end_time': etime,
                'content': content
            })

            # 将结果列表转换为JSON字符串
        temp_json_data = json.dumps(result)

        # else:
        #     多条件动态查询
        #     temp_data 保存
        #     数组转为 json 格式

        return HttpResponse(temp_json_data, content_type='application/json')

    # return HttpResponse('预约查询')


def activity_attend(request):
    """
         参加活动
         @param request:
         @return:
    """
    # GET请求, 进入活动参加
    if request.method == 'GET':
        return render(request, 'temp_活动参加')

    # POST请求, 业务实现
    elif request.method == 'POST':
        temp_aid = request.POST.get('temp_activity_id')
        temp_tid = request.POST.get('temp_activity_id')

        if not all([temp_aid, temp_tid]):
            return HttpResponse('参数不全')
        elif temp_aid and temp_tid:
            attend = TeacherAttend.objects.create(activityid=temp_aid, teacherid=temp_tid)
            return HttpResponse('ok')

    return HttpResponse('活动参加')


def activity_cancel(request):
    """
         取消活动
         @param request:
         @return:
    """
    # GET请求, 进入活动取消
    if request.method == 'GET':
        return render(request, 'temp_活动取消')

    # POST请求, 业务实现
    elif request.method == 'POST':
        temp_aid = request.POST.get('temp_activity_id')
        temp_tid = request.POST.get('temp_activity_id')

        if not all([temp_aid, temp_tid]):
            return HttpResponse('参数不全')
        elif temp_aid and temp_tid:
            TeacherAttend.objects.get(activityid=temp_aid, teacherid=temp_tid).delete()

            return HttpResponse('ok')

    return HttpResponse('活动取消')


def activity_show(request):
    """
             活动展示
             @param request:
             @return:
    """
    # GET请求, 进入活动展示
    if request.method == 'GET':
        return render(request, 'temp_活动展示')

    # POST请求, 业务实现
    elif request.method == 'POST':
        temp_aid = request.POST.get('temp_activity_id')
        temp_tid = request.POST.get('temp_teacher_id')

        if temp_aid and temp_tid:
            activities = [Teacherattend.objects.get(activityid=temp_aid, teacherid=temp_tid).activityid]
        elif temp_tid:
            activities = [x.activityid for x in Teacherattend.objects.filter(teacherid=temp_tid)]
        else:
            activities = Activity.objects.all()
        result = []

        for activity in activities:
            activity_id = activity.activityid
            activity_content = activity.activitycontent
            activity_place = activity.activityplace
            activity_stime = activity.activitystarttime
            if activity_stime:
                activity_stime = activity_stime.strftime('%Y-%m-%d %X')

            activity_etime = activity.activityendtime
            if activity_etime:
                activity_etime = activity_etime.strftime('%Y-%m-%d %X')
            result.append({
                'activity_id': activity_id,
                'content': activity_content,
                'place': activity_place,
                'start_time': activity_stime,
                'end_time': activity_etime,
            })

        temp_json_data = json.dumps(result)

        return HttpResponse(temp_json_data, content_type='application/json')


def announcement_show(request):
    """
            公告展示
            @param request:
            @return:
    """
    # GET请求, 进入活动展示
    if request.method == 'GET':
        return render(request, 'temp_活动展示')

    # POST请求, 业务实现
    elif request.method == 'POST':
        announcements = Announcement.objects.all()
        result = []

        for announcement in announcements:
            announcement_id = announcement.announceid
            content = announcement.announcecontent
            time = announcement.announcepublishtime
            if time:
                time = time.strftime('%Y-%m-%d %X')
            result.append({
                'announcement_id': announcement_id,
                'content': content,
                'publish_time': time
            })

        temp_json_data = json.dumps(result)

        return HttpResponse(temp_json_data, content_type='application/json')
