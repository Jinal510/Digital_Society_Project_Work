from django.shortcuts import render    
import random
from .models import *
from django.core.mail import send_mail
from .utils import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .paytm import generate_checksum, verify_checksum


# Create your views here.

# paytm integration start

def paytmhome(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        if uid.role == "Chairman":
            cid = Chairman.objects.get(user_id=uid)
            return render(request,"secretary/dashboard/pay.html",{'cid':cid,'uid':uid})
        elif uid.role == "Members":
            user_id = User.objects.get(role="Chairman")
            cid = Chairman.objects.get(user_id=user_id)
            mid = Members.objects.get(user_id=uid)
            return render(request,"secretary/dashboard/pay_members.html",{'cid':cid,'mid':mid,'uid':uid})       
    else:
        return render(request,"secretary/dashboard/home.html")       
        
    

def initiate_payment(request):
    print("------------>>>> called")
    if request.method == "GET":
        return render(request, 'secretary/dashboard/pay.html')
    
    id = request.POST['id']
    amount = int(request.POST['price'])
    print("---->amount ",amount)
    uid = User.objects.get(id=id)
    

    transaction = Transaction.objects.create(made_by=uid, amount=amount)
    transaction.save()
    merchant_key = settings.PAYTM_SECRET_KEY

    params = (
        ('MID', settings.PAYTM_MERCHANT_ID),
        ('ORDER_ID', str(transaction.order_id)),
        ('CUST_ID', str(transaction.made_by.email)),
        ('TXN_AMOUNT', str(transaction.amount)),
        ('CHANNEL_ID', settings.PAYTM_CHANNEL_ID),
        ('WEBSITE', settings.PAYTM_WEBSITE),
        # ('EMAIL', request.user.email),
        # ('MOBILE_N0', '9911223388'),
        ('INDUSTRY_TYPE_ID', settings.PAYTM_INDUSTRY_TYPE_ID),
        ('CALLBACK_URL', 'http://127.0.0.1:8000/callback/'),
        # ('PAYMENT_MODE_ONLY', 'NO'),
    )

    paytm_params = dict(params)
    checksum = generate_checksum(paytm_params, merchant_key)

    transaction.checksum = checksum
    transaction.save()

    paytm_params['CHECKSUMHASH'] = checksum
    print('SENT: ', checksum)
    return render(request, 'secretary/dashboard/redirect.html', context=paytm_params)

    
@csrf_exempt
def callback(request):
    if request.method == 'POST':
        paytm_checksum = ''
        print(request.body)
        print(request.POST)
        received_data = dict(request.POST)
        print(received_data)
        paytm_params = {}
        paytm_checksum = received_data['CHECKSUMHASH'][0]
        for key, value in received_data.items():
            if key == 'CHECKSUMHASH':
                paytm_checksum = value[0]
            else:
                paytm_params[key] = str(value[0])
        # Verify checksum
        is_valid_checksum = verify_checksum(paytm_params, settings.PAYTM_SECRET_KEY, str(paytm_checksum))
        if is_valid_checksum:
            print("Checksum Matched")
            received_data['message'] = "Checksum Matched"
        else:
            print("Checksum Mismatched")
            received_data['message'] = "Checksum Mismatched"
            return render(request, 'secretary/dashboard/callback.html', context=received_data)
        return render(request, 'secretary/dashboard/callback.html', context=received_data)


# paytm integration end


# home page start      

def index7(request):
    return render(request,"secretary/mainhome.html")


def mainhome(request):
    
    eall = Events.objects.all()
    nall = NoticeBoard.objects.all()
    nlis = NoticeBoard.objects.all().count()
    mall = Members.objects.all().count()
    ec = Events.objects.all().count()
    return render(request,"secretary/mainhome.html",{'eall':eall,'nall':nall,'nlis':str(nlis),'mall':str(mall),'ec':str(ec)})

def home(request): 
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])

        if uid.role == "Chairman":
            cid = Chairman.objects.get(user_id=uid)    
            nall = NoticeBoard.objects.order_by('-created_at')
            nlis = NoticeBoard.objects.all().count()
            mall = Members.objects.all().count()
            ec = Events.objects.all().count()
            eall = Events.objects.order_by('-created_at')
            print("----->notice",nall)
            
            return render(request,"secretary/dashboard/index.html",{'eall':eall,'ec':str(ec),'nall':nall,'uid':uid,'cid':cid,'nlis':str(nlis),'mall':str(mall)})
         
    return render(request,"secretary/login.html")

def mem(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])

        if uid.role == "Members":
            mid = Members.objects.get(user_id=uid)
            user_id = User.objects.get(role="Chairman")
            cid = Chairman.objects.get(user_id=user_id) 
            nall = NoticeBoard.objects.order_by('-created_at')
            nlis = NoticeBoard.objects.all().count()
            mall = Members.objects.all().count()
            ec = Events.objects.all().count()
            eall = Events.objects.order_by('-created_at')
            print("----->notice",nall)

            cid = Chairman.objects.get(user_id=user_id) 

            return render(request,"secretary/dashboard/members-index.html",{'eall':eall,'ec':str(ec),'nall':nall,'uid':uid,'mid':mid,'cid':cid,'nlis':str(nlis),'mall':str(mall)})
     
    return render(request,"secretary/login.html")

def watchman_home(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])

        if uid.role == "Watchman":
            wid = Watchman.objects.get(user_id=uid)
            user_id = User.objects.get(role="Chairman")
            cid = Chairman.objects.get(user_id=user_id) 
            nall = NoticeBoard.objects.order_by('-created_at')
            nlis = NoticeBoard.objects.all().count()
            mall = Members.objects.all().count()
            ec = Events.objects.all().count()
            eall = Events.objects.order_by('-created_at')
            print("----->notice",nall)
            return render(request,"secretary/dashboard/watchman-index.html",{'eall':eall,'ec':str(ec),'nall':nall,'uid':uid,'wid':wid,'cid':cid,'nlis':str(nlis),'mall':str(mall)})
     
    return render(request,"secretary/login.html")


# home page end

# login and register page start

