# Generated by Django 3.2.12 on 2022-05-10 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_alter_pizza_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='image',
            field=models.ImageField(default='', upload_to='home/pizza_uploaded_images'),
        ),
    ]
