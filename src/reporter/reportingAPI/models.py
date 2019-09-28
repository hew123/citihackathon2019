# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    categoryName = models.CharField(db_column='categoryName', max_length=64, blank=True, null=True)  # Field name made lowercase.
    createdTime = models.DateTimeField(db_column='createdTime', blank=True, null=True)  # Field name made lowercase.
    updatedTime = models.DateTimeField(db_column='updatedTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Category'


class Event(models.Model):
    id = models.IntegerField(primary_key=True)
    eventName = models.CharField(db_column='eventName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    startDateTime = models.DateTimeField(db_column='startDateTime', blank=True, null=True)  # Field name made lowercase.
    endDateTime = models.DateTimeField(db_column='endDateTime', blank=True, null=True)  # Field name made lowercase.
    maxParticipants = models.IntegerField(db_column='maxParticipants', blank=True, null=True)  # Field name made lowercase.
    minParticipants = models.IntegerField(db_column='minParticipants', blank=True, null=True)  # Field name made lowercase.
    organizerName = models.CharField(db_column='organizerName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(blank=True, null=True)
    eventStatus = models.CharField(db_column='eventStatus', max_length=6, blank=True, null=True)  # Field name made lowercase.
    createdDateTime = models.DateTimeField(db_column='createdDateTime', blank=True, null=True)  # Field name made lowercase.
    updatedDateTime = models.DateTimeField(db_column='updatedDateTime', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Event'


class Eventcategory(models.Model):
    categoryId = models.ForeignKey(Category, models.DO_NOTHING, db_column='categoryId', primary_key=True)  # Field name made lowercase.
    eventId = models.ForeignKey(Event, models.DO_NOTHING, db_column='eventId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'EventCategory'
        unique_together = (('categoryId', 'eventId'),)


class Eventregistration(models.Model):
    eventId = models.ForeignKey(Event, models.DO_NOTHING, db_column='eventId')  # Field name made lowercase.
    userId = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', primary_key=True)  # Field name made lowercase.
    attended = models.IntegerField(blank=True, null=True)
    createdTime = models.DateTimeField(db_column='createdTime', blank=True, null=True)  # Field name made lowercase.
    updatedTime = models.DateTimeField(db_column='updatedTime', blank=True, null=True)  # Field name made lowercase.
    withdrawed = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'EventRegistration'
        unique_together = (('userId', 'eventId'),)


class Feedback(models.Model):
    eventId = models.ForeignKey(Event, models.DO_NOTHING, db_column='eventId')  # Field name made lowercase.
    userId = models.ForeignKey('User', models.DO_NOTHING, db_column='userId', primary_key=True)  # Field name made lowercase.
    feedback = models.TextField(blank=True, null=True)
    sentimeterScore = models.FloatField(db_column='sentimeterScore', blank=True, null=True)  # Field name made lowercase.
    magnitude = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Feedback'
        unique_together = (('userId', 'eventId'),)


class User(models.Model):
    userId = models.IntegerField(db_column='id',primary_key=True)
    userName = models.CharField(db_column='username',unique=True, max_length=50, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    accountType = models.CharField(db_column='accountType', max_length=10, blank=True, null=True)  # Field name made lowercase.
    emailAddress = models.CharField(db_column='emailAddress', unique=True, max_length=255, blank=True, null=True)  # Field name made lowercase.
    firstName = models.CharField(db_column='firstName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    lastName = models.CharField(db_column='lastName', max_length=50, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(max_length=6, blank=True, null=True)
    dateOfBirth = models.DateField(db_column='dateOfBirth', blank=True, null=True)  # Field name made lowercase.
    clientSecret = models.CharField(db_column='clientSecret', max_length=255, blank=True, null=True)  # Field name made lowercase.
    twoFactorEnabled = models.IntegerField(db_column='twoFactorEnabled', blank=True, null=True)  # Field name made lowercase.
    verified = models.IntegerField(blank=True, null=True)
    createdDateTime = models.DateTimeField(db_column='createdDateTime', blank=True, null=True)  # Field name made lowercase.
    updatedDateTime = models.DateTimeField(db_column='updatedDateTime', blank=True, null=True)  # Field name made lowercase.
    status = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'User'


class ArInternalMetadata(models.Model):
    key = models.CharField(primary_key=True, max_length=255)
    value = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'ar_internal_metadata'


class SchemaMigrations(models.Model):
    version = models.CharField(primary_key=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'schema_migrations'