def login(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        if uid.role == "Chairman":
            print(Chairman)
            cid = Chairman.objects.get(user_id=uid)
            nall = NoticeBoard.objects.order_by('-created_at')
            nlis = NoticeBoard.objects.all().count()
            mall = Members.objects.all().count()
            ec = Events.objects.all().count()
            eall = Events.objects.order_by('-created_at')
            print("----->notice",nall)
            return render(request,"secretary/dashboard/index.html",{'cid':cid,'eall':eall,'nall':nall,'uid':uid,'nlis':str(nlis),'mall':str(mall),'ec':str(ec)})
        elif uid.role == "Members":
            print("email")
            user_id=User.objects.get(role="Chairman")
            cid = Chairman.objects.get(user_id=user_id)
            mid = Members.objects.get(user_id=uid)
            nall = NoticeBoard.objects.order_by('-created_at')
            nlis = NoticeBoard.objects.all().count()
            mall = Members.objects.all().count()
            ec = Events.objects.all().count()
            eall = Events.objects.order_by('-created_at')
            print("----->notice",nall)
            return render(request,"secretary/dashboard/members-index.html",{'eall':eall,'nall':nall,'uid':uid,'mid':mid,'cid':cid,'nlis':str(nlis),'mall':str(mall),'ec':str(ec)})
        elif uid.role == "Watchman":
            user_id = User.objects.get(role="Chairman")
            cid = Chairman.objects.get(user_id=user_id) 
            wid = Watchman.objects.get(user_id=uid)
            nall = NoticeBoard.objects.order_by('-created_at')
            nlis = NoticeBoard.objects.all().count()
            mall = Members.objects.all().count()
            ec = Events.objects.all().count()
            eall = Events.objects.order_by('-created_at')
            print("----->notice",nall)
            return render(request,"secretary/dashboard/watchman-index.html",{'cid':cid,'eall':eall,'nall':nall,'uid':uid,'wid':wid,'nlis':str(nlis),'mall':str(mall),'ec':str(ec)})
        
    else:
        if request.POST:
            uid = User.objects.get(email=request.POST['email'])
            if uid.password == request.POST['password']:
                print("Role---",uid.role)
                if uid.role == 'Chairman':
                    
                    cid = Chairman.objects.get(user_id=uid)
                    nlis = NoticeBoard.objects.all().count()
                    mall = Members.objects.all().count()
                    ec = Events.objects.all().count()
                    eall = Events.objects.order_by('-created_at')
                    nall = NoticeBoard.objects.order_by('-created_at')
                   

                    if uid.is_verfied: 
                        request.session['email'] = uid.email
                        return render(request,"secretary/dashboard/index.html",{'eall':eall,'nall':nall,'uid':uid,'cid':cid,'nlis':str(nlis),'mall':str(mall),'ec':str(ec)})
                    else : 
                        return render(request,"secretary/resetpassword.html",{'email': uid.email})
                        
                elif uid.role == 'Members': 
                    #patients login code

                    mid = Members.objects.get(user_id=uid)
                    user_id=User.objects.get(role="Chairman")
                    print("-->",user_id)
                    cid = Chairman.objects.get(user_id=user_id)
                    print("--->",cid.address)
                    nall = NoticeBoard.objects.order_by('-created_at')
                    eall = Events.objects.order_by('-created_at')
                    nlis = NoticeBoard.objects.all().count()
                    mall = Members.objects.all().count()
                    ec = Events.objects.all().count()
                    eall = Events.objects.all()
                    
                
                    
                    print("----->notice",nall)
                    if uid.is_verfied: 
                        request.session['email'] = uid.email
                        return render(request,"secretary/dashboard/members-index.html",{'eall':eall,'nall':nall,'uid':uid,'mid':mid,'cid':cid,'nlis':str(nlis),'mall':str(mall),'ec':str(ec)})
                    else : 
                        return render(request,"secretary/resetpassword.html",{'email': uid.email})
                
                elif uid.role == 'Watchman': 
                    #patients login code
                    
                    wid = Watchman.objects.get(user_id=uid)
                    print("Firstname--",wid.firstname)
                    user_id=User.objects.get(role="Chairman")
                    print("-->",user_id)
                    cid = Chairman.objects.get(user_id=user_id)
                    print("--->",cid.address)
                    print("WATCHMAN")
                    nall = NoticeBoard.objects.order_by('-created_at')
                    nlis = NoticeBoard.objects.all().count()
                    mall = Members.objects.all().count()
                    ec = Events.objects.all().count()
                    eall = Events.objects.order_by('-created_at')
                
                    print("----->notice",nall)
                    if uid.is_verfied: 
                        request.session['email'] = uid.email
                        return render(request,"secretary/dashboard/watchman-index.html",{'eall':eall,'nall':nall,'uid':uid,'wid':wid,'cid':cid,'nlis':str(nlis),'mall':str(mall),'ec':str(ec)})
                    else : 
                        return render(request,"secretary/resetpassword.html",{'email': uid.email})
                        
            else:
                e_msg = "Invalid password"
                return render(request,"secretary/login.html",{'e_msg':e_msg})

        return render(request,"secretary/login.html")   
def register(request):
    try:
        if request.POST:
            firstname = request.POST['firstname']
            email = request.POST['email']
            contact = request.POST['contact']
            role = request.POST['role']

            li = ["65","55","98","74","62","32","54"]
            ch = random.choice(li)
            password = firstname[1:]+email[3:6]+ch

            print("----------> password",password)
        
            if role == "Chairman":
                uid = User.objects.create(email=email,password=password,role=role)
                cid = Chairman.objects.create(user_id=uid,firstname=firstname,contact=contact)

                subject = "WELCOME TO Digital-Society"
                
                # send_mail(subject,message,from_email,[email])
                sendmail(subject,'maintemplate',email,{'firstname': firstname ,'password' : password})
                return render(request,"secretary/login.html")

            elif role == "Members":
                # patient coding
                uid = User.objects.create(email=email,password=password,role=role)
                mid = Members.objects.create(user_id=uid,firstname=firstname,contact=contact)

               
                return render(request,"secretary/login.html")

            elif role == "Watchman":
                # patient coding
                uid = User.objects.create(email=email,password=password,role=role)
                wid = Watchman.objects.create(user_id=uid,firstname=firstname,contact=contact)

                subject = "WELCOME TO Digital-Society"
                
                # send_mail(subject,message,from_email,[email])
                sendmail(subject,'watchman_maintemplate',email,{'firstname': firstname})
                return render(request,"secretary/login.html")
        else:
            return render(request,"secretary/register.html")
    except:
        e_msg = "Something went wrong"
        return render(request,"secretary/register.html",{'e_msg':e_msg})


# login and register page end

def reset_password(request):
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        newpassword = request.POST['newpassword']
        repassword = request.POST['repassword']
        uid = User.objects.get(email=email)
        if uid.is_verfied:
            pass
        else:
            if uid.password == password and newpassword == repassword:
                uid.password = newpassword   # set your new password
                uid.is_verfied = True
                uid.save()     # update
                #s_msg ="Your password is sucessfully reset"
                messages.info(request, "You have sucessfully login and yor password is reset")
                return render(request,"secretary/login.html")
                #return HttpResponseRedirect(reverse('login'))
            elif newpassword != repassword:
                p_msg = "Password doesn't match"
                return render(request,"secretary/resetpassword.html",{'email':uid.email,'p_msg':p_msg})
    else:
        return render(request,"secretary/resetpassword.html")

def logout(request):
    if "email" in request.session:
        del request.session['email']
        return render(request,"secretary/mainhome.html")
    else:
        return render(request,"secretary/mainhome.html")
    
def forgot_password(request):
    if request.POST:
        try:
            email = request.POST['email']
            uid = User.objects.get(email=email)
            if uid:
                otp = random.randint(1111,9999)
                uid.otp = otp
                uid.save()
                sendmail('FORGOT - PASSWORD','otp_template',email,{'otp':str(otp)})
                return render(request,'secretary/reset_password_view.html',{'email':email})

        except Exception as e:
            e_msg = "email does not exist"
            return render(request,'secretary/forgot_password.html',{'e_msg':e_msg})
    else:
        return render(request,'secretary/forgot_password.html')
    
def reset_password_view(request):
    email = request.POST['email']
    otp = request.POST['otp']
    newpassword = request.POST['newpassword']
    repassword = request.POST['repassword']

    uid = User.objects.get(email=email)

    if str(uid.otp) == otp:
        if newpassword == repassword:
            uid.password = newpassword
            uid.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            e_msg = "Newpassword and Re-Password does not match"
            return render(request,'secretary/reset_password_view.html',{'e_msg':e_msg,'email':email})
    else:
        e_msg = "Invalid OTP"
        return render(request,'secretary/reset_password.html_view',{'e_msg':e_msg,'email':email})

def myprofile(request):
    uid = User.objects.get(email = request.session['email'])
    cid = Chairman.objects.get(user_id=uid)  
    return render(request,'secretary/dashboard/profile.html',{'uid':uid,'cid':cid})


def resetprofile(request):
    uid = User.objects.get(email = request.session['email'])
    cid = Chairman.objects.get(user_id=uid)

    if request.POST:
        cid.firstname = request.POST['firstname']
        cid.lastname = request.POST['lastname']
        cid.country = request.POST['country']
        cid.state = request.POST['state']
        cid.city = request.POST['city']
        cid.contact = request.POST['contact']
        cid.address = request.POST['age']
        cid.gender = request.POST['gender']
        cid.address = request.POST['address']
        cid.aboutme = request.POST['aboutme']
        cid.work = request.POST['work']
        cid.age = request.POST['age']
        
        if request.FILES:
            cid.profile_pic = request.FILES['profile']

        cid.save()
    return render(request,'secretary/dashboard/profile.html',{'uid':uid,'cid':cid})

def reset_profile_password(request):
    uid = User.objects.get(email = request.session['email'])
    cid = Chairman.objects.get(user_id=uid)

    currentpassword = request.POST['currentpassword']
    newpassword = request.POST['newpassword']

    if uid.password == currentpassword:
        uid.password = newpassword
        uid.save()
    else:
        msg = "Invalid Password"
    return render(request,'secretary/dashboard/profile.html',{'uid':uid,'cid':cid})

def memberprofile(request):
    uid = User.objects.get(email = request.session['email'])
    mid = Members.objects.get(user_id=uid)  
    user_id = User.objects.get(role="Chairman")
    cid = Chairman.objects.get(user_id=user_id)

    return render(request,'secretary/dashboard/memprofile.html',{'uid':uid,'mid':mid,'cid':cid})

def watchmanprofile(request):
    uid = User.objects.get(email = request.session['email'])
    wid = Watchman.objects.get(user_id=uid)  
    user_id = User.objects.get(role="Chairman")
    cid = Chairman.objects.get(user_id=user_id)

    return render(request,'secretary/dashboard/watchman_profile.html',{'uid':uid,'wid':wid,'cid':cid})

def memberresetprofile(request):
    uid = User.objects.get(email = request.session['email'])
    mid = Members.objects.get(user_id=uid)

    if request.POST:
        mid.firstname = request.POST['firstname']
        mid.lastname = request.POST['lastname']
        mid.country = request.POST['country']
        mid.state = request.POST['state']
        mid.city = request.POST['city']
        mid.contact = request.POST['contact']
        mid.address = request.POST['age']
        mid.gender = request.POST['gender']
        mid.address = request.POST['address']
        mid.aboutme = request.POST['aboutme']
        mid.work = request.POST['work']
        mid.age = request.POST['age']
        mid.blood_grp = request.POST['blood_grp']
        mid.birthdate = request.POST['birthdate']
        # mid.job_address = request.POST['job_address']
        mid.vechicle_deatails = request.POST['vechicle_deatails']
        mid.marrial_status = request.POST['marrial_status']
        mid.house_no = request.POST['house_no']
        mid.family_members = request.POST['family_members']
        
        if request.FILES:
            mid.profile_pic = request.FILES['profile']

        mid.save()
    return render(request,'secretary/dashboard/memprofile.html',{'uid':uid,'mid':mid})

def watchmanresetprofile(request):
    uid = User.objects.get(email = request.session['email'])
    wid = Watchman.objects.get(user_id=uid)

    if request.POST:
        wid.firstname = request.POST['firstname']
        wid.lastname = request.POST['lastname']
        wid.country = request.POST['country']
        wid.state = request.POST['state']
        wid.city = request.POST['city']
        wid.contact = request.POST['contact']
        wid.address = request.POST['age']
        wid.gender = request.POST['gender']
        wid.address = request.POST['address']
        wid.aboutme = request.POST['aboutme']
        wid.work = request.POST['work']
        wid.age = request.POST['age']
        wid.blood_grp = request.POST['blood_grp']
        wid.birthdate = request.POST['birthdate']
        wid.vechicle_deatails = request.POST['vechicle_deatails']
        wid.marrial_status = request.POST['marrial_status']
        
        if request.FILES:
            wid.profile_pic = request.FILES['profile']

        wid.save()
    return render(request,'secretary/dashboard/watchman_profile.html',{'uid':uid,'wid':wid})


def memberreset_profile_password(request):
    uid = User.objects.get(email = request.session['email'])
    mid = Members.objects.get(user_id=uid)

    currentpassword = request.POST['currentpassword']
    newpassword = request.POST['newpassword']

    if uid.password == currentpassword:
        uid.password = newpassword
        uid.save()
    else:
        msg = "Invalid Password"
    return render(request,'secretary/dashboard/memprofile.html',{'uid':uid,'mid':mid})

def watchmanreset_profile_password(request):
    uid = User.objects.get(email = request.session['email'])
    wid = Watchman.objects.get(user_id=uid)

    currentpassword = request.POST['currentpassword']
    newpassword = request.POST['newpassword']

    if uid.password == currentpassword:
        uid.password = newpassword
        uid.save()
    else:
        msg = "Invalid Password"
    return render(request,'secretary/dashboard/watchman_profile.html',{'uid':uid,'wid':wid})


def allmembers(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        user_id = User.objects.get(role="Chairman")
        cid = Chairman.objects.get(user_id=user_id)
        mid = Members.objects.get(user_id=uid)
        mall = Members.objects.exclude(user_id=uid) # retrive all data from the model
        print("cid",cid)
        print("user_id",user_id)
        return render(request,'secretary/dashboard/Allmembers.html',{'uid':uid,'mid':mid,'mall':mall,'cid':cid})
    else:
        uid = User.objects.get(email = request.session['email'])
        user_id = User.objects.get(role="Chairman")
        cid = Chairman.objects.get(user_id=user_id)
        mid = Members.objects.get(user_id=uid)
        mall = Members.objects.exclude(user_id=uid) # retrive all data from the model
        print("cid",cid)
        print("user_id",user_id)
        return render(request,'secretary/dashboard/Allmembers.html',{'uid':uid,'mid':mid,'mall':mall,'cid':cid})

def payment_view(request):
    uid = User.objects.get(email = request.session['email'])
    user_id=User.objects.get(role="Chairman")
    print("-->",user_id)
    cid = Chairman.objects.get(user_id=user_id)
    tall = Transaction.objects.all()
    return render(request,'secretary/dashboard/all-payment.html',{'uid':uid,'tall':tall,'cid':cid})
    


def contacts(request):
    uid = User.objects.get(email = request.session['email'])
    user_id=User.objects.get(role="Chairman")
    print("-->",user_id)
    cid = Chairman.objects.get(user_id=user_id)
    tall = Members.objects.all()
    aall= Members.objects.filter(status="Pending")
    return render(request,'secretary/dashboard/allcontacts.html',{'aall':aall,'uid':uid,'tall':tall,'cid':cid})
    
    
        

def watchman_all_members(request):
    uid = User.objects.get(email = request.session['email'])
    user_id=User.objects.get(role="Chairman")
    print("-->",user_id)
    cid = Chairman.objects.get(user_id=user_id)
    wid = Watchman.objects.get(user_id=uid)
    mall = Members.objects.exclude(user_id=uid) # retrive all data from the model

    # dall = Doctor.objects.all()  
    return render(request,'secretary/dashboard/watchman_all_member.html',{'uid':uid,'wid':wid,'mall':mall,'cid':cid})

def allmember(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])
        cid = Chairman.objects.get(user_id=uid)
        mall = Members.objects.exclude(user_id=uid) # retrive all data from the model
        
        return render(request,'secretary/dashboard/Allmember.html',{'uid':uid,'cid':cid,'mall':mall})
    else:
        
        mall = Members.objects.all()
        return render(request,'secretary/dashboard/Allmember2.html',{'mall':mall})
def view_profile(request,pk):
    memberid = Members.objects.get(id = pk)  # for respective selected user
    uid = User.objects.get(email = request.session['email'])  # for logged in
    mid = Members.objects.get(user_id=uid)
    return render(request,'secretary/dashboard/view-profile.html',{'uid':uid,'memberid':memberid,'mid':mid})

def watchman_can_see_member_view_profile(request,pk):
    user_id=User.objects.get(role="Chairman")
    cid = Chairman.objects.get(user_id=user_id)
    memberid = Members.objects.get(id = pk)  # for respective selected user
    uid = User.objects.get(email = request.session['email'])  # for logged in
    # mid = Members.objects.get(user_id=uid)
    wid = Watchman.objects.get(user_id=uid)
    return render(request,'secretary/dashboard/watchman_can_see_member_view_profile.html',{'uid':uid,'cid':cid,'memberid':memberid,'wid':wid})

def c_view_memprofile(request,pk):
    memberid = Members.objects.get(id = pk)  # for respective selected user
    uid = User.objects.get(email = request.session['email'])  # for logged in
    # mid = Members.objects.get(user_id=uid)
    cid = Chairman.objects.get(user_id=uid)
    return render(request,'secretary/dashboard/c-view-memprofile.html',{'uid':uid,'memberid':memberid,'cid':cid})

def watchman_request(request):
    uid = User.objects.get(email = request.session['email'])
    cid = Chairman.objects.get(user_id=uid)
    wid = Watchman.objects.all()
    
    return render(request,'secretary/dashboard/watchman_request.html',{'uid':uid,'cid':cid,'wid':wid})

def members_request(request):
    uid = User.objects.get(email = request.session['email'])
    cid = Chairman.objects.get(user_id=uid)
    mid = Members.objects.all()
    
    return render(request,'secretary/dashboard/members_request.html',{'uid':uid,'cid':cid,'mid':mid})

def watchman_status(request,pk,status):
    if "email" in request.session:
        uid=User.objects.get(email=request.session['email'])
        wid=Watchman.objects.get(id=pk)
        cid=Chairman.objects.get(user_id=uid)
        wid.status=status
        wid.save()
        if wid.status=="Approved":
            li = ["65","55","98","74","62","32","54"]
            ch = random.choice(li)
            password = wid.firstname[1:]+ch
            wuid=User.objects.get(id=wid.user_id.id)
            wuid.password = password
            wuid.save()
            uid.save()
            
            subject = "WELCOME TO Digital-Society"
                
            # send_mail(subject,message,from_email,[email])
            
            sendmail(subject,"watchman_req_maintemplate",wuid.email,{"wid":wid,"status":status,'password':password})
        wid = Watchman.objects.all()
     
        return render(request,"secretary/dashboard/watchman_request.html",{'uid':uid,'wid':wid,'cid':cid})
    else:
        return render(request,"secretary/login.html")    

def members_status(request,pk,status):
    if "email" in request.session:
        uid=User.objects.get(email=request.session['email'])
        mid=Members.objects.get(id=pk)
        cid=Chairman.objects.get(user_id=uid)
        mid.status=status
        mid.save()
        if mid.status=="Approved":
            li = ["65","55","98","74","62","32","54"]
            ch = random.choice(li)
            password = mid.firstname[1:]+ch
            muid=User.objects.get(id=mid.user_id.id)
            muid.password = password
            muid.save()
            uid.save()
            
            subject = "WELCOME TO Digital-Society"
                
            # send_mail(subject,message,from_email,[email])
            
            sendmail(subject,"maintemplate",muid.email,{"mid":mid,"status":status,'password':password})
        mid = Members.objects.all()
     
        return render(request,"secretary/dashboard/members_request.html",{'uid':uid,'mid':mid,'cid':cid})
    else:
        return render(request,"secretary/login.html")

def myfamilyprofile(request):
    uid = User.objects.get(email = request.session['email'])
    mid = Members.objects.get(user_id=uid)
    all_members = Myfamily.objects.filter(user_id=uid)
    
    
    return render(request,'secretary/dashboard/myfamilyprofile.html',{'mid':mid,'uid':uid,'all_members':all_members})

def chairmanmyfamilyprofile(request):
    uid = User.objects.get(email = request.session['email'])
    cid = Chairman.objects.get(user_id=uid)
    all_members = Myfamily.objects.filter(user_id=uid)
    
    return render(request,'secretary/dashboard/chairmanmyfamilyprofile.html',{'uid':uid,'cid':cid,'all_members':all_members})

def add_my_member(request):
    uid = User.objects.get(email = request.session['email'])    
    mid=Members.objects.get(user_id=uid)
    all_members = Myfamily.objects.filter(user_id=uid)
    
    

    if request.POST:
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        work = request.POST['work']
        contact = request.POST['contact']
        age = request.POST['age']
        gender = request.POST['gender']
        work = request.POST['work']
        blood_grp = request.POST['blood_grp']
        job_address = request.POST['job_address']
        birthdate = request.POST['birthdate']
        relation = request.POST['relation']
       
        Myfamily.objects.create(user_id=uid,firstname=firstname,lastname=lastname,contact=contact,age=age,gender=gender,work=work,blood_grp=blood_grp,job_address=job_address,birthdate=birthdate,relation=relation)
        return HttpResponseRedirect(reverse('myfamilyprofile'))
    else:
        return render(request,'secretary/dashboard/add_my_member.html',{'uid':uid,'mid':mid,'all_members':all_members})

def chairman_add_my_member(request):
    uid = User.objects.get(email = request.session['email'])    
    cid = Chairman.objects.get(user_id=uid)
    all_members = Myfamily.objects.filter(user_id=uid)
 
    if request.POST:
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        work = request.POST['work']
        contact = request.POST['contact']
        age = request.POST['age']
        gender = request.POST['gender']
        work = request.POST['work']
        blood_grp = request.POST['blood_grp']
        job_address = request.POST['job_address']
        birthdate = request.POST['birthdate']
        relation = request.POST['relation']
       
        Myfamily.objects.create(user_id=uid,firstname=firstname,lastname=lastname,contact=contact,age=age,gender=gender,work=work,blood_grp=blood_grp,job_address=job_address,birthdate=birthdate,relation=relation)
        return HttpResponseRedirect(reverse('chairman_add_my_member'))
    else:
        return render(request,'secretary/dashboard/chairman_add_my_member.html',{'uid':uid,'cid':cid,'all_members':all_members})


def Editmyfamilyprofile(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])     
        mid = Members.objects.get(user_id=uid)
        all_members = Myfamily.objects.filter(user_id=uid)
        fid=Myfamily.objects.get(id=pk)
        if request.POST:
            firstname=request.POST['firstname']
            lastname=request.POST['lastname']
            contact=request.POST['contact']
            birthdate=request.POST['birthdate']
            gender=request.POST['gender']
            age=request.POST['age']
            blood_grp=request.POST['blood_grp']
                
            work=request.POST['work']
            relation=request.POST['relation']
                
                
            fid.firstname=firstname
            fid.lastname=lastname
            fid.contact=contact
            fid.birthdate=birthdate
            fid.gender=gender
            fid.age=age
            fid.blood_grp=blood_grp
                
            fid.work=work
            fid.relation=relation
            fid.save()

            if "profile_pic" in request.FILES:
                profile=request.FILES['profile_pic']
                fid.profile_pic=profile               
                fid.save()
                s_msg="successfully profile updated"
                return render(request,"secretary/dashboard/myfamilyprofile.html",{'all_members':all_members,'fid':fid,'uid':uid,'mid':mid,'s_msg':s_msg})
            else:
                return render(request,'secretary/dashboard/myfamilyprofile.html',{'all_members':all_members,'fid':fid,'uid':uid,'mid':mid}) 
        else:
            return render(request,'secretary/dashboard/Editmyfamilyprofile.html',{'fid':fid,'uid':uid,'mid':mid})
    else:
        return render(request,'secretary/dashboard/Editmyfamilyprofile.html')

