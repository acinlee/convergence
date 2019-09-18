from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls import(handler400, handler403, handler404, handler500)
from django.conf.urls.static import static

app_name = 'convergence'

handler400 = 'convergence.views.bad_request'
handler403 = 'convergence.views.permission_denied'
handler404 = 'convergence.views.page_not_found'
handler500 = 'convergence.views.server_error'

urlpatterns = [
    path('Convergence/', views.main, name='main'),
    path('Convergence/loginpage', views.loginpage, name='loginpage'),
    path('Convergence/Login', views.login, name='login'),
    path('Convergence/Loginout', views.logout, name='logout'),
    path('Convergence/toSignUp', views.toSignUp, name='toSignUp'),
    path('Convergence/SignUp', views.SignUp, name='signup'),
    path("Convergence/tousrmodify", views.tousr_modify, name='tousr_modify'),
    path("Convergence/usrmodify", views.usr_modify, name='usr_modify'),
    
    #게시판(커뮤니티)
    path('board1/page/<page_num>', views.board_menu1, name='board_menu1'),
    path('board2/page/<page_num>', views.board_menu2, name='board_menu2'),
    path('board3/page/<page_num>', views.board_menu3, name='board_menu3'),
    path('board4/page/<page_num>', views.board_menu4, name='board_menu4'),
    path("Convergence/Writeboard", views.write_board, name="write_board"),
    path('board/view/<board_num>', views.ViewBoard, name='viewBoard'),
    path('board/edit/<board_num>/', views.EditBoard, name='editBoard'),
    path("Convergence/FindBoard/<type_num>", views.findBoard, name="findBoard"), #커뮤니티 검색 기능
    path("Convergence/SortBoard/<type_num>", views.sortBoard, name="sortBoard"), #커뮤니티 정렬 기능
    path("board/delete/<board_num>/", views.DeleteBoard, name="DeleteBoard"),#커뮤니티 삭제

    #커뮤니티 댓글, 대댓글
    path('Convergence/comment_write/<board_num>/',views.comment_write,name='comment_write'),#댓글 쓰기
    path('Convergence/comment_edit/<str:board_num>/',views.comment_edit,name='comment_edit'),#댓글 수정
    path('Convergence/comment_remove/<str:board_num>/',views.comment_remove,name='comment_remove'),#댓글 삭제
    path('Convergence/comment_reply/<board_num>/',views.comment_reply,name='comment_reply'), #대댓글 쓰기
    path('Convergence/comment_reply_edit/<str:board_num>',views.comment_reply_edit,name='comment_reply_edit'),#대댓글 수정
    path('Convergence/comment_reply_remove/<board_num>',views.comment_reply_remove,name='comment_reply_remove'),#대댓글 삭제

    #가입자 확인
    path('Convergence/usr_list1/',views.usr_list_view1,name='usr_list_view1'),
    path('Convergence/usr_list2/',views.usr_list_view2,name='usr_list_view2'),
    path('Convergence/usr_list3/',views.usr_list_view3,name='usr_list_view3'),
    path('Convergence/usr_list4/',views.usr_list_view4,name='usr_list_view4'),

    #ajax
    path('SignUp_idcheck', views.SignUp_idcheck, name='SignUp_idcheck'), #user id 중복 확인
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)