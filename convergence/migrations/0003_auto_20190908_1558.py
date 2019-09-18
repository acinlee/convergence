# Generated by Django 2.1.7 on 2019-09-08 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convergence', '0002_user_convergence_classcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Convergence_SubClassCode',
            field=models.CharField(blank=True, choices=[('1', '지식재산 디자인기반 소프트웨어'), ('2', '정보처리와 소프트웨어 지식재산'), ('3', '글로벌 엔터테인먼트'), ('4', '개인 비행체 프로토타입 설계')], default='분류없음', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='convergence_board',
            name='Board_ClassCode',
            field=models.CharField(blank=True, choices=[('1', '지식재산 디자인기반 소프트웨어'), ('2', '정보처리와 소프트웨어 지식재산'), ('3', '글로벌 엔터테인먼트'), ('4', '개인 비행체 프로토타입 설계')], default='분류없음', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='Convergence_ClassCode',
            field=models.CharField(blank=True, choices=[('1', '지식재산 디자인기반 소프트웨어'), ('2', '정보처리와 소프트웨어 지식재산'), ('3', '글로벌 엔터테인먼트'), ('4', '개인 비행체 프로토타입 설계')], default='분류없음', max_length=10, null=True),
        ),
    ]
