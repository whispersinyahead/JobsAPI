# Generated by Django 3.1 on 2021-08-17 04:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='images')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='main.job')),
            ],
        ),
    ]
