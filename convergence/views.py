from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import *
from datetime import datetime
import json, random, string
from .forms import *
from django.utils import timezone
from django.utils.encoding import smart_text
from django.core.files.storage import FileSystemStorage
from django.views.generic import UpdateView
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.conf import settings
#이메일 관련 import
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .tokens import AccountActivationTokenGenerator
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Q, F

import itertools
#csv export
import csv
import xlwt
# 다중 파일 업로드
from .forms import FileForm
from .models import Convergence_Files

#simple json
import simplejson as json

def page_not_found(request):
    response = render_to_response('convergence/page_404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response

def server_error(request):
    response = render_to_response('convergence/page_500.html', {}, context_instance=RequestContext(request))
    response.status_code = 500
    return response

# 세션 관리
def addSessions(request, user):
    request.session['convergence_id'] = user.Convergence_ID
    request.session['convergence_name'] = user.Convergence_Name
    request.session['rank'] = user.rank

# 접속자의 유저 객체 반환
def getInfo(request):
    user = User.objects.get(Convergence_ID=request.session['convergence_id'])
    return user

def loginpage(request):
    return render(request, 'convergence/login/loginpage.html')

def login(request, page_num=1):
    if request.method == 'POST':
        user_id = request.POST['convergence_id']
        user_pw = request.POST['convergence_pw']
        try:
            user = User.objects.get(Convergence_ID=user_id)
            board_list = Convergence_Board.objects.all().order_by('-Board_CreateDate')[(int(page_num)-1)*3:int(page_num)*3]
            if ((user.rank == '1' or user.rank == '2') and user_pw == user.Convergence_PW):
                addSessions(request, user)
                return render(request, 'convergence/base.html', {
                    'user_info' : user,
                    'board' : board_list ,
                    })
            elif user_pw != user.Convergence_PW:
                return render_to_response('convergence/Error/Error.html', {
                    'alert_msg' : '비밀번호가 맞지 않습니다.',
                    'url' : '/'
                })
        except User.DoesNotExist:
            return render_to_response('convergence/Error/Error.html', {
                    'alert_msg' : '해당 아이디가 없습니다.',
                    'url' : '/'
                })
                #raise (Http404("해당 아이디가 없습니다."))
    else:
        return render(request, 'convergence/login/loginpage.html', {
            'user_info' : getInfo(request),
             })

# 로그아웃 클릭 시 + user_ip + 마지막 접속 시간
def logout(request, page_num=1):
    board_list = Convergence_Board.objects.all().order_by('-Board_CreateDate')[(int(page_num)-1)*3:int(page_num)*3]
    for item in list(request.session.keys()):
        del request.session[item]
       
    return render(request, 'convergence/base.html',{'board' : board_list })

#메인페이지
def main(request, page_num=1):
    board_list = Convergence_Board.objects.all().order_by('-Board_CreateDate')[(int(page_num)-1)*3:int(page_num)*3]

    if request.user_agent.is_pc:
        return render(request, 'convergence/base.html',{'board' : board_list ,})

    elif request.user_agent.is_mobile:
        return redirect('convergence:m_main')

#회원 가입 페이지 이동
def toSignUp(request):
    user = User.objects.all()
    return render(request, 'convergence/signup/SignUp.html', {'user_info':user})

#회원 가입
def SignUp(request):
    if request.method == "POST":
        #추가 수강 여부
        sub_class_check = request.POST['sub_usr_class']
        sub_class1 = ''
        sub_class2 = ''
        if sub_class_check == 'sub_usr_class_agree':
            if request.POST['select_sub_usr_class1'] == "선택":
                sub_class1 = '분류없음'
            else:
                sub_class1 = request.POST['select_sub_usr_class1']

            if request.POST['select_sub_usr_class2'] == "선택":
                sub_class2 = '분류없음'
            else:
                sub_class2 = request.POST['select_sub_usr_class2']
        else:
            sub_class1 = '분류없음'
            sub_class2 = '분류없음'

        array_classcode = [request.POST['usr_class'], sub_class1, sub_class2]
        try:
            array_classcode.remove('분류없음')
        except:
            pass
        
        try:
            array_classcode.remove('분류없음')
        except:
            pass

        usr_rank = "2"
        if request.POST['usr_grade'] == "6" or request.POST['usr_grade'] == "7":
            usr_rank = "1"
        User.objects.create(
        Convergence_ID = request.POST['convergence_id'],
        Convergence_PW = request.POST['convergence_pw'],
        Convergence_Name = request.POST['usr_name'],
        Convergence_Dept = request.POST['usr_major'],
        Convergence_grade = request.POST['usr_grade'],
        Convergence_PhoneNumber = request.POST['usr_phonenumber'],
        Convergence_ClassCode = json.dumps(array_classcode),
        rank = usr_rank
        )        
        messages.success(request, '회원가입이 완료되었습니다.')
        return render(request, 'convergence/base.html')

    return render(request, 'convergence/signup/SignUp.html')

#회원가입시 유저 id 중복 방지
def SignUp_idcheck(request):
    id_check = request.POST['idcheck']
    UserList = User.objects.filter(Convergence_ID=id_check)
    if not UserList:
        context = {  'msg' : 'Y',  }
    else:
        context = {  'msg' : 'N',  }

    return HttpResponse(json.dumps(context), content_type="application/json")

#회원 정보 수정 사용자 비밀번호 입력
def tousr_modify(request):
    if request.method == "POST":
        user = User.objects.get(Convergence_ID=request.session['convergence_id'])
        if user.Convergence_PW==request.POST['convergence_pw']:
            return redirect('convergence:usr_modify')
        else:
            messages.error(request, '비밀번호 오류')
            return redirect('convergence:main')
    else:
        return render(request,'convergence/mypage/mypagePW.html')

#회원 정보 수정
def usr_modify(request):
    if request.method == "POST":
        User.objects.filter(Convergence_ID=request.session['convergence_id']).update(
            Convergence_PW = request.POST['convergence_pw']
        )
        messages.success(request, '비밀번호 변경 완료')
        return redirect('convergence:main')
    else:
        return render(request,'convergence/mypage/usrmodify.html')


#-------------------------------------------------------------------------------------------
# 커뮤니티 메뉴 클릭 시
# 창업과 시장분석 실무
def board_menu1(request, page_num=1):
    #board_list = Convergence_Board.objects.all().order_by('-Board_CreateDate')[(int(page_num)-1)*10:int(page_num)*10]
    try:
        if request.session['convergence_id']:
            user = User.objects.get(Convergence_ID=request.session['convergence_id'])
            jsonDec = json.decoder.JSONDecoder()
            user_classcode = jsonDec.decode(user.Convergence_ClassCode)
            if '1' in user_classcode or user.rank == '1':
                board_list = Convergence_Board.objects.filter(Board_ClassCode='1').order_by('-Board_CreateDate')
                page = request.GET.get('page', 1)
                paginator = Paginator(board_list, 10)
                posts = paginator.page(page)
                post_count = posts.paginator.count
                type_num=1

                return render(request, 'convergence/board/board.html', {'board' : board_list ,'posts':posts,'post_count':post_count, 'type_num':type_num, 'user_info' : getInfo(request)})
            else:
                messages.error(request, '수강하는 과목의 게시판이 아닙니다.')
                return redirect('convergence:main')
        else:
            messages.error(request, '로그인시 이용가능 합니다.')
            return redirect('convergence:main')
    except Exception as e:
        print(e)
        messages.error(request, '로그인시 이용가능 합니다.')
        return redirect('convergence:main')

# 호텔경제
def board_menu2(request, page_num=1):
    #board_list = Convergence_Board.objects.all().order_by('-Board_CreateDate')[(int(page_num)-1)*10:int(page_num)*10]
    try:
        if request.session['convergence_id']:
            user = User.objects.get(Convergence_ID=request.session['convergence_id'])
            jsonDec = json.decoder.JSONDecoder()
            user_classcode = jsonDec.decode(user.Convergence_ClassCode)
            if '2' in user_classcode or user.rank == '1':
                board_list = Convergence_Board.objects.filter(Board_ClassCode='2').order_by('-Board_CreateDate')
                page = request.GET.get('page', 1)
                paginator = Paginator(board_list, 10)
                posts = paginator.page(page)
                post_count = posts.paginator.count
                type_num=2
        
                return render(request, 'convergence/board/board.html', {'board' : board_list ,'posts':posts,'post_count':post_count, 'type_num':type_num, 'user_info' : getInfo(request)})
            else:
                messages.error(request, '수강하는 과목의 게시판이 아닙니다.')
            return redirect('convergence:main')
        else:
            messages.error(request, '로그인시 이용가능 합니다.')
            return redirect('convergence:main')
    except:
        messages.error(request, '로그인시 이용가능 합니다.')
        return redirect('convergence:main')

# 셀프 브랜드 디자인
def board_menu3(request, page_num=1):
    #board_list = Convergence_Board.objects.all().order_by('-Board_CreateDate')[(int(page_num)-1)*10:int(page_num)*10]
    try:
        if request.session['convergence_id']:
            user = User.objects.get(Convergence_ID=request.session['convergence_id'])
            jsonDec = json.decoder.JSONDecoder()
            user_classcode = jsonDec.decode(user.Convergence_ClassCode)
            if '3' in user_classcode or user.rank == '1':
                board_list = Convergence_Board.objects.filter(Board_ClassCode='3').order_by('-Board_CreateDate')
                page = request.GET.get('page', 1)
                paginator = Paginator(board_list, 10)
                posts = paginator.page(page)
                post_count = posts.paginator.count
                type_num=3

                return render(request, 'convergence/board/board.html', {'board' : board_list ,'posts':posts,'post_count':post_count, 'type_num':type_num, 'user_info' : getInfo(request)})
            else:
                messages.error(request, '수강하는 과목의 게시판이 아닙니다.')
                return redirect('convergence:main')
        else:
            messages.error(request, '로그인시 이용가능 합니다.')
            return redirect('convergence:main')
    except:
        messages.error(request, '로그인시 이용가능 합니다.')
        return redirect('convergence:main')

# 디자인기반 소프트웨어 시스템 구현과 지식재산
def board_menu4(request, page_num=1):
    #board_list = Convergence_Board.objects.all().order_by('-Board_CreateDate')[(int(page_num)-1)*10:int(page_num)*10]
    try:
        if request.session['convergence_id']:
            user = User.objects.get(Convergence_ID=request.session['convergence_id'])
            jsonDec = json.decoder.JSONDecoder()
            user_classcode = jsonDec.decode(user.Convergence_ClassCode)
            if '4' in user_classcode or user.rank == '1':
                board_list = Convergence_Board.objects.filter(Board_ClassCode='4').order_by('-Board_CreateDate')
                page = request.GET.get('page', 1)
                paginator = Paginator(board_list, 10)
                posts = paginator.page(page)
                post_count = posts.paginator.count
                type_num=4

                return render(request, 'convergence/board/board.html', {'board' : board_list ,'posts':posts,'post_count':post_count, 'type_num':type_num, 'user_info' : getInfo(request)})
            else:
                messages.error(request, '수강하는 과목의 게시판이 아닙니다.')
                return redirect('convergence:main')
        else:
            messages.error(request, '로그인시 이용가능 합니다.')
            return redirect('convergence:main')
    except:
        messages.error(request, '로그인시 이용가능 합니다.')
        return redirect('convergence:main')

# 파이썬 기반 텍스트 정보분석 심화
def board_menu5(request, page_num=1):
    #board_list = Convergence_Board.objects.all().order_by('-Board_CreateDate')[(int(page_num)-1)*10:int(page_num)*10]
    try:
        if request.session['convergence_id']:
            user = User.objects.get(Convergence_ID=request.session['convergence_id'])
            jsonDec = json.decoder.JSONDecoder()
            user_classcode = jsonDec.decode(user.Convergence_ClassCode)
            if '5' in user_classcode or user.rank == '1':
                board_list = Convergence_Board.objects.filter(Board_ClassCode='5').order_by('-Board_CreateDate')
                page = request.GET.get('page', 1)
                paginator = Paginator(board_list, 10)
                posts = paginator.page(page)
                post_count = posts.paginator.count
                type_num=5

                return render(request, 'convergence/board/board.html', {'board' : board_list ,'posts':posts,'post_count':post_count, 'type_num':type_num, 'user_info' : getInfo(request)})
            else:
                messages.error(request, '수강하는 과목의 게시판이 아닙니다.')
                return redirect('convergence:main')
        else:
            messages.error(request, '로그인시 이용가능 합니다.')
            return redirect('convergence:main')
    except:
        messages.error(request, '로그인시 이용가능 합니다.')
        return redirect('convergence:main')

# 융합모빌리티 종합 설계
def board_menu6(request, page_num=1):
    #board_list = Convergence_Board.objects.all().order_by('-Board_CreateDate')[(int(page_num)-1)*10:int(page_num)*10]
    try:
        if request.session['convergence_id']:
            user = User.objects.get(Convergence_ID=request.session['convergence_id'])
            jsonDec = json.decoder.JSONDecoder()
            user_classcode = jsonDec.decode(user.Convergence_ClassCode)
            if '6' in user_classcode or user.rank == '1':
                board_list = Convergence_Board.objects.filter(Board_ClassCode='6').order_by('-Board_CreateDate')
                page = request.GET.get('page', 1)
                paginator = Paginator(board_list, 10)
                posts = paginator.page(page)
                post_count = posts.paginator.count
                type_num=6

                return render(request, 'convergence/board/board.html', {'board' : board_list ,'posts':posts,'post_count':post_count, 'type_num':type_num, 'user_info' : getInfo(request)})
            else:
                messages.error(request, '수강하는 과목의 게시판이 아닙니다.')
                return redirect('convergence:main')
        else:
            messages.error(request, '로그인시 이용가능 합니다.')
            return redirect('convergence:main')
    except:
        messages.error(request, '로그인시 이용가능 합니다.')
        return redirect('convergence:main')

# 화재시 안전 대피를 위한 생체모방기술
# def board_menu7(request, page_num=1):
#     #board_list = Convergence_Board.objects.all().order_by('-Board_CreateDate')[(int(page_num)-1)*10:int(page_num)*10]
#     try:
#         if request.session['convergence_id']:
#             user = User.objects.get(Convergence_ID=request.session['convergence_id'])
#             jsonDec = json.decoder.JSONDecoder()
#             user_classcode = jsonDec.decode(user.Convergence_ClassCode)
#             if '7' in user_classcode or user.rank == '1':
#                 board_list = Convergence_Board.objects.filter(Board_ClassCode='7').order_by('-Board_CreateDate')
#                 page = request.GET.get('page', 1)
#                 paginator = Paginator(board_list, 10)
#                 posts = paginator.page(page)
#                 post_count = posts.paginator.count
#                 type_num=7

#                 return render(request, 'convergence/board/board.html', {'board' : board_list ,'posts':posts,'post_count':post_count, 'type_num':type_num, 'user_info' : getInfo(request)})
#             else:
#                 messages.error(request, '수강하는 과목의 게시판이 아닙니다.')
#                 return redirect('convergence:main')
#         else:
#             messages.error(request, '로그인시 이용가능 합니다.')
#             return redirect('convergence:main')
#     except:
#         messages.error(request, '로그인시 이용가능 합니다.')
#         return redirect('convergence:main')

# # V.Company
# def board_menu8(request, page_num=1):
#     #board_list = Convergence_Board.objects.all().order_by('-Board_CreateDate')[(int(page_num)-1)*10:int(page_num)*10]
#     try:
#         if request.session['convergence_id']:
#             user = User.objects.get(Convergence_ID=request.session['convergence_id'])
#             jsonDec = json.decoder.JSONDecoder()
#             user_classcode = jsonDec.decode(user.Convergence_ClassCode)
#             if '8' in user_classcode or user.rank == '1':
#                 board_list = Convergence_Board.objects.filter(Board_ClassCode='8').order_by('-Board_CreateDate')
#                 page = request.GET.get('page', 1)
#                 paginator = Paginator(board_list, 10)
#                 posts = paginator.page(page)
#                 post_count = posts.paginator.count
#                 type_num=8

#                 return render(request, 'convergence/board/board.html', {'board' : board_list ,'posts':posts,'post_count':post_count, 'type_num':type_num, 'user_info' : getInfo(request)})
#             else:
#                 messages.error(request, '수강하는 과목의 게시판이 아닙니다.')
#                 return redirect('convergence:main')
#         else:
#             messages.error(request, '로그인시 이용가능 합니다.')
#             return redirect('convergence:main')
#     except:
#         messages.error(request, '로그인시 이용가능 합니다.')
#         return redirect('convergence:main')

# 강의 페이로드 관리
@csrf_exempt
def ajax_lecture_do(request):
    if request.is_ajax():
        payload = json.loads(request.body)
        learner = payload.get('learner')
        lecture = payload.get('lecture')
        start_time = payload.get('start_time')
        played_time = payload.get('played_time')
        duration = payload.get('duration')

        try:
            ls = Lecture_Status.objects.get(
                            ls_learner__Convergence_ID=learner,
                            ls_lecture__l_board__pk=lecture)
                
            ls.ls_learning_time = played_time

            if duration <= played_time:
                ls.ls_isFinished = True
                ls.ls_finished_at = timezone.now()
                
            ls.save()
        except Exception as e: 
            print(e)



        print(payload)

    return HttpResponse({}, status=200) 

def create_lecture(board, prof):
    if board and prof:
        try:
            lecture = Lecture.objects.create(
                                        l_board = board,
                                        l_prof = prof,
                                        # l_start_at =
                                        # l_end_at =
                                    )
            learners = User.objects.filter(Convergence_ClassCode__icontains=board.Board_ClassCode).exclude(Q(Convergence_grade='6')|Q(Convergence_grade='7'))
            print(learners)
            print('hhi')
            if learners:
                for l in learners:
                    try:
                        Lecture_Status.objects.create(
                                            ls_learner=l,
                                            ls_lecture=lecture,
                                        )
                    except:
                        pass
        except Exception as e:
            print(e)

# 수강생 관리 메인
def learner_manage(request):
    prof = User.objects.get(Convergence_ID=request.session.get('convergence_id'))
    if prof.Convergence_grade != '6':
        messages.success(request, '접근 권한이 없습니다.')
        return redirect('/convergence')
    lectures = Lecture.objects.filter(l_prof=prof)
    return render(request, 'convergence/lecture/learner_manage.html', {
        'lectures' : lectures,
        'prof' : prof,
    })

# 수강생 관리
def learner_manage_detail(request, pk):
    prof = User.objects.get(Convergence_ID=request.session.get('convergence_id'))
    if prof.Convergence_grade != '6':
        messages.success(request, '접근 권한이 없습니다.')
        return redirect('/convergence')
    lecture = Lecture.objects.get(pk=pk)
    lectures = Lecture.objects.filter(l_prof=prof)
    lecture_status = lecture.lecture_status_set.all()
    return render(request, 'convergence/lecture/detail.html', {
        'prof' : prof,
        'lectures' : lectures,
        'lecture' : lecture,
        'lecture_status' : lecture_status
    })

# 게시글 작성 시
def write_board(request):
    if request.method == 'POST': # method가 POST 방식이라면 글이 써진 것
        '''
            JY  
        '''
        
        cb_isLecture = True if request.POST.get('is_lecture', '1') == '2' else False

        convergence_obj = Convergence_Board.objects.create(
            Board_Title = request.POST['Board_Title'],
            Board_Content = request.POST['Board_Content'],
            Board_CreateDate = timezone.now(),
            Board_ClassCode = request.POST['board_classcode'],
            Board_User = User.objects.get(Convergence_ID=request.session['convergence_id']),
            cb_isLecture=cb_isLecture
        )

        if cb_isLecture:
            create_lecture(convergence_obj, User.objects.get(Convergence_ID=request.session['convergence_id']))

  
        
        for f in request.FILES.getlist('file'):
            f_name_first = (''.join(reversed(str(f))))
            f_name_second = f_name_first.split('.')[0]
            f_name_last = (''.join(reversed(f_name_second)))
            Convergence_Files.objects.create(
                Board_File = convergence_obj,
                Convergence_File=f,
                Convergence_extension = f_name_last
           )
           
        if request.POST['board_classcode'] == "1":
            return redirect('/convergence/board1/page/1')
        elif request.POST['board_classcode'] == "2":
            return redirect('/convergence/board2/page/1')
        elif request.POST['board_classcode'] == "3":
            return redirect('/convergence/board3/page/1')
        elif request.POST['board_classcode'] == "4":
            return redirect('/convergence/board4/page/1')
        elif request.POST['board_classcode'] == "5":
            return redirect('/convergence/board5/page/1')
        elif request.POST['board_classcode'] == "6":
            return redirect('/convergence/board6/page/1')

    return render(request, 'convergence/board/writeboard.html', {'user_info' : getInfo(request)})


# 커뮤니티 확인
def ViewBoard(request, board_num):
    board = Convergence_Board.objects.get(id=board_num)
    board_file = Convergence_Files.objects.filter(Board_File=board)

    if board.Board_ClassCode == '1':
        type_num=1
    elif board.Board_ClassCode == '2':
        type_num=2
    elif board.Board_ClassCode == '3':
        type_num=3
    elif board.Board_ClassCode == '4':
        type_num=4
    elif board.Board_ClassCode == '5':
        type_num=5
    elif board.Board_ClassCode == '6':
        type_num=6

    '''
        jy
    '''
    init_payloads = {}
    if board.cb_isLecture:
        ls = None
        user_id = request.session.get('convergence_id')
        try:
            lc = Lecture.objects.get(l_board=board)
            try:
                ls = Lecture_Status.objects.get(
                                ls_learner__Convergence_ID=user_id,
                                ls_lecture=lc)
            except:
                # 수업이 없는 경우 -> 기존에 추가되지 못한 사용자 -> 추가
                try:
                    user = User.objects.get(Convergence_ID=user_id)
                    print(user.Convergence_grade)
                    if user.Convergence_grade != '6' and user.Convergence_grade != '7':
                        ls = Lecture_Status.objects.create(
                                        ls_learner=User.objects.get(Convergence_ID=user_id),
                                        ls_lecture=lc,
                                    )
                except:
                    # 유저 없음
                    pass
            
            if ls:
                init_payloads['ls_learning_time'] = ls.ls_learning_time
            
            
        except Exception as e:
            print(e)



    comment = Convergence_Comment.objects.filter(comment_Board=board) #게시글에 해당하는 댓글
    reply = Convergence_Comment_reply.objects.filter(convergence_comment=comment) #게시글에 해당하는 대댓글
    board.Board_hits = board.Board_hits + 1
    board.save()
    #next_board = Convergence_Board.objects.filter(Board_ClassCode=str(type_num)).filter(id__gt=board_num).order_by('id')[:1]
    #previous_board = Convergence_Board.objects.filter(Board_ClassCode=str(type_num)).filter(id__lt=board_num).order_by('id')[:1]
    
    if request.method == 'POST':
        form = ComentForm(request.POST)
        if form.is_valid:
            board_ = form.save(commit=False)
            board_.Convergence_Board = board
            board_.Convergence_Comment = request.POST['comment']
            board_.save()
            if board.Board_ClassCode == '1':
                return redirect('/convergence/board1/page/1')
            elif board.Board_ClassCode == '2':
                return redirect('/convergence/board2/page/1')
            elif board.Board_ClassCode == '3':
                return redirect('/convergence/board3/page/1')
            elif board.Board_ClassCode == '4':
                return redirect('/convergence/board4/page/1')
            elif board.Board_ClassCode == '5':
                return redirect('/convergence/board5/page/1')
            elif board.Board_ClassCode == '6':
                return redirect('/convergence/board6/page/1')
    else:
        form = CommentForm()

    return render(request, "convergence/board/boardView.html", {'init_payloads' : json.dumps(init_payloads), 'board' : board, 'board_file':board_file, 'comment':comment,'reply':reply, 'type_num':type_num, 'user_info' : getInfo(request)})

# 커뮤니티 수정
def EditBoard(request, board_num):
    toboard = Convergence_Board.objects.get(id=board_num)
    board_file = Convergence_Files.objects.filter(Board_File=toboard)
    if toboard.Board_ClassCode == '1':
        type_num=1
    elif toboard.Board_ClassCode == '2':
        type_num=2
    elif toboard.Board_ClassCode == '3':
        type_num=3
    elif toboard.Board_ClassCode == '4':
        type_num=4
    elif toboard.Board_ClassCode == '5':
        type_num=5
    elif toboard.Board_ClassCode == '6':
        type_num=6

    if request.method == 'POST': 
        toboard.Board_Title = request.POST['Board_Title']
        toboard.Board_Content = request.POST['Board_content']
        toboard.Board_ClassCode = request.POST['board_classcode'] 
        toboard.save()
        for f in request.FILES.getlist('file'):
            Convergence_Files.objects.create(
                Board_File = toboard,
                Convergence_File=f
           )
        messages.success(request, '게시판 수정이 완료되었습니다.')
        return redirect('convergence:main') 

    return render(request, 'convergence/board/board_edit.html', {'board_file':board_file, 'user_info' : getInfo(request), 'board_num':board_num, 'toboard':toboard, 'type_num':type_num})

#게시판 수정시 파일 삭제
def Board_edit_file_delete(request):
    file_id = request.POST['file_id']
    Convergence_Files.objects.get(id=file_id).delete()

    return HttpResponse("success")

# 커뮤니티 삭제
@csrf_exempt
def DeleteBoard(request, board_num):
    board = Convergence_Board.objects.get(id=board_num)
    if request.method == 'POST':
        if board.Board_User.Convergence_PW == request.POST['convergence_pw']:
            Convergence_Board.objects.get(id=board_num).delete()
        else:
            messages.error(request, '비밀번호 오류')
            return redirect('/convergence/board/view/' + str(board_num))
    
    messages.success(request, '삭제가 완료되었습니다.')
    return redirect('convergence:main')

# 커뮤니티 내용, 제목 검색
def findBoard(request, type_num):
    find_kind = request.POST['board_find'] #제목인지 내용 인지 판별
    find_content = request.POST['board_content_find'] #유저가 입력한 텍스트
    #나중에 검색 기능 추가적으로 개발할 사항 : 단어 띄어쓰기 무시하고 검색 되는 기능 - 2019년 8월에 개발 1차 마무리 되고 할 예정
    if find_kind == "제목":
        if find_content == "":
            board = Convergence_Board.objects.all().order_by('-Board_CreateDate')
        else:
            board = Convergence_Board.objects.filter(Board_ClassCode=type_num).filter(Board_Title__icontains=find_content).order_by('-Board_CreateDate')
    else:
        if find_content == "":
            board = Convergence_Board.objects.all().order_by('-Board_CreateDate')
        else:
            board = Convergence_Board.objects.filter(Board_ClassCode=type_num).filter(Board_Content__icontains=find_content).order_by('-Board_CreateDate')

    page = request.GET.get('page', 1)
    paginator = Paginator(board, 10)
    posts = paginator.page(page)
    post_count = posts.paginator.count
    findtype_num = int(type_num)
    return render(request, 'convergence/board/board.html', {'board' : board ,'posts':posts,'post_count':post_count, 'type_num':findtype_num})

# 커뮤니티 정렬
def sortBoard(request, type_num):
    sort_board = request.POST['board_sort'] #정렬 종류
    sort_numeber = 0
    #나중에 검색 기능 추가적으로 개발할 사항 : 단어 띄어쓰기 무시하고 검색 되는 기능 - 2019년 8월에 개발 1차 마무리 되고 할 예정
    if sort_board == "최신순":
        board = Convergence_Board.objects.filter(Board_ClassCode=type_num).order_by('-Board_CreateDate')
    else:
        board = Convergence_Board.objects.filter(Board_ClassCode=type_num).order_by('Board_CreateDate')
        sort_numeber = 1
    
    page = request.GET.get('page', 1)
    paginator = Paginator(board, 10)
    posts = paginator.page(page)
    post_count = posts.paginator.count
    re_type_num = type_num
    return render(request, 'convergence/board/board.html', {'board' : board , 'sort_numeber':sort_numeber,'posts':posts,'post_count':post_count, 'type_num':re_type_num})

#커뮤니티 댓글 및 대댓글
#댓글 작성 
def comment_write(request, board_num):
    comment_wr = Convergence_Board.objects.get(id=board_num)
    if request.method == 'POST':
        user = User.objects.get(Convergence_ID = request.session['convergence_id'])
        Convergence_Comment.objects.create(
            comment_Board = comment_wr,
            comment_user = user,
            comment = request.POST.get('comment_content'),
        )
        return redirect('/convergence/board/view/'+str(board_num))
    return render('convergence/base.html', {'user_info' : getInfo(request)})
    
#댓글 삭제
def comment_remove(request, board_num):
    comment_re = Convergence_Comment.objects.get(id=board_num)
    comment_pk = comment_re.comment_Board.id
    comment_re.delete()
    return redirect('/convergence/board/view/'+str(comment_pk))


#댓글수정
def comment_edit(request, board_num):
    comment_ed = Convergence_Comment.objects.get(id=board_num)
    comment_pk = comment_ed.comment_Board.id
    comment_ed.comment = request.GET['content']
    comment_ed.save()
    return redirect('/convergence/board/view/'+ str(comment_pk))

#대댓글 달기^^7
def comment_reply(request, board_num):
    comment_re = Convergence_Comment.objects.get(id=board_num)
    comment_rr = Convergence_Comment_reply.objects.filter(convergence_comment=comment_re) #대댓글
    user = User.objects.get(Convergence_ID = request.session['convergence_id'])
    comment_rr=Convergence_Comment_reply.objects.create(
        convergence_comment = comment_re,
        comment_reply = request.GET['content'],
        reply_user = user
    )
    number = comment_rr.convergence_comment.comment_Board.id
    return redirect("/convergence/board/view/"+str(number))

#대댓글 수정
def comment_reply_edit(request, board_num):
    comment_red = Convergence_Comment_reply.objects.get(id=board_num)
    comment_red.comment_reply = request.GET['content']
    comment_red.save()
    number = comment_red.convergence_comment.comment_Board.id
    return redirect('/convergence/board/view/'+str(number))

#대댓글 삭제
def comment_reply_remove(request, board_num):
    comment_remo = Convergence_Comment_reply.objects.get(id=board_num)
    comment_remo.delete()
    number = comment_remo.convergence_comment.comment_Board.id
    return redirect('/convergence/board/view/'+str(number))
#댓글 종료
#인원 현황 조회
def usr_list_view1(request):
    if request.session['rank'] == '1':
        user_list = User.objects.filter(Convergence_ClassCode__icontains = '1').exclude(Q(Convergence_grade='6')|Q(Convergence_grade='7'))
        return render(request, 'convergence/usrlist/usr_class_list1.html', {'usr_list':user_list,})
    else:
        messages.error(request, '권한이 없습니다.')
        return redirect('convergence:main')

def usr_list_view2(request):
    if request.session['rank'] == '1':
        user_list = User.objects.filter(Convergence_ClassCode__icontains = '2').exclude(Q(Convergence_grade='6')|Q(Convergence_grade='7'))
            
        return render(request, 'convergence/usrlist/usr_class_list2.html', {'usr_list':user_list})
    else:
        messages.error(request, '권한이 없습니다.')
        return redirect('convergence:main')

def usr_list_view3(request):
    if request.session['rank'] == '1':
        user_list = User.objects.filter(Convergence_ClassCode__icontains = '3').exclude(Q(Convergence_grade='6')|Q(Convergence_grade='7'))

        return render(request, 'convergence/usrlist/usr_class_list3.html', {'usr_list':user_list})
    else:
        messages.error(request, '권한이 없습니다.')
        return redirect('convergence:main')

def usr_list_view4(request):
    if request.session['rank'] == '1':
        user_list = User.objects.filter(Convergence_ClassCode__icontains = '4').exclude(Q(Convergence_grade='6')|Q(Convergence_grade='7'))

        return render(request, 'convergence/usrlist/usr_class_list4.html', {'usr_list':user_list})
    else:
        messages.error(request, '권한이 없습니다.')
        return redirect('convergence:main')

def usr_list_view5(request):
    if request.session['rank'] == '1':
        user_list = User.objects.filter(Convergence_ClassCode__icontains = '5').exclude(Q(Convergence_grade='6')|Q(Convergence_grade='7'))

        return render(request, 'convergence/usrlist/usr_class_list5.html', {'usr_list':user_list})
    else:
        messages.error(request, '권한이 없습니다.')
        return redirect('convergence:main')

def usr_list_view6(request):
    if request.session['rank'] == '1':
        user_list = User.objects.filter(Convergence_ClassCode__icontains = '6').exclude(Q(Convergence_grade='6')|Q(Convergence_grade='7'))

        return render(request, 'convergence/usrlist/usr_class_list6.html', {'usr_list':user_list})
    else:
        messages.error(request, '권한이 없습니다.')
        return redirect('convergence:main')

#################################모바일########################################3
# def m_main(request):

#     return render(request, 'convergence/mobile/m_base.html',)

# def m_loginpage(request):
#     return render(request, 'convergence/mobile/m_login.html')

# def m_login(request):
#     if request.method == 'POST':
#         user_id = request.POST['convergence_id']
#         user_pw = request.POST['convergence_pw']
#         try:
#             user = User.objects.get(Convergence_ID=user_id)
#             if ((user.rank == '1' or user.rank == '2') and user_pw == user.Convergence_PW):
#                 addSessions(request, user)
#                 return render(request, 'convergence/mobile/m_base.html', {
#                     'user_info' : user,
#                     })
#             elif user_pw != user.Convergence_PW:
#                 return render_to_response('convergence/Error/Error.html', {
#                     'alert_msg' : '비밀번호가 맞지 않습니다.',
#                     'url' : '/'
#                 })
#         except User.DoesNotExist:
#             return render_to_response('convergence/Error/Error.html', {
#                     'alert_msg' : '해당 아이디가 없습니다.',
#                     'url' : '/'
#                 })
#                 #raise (Http404("해당 아이디가 없습니다."))
#     else:
#         return render(request, 'convergence/mobile/m_login.html', {
#             'user_info' : getInfo(request),
#              })


# def m_logout(request):
#     for item in list(request.session.keys()):
#         del request.session[item]

#     return render(request, 'convergence/mobile/m_base.html')

# def m_myPW(request):
#     if request.method == "POST":
#         user = User.objects.get(Convergence_ID=request.session['convergence_id'])
#         if user.Convergence_PW==request.POST['convergence_pw']:
#             return redirect('convergence:m_user_modify')
#         else:
#             messages.error(request, '비밀번호 오류')
#             return redirect('convergence:main')
#     else:
#         return render(request,'convergence/mobile/m_myPW.html')

# #회원 정보 수정
# def m_user_modify(request):
#     if request.method == "POST":
#         User.objects.filter(Convergence_ID=request.session['convergence_id']).update(
#             Convergence_PW = request.POST['convergence_pw']
#         )
#         messages.success(request, '비밀번호 변경 완료')
#         return redirect('convergence:m_main')
#     else:
#         return render(request,'convergence/mobile/m_modifyPW.html')

# #회원 가입 페이지 이동
# def m_toSignUp(request):
#     user = User.objects.all()
#     return render(request, 'convergence/mobile/m_signup.html', {'user_info':user})

# #회원 가입
# def m_SignUp(request):
#     if request.method == "POST":
#         #추가 수강 여부
#         sub_class_check = request.POST['sub_usr_class']
#         sub_class = ''
#         if sub_class_check == 'sub_usr_class_agree':
#             if request.POST['select_sub_usr_class'] == "선택":
#                 sub_class = '분류없음'
#             else:
#                 sub_class = request.POST['select_sub_usr_class']
#         else:
#             sub_class = '분류없음'


#         usr_rank = "2"
#         if request.POST['usr_grade'] == "6" or request.POST['usr_grade'] == "7":
#             usr_rank = "1"
#         User.objects.create(
#         Convergence_ID = request.POST['convergence_id'],
#         Convergence_PW = request.POST['convergence_pw'],
#         Convergence_Name = request.POST['usr_name'],
#         Convergence_Dept = request.POST['usr_major'],
#         Convergence_grade = request.POST['usr_grade'],
#         Convergence_PhoneNumber = request.POST['usr_phonenumber'],
#         Convergence_ClassCode = request.POST['usr_class'],
#         Convergence_SubClassCode = sub_class,
#         rank = usr_rank
#         )
#         messages.success(request, '회원가입이 완료되었습니다.')
#         return render(request, 'convergence/mobile/m_main.html')

#     return render(request, 'convergence/mobile/m_signup.html')

# def m_write_board(request):
#     if request.method == 'POST': # method가 POST 방식이라면 글이 써진 것
#         form = PostForm(request.POST, request.FILES) # 이때는 해당 데이터를 다시 폼으로 넘겨보린다.
#         # 그리고 나서 올바른 값들이 들어왔는지 확인해야 한다.
#         if form.is_valid():
#             Convergence_Board = form.save(commit=False) # commit=Flase는 넘겨진 데이터를 바로 저장하지 말라는 뜻.
#             Convergence_Board.Board_Title = request.POST['Board_Title']
#             Convergence_Board.Board_Content = request.POST.get('Board_Content')
#             Convergence_Board.Board_CreateDate = timezone.now()
#             Convergence_Board.Board_ClassCode = request.POST['board_classcode']
#             Convergence_Board.Board_User = User.objects.get(Convergence_ID=request.session['convergence_id'])
#             try:
#                 Convergence_Board.Board_Files = request.FILES['file_upload']
#             except:
#                 pass
#             Convergence_Board.save()
#             if request.POST['board_classcode'] == "1":
#                 return redirect('board1/1')
#             elif request.POST['board_classcode'] == "2":
#                 return redirect('board2/1')
#             elif request.POST['board_classcode'] == "3":
#                 return redirect('board3/1')
#             elif request.POST['board_classcode'] == "4":
#                 return redirect('board4/1')
#     else:
#         form = PostForm()

#     return render(request, 'convergence/mobile/m_writeboard.html', {'form' : form, 'user_info' : getInfo(request)})


# def m_board_1(request, page_num):
#     #board_list = Convergence_Board.objects.all().order_by('-Board_CreateDate')[(int(page_num)-1)*10:int(page_num)*10]
#     try:
#         if request.session['convergence_id']:
#             user = User.objects.get(Convergence_ID=request.session['convergence_id'])
#             if user.Convergence_ClassCode == '1' or user.rank == '1' or user.Convergence_SubClassCode == '1':
#                 board_list = Convergence_Board.objects.filter(Board_ClassCode='1').order_by('-Board_CreateDate')
#                 page = request.GET.get('page', 1)
#                 paginator = Paginator(board_list, 5)
#                 posts = paginator.page(page)
#                 post_count = posts.paginator.count
#                 type_num=1
#                 return render(request, 'convergence/mobile/m_board.html', {'board' : board_list ,'posts':posts,'post_count':post_count, 'type_num':type_num, 'user_info' : getInfo(request)})
#             else:
#                 messages.error(request, '수강하는 과목의 게시판이 아닙니다.')
#                 return redirect('convergence:m_main')
#         else:
#             messages.error(request, '로그인시 이용가능 합니다.')
#             return redirect('convergence:m_main')
#     except:
#         messages.error(request, '로그인시 이용가능 합니다.')
#         return redirect('convergence:m_main')


# def m_board_2(request, page_num):
#     #board_list = Convergence_Board.objects.all().order_by('-Board_CreateDate')[(int(page_num)-1)*10:int(page_num)*10]
#     try:
#         if request.session['convergence_id']:
#             user = User.objects.get(Convergence_ID=request.session['convergence_id'])
#             if user.Convergence_ClassCode == '2' or user.rank == '1' or user.Convergence_SubClassCode == '2':
#                 board_list = Convergence_Board.objects.filter(Board_ClassCode='2').order_by('-Board_CreateDate')
#                 page = request.GET.get('page', 1)
#                 paginator = Paginator(board_list, 5)
#                 posts = paginator.page(page)
#                 post_count = posts.paginator.count
#                 type_num=2
#                 return render(request, 'convergence/mobile/m_board.html', {'board' : board_list ,'posts':posts,'post_count':post_count, 'type_num':type_num, 'user_info' : getInfo(request)})
#             else:
#                 messages.error(request, '수강하는 과목의 게시판이 아닙니다.')
#                 return redirect('convergence:m_main')
#         else:
#             messages.error(request, '로그인시 이용가능 합니다.')
#             return redirect('convergence:m_main')
#     except:
#         messages.error(request, '로그인시 이용가능 합니다.')
#         return redirect('convergence:m_main')


# def m_board_3(request, page_num):
#     #board_list = Convergence_Board.objects.all().order_by('-Board_CreateDate')[(int(page_num)-1)*10:int(page_num)*10]
#     try:
#         if request.session['convergence_id']:
#             user = User.objects.get(Convergence_ID=request.session['convergence_id'])
#             if user.Convergence_ClassCode == '3' or user.rank == '1' or user.Convergence_SubClassCode == '3':
#                 board_list = Convergence_Board.objects.filter(Board_ClassCode='3').order_by('-Board_CreateDate')
#                 page = request.GET.get('page', 1)
#                 paginator = Paginator(board_list, 5)
#                 posts = paginator.page(page)
#                 post_count = posts.paginator.count
#                 type_num=3
#                 return render(request, 'convergence/mobile/m_board.html', {'board' : board_list ,'posts':posts,'post_count':post_count, 'type_num':type_num, 'user_info' : getInfo(request)})
#             else:
#                 messages.error(request, '수강하는 과목의 게시판이 아닙니다.')
#                 return redirect('convergence:m_main')
#         else:
#             messages.error(request, '로그인시 이용가능 합니다.')
#             return redirect('convergence:m_main')
#     except:
#         messages.error(request, '로그인시 이용가능 합니다.')
#         return redirect('convergence:m_main')


# def m_board_4(request, page_num):
#     #board_list = Convergence_Board.objects.all().order_by('-Board_CreateDate')[(int(page_num)-1)*10:int(page_num)*10]
#     try:
#         if request.session['convergence_id']:
#             user = User.objects.get(Convergence_ID=request.session['convergence_id'])
#             if user.Convergence_ClassCode == '4' or user.rank == '1' or user.Convergence_SubClassCode == '4':
#                 board_list = Convergence_Board.objects.filter(Board_ClassCode='4').order_by('-Board_CreateDate')
#                 page = request.GET.get('page', 1)
#                 paginator = Paginator(board_list, 5)
#                 posts = paginator.page(page)
#                 post_count = posts.paginator.count
#                 type_num=4
#                 return render(request, 'convergence/mobile/m_board.html', {'board' : board_list ,'posts':posts,'post_count':post_count, 'type_num':type_num, 'user_info' : getInfo(request)})
#             else:
#                 messages.error(request, '수강하는 과목의 게시판이 아닙니다.')
#                 return redirect('convergence:m_main')
#         else:
#             messages.error(request, '로그인시 이용가능 합니다.')
#             return redirect('convergence:m_main')
#     except:
#         messages.error(request, '로그인시 이용가능 합니다.')
#         return redirect('convergence:m_main')

# def m_findBoard(request, type_num):
#     find_kind = request.POST['board_find'] #제목인지 내용 인지 판별
#     find_content = request.POST['board_content_find'] #유저가 입력한 텍스트
#     #나중에 검색 기능 추가적으로 개발할 사항 : 단어 띄어쓰기 무시하고 검색 되는 기능 - 2019년 8월에 개발 1차 마무리 되고 할 예정
#     if find_kind == "제목":
#         if find_content == "":
#             board = Convergence_Board.objects.all().order_by('-Board_CreateDate')
#         else:
#             board = Convergence_Board.objects.filter(Board_ClassCode=type_num).filter(Board_Title__icontains=find_content).order_by('-Board_CreateDate')
#     else:
#         if find_content == "":
#             board = Convergence_Board.objects.all().order_by('-Board_CreateDate')
#         else:
#             board = Convergence_Board.objects.filter(Board_ClassCode=type_num).filter(Board_Content__icontains=find_content).order_by('-Board_CreateDate')

#     page = request.GET.get('page', 1)
#     paginator = Paginator(board, 10)
#     posts = paginator.page(page)
#     post_count = posts.paginator.count
#     findtype_num = int(type_num)
#     return render(request, 'convergence/mobile/m_board.html', {'board' : board ,'posts':posts,'post_count':post_count, 'type_num':findtype_num})



# def m_ViewBoard(request, board_num):
#     board = Convergence_Board.objects.get(id=board_num)
#     if board.Board_ClassCode == '1':
#         type_num=1
#     elif board.Board_ClassCode == '2':
#         type_num=2
#     elif board.Board_ClassCode == '3':
#         type_num=3
#     else:
#         type_num=4
#     comment = Convergence_Comment.objects.filter(comment_Board=board) #게시글에 해당하는 댓글
#     reply = Convergence_Comment_reply.objects.filter(convergence_comment=comment) #게시글에 해당하는 대댓글
#     board.Board_hits = board.Board_hits + 1
#     board.save()
#     next_board = Convergence_Board.objects.filter(id__gt=board_num).order_by('id')[:1]
#     previous_board = Convergence_Board.objects.filter(id__lt=board_num).order_by('id')[:1]

#     if request.method == 'POST':
#         form = ComentForm(request.POST)
#         if form.is_valid:
#             board_ = form.save(commit=False)
#             board_.Convergence_Board = board
#             board_.Convergence_Comment = request.POST['comment']
#             board_.save()
#             return redirect('/board/post/' + str(board_num))
#     else:
#         form = CommentForm()

#     return render(request, "convergence/mobile/m_boardView.html", {'board' : board, 'previous_board':previous_board, 'next_board':next_board,'comment':comment,'reply':reply, 'type_num':type_num, 'user_info' : getInfo(request)})

# def m_EditBoard(request, board_num):
#     toboard = Convergence_Board.objects.get(id=board_num)
#     if toboard.Board_ClassCode == '1':
#         type_num=1
#     elif toboard.Board_ClassCode == '2':
#         type_num=2
#     elif toboard.Board_ClassCode == '4':
#         type_num=3
#     else:
#         type_num=4
#     if request.method == 'POST':
#         toboard.Board_Title = request.POST['Board_Title']
#         toboard.Board_Content = request.POST.get('Board_Content')
#         toboard.Board_ClassCode = request.POST['board_classcode']
#         try:
#             toboard.Board_Files = request.FILES['file_upload']
#         except:
#             pass
#         toboard.save()
#         messages.success(request, '게시판 수정이 완료되었습니다.')
#         return redirect('convergence:m_main')
#     else:
#         form = PostForm(initial={'Board_Files':toboard.Board_Files })

#     return render(request, 'convergence/mobile/m_board_edit.html', {'form' : form, 'user_info' : getInfo(request), 'board_num':board_num,
#                     'toboard':toboard, 'type_num':type_num})

# # 커뮤니티 삭제
# @csrf_exempt
# def m_DeleteBoard(request, board_num):
#     board = Convergence_Board.objects.get(id=board_num)
#     if request.method == 'POST':
#         if board.Board_User.Convergence_PW == request.POST['convergence_pw']:
#             Convergence_Board.objects.get(id=board_num).delete()
#         else:
#             messages.error(request, '비밀번호 오류')
#             return redirect('/board/view/' + str(board_num))

#     messages.success(request, '삭제가 완료되었습니다.')
#     return redirect('convergence:m_main')

#user_list excel export

def export_users_list(request, list_num):
    print(list_num)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0
    col_num_ = 1
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['번호','과목', '학번', '학년/직책', '학과', '이름']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    ws.col(1).width = int(35*260)
    ws.col(2).width = int(18*260)
    ws.col(4).width = int(18*260)
    rows_class = User.objects.filter(Convergence_ClassCode__icontains = list_num).exclude(Q(Convergence_grade='6')|Q(Convergence_grade='7'))
    for row in rows_class:
        print(row)
        row_num += 1
        class_code = [str(col_num_), str(row.getStringofClassCode(row, list_num)), str(row.Convergence_ID), str(row.getStringofGrade(row)), str(row.Convergence_Dept), str(row.Convergence_Name)]
        ws.write(row_num, 0, class_code[0], font_style)
        ws.write(row_num, 1, class_code[1], font_style)
        ws.write(row_num, 2, class_code[2], font_style)
        ws.write(row_num, 3, class_code[3], font_style)
        ws.write(row_num, 4, class_code[4], font_style)
        ws.write(row_num, 5, class_code[5], font_style)
        col_num_ += 1

    wb.save(response)
    return response

