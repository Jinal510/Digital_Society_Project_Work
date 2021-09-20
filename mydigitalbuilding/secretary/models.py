from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
import math
from django.utils import timezone

# Create your models here.

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)
    otp = models.IntegerField(default=459)
    is_activate = models.BooleanField(default=True)
    is_verfied = models.BooleanField(default=False)
    role = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now = True,blank = False)

    def __str__(self):
        return self.email

class Chairman(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20,blank=True)
    contact = models.CharField(max_length=20)
    profile_pic = models.FileField(upload_to="media\images",default="media\images\default.png")
    # Chairman Profile   
    gender = models.CharField(max_length=20,blank=True)
    age = models.CharField(max_length=20,blank=True)
    country = models.CharField(max_length=30,blank=True)
    state = models.CharField(max_length=30,blank=True)
    city = models.CharField(max_length=30,blank=True)
    address = models.CharField(max_length=200,blank=True)
    aboutme = models.TextField(max_length=500,blank=True)
    work = models.CharField(max_length=20,blank=True)
    
    def __str__(self):
        return self.firstname

class Members(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20,blank=True)
    contact = models.CharField(max_length=20)
    profile_pic = models.FileField(upload_to="media\images",default="media\images\default.png")
    status = models.CharField(max_length=20,default='Pending')
    # Member Profile
    gender = models.CharField(max_length=20,blank=True)
    age = models.CharField(max_length=20,blank=True)
    state = models.CharField(max_length=30,blank=True)
    country = models.CharField(max_length=30,blank=True)
    city = models.CharField(max_length=30,blank=True)
    address = models.CharField(max_length=200,blank=True)
    aboutme = models.TextField(max_length=500,blank=True)
    work = models.CharField(max_length=20,blank=True)
    job_address = models.CharField(max_length=200,blank=True)
    blood_grp = models.CharField(max_length=200,blank=True)
    birthdate = models.DateField(blank=True,null=True)
    marrial_status = models.CharField(max_length=200,blank=True)
    house_no = models.CharField(max_length=200,blank=True)
    vechicle_deatails = models.CharField(max_length=200,blank=True)
    family_members = models.CharField(max_length=200,blank=True)
    o_r = models.CharField(max_length=20,blank=True)

    def __str__(self):
        return self.firstname

class Watchman(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20,blank=True)
    contact = models.CharField(max_length=20)
    profile_pic = models.FileField(upload_to="media\images",default="media\images\default.png")
    # Watchman Profile
    gender = models.CharField(max_length=20,blank=True)
    status = models.CharField(max_length=20,default='Pending')
    age = models.CharField(max_length=20,blank=True)
    state = models.CharField(max_length=30,blank=True)
    country = models.CharField(max_length=30,blank=True)
    city = models.CharField(max_length=30,blank=True)
    address = models.CharField(max_length=200,blank=True)
    aboutme = models.TextField(max_length=500,blank=True)
    work = models.CharField(max_length=20,blank=True)
    blood_grp = models.CharField(max_length=200,blank=True)
    birthdate = models.DateField(blank=True,null=True)
    vechicle_deatails = models.CharField(max_length=200,blank=True)
    marrial_status = models.CharField(max_length=200,blank=True)
    
    def __str__(self):
        return self.firstname

class Myfamily(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20,blank=True)
    contact = models.CharField(max_length=20)
    profile_pic = models.FileField(upload_to="media\images",default="media\images\default.png")
    # Member Profile
    gender = models.CharField(max_length=20,blank=True)
    age = models.CharField(max_length=20,blank=True)
    aboutme = models.TextField(max_length=500,blank=True)
    work = models.CharField(max_length=20,blank=True)
    job_address = models.CharField(max_length=200,blank=True)
    blood_grp = models.CharField(max_length=200,blank=True)
    birthdate = models.DateField(blank=True,null=True)
    relation = models.CharField(max_length=200,blank=True)
  
    def __str__(self):
        return self.firstname

