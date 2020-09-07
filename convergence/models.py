from django.db import models
import simplejson as json

class User(models.Model):
    class meta:
        db_table = '사용자 속성'
    Convergence_ID = models.CharField(max_length=20, null=True, blank=False)
    Convergence_PW = models.CharField(max_length=20, null=True, blank=False)
    Convergence_Name = models.CharField(max_length=20, null=True, blank=False)
    Convergence_Dept = models.CharField(max_length=20, null=True, blank=False)
    Convergence_ClassCode = models.TextField(null=True)
    Convergence_grade = models.CharField(max_length=2, null=True, blank=False)
    Convergence_PhoneNumber = models.CharField(max_length=20, null=True, blank=False)
    rank_list = (('1', '시스템관리자'),('2', '사용자'))
    rank = models.CharField(max_length=10, choices=rank_list, default='2', null=True, blank=False)
    
    # xls 추출 시 해당 랭크·직업의 숫자 값이 아닌 한글 값
    @staticmethod
    def getStringofGrade(self):
        if self.Convergence_grade == "6":
            return '교수'
        elif self.Convergence_grade == "7":
            return '직원'
        return self.Convergence_grade + '학년'
    @staticmethod
    def getStringofClassCode(self, num):
        jsonDec = json.decoder.JSONDecoder()
        usr_classcode = jsonDec.decode(self.Convergence_ClassCode)
        if '' in usr_classcode:
            return '-'
        elif '1' in usr_classcode and  '1' == str(num):
            return '창업과 시장분석 실무'
        elif '2' in usr_classcode and  '2' == str(num):
            return '호텔경제'
        elif '3' in usr_classcode and  '3' == str(num):
            return '셀프 브랜드 디자인'
        elif '4' in usr_classcode and  '4' == str(num):
            return '디자인기반 소프트웨어 시스템 구현과 지식재산'
        elif '5' in usr_classcode and  '5' == str(num):
            return '파이썬 기반 텍스트 정보 분석 심화'
        elif '6' in usr_classcode and  '6' == str(num):
            return '융합모빌리티 종합설계'
        # elif '7' in usr_classcode and  '7' == str(num):
        #     return '화재시 안전 대피를 위한 생체모방기술'
        # elif '8' in usr_classcode and  '8' == str(num):
        #     return 'V.Company'

#커뮤니티
class Convergence_Board(models.Model):
    class meta:
        db_table = '커뮤니티'
    Board_User = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=False)
    Board_Title = models.CharField(max_length=150, null=True, blank=False)
    Board_Content = models.TextField()
    Board_CreateDate = models.DateTimeField(null=True, blank=False)
    Board_ClassificationList = (('1', '창업과 시장분석 실무'), ('2','호텔경제'), ('3','셀프 브랜드 디자인'), ('4','디자인기반 소프트웨어 시스템 구현과 지식재산'), ('5','파이썬 기반 텍스트 정보 분석 심화'), ('6','융합모빌리티 종합설계')) #게시글 분류 코드
    Board_ClassCode = models.CharField(max_length=10, choices=Board_ClassificationList, default='분류없음', null=True, blank=True)
    Board_hits= models.PositiveIntegerField(default=0)

    # 강의 여부
    cb_isLecture = models.BooleanField(default=False)

# 강의 
class Lecture(models.Model):
    l_board = models.OneToOneField(Convergence_Board, on_delete=models.CASCADE)
    l_prof = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    l_start_at = models.DateTimeField(null=True, blank=True)
    l_end_at = models.DateTimeField(null=True, blank=True)

# 수강 여부
class Lecture_Status(models.Model):
    ls_learner = models.ForeignKey(User, on_delete=models.CASCADE)
    ls_lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    ls_learning_time = models.IntegerField(default=0)
    ls_start_at = models.DateTimeField(null=True, blank=True)
    ls_isFinished = models.BooleanField(default=False)
    ls_finished_at = models.DateTimeField(null=True, blank=True)
    ls_checkpoint = models.IntegerField(default=0)


#파일
class Convergence_Files(models.Model):
    Board_File = models.ForeignKey(Convergence_Board, on_delete=models.CASCADE, default="")
    Convergence_File = models.FileField(null=True, blank=True)
    Convergence_extension = models.CharField(null=True, blank=True, max_length=10)


#게시판 댓글
class Convergence_Comment(models.Model):
    class meta:
        db_table = '댓글'
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    comment = models.CharField(max_length=150, null=True, blank=True)
    recommend = models.IntegerField(default=0)
    comment_Board = models.ForeignKey(Convergence_Board, on_delete=models.CASCADE, default="", related_name ='comment')
    
    @staticmethod
    def getCommentAboutArticle(board_num):
        return comment.objects.filter(Convergence_Board__id=board_num)

#게시판 댓글에 댓글
class Convergence_Comment_reply(models.Model):
    class meta:
        db_table = '대댓글'
    convergence_comment = models.ForeignKey(Convergence_Comment, on_delete=models.CASCADE, null=True, blank=False)
    comment_reply = models.CharField(max_length=150, null=True, blank=True, verbose_name='대댓글')
    reply_user = models.ForeignKey(User,on_delete=models.CASCADE, default="")
    reply_recommend = models.IntegerField(default=0)
    reply_createdate = models.DateTimeField(null=True, blank=False,auto_now_add=True)
    def __str__(self):
        return self.comment_reply
