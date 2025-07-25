# Generated by Django 5.1.5 on 2025-07-26 13:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название бренда')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, verbose_name='Описание бренда')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='brands/')),
            ],
            options={
                'verbose_name': 'Бренд',
                'verbose_name_plural': 'Бренды',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Категория')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('category_icon', models.ImageField(upload_to='products/catalog/')),
                ('category_desc', models.CharField(blank=True, max_length=100, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('main_image', models.ImageField(upload_to='products/main/', verbose_name='Основное изображение')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('discount', models.PositiveIntegerField(default=0, verbose_name='Скидка (%)')),
                ('frame_type', models.CharField(choices=[('full', 'Полная оправа'), ('half', 'Полуоправа'), ('rimless', 'Без оправы')], max_length=20, verbose_name='Тип оправы')),
                ('lens_type', models.CharField(choices=[('single', 'Однофокальные'), ('progressive', 'Прогрессивные'), ('bifocal', 'Бифокальные')], max_length=20, verbose_name='Тип линз')),
                ('frame_material', models.CharField(max_length=100, verbose_name='Материал оправы')),
                ('lens_material', models.CharField(max_length=100, verbose_name='Материал линз')),
                ('color', models.CharField(max_length=50, verbose_name='Цвет')),
                ('gender', models.CharField(choices=[('men', 'Мужские'), ('women', 'Женские'), ('unisex', 'Унисекс')], max_length=20)),
                ('is_available', models.BooleanField(default=True, verbose_name='Доступен')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.brand', verbose_name='Бренд')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.category', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Товар',
                'verbose_name_plural': 'Товары',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/extra/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='shop.product')),
            ],
            options={
                'verbose_name': 'Изображение товара',
                'verbose_name_plural': 'Изображения товаров',
            },
        ),
    ]