class EditMyfamily(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    firstname = models.CharField(max_length=20)
    lastname = models.CharField(max_length=20,blank=True)
    contact = models.CharField(max_length=20)
    profile_pic = models.FileField(upload_to="media\images",default="media\images\default.png")
    # Member Profile
    gender = models.CharField(max_length=20,blank=True)
    age = models.CharField(max_length=20,blank=True)
    aboutme = models.TextField(max_length=500,blank=True)
    work = models.CharField(max_length=20,blank=True)
    job_address = models.CharField(max_length=200,blank=True)
    blood_grp = models.CharField(max_length=200,blank=True)
    birthdate = models.DateField(blank=True,null=True)
    relation = models.CharField(max_length=200,blank=True)
  
    def __str__(self):
        return self.firstname


class Events(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    subject = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    profile_pic = models.FileField(upload_to="media\images",blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now = True,blank = False)

    def __str__(self):
        return self.subject

    def whenpublished(self):
            now = timezone.now()
            
            diff= now - self.created_at

            if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
                seconds= diff.seconds
                
                if seconds == 1:
                    return str(seconds) +  "second ago"
                
                else:
                    return str(seconds) + " seconds ago"

            if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
                minutes= math.floor(diff.seconds/60)

                if minutes == 1:
                    return str(minutes) + " minute ago"
                
                else:
                    return str(minutes) + " minutes ago"



            if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
                hours= math.floor(diff.seconds/3600)

                if hours == 1:
                    return str(hours) + " hour ago"

                else:
                    return str(hours) + " hours ago"

            # 1 day to 30 days
            if diff.days >= 1 and diff.days < 30:
                days = diff.days

                if days == 1 :
                    return str(days) + "day ago"

                else:
                    return str(days) + "days ago"

            if diff.days >= 30 and diff.days < 365:
                month = math.floor(diff.days/30)

                if month == 1:
                    return str(month) + "month ago"

                else:
                    return str(month) + "months ago"


            if diff.days >= 365 :
                year = math.floor(diff.day/365)

                if year == 1:
                    return str(year) + "year ago"

                else:
                    return str(year) + "years ago"

class Complain(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    subject = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now = True,blank = False)

    def __str__(self):
        return self.subject

    def whenpublished(self):
            now = timezone.now()
            
            diff= now - self.created_at

            if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
                seconds= diff.seconds
                
                if seconds == 1:
                    return str(seconds) +  "second ago"
                
                else:
                    return str(seconds) + " seconds ago"

            if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
                minutes= math.floor(diff.seconds/60)

                if minutes == 1:
                    return str(minutes) + " minute ago"
                
                else:
                    return str(minutes) + " minutes ago"



            if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
                hours= math.floor(diff.seconds/3600)

                if hours == 1:
                    return str(hours) + " hour ago"

                else:
                    return str(hours) + " hours ago"

            # 1 day to 30 days
            if diff.days >= 1 and diff.days < 30:
                days = diff.days

                if days == 1 :
                    return str(days) + "day ago"

                else:
                    return str(days) + "days ago"

            if diff.days >= 30 and diff.days < 365:
                month = math.floor(diff.days/30)

                if month == 1:
                    return str(month) + "month ago"

                else:
                    return str(month) + "months ago"


            if diff.days >= 365 :
                year = math.floor(diff.day/365)

                if year == 1:
                    return str(year) + "year ago"

                else:
                    return str(year) + "years ago"

class Suggestions(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    subject = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now = True,blank = False)

    def __str__(self):
        return self.subject

    def whenpublished(self):
            now = timezone.now()
            
            diff= now - self.created_at

            if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
                seconds= diff.seconds
                
                if seconds == 1:
                    return str(seconds) +  "second ago"
                
                else:
                    return str(seconds) + " seconds ago"

            if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
                minutes= math.floor(diff.seconds/60)

                if minutes == 1:
                    return str(minutes) + " minute ago"
                
                else:
                    return str(minutes) + " minutes ago"



            if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
                hours= math.floor(diff.seconds/3600)

                if hours == 1:
                    return str(hours) + " hour ago"

                else:
                    return str(hours) + " hours ago"

            # 1 day to 30 days
            if diff.days >= 1 and diff.days < 30:
                days = diff.days

                if days == 1 :
                    return str(days) + "day ago"

                else:
                    return str(days) + "days ago"

            if diff.days >= 30 and diff.days < 365:
                month = math.floor(diff.days/30)

                if month == 1:
                    return str(month) + "month ago"

                else:
                    return str(month) + "months ago"


            if diff.days >= 365 :
                year = math.floor(diff.day/365)

                if year == 1:
                    return str(year) + "year ago"

                else:
                    return str(year) + "years ago"

class Vistiors(models.Model):
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now = True,blank = False)
    member_firstname = models.CharField(max_length=20)
    visitor_firstname = models.CharField(max_length=20)
    contact = models.CharField(max_length=20)
    gender = models.CharField(max_length=20,blank=True)
    currentdate = models.DateField(blank=True,null=True)
    time = models.TimeField(blank=True,null=True)
    house_no = models.CharField(max_length=200,blank=True)
    vechicle_deatails = models.CharField(max_length=200,blank=True)
   
    def __str__(self):
        return self.visitor_firstname

    def whenpublished(self):
            now = timezone.now()
            
            diff= now - self.created_at

            if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
                seconds= diff.seconds
                
                if seconds == 1:
                    return str(seconds) +  "second ago"
                
                else:
                    return str(seconds) + " seconds ago"

            if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
                minutes= math.floor(diff.seconds/60)

                if minutes == 1:
                    return str(minutes) + " minute ago"
                
                else:
                    return str(minutes) + " minutes ago"



            if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
                hours= math.floor(diff.seconds/3600)
                
class ChatBoard(models.Model):               
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    subject = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now = True,blank = False)

    def __str__(self):
        return self.subject

    def whenpublished(self):
            now = timezone.now()
            
            diff= now - self.created_at

            if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
                seconds= diff.seconds
                
                if seconds == 1:
                    return str(seconds) +  "second ago"
                
                else:
                    return str(seconds) + " seconds ago"

            if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
                minutes= math.floor(diff.seconds/60)

                if minutes == 1:
                    return str(minutes) + " minute ago"
                
                else:
                    return str(minutes) + " minutes ago"



            if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
                hours= math.floor(diff.seconds/3600)

                if hours == 1:
                    return str(hours) + " hour ago"

                else:
                    return str(hours) + " hours ago"

            # 1 day to 30 days
            if diff.days >= 1 and diff.days < 30:
                days = diff.days

                if days == 1 :
                    return str(days) + "day ago"

                else:
                    return str(days) + "days ago"

            if diff.days >= 30 and diff.days < 365:
                month = math.floor(diff.days/30)

                if month == 1:
                    return str(month) + "month ago"

                else:
                    return str(month) + "months ago"


            if diff.days >= 365 :
                year = math.floor(diff.day/365)

                if year == 1:
                    return str(year) + "year ago"

                else:
                    return str(year) + "years ago"


                if hours == 1:
                    return str(hours) + " hour ago"

                else:
                    return str(hours) + " hours ago"

            # 1 day to 30 days
            if diff.days >= 1 and diff.days < 30:
                days = diff.days

                if days == 1 :
                    return str(days) + "day ago"
                else:
                    return str(days) + "days ago"

            if diff.days >= 30 and diff.days < 365:
                month = math.floor(diff.days/30)

                if month == 1:
                    return str(month) + "month ago"

                else:
                    return str(month) + "months ago"


            if diff.days >= 365 :
                year = math.floor(diff.day/365)

                if year == 1:
                    return str(year) + "year ago"

                else:
                    return str(year) + "years ago"