def chairmanEditmyfamilyprofile(request,pk):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])    
        cid = Chairman.objects.get(user_id=uid)
        fid=Myfamily.objects.get(id=pk)
        all_members = Myfamily.objects.filter(user_id=uid)
        if request.POST:
            
            firstname=request.POST['firstname']
            lastname=request.POST['lastname']
            contact=request.POST['contact']
            birthdate=request.POST['birthdate']
            gender=request.POST['gender']
            age=request.POST['age']
            blood_grp=request.POST['blood_grp']
            
            work=request.POST['work']
            relation=request.POST['relation']
            
            
            fid.firstname=firstname
            fid.lastname=lastname
            fid.contact=contact
            fid.birthdate=birthdate
            fid.gender=gender
            fid.age=age
            fid.blood_grp=blood_grp
            
            fid.work=work
            fid.relation=relation
            fid.save()

            if "profile_pic" in request.FILES:
                profile=request.FILES['profile_pic']
                fid.profile_pic=profile               
                fid.save()
                s_msg="successfully profile updated"
                return render(request,"foodhelp/chairmanmyfamilyprofile.html",{'all_members':all_members,'fid':fid,'uid':uid,'cid':cid,'s_msg':s_msg})
            else:
                return render(request,'secretary/dashboard/chairmanmyfamilyprofile.html',{'all_members':all_members,'fid':fid,'uid':uid,'cid':cid}) 
        else:
            return render(request,'secretary/dashboard/chairmanEditmyfamilyprofile.html',{'fid':fid,'uid':uid,'cid':cid})
    else:
        return render(request,'secretary/dashboard/chairmanEditmyfamilyprofile.html')


