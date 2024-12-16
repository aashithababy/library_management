# Generated by Django 4.2.17 on 2024-12-15 10:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('catalog', '0002_book_is_available'),
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
            name='SubscriptionPlan',
            fields=[
                ('plan_id', models.AutoField(primary_key=True, serialize=False)),
                ('plan_name', models.CharField(max_length=255)),
                ('book_rent_limit', models.PositiveIntegerField()),
                ('rent_duration_week', models.PositiveIntegerField()),
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
