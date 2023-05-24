# Generated by Django 4.2.1 on 2023-05-24 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reg_log', '0008_cart_alter_users_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users1',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='id')),
                ('Name', models.CharField(max_length=100, verbose_name='Имя')),
                ('Surname', models.CharField(max_length=100, verbose_name='Фамилия')),
                ('Email', models.EmailField(max_length=254, verbose_name='Почта')),
                ('Pass1', models.CharField(max_length=20, verbose_name='Пароль')),
                ('Pass2', models.CharField(max_length=20, verbose_name='Проверка пароля')),
                ('Age', models.IntegerField(verbose_name='Возраст')),
                ('Face', models.ImageField(default='users/default.png', upload_to='users/', verbose_name='Фотография')),
                ('FaceLink', models.CharField(max_length=400, verbose_name='Фотография')),
                ('Balance', models.IntegerField(verbose_name='Баланс')),
            ],
        ),
        migrations.RenameField(
            model_name='users',
            old_name='ID',
            new_name='id',
        ),
    ]
