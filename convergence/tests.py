from django.test import TestCase
from .models import *
import random
# Create your tests here.

'''
    JY
'''

class UserTestModels:
    @staticmethod
    def create():
        num = 1999
        for _ in range(50):
            User.objects.create(
                Convergence_ID = num,
                Convergence_PW = 'nf1yfa23',
                Convergence_Name = '안주{0}'.format(['영', '진', '홍', '상', '도', '혁', '현', '한', '훈', '연', '역'][random.randint(0, 10)]),
                Convergence_Dept = '컴퓨터 공학과',
                Convergence_ClassCode = '7',
                Convergence_PhoneNumber = '01024425148',
                Convergence_grade = '3',
                rank = '2'
            ) 
            num += 1

UserTestModels.create()