def notice(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])    
        cid = Chairman.objects.get(user_id=uid)
        if request.POST:
            subject = request.POST['subject']
            description = request.POST['description']
            if "noticepic" in request.FILES:
                noticepic = request.FILES['noticepic']
                nid = NoticeBoard.objects.create(user_id = uid, subject=subject, description=description,profile_pic=noticepic)
            else:
                nid = NoticeBoard.objects.create(user_id = uid, subject=subject, description=description)
                
                nall = NoticeBoard.objects.order_by('-created_at')
                return render(request,"secretary/dashboard/notice-details.html",{'uid':uid,'cid':cid,'nall':nall})
            nall = NoticeBoard.objects.order_by('-created_at')
            return render(request,"secretary/dashboard/notice-details.html",{'uid':uid,'cid':cid,'nall':nall})
        else:
            return render(request,"secretary/dashboard/notice-page.html",{'uid':uid,'cid':cid})
    else:
        return HttpResponseRedirect(reverse('login'))

def notice_view(request):
    uid = User.objects.get(email = request.session['email'])    
    cid = Chairman.objects.get(user_id=uid)
    nall = NoticeBoard.objects.order_by('-created_at')
    return render(request,"secretary/dashboard/notice-details.html",{'uid':uid,'cid':cid,'nall':nall})

