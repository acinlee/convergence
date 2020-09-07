from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls import(handler400, handler403, handler404, handler500)
from django.conf.urls.static import static

app_name = 'convergence'

# handler400 = 'convergence.views.bad_request'
# handler403 = 'convergence.views.permission_denied'
# handler404 = 'convergence.views.page_not_found'
# handler500 = 'convergence.views.server_error'

urlpatterns = [
    path('', views.main, name='main'),
    path('loginpage', views.loginpage, name='loginpage'),
    path('Login', views.login, name='login'),
    path('Loginout', views.logout, name='logout'),
    path('toSignUp', views.toSignUp, name='toSignUp'),
    path('SignUp', views.SignUp, name='signup'),
    path("tousrmodify", views.tousr_modify, name='tousr_modify'),
    path("usrmodify", views.usr_modify, name='usr_modify'),
    
    #게시판(커뮤니티)
    path('board1/page/<page_num>', views.board_menu1, name='board_menu1'),
    path('board2/page/<page_num>', views.board_menu2, name='board_menu2'),
    path('board3/page/<page_num>', views.board_menu3, name='board_menu3'),
    path('board4/page/<page_num>', views.board_menu4, name='board_menu4'),
    path('board5/page/<page_num>', views.board_menu5, name='board_menu5'),
    path('board6/page/<page_num>', views.board_menu6, name='board_menu6'),
    path("Writeboard", views.write_board, name="write_board"),
    path('board/view/<board_num>', views.ViewBoard, name='viewBoard'),
    path('board/edit/<board_num>/', views.EditBoard, name='editBoard'),
    path("FindBoard/<type_num>", views.findBoard, name="findBoard"), #커뮤니티 검색 기능
    path("SortBoard/<type_num>", views.sortBoard, name="sortBoard"), #커뮤니티 정렬 기능
    path("board/delete/<board_num>/", views.DeleteBoard, name="DeleteBoard"),#커뮤니티 삭제

    #커뮤니티 댓글, 대댓글
    path('comment_write/<board_num>/',views.comment_write,name='comment_write'),#댓글 쓰기
    path('comment_edit/<str:board_num>/',views.comment_edit,name='comment_edit'),#댓글 수정
    path('comment_remove/<str:board_num>/',views.comment_remove,name='comment_remove'),#댓글 삭제
    path('comment_reply/<board_num>/',views.comment_reply,name='comment_reply'), #대댓글 쓰기
    path('comment_reply_edit/<str:board_num>',views.comment_reply_edit,name='comment_reply_edit'),#대댓글 수정
    path('comment_reply_remove/<board_num>',views.comment_reply_remove,name='comment_reply_remove'),#대댓글 삭제
    
    #가입자 확인
    path('usr_list1/',views.usr_list_view1,name='usr_list_view1'),
    path('usr_list2/',views.usr_list_view2,name='usr_list_view2'),
    path('usr_list3/',views.usr_list_view3,name='usr_list_view3'),
    path('usr_list4/',views.usr_list_view4,name='usr_list_view4'),
    path('usr_list5/',views.usr_list_view5,name='usr_list_view5'),
    path('usr_list6/',views.usr_list_view6,name='usr_list_view6'),

    #export user list
    path('Convergence/export_users_list/<list_num>/', views.export_users_list, name='export_users_list'),


    #모바일
    # path('m/Convergence/', views.m_main, name='m_main'),
    # path('m/Convergence/board1/<page_num>', views.m_board_1, name='m_board1'),
    # path('m/Convergence/board2/<page_num>', views.m_board_2, name='m_board2'),
    # path('m/Convergence/board3/<page_num>', views.m_board_3, name='m_board3'),
    # path('m/Convergence/board4/<page_num>', views.m_board_4, name='m_board4'),
    # path('m/Convergence/Login', views.m_login, name='m_login'),
    # path('m/Convergence/LoginPage', views.m_loginpage, name='m_loginpage'),
    # path('m/Convergence/logout', views.m_logout, name='m_logout'),
    # path('m/Convergence/myPW', views.m_myPW, name='m_myPW'),
    # path('m/Convergence/user_modify', views.m_user_modify, name='m_user_modify'),
    # path('m/Convergence/toSignup', views.m_toSignUp, name='m_toSignUp'),
    # path('m/Convergence/SignUp', views.m_SignUp, name='m_SignUp'),
    # path('m/Convergence/boardView/<board_num>', views.m_ViewBoard, name='m_ViewBoard'),
    # path('m/Convergence/writeboard', views.m_write_board, name='m_write_board'),
    # path('m/Convergence/EditBoard/<board_num>', views.m_EditBoard, name='m_EditBoard'),
    # path('m/Convergence/deleteBoard/<board_num>',views.m_DeleteBoard, name='m_DeleteBoard'),
    # path('m/Convergence/FindBoard/<type_num>', views.m_findBoard, name='m_findBoard'),
    
    #ajax
    path('SignUp_idcheck', views.SignUp_idcheck, name='SignUp_idcheck'), #user id 중복 확인
    path('Board_edit_file_delete', views.Board_edit_file_delete, name='Board_edit_file_delete'), #게시판 수정시 파일 삭제

    # 강의 
    path('lecture/do', views.ajax_lecture_do),
    path('manage/student', views.learner_manage, name='lecture-manage'),
    path('manage/student/<pk>', views.learner_manage_detail, name='lecture-manage-detail')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
