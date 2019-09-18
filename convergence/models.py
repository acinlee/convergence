from django.db import models

class User(models.Model):
    class meta:
        db_table = '사용자 속성'
    Convergence_ID = models.CharField(max_length=20, null=True, blank=False)
    Convergence_PW = models.CharField(max_length=20, null=True, blank=False)
    Convergence_Name = models.CharField(max_length=20, null=True, blank=False)
    Convergence_Dept = models.CharField(max_length=20, null=True, blank=False)
    Convergence_ClassificationList = (('1', '지식재산 디자인기반 소프트웨어'), ('2','정보처리와 소프트웨어 지식재산'), ('3','글로벌 엔터테인먼트'), ('4','개인 비행체 프로토타입 설계')) #게시글 분류 코드
    Convergence_ClassCode = models.CharField(max_length=10, choices=Convergence_ClassificationList, default='분류없음', null=True, blank=True)
    Convergence_SubClassCode = models.CharField(max_length=10, choices=Convergence_ClassificationList, default='분류없음', null=True, blank=True)
    Convergence_grade = models.CharField(max_length=2, null=True, blank=False)
    Convergence_PhoneNumber = models.CharField(max_length=20, null=True, blank=False)
    rank_list = (('1', '시스템관리자'),('2', '사용자'))
    rank = models.CharField(max_length=10, choices=rank_list, default='2', null=True, blank=False)

#커뮤니티
class Convergence_Board(models.Model):
    class meta:
        db_table = '커뮤니티'
    Board_User = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=False)
    Board_Title = models.CharField(max_length=150, null=True, blank=False)
    Board_Content = models.TextField()
    Board_CreateDate = models.DateTimeField(null=True, blank=False)
    Board_ClassificationList = (('1', '지식재산 디자인기반 소프트웨어'), ('2','정보처리와 소프트웨어 지식재산'), ('3','글로벌 엔터테인먼트'), ('4','개인 비행체 프로토타입 설계'),) #게시글 분류 코드
    Board_ClassCode = models.CharField(max_length=10, choices=Board_ClassificationList, default='분류없음', null=True, blank=True)
    Board_Files = models.FileField(null=True, blank=True)
    Board_hits= models.PositiveIntegerField(default=0)

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