def chat(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])    
        mid = Members.objects.get(user_id=uid)
        user_id = User.objects.get(role="Chairman")
        cid = Chairman.objects.get(user_id=user_id)
        call = ChatBoard.objects.order_by('created_at')
        if request.POST:
            call = ChatBoard.objects.order_by('created_at')
            subject = request.POST['subject']
            clid = ChatBoard.objects.create(user_id = uid, subject=subject)
            call = ChatBoard.objects.order_by('created_at')
            return render(request,"secretary/dashboard/add_chat.html",{'uid':uid,'cid':cid,'mid':mid,'call':call,'clid':clid})
        else:
            return render(request,"secretary/dashboard/add_chat.html",{'uid':uid,'mid':mid,'cid':cid,'call':call})
    else:
        return HttpResponseRedirect(reverse('login'))

def chat_view(request):
    uid = User.objects.get(email = request.session['email'])    
    mid = Members.objects.get(user_id=uid)
    user_id = User.objects.get(role="Chairman")
    cid = Chairman.objects.get(user_id=user_id)
    call = ChatBoard.objects.order_by('created_at')
    return render(request,"secretary/dashboard/add_chat.html",{'uid':uid,'cid':cid,'mid':mid,'call':call})

def delete_chat(request,pk):
    if "email" in request.session:
        uid=User.objects.get(email=request.session['email'])
        mid=Members.objects.get(user_id=uid)
        ChatBoard.objects.filter(id=pk).delete()
        # nall=NoticeBoard.objects.get(id=pk)
        # nall.delete()
        call = ChatBoard.objects.order_by('created_at')
        return render(request,"secretary/dashboard/add_chat.html",{'uid':uid,'mid':mid,'call':call})
    
def all_delete_chat(request,pk):
    if "email" in request.session:
        uid=User.objects.get(email=request.session['email'])
        mid=Members.objects.get(user_id=uid)
        ChatBoard.objects.all().delete()
        # nall=NoticeBoard.objects.get(id=pk)
        # nall.delete()
        call = ChatBoard.objects.order_by('created_at')
        return render(request,"secretary/dashboard/add_chat.html",{'uid':uid,'mid':mid,'call':call})
    

def memnotice_view(request):
    uid = User.objects.get(email = request.session['email'])    
    mid = Members.objects.get(user_id=uid)
    nall = NoticeBoard.objects.all()
    user_id = User.objects.get(role="Chairman")
    cid = Chairman.objects.get(user_id=user_id)

    return render(request,"secretary/dashboard/memnotice-details.html",{'uid':uid,'mid':mid,'nall':nall,'cid':cid})

