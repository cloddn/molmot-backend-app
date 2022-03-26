# Generated by Django 3.2.12 on 2022-03-26 08:32

from django.db import migrations, models
import user.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, null=True, unique=True)),
                ('username', models.CharField(max_length=50)),
                ('age', models.IntegerField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', '남성(Man)'), ('W', '여성(Woman)'), ('N', '어느쪽도 아님(None)')], default='N', max_length=1, null=True, verbose_name='gender')),
                ('birth', models.CharField(blank=True, max_length=10, null=True, verbose_name='birth')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', user.models.MemberManager()),
            ],
        ),
    ]