class NoticeBoard(models.Model):               
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    subject = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    profile_pic = models.FileField(upload_to="media\images",blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now = True,blank = False)

    def __str__(self):
        return self.subject

    def whenpublished(self):
            now = timezone.now()
            
            diff= now - self.created_at

            if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
                seconds= diff.seconds
                
                if seconds == 1:
                    return str(seconds) +  "second ago"
                
                else:
                    return str(seconds) + " seconds ago"

            if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
                minutes= math.floor(diff.seconds/60)

                if minutes == 1:
                    return str(minutes) + " minute ago"
                
                else:
                    return str(minutes) + " minutes ago"



            if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
                hours= math.floor(diff.seconds/3600)

                if hours == 1:
                    return str(hours) + " hour ago"

                else:
                    return str(hours) + " hours ago"

            # 1 day to 30 days
            if diff.days >= 1 and diff.days < 30:
                days = diff.days

                if days == 1 :
                    return str(days) + "day ago"

                else:
                    return str(days) + "days ago"

            if diff.days >= 30 and diff.days < 365:
                month = math.floor(diff.days/30)

                if month == 1:
                    return str(month) + "month ago"

                else:
                    return str(month) + "months ago"


            if diff.days >= 365 :
                year = math.floor(diff.day/365)

                if year == 1:
                    return str(year) + "year ago"

                else:
                    return str(year) + "years ago"


                if hours == 1:
                    return str(hours) + " hour ago"

                else:
                    return str(hours) + " hours ago"

            # 1 day to 30 days
            if diff.days >= 1 and diff.days < 30:
                days = diff.days

                if days == 1 :
                    return str(days) + "day ago"
                else:
                    return str(days) + "days ago"

            if diff.days >= 30 and diff.days < 365:
                month = math.floor(diff.days/30)

                if month == 1:
                    return str(month) + "month ago"

                else:
                    return str(month) + "months ago"


            if diff.days >= 365 :
                year = math.floor(diff.day/365)

                if year == 1:
                    return str(year) + "year ago"

                else:
                    return str(year) + "years ago"