def watchman_notice_view(request):
    uid = User.objects.get(email = request.session['email'])    
    wid = Watchman.objects.get(user_id=uid)
    nall = NoticeBoard.objects.all()
    user_id = User.objects.get(role="Chairman")
    cid = Chairman.objects.get(user_id=user_id)
    return render(request,"secretary/dashboard/watchman-notice-details.html",{'uid':uid,'wid':wid,'nall':nall,'cid':cid})

def delete_notice(request,pk):
    if "email" in request.session:
        uid=User.objects.get(email=request.session['email'])
        cid=Chairman.objects.get(user_id=uid)
        NoticeBoard.objects.filter(id=pk).delete()
        # nall=NoticeBoard.objects.get(id=pk)
        # nall.delete()
        nall = NoticeBoard.objects.order_by('-created_at')
        return render(request,"secretary/dashboard/notice-details.html",{'uid':uid,'cid':cid,'nall':nall})

def delete_visitor(request,pk):
    if "email" in request.session:
        uid=User.objects.get(email=request.session['email'])
        user_id = User.objects.get(role="Chairman")
        cid = Chairman.objects.get(user_id=user_id)
        wid=Watchman.objects.get(user_id=uid)
        Vistiors.objects.filter(id=pk).delete()
        # nall=NoticeBoard.objects.get(id=pk)
        # nall.delete()
        vall =  Vistiors.objects.order_by('-created_at')
        return render(request,"secretary/dashboard/Allvisitors.html",{'uid':uid,'cid':cid,'wid':wid,'vall':vall})


def events(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])    
        cid = Chairman.objects.get(user_id=uid)
        if request.POST:
            subject = request.POST['subject']
            description = request.POST['description']

            if "eventpic" in request.FILES:
                eventpic = request.FILES['eventpic']
                eid = Events.objects.create(user_id = uid, subject=subject, description=description,profile_pic=eventpic)
            else:
                eid = Events.objects.create(user_id = uid, subject=subject, description=description)
                eall = Events.objects.order_by('-created_at')
                return render(request,"secretary/dashboard/event-details.html",{'uid':uid,'cid':cid,'eall':eall,'eid':eid})
            eall = Events.objects.order_by('-created_at')
            return render(request,"secretary/dashboard/event-details.html",{'uid':uid,'cid':cid,'eall':eall,'eid':eid})
        else:
            return render(request,"secretary/dashboard/event-page.html",{'uid':uid,'cid':cid})
    else:
        return HttpResponseRedirect(reverse('login'))

def event_view(request):
    
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])    
        
        eall = Events.objects.order_by('-created_at')
        if uid.role=="Chairman":
            cid = Chairman.objects.get(user_id=uid)
            return render(request,"secretary/dashboard/event-details-chairman.html",{'uid':uid,'cid':cid,'eall':eall})
        else:
            return render(request,"secretary/dashboard/event-details.html",{'uid':uid,'eall':eall})   
    else:
        eall = Events.objects.all()
        return render(request,"secretary/dashboard/event-details.html",{'eall':eall})
def delete_event(request,pk):
    if "email" in request.session:
        uid=User.objects.get(email=request.session['email'])
        cid=Chairman.objects.get(user_id=uid)
        Events.objects.filter(id=pk).delete()
        # nall=NoticeBoard.objects.get(id=pk)
        # nall.delete()
        eall = Events.objects.order_by('-created_at')
        return render(request,"secretary/dashboard/event-details.html",{'uid':uid,'cid':cid,'eall':eall})

def add_complain(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])    
        mid = Members.objects.get(user_id=uid)
        user_id = User.objects.get(role="Chairman")
        cid = Chairman.objects.get(user_id=user_id)
        if request.POST:
            subject = request.POST['subject']
            description = request.POST['description']

            clid = Complain.objects.create(user_id = uid, subject=subject, description=description)
            call = Complain.objects.filter(user_id=uid)
            return render(request,"secretary/dashboard/complain_details.html",{'uid':uid,'cid':cid,'mid':mid,'call':call,'clid':clid})
        else:
            return render(request,"secretary/dashboard/add_complain.html",{'uid':uid,'mid':mid,'cid':cid})
    else:
        return HttpResponseRedirect(reverse('login'))

def complain_details(request):
    uid = User.objects.get(email = request.session['email'])    
    mid = Members.objects.get(user_id=uid)
    user_id = User.objects.get(role="Chairman")
    cid = Chairman.objects.get(user_id=user_id)
    call = Complain.objects.all(user_id=uid)
    return render(request,"secretary/dashboard/complain_details.html",{'uid':uid,'cid':cid,'mid':mid,'call':call})

def delete_complain(request,pk):
    if "email" in request.session:
        uid=User.objects.get(email=request.session['email'])
        mid=Members.objects.get(user_id=uid)
        Complain.objects.filter(id=pk).delete()
        # nall=NoticeBoard.objects.get(id=pk)
        # nall.delete()
        call = Complain.objects.order_by('-created_at')
        return render(request,"secretary/dashboard/complain_details.html",{'uid':uid,'mid':mid,'call':call})

def memeber_event_view(request):
    uid = User.objects.get(email = request.session['email'])    
    mid = Members.objects.get(user_id=uid)
    user_id = User.objects.get(role="Chairman")
    cid = Chairman.objects.get(user_id=user_id)
    eall = Events.objects.order_by('-created_at')
    return render(request,"secretary/dashboard/member-event-details.html",{'uid':uid,'cid':cid,'mid':mid,'eall':eall})

def chairman_complain_details(request):
    uid = User.objects.get(email = request.session['email'])    
    cid = Chairman.objects.get(user_id=uid)
    call = Complain.objects.order_by('-created_at')
    return render(request,"secretary/dashboard/chairman_complain_details.html",{'uid':uid,'cid':cid,'call':call})

def watchman_complain_details(request):
    uid = User.objects.get(email = request.session['email']) 
    user_id=User.objects.get(role="Chairman")
    print("-->",user_id)
    cid = Chairman.objects.get(user_id=user_id)   
    wid = Watchman.objects.get(user_id=uid)
    call = Complain.objects.order_by('-created_at')
    return render(request,"secretary/dashboard/watchman_complain_details.html",{'uid':uid,'wid':wid,'call':call,'cid':cid})

def watchman_add_complain(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email']) 
        user_id=User.objects.get(role="Chairman")
        print("-->",user_id)
        cid = Chairman.objects.get(user_id=user_id)   
        wid = Watchman.objects.get(user_id=uid)
        if request.POST:
            subject = request.POST['subject']
            description = request.POST['description']

            clid = Complain.objects.create(user_id = uid, subject=subject, description=description)
            call = Complain.objects.order_by('-created_at')
            return render(request,"secretary/dashboard/watchman_complain_details.html",{'uid':uid,'wid':wid,'call':call,'clid':clid,'cid':cid})
        else:
            return render(request,"secretary/dashboard/watchman_add_complain.html",{'uid':uid,'wid':wid,'cid':cid})
    else:
        return HttpResponseRedirect(reverse('login'))

def watchman_delete_complain(request,pk):
    if "email" in request.session:
        uid=User.objects.get(email=request.session['email'])
        wid=Watchman.objects.get(user_id=uid)
        Complain.objects.filter(id=pk).delete()
        # nall=NoticeBoard.objects.get(id=pk)
        # nall.delete()
        call = Complain.objects.order_by('-created_at')
        return render(request,"secretary/dashboard/watchman_complain_details.html",{'uid':uid,'wid':wid,'call':call})

def members_suggestion_box(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])    
        user_id=User.objects.get(role="Chairman")
        print("-->",user_id)
        cid = Chairman.objects.get(user_id=user_id)  
        mid = Members.objects.get(user_id=uid)
        if request.POST:
            subject = request.POST['subject']
            description = request.POST['description']

            sid = Suggestions.objects.create(user_id = uid, subject=subject, description=description)
            sall = Suggestions.objects.order_by('-created_at')
            return render(request,"secretary/dashboard/members_suggestion_box.html",{'uid':uid,'mid':mid,'sall':sall,'sid':sid,'cid':cid})
        else:
            return render(request,"secretary/dashboard/add_members_suggestions.html",{'uid':uid,'mid':mid,'cid':cid})
    else:
        return HttpResponseRedirect(reverse('login'))

