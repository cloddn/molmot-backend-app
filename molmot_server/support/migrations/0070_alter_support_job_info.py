# Generated by Django 3.2.12 on 2022-05-19 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0069_auto_20220519_2337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='support',
            name='job_info',
            field=models.CharField(blank=True, choices=[('학생', '학생'), ('직장인', '직장인'), ('프리랜서', '프리랜서'), ('자영업자', '자영업자'), ('해당없음', '해당없음')], default='학생', max_length=6, null=True, verbose_name='직업'),
        ),
    ]