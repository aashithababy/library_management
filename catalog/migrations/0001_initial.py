# Generated by Django 4.2.17 on 2024-12-22 06:45

import catalog.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessRestriction',
            fields=[
                ('restriction_id', models.AutoField(primary_key=True, serialize=False)),
                ('membership_type', models.CharField(max_length=255)),
                ('allow_bestseller', models.BooleanField()),
                ('allow_early_release', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('author_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('bio', models.TextField()),
                ('nationality', models.CharField(blank=True, max_length=255, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('death_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('genre', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('published_year', models.PositiveIntegerField()),
                ('isbn', models.CharField(max_length=13)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rent_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('is_bestseller', models.BooleanField()),
                ('is_early_release', models.BooleanField()),
                ('content_link', models.URLField(blank=True, null=True, validators=[catalog.models.validate_url_or_local_path])),
                ('access_level', models.CharField(blank=True, max_length=50, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('read_count', models.PositiveIntegerField(blank=True, null=True)),
                ('popularity_score', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('rating', models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.author')),
            ],
            options={
                'ordering': ['author'],
            },
        ),
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('plan_id', models.AutoField(primary_key=True, serialize=False)),
                ('plan_name', models.CharField(max_length=255)),
                ('book_rent_limit', models.PositiveIntegerField()),
                ('rent_duration_week', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='YourModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_link', models.URLField(blank=True, null=True, validators=[catalog.models.validate_url_or_local_path])),
            ],
        ),
        migrations.CreateModel(
            name='RentedBook',
            fields=[
                ('rental_id', models.AutoField(primary_key=True, serialize=False)),
                ('rent_start_date', models.DateField()),
                ('rent_end_date', models.DateField()),
                ('status', models.CharField(max_length=50)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
        migrations.CreateModel(
            name='OurBestseller',
            fields=[
                ('bestseller_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_bestseller', models.BooleanField()),
                ('is_early_release', models.BooleanField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.book')),
            ],
        ),
        migrations.CreateModel(
            name='OurBestNonFictionBook',
            fields=[
                ('nonfiction_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_bestseller', models.BooleanField()),
                ('is_early_release', models.BooleanField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.book')),
            ],
        ),
        migrations.CreateModel(
            name='OurBestFictionBook',
            fields=[
                ('fantasy_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_bestseller', models.BooleanField()),
                ('is_early_release', models.BooleanField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.book')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('genre_id', models.AutoField(primary_key=True, serialize=False)),
                ('genre_name', models.CharField(max_length=255)),
                ('is_early_release', models.BooleanField()),
                ('is_bestseller', models.BooleanField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='genres', to='catalog.book')),
            ],
        ),
        migrations.CreateModel(
            name='EveryoneTalkingAbout',
            fields=[
                ('talking_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_bestseller', models.BooleanField()),
                ('is_early_release', models.BooleanField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.book')),
            ],
        ),
        migrations.CreateModel(
            name='EarlyRelease',
            fields=[
                ('early_release_id', models.AutoField(primary_key=True, serialize=False)),
                ('is_bestseller', models.BooleanField()),
                ('is_early_release', models.BooleanField()),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.book')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('cart_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_added', models.DateField()),
                ('quantity', models.PositiveIntegerField()),
                ('status', models.CharField(max_length=50)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
        migrations.CreateModel(
            name='AuthorBook',
            fields=[
                ('author_book_id', models.AutoField(primary_key=True, serialize=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.author')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.book')),
            ],
        ),
        migrations.CreateModel(
            name='AdminBookAction',
            fields=[
                ('action_id', models.AutoField(primary_key=True, serialize=False)),
                ('action', models.CharField(max_length=255)),
                ('action_date', models.DateField()),
                ('details', models.TextField()),
                ('admin_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.book')),
            ],
        ),
    ]