def view_members_suggestion_box(request):
    uid = User.objects.get(email = request.session['email']) 
    user_id=User.objects.get(role="Chairman")
    print("-->",user_id)
    cid = Chairman.objects.get(user_id=user_id)     
    mid = Members.objects.get(user_id=uid)
    sall = Suggestions.objects.order_by('-created_at')
    return render(request,"secretary/dashboard/members_suggestion_box.html",{'uid':uid,'mid':mid,'sall':sall,'cid':cid})

def delete_members_suggestion(request,pk):
    if "email" in request.session:
        uid=User.objects.get(email=request.session['email'])
        mid=Members.objects.get(user_id=uid)
        Suggestions.objects.filter(id=pk).delete()
        # nall=NoticeBoard.objects.get(id=pk)
        # nall.delete()
        sall = Suggestions.objects.order_by('-created_at')
        return render(request,"secretary/dashboard/members_suggestion_box.html",{'uid':uid,'mid':mid,'sall':sall})

def watchman_suggestion_box(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])    
        user_id=User.objects.get(role="Chairman")
        print("-->",user_id)
        cid = Chairman.objects.get(user_id=user_id)  
        wid = Watchman.objects.get(user_id=uid)
        if request.POST:
            subject = request.POST['subject']
            description = request.POST['description']

            sid = Suggestions.objects.create(user_id = uid, subject=subject, description=description)
            sall = Suggestions.objects.order_by('-created_at')
            return render(request,"secretary/dashboard/watchman_suggestion_box.html",{'uid':uid,'wid':wid,'sall':sall,'sid':sid,'cid':cid})
        else:
            return render(request,"secretary/dashboard/add_watchman_suggestions.html",{'uid':uid,'wid':wid,'cid':cid})
    else:
        return HttpResponseRedirect(reverse('login'))

def view_watchman_suggestion_box(request):
    uid = User.objects.get(email = request.session['email']) 
    user_id=User.objects.get(role="Chairman")
    print("-->",user_id)
    cid = Chairman.objects.get(user_id=user_id)     
    wid = Watchman.objects.get(user_id=uid)
    sall = Suggestions.objects.order_by('-created_at')
    return render(request,"secretary/dashboard/watchman_suggestion_box.html",{'uid':uid,'wid':wid,'sall':sall,'cid':cid})


def delete_watchman_suggestion(request,pk):
    if "email" in request.session:
        uid=User.objects.get(email=request.session['email'])
        wid=Watchman.objects.get(user_id=uid)
        Suggestions.objects.filter(id=pk).delete()
        # nall=NoticeBoard.objects.get(id=pk)
        # nall.delete()
        sall = Suggestions.objects.order_by('-created_at')
        return render(request,"secretary/dashboard/watchman_suggestion_box.html",{'uid':uid,'wid':wid,'sall':sall})

def view_chairman_suggestion_box(request):
    uid = User.objects.get(email = request.session['email'])      
    cid = Chairman.objects.get(user_id=uid)
    sall = Suggestions.objects.order_by('-created_at')
    return render(request,"secretary/dashboard/chairman_suggestion_box.html",{'uid':uid,'sall':sall,'cid':cid})

def delete_chairman_suggestion(request,pk):
    if "email" in request.session:
        uid=User.objects.get(email=request.session['email'])
        cid=Chairman.objects.get(user_id=uid)
        Suggestions.objects.filter(id=pk).delete()
        # nall=NoticeBoard.objects.get(id=pk)
        # nall.delete()
        sall = Suggestions.objects.order_by('-created_at')
        return render(request,"secretary/dashboard/chairman_suggestion_box.html",{'uid':uid,'sall':sall,'cid':cid})

def add_vistiors(request):
    uid = User.objects.get(email = request.session['email'])    
    wid = Watchman.objects.get(user_id=uid)
    user_id = User.objects.get(role="Chairman")
    cid = Chairman.objects.get(user_id=user_id)
    all_visitors = Vistiors.objects.filter(user_id=uid)
   
    if request.POST:
        member_firstname = request.POST['member_firstname']
        visitor_firstname = request.POST['visitor_firstname']
        description = request.POST['description']
        house_no = request.POST['house_no']
        vechicle_deatails = request.POST['vechicle_deatails']
        contact = request.POST['contact']
        gender = request.POST['gender']
        currentdate = request.POST['currentdate']
        time = request.POST['time']
        house_no =  request.POST['house_no']

        Vistiors.objects.create(user_id=uid,description=description,member_firstname=member_firstname,visitor_firstname=visitor_firstname,contact=contact,house_no=house_no,gender=gender,vechicle_deatails=vechicle_deatails,currentdate=currentdate,time=time)
        
        return render(request,'secretary/dashboard/add_my_visitor.html',{'uid':uid,'wid':wid,'cid':cid})
    else:
        return render(request,'secretary/dashboard/add_my_visitor.html',{'uid':uid,'wid':wid,'all_visitors':all_visitors,'cid':cid})

def allvisitors(request):
    uid = User.objects.get(email = request.session['email'])
    user_id = User.objects.get(role="Chairman")
    cid = Chairman.objects.get(user_id=user_id) 
    wid = Watchman.objects.get(user_id=uid)
    vall = Vistiors.objects.order_by('-created_at') # retrive all data from the model
      
    return render(request,'secretary/dashboard/Allvisitors.html',{'uid':uid,'wid':wid,'vall':vall,'cid':cid})

def vistiordetails(request,d_pk):
    vid = Vistiors.objects.get(id = d_pk)  # for respective selected user
    uid = User.objects.get(email = request.session['email'])  # for logged in
    wid = Watchman.objects.get(user_id=uid)
    return render(request,'secretary/dashboard/visitor_details.html',{'uid':uid,'vid':vid,'wid':wid})

def image_gallery(request):
    uid = User.objects.get(email = request.session['email'])  # for logged in
    mid = Members.objects.get(user_id=uid)
    user_id = User.objects.get(role="Chairman")
    cid = Chairman.objects.get(user_id=user_id)
    
    return render(request,'secretary/dashboard/image-gallery.html',{'uid':uid,'cid':cid,'mid':mid})