class Rent(models.Model):            
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    subject = models.CharField(max_length=200)
    h_no = models.CharField(max_length=200)
    bhk = models.CharField(max_length=200)
    h_price = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    profile_pic = models.FileField(upload_to="media\images",blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=False)
    updated_at = models.DateTimeField(auto_now = True,blank = False)

    def __str__(self):
        return self.subject

    def whenpublished(self):
            now = timezone.now()
            
            diff= now - self.created_at

            if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
                seconds= diff.seconds
                
                if seconds == 1:
                    return str(seconds) +  "second ago"
                
                else:
                    return str(seconds) + " seconds ago"

            if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600:
                minutes= math.floor(diff.seconds/60)

                if minutes == 1:
                    return str(minutes) + " minute ago"
                
                else:
                    return str(minutes) + " minutes ago"



            if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400:
                hours= math.floor(diff.seconds/3600)

                if hours == 1:
                    return str(hours) + " hour ago"

                else:
                    return str(hours) + " hours ago"

            # 1 day to 30 days
            if diff.days >= 1 and diff.days < 30:
                days = diff.days

                if days == 1 :
                    return str(days) + "day ago"

                else:
                    return str(days) + "days ago"

            if diff.days >= 30 and diff.days < 365:
                month = math.floor(diff.days/30)

                if month == 1:
                    return str(month) + "month ago"

                else:
                    return str(month) + "months ago"


            if diff.days >= 365 :
                year = math.floor(diff.day/365)

                if year == 1:
                    return str(year) + "year ago"

                else:
                    return str(year) + "years ago"


                if hours == 1:
                    return str(hours) + " hour ago"

                else:
                    return str(hours) + " hours ago"

            # 1 day to 30 days
            if diff.days >= 1 and diff.days < 30:
                days = diff.days

                if days == 1 :
                    return str(days) + "day ago"
                else:
                    return str(days) + "days ago"

            if diff.days >= 30 and diff.days < 365:
                month = math.floor(diff.days/30)

                if month == 1:
                    return str(month) + "month ago"

                else:
                    return str(month) + "months ago"


            if diff.days >= 365 :
                year = math.floor(diff.day/365)

                if year == 1:
                    return str(year) + "year ago"

                else:
                    return str(year) + "years ago"
                
class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return self.order_id

class Gallery(models.Model):
    profile_pic = models.FileField(upload_to="media\images",default="media\images\default.png")