def image_gallery_chairman(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])  # for logged in
        if uid.role == "Chairman":
            cid = Chairman.objects.get(user_id=uid)
            
            return render(request,'secretary/dashboard/image-gallery-chairman.html',{'uid':uid,'cid':cid})
        else:
            return render(request,'secretary/dashboard/image-gallery-chairman2.html',{'uid':uid})
    else:
        return render(request,'secretary/dashboard/image-gallery-chairman2.html')
     
def image_gallery_watchman(request):
    user_id = User.objects.get(role="Chairman")
    cid = Chairman.objects.get(user_id=user_id)
    uid = User.objects.get(email = request.session['email'])  # for logged in
    wid = Watchman.objects.get(user_id=uid)
   
    return render(request,'secretary/dashboard/image-gallery-watchman.html',{'uid':uid,'wid':wid,'cid':cid})

def watchman_event_view(request):
    uid = User.objects.get(email = request.session['email'])   
    user_id = User.objects.get(role="Chairman")
    cid = Chairman.objects.get(user_id=user_id) 
    wid = Watchman.objects.get(user_id=uid)
    eall = Events.objects.order_by('-created_at')
    return render(request,"secretary/dashboard/watchman-event-details.html",{'uid':uid,'wid':wid,'eall':eall,'cid':cid})

# def my_vistiordetails(request,pk):
#     vid = Vistiors.objects.get(id = pk) 
#     uid = User.objects.get(email = request.session['email'])
#     user_id = User.objects.get(role="Chairman")
#     cid = Chairman.objects.get(user_id=user_id) 
#     mid = Members.objects.get(user_id=uid)
#     vall = Vistiors.objects.get(user_id=uid) # retrive all data from the model
      
#     return render(request,"secretary/dashboard/myvisitors.html"{'uid':uid,'user_id':user_id,'cid':cid,'mid':mid,'vall':vall,'vid':vid})

# def add_photo(request):
#     if request.POST:
#         audio = request.FILES['audio']
#         aid = Audio.objects.create(audio=audio)
#         return render(request,"myapp/index.html")

def house_on_rent(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])    
        mid = Members.objects.get(user_id=uid)
        user_id = User.objects.get(role="Chairman")
        cid = Chairman.objects.get(user_id=user_id)
        if request.POST:
            subject = request.POST['subject']
            description = request.POST['description']
            h_no = request.POST['h_no']
            bhk = request.POST['bhk']
            h_price = request.POST['h_price']
            contact = request.POST['contact']
            if "noticepic" in request.FILES:
                noticepic = request.FILES['noticepic']
                rid = Rent.objects.create(user_id=uid,subject=subject,h_no=h_no,bhk=bhk,h_price=h_price,contact=contact,description=description,profile_pic=noticepic)
            else:
                rid = Rent.objects.create(user_id=uid,subject=subject,h_no=h_no,bhk=bhk,h_price=h_price,contact=contact,description=description)
                rall = Rent.objects.order_by('-created_at')
                return render(request,"secretary/dashboard/house_on_rent_view_details.html",{'uid':uid,'mid':mid,'cid':cid,'rall':rall})
            rall = Rent.objects.order_by('-created_at')
            return render(request,"secretary/dashboard/house_on_rent_view_details.html",{'uid':uid,'mid':mid,'cid':cid,'rall':rall})
        else:
            return render(request,"secretary/dashboard/house_on_rent.html",{'uid':uid,'cid':cid,'mid':mid})
    else:
        return HttpResponseRedirect(reverse('login'))

def house_on_rent_view(request):
    uid = User.objects.get(email = request.session['email'])    
    mid = Members.objects.get(user_id=uid)
    user_id = User.objects.get(role="Chairman")
    cid = Chairman.objects.get(user_id=user_id)
    rall = Rent.objects.order_by('-created_at')
    return render(request,"secretary/dashboard/house_on_rent_view_details.html",{'uid':uid,'mid':mid,'cid':cid,'rall':rall})

def delete_member_house_on_rent(request,pk):
    if "email" in request.session:
        uid=User.objects.get(email=request.session['email'])
        mid=Members.objects.get(user_id=uid)
        Rent.objects.filter(id=pk).delete()
        # nall=NoticeBoard.objects.get(id=pk)
        # nall.delete()
        rall = Rent.objects.order_by('-created_at')
        return render(request,"secretary/dashboard/house_on_rent_view_details.html",{'uid':uid,'mid':mid,'rall':rall})

def chairman_house_on_rent(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email'])    
        cid = Chairman.objects.get(user_id=uid)
        if request.POST:
            subject = request.POST['subject']
            description = request.POST['description']
            h_no = request.POST['h_no']
            bhk = request.POST['bhk']
            h_price = request.POST['h_price']
            contact = request.POST['contact']
            if "noticepic" in request.FILES:
                noticepic = request.FILES['noticepic']
                rid = Rent.objects.create(user_id = uid, subject=subject,h_no=h_no,bhk=bhk,h_price=h_price,contact=contact,description=description,profile_pic=noticepic)
            else:
                rid = Rent.objects.create(user_id = uid, subject=subject,h_no=h_no,bhk=bhk,h_price=h_price,contact=contact, description=description)
                
                rall = Rent.objects.order_by('-created_at')
                return render(request,"secretary/dashboard/chairman_house_on_rent_view_details.html",{'uid':uid,'cid':cid,'rall':rall})
            rall = Rent.objects.order_by('-created_at')
            return render(request,"secretary/dashboard/chairman_house_on_rent_view_details.html",{'uid':uid,'cid':cid,'rall':rall})
        else:
            return render(request,"secretary/dashboard/chairman_house_on_rent.html",{'uid':uid,'cid':cid})
    else:
        return HttpResponseRedirect(reverse('login'))

def chairman_house_on_rent_view(request):
    if "email" in request.session:
        uid = User.objects.get(email = request.session['email']) 
          
        if uid.role=="Chairman":
            cid = Chairman.objects.get(user_id=uid)
            rall = Rent.objects.order_by('-created_at') 
            return render(request,"secretary/dashboard/chairman_house_on_rent_view_details.html",{'uid':uid,'cid':cid,'rall':rall})
        else:
            rall = Rent.objects.order_by('-created_at') 
            return render(request,"secretary/dashboard/chairman_house_on_rent_view_details.html",{'rall':rall})
    else:
        rall = Rent.objects.order_by('-created_at') 
        return render(request,"secretary/dashboard/chairman_house_on_rent_view_details2.html",{'rall':rall})
def delete_chairman_house_on_rent(request,pk):
    if "email" in request.session:
        uid=User.objects.get(email=request.session['email'])
        cid=Chairman.objects.get(user_id=uid)
        Rent.objects.filter(id=pk).delete()
        # nall=NoticeBoard.objects.get(id=pk)
        # nall.delete()
        rall = Rent.objects.order_by('-created_at')
        return render(request,"secretary/dashboard/chairman_house_on_rent_view_details.html",{'uid':uid,'cid':cid,'rall':rall})

def approve_members(request,pk):
    uid = User.objects.get(email = request.session['email'])
    cid = Chairman.objects.get(user_id = uid)
    
    
    mid = Members.objects.get(id = pk)
    mid.status = "True"
    mid.save()

    subject = "WELCOME TO Digital-Society"
                
   
    sendmail(subject,'members_maintemplate',mid.user_id.email,{'firstname': mid.firstname, 'password':mid.user_id.password})
    return render(request,"secretary/dashboard/index.html",{'uid':uid,'cid':cid})
