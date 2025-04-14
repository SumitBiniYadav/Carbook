from django.shortcuts import render,redirect
from . models import *
import random
import requests
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import razorpay
from django.shortcuts import get_object_or_404
import pkg_resources
from django.core.mail import send_mail
from django.core.paginator import Paginator
from .models import Booking
from .utils import generate_invoice_pdf
from django.db.models import Sum, Avg, Count
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def signup(request):
    if request.method=="POST":
        try:
            user = user.objects.get(email=request.POST['email'])
            msg = "User already exists !"
            return render(request,'signup.html',{'msg':msg})
        
        except:
            if request.POST['password']==request.POST['cpassword']:
                User.objects.create(
                    name=request.POST['name'],
                    email=request.POST['email'],
                    mobile = request.POST['mobile'],
                    password=request.POST['password'],
                    profile=request.FILES['profile'],
                    usertype=request.POST['usertype']
                )
                msg = "User created successfully !"
                return render(request,'signup.html',{'msg':msg})
            else:
                msg = "Password and Confirm Password does not match !"
                return render(request,'signup.html',{'msg':msg})
    else:
        return render(request,'signup.html')
    
@csrf_exempt
def login(request):
    if request.method=="POST":
        try:
            user = User.objects.get(email=request.POST['email'])
            if user.password == request.POST['password']:
                request.session['email'] = user.email
                request.session['profile']=user.profile.url

                if user.usertype == 'user':
                    return redirect('index')
                
                else:
                    return redirect('lindex')
            else:
                msg = "Password is incorrect !"
                return render(request,'login.html',{'msg':msg})
        
        except:
            msg = "User not found !"
            return render(request,'login.html',{'msg':msg})
    else:    
        return render(request, 'login.html')
    

def logout(request):
    del request.session['profile']
    del request.session['email']
    return redirect('login')
    
    

def changepass(request):
    if request.method =="POST":
        try:
            user=User.objects.get(email=request.session['email'])
            if request.POST['opassword']==user.password:
                if request.POST['npassword']==request.POST['cnpassword']:
                    user.password=request.POST['npassword']
                    user.save()
                    msg="Password changed successfully !"
                    return render(request,'changepass.html',{'msg':msg})
                else:
                    msg="New Password and Confirm New Password does not match !"
                    return render(request,'changepass.html',{'msg':msg})
            else:
                msg="Old Password is incorrect !"
                return render(request,'changepass.html',{'msg':msg})
        except:
            return redirect('login')
        
    else:
        return render(request,'changepass.html')
    

def fpass(request):
    if request.method == "POST":
        try:
            email = request.POST.get('email')
            user = User.objects.get(email=email)
            
            otp = random.randint(1001, 9999)
            subject = "OTP for Password Reset"
            message = f"""
                        Dear User,

                        We received a request to reset your password. Please use the One-Time Password (OTP) below to proceed with resetting your account password:

                        Your OTP: {otp}

                        This OTP is valid for the next 10 minutes. Please do not share this code with anyone for security reasons. If you did not request a password reset, please ignore this email or contact our support team immediately.

                        Thank you,  
                        CarBook Support Team
                        """
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email]
            
            send_mail(subject, message, email_from, recipient_list)

            request.session['email'] = user.email
            request.session['otp'] = otp
            return render(request, 'otp.html')

        except User.DoesNotExist:
            msg = "Invalid Email ID!"
            return render(request, 'fpass.html', {'msg': msg})

    return render(request, 'fpass.html')


def otp(request):
    if request.method == "POST":
        try:
            otp = int(request.session.get('otp', 0))
            uotp = int(request.POST.get('uotp', 0))

            if otp == uotp:
                del request.session['otp']
                return render(request, 'newpass.html')
            else:
                msg = "Invalid OTP!"
                return render(request, 'otp.html', {'msg': msg})

        except (ValueError, TypeError):
            msg = "An error occurred. Please try again."
            return render(request, 'otp.html', {'msg': msg})

    return render(request, 'otp.html')


def newpass(request):
    if request.method == "POST":
        try:
            email = request.session.get('email')
            user = User.objects.get(email=email)

            npassword = request.POST.get('npassword')
            cnpassword = request.POST.get('cnpassword')

            if npassword == cnpassword:
                user.password = request.POST['npassword']
                user.save()
                del request.session['email']
                return render(request, 'login.html')
            else:
                msg = "New Password and Confirm New Password do not match!"
                return render(request, 'newpass.html', {'msg': msg})

        except User.DoesNotExist:
            msg = "User not found. Please try again."
            return render(request, 'newpass.html', {'msg': msg})

    return render(request, 'newpass.html')

def uprofile(request):
    user=User.objects.get(email=request.session['email'])

    if request.method=="POST":
        user.name=request.POST['name']
        user.email=request.POST['email']
        user.mobile=request.POST['mobile']
        user.profile=request.FILES['profile']
        user.save()
        request.session['profile']=user.profile.url
        return redirect('index')
    
    else:
        return render(request,'uprofile.html',{'user':user})
    



def add(request):
    if request.method=="POST":
        lessor = User.objects.get(email = request.session['email'])
        try:
            Car.objects.create(
                lessor = lessor,
                stransmission = request.POST['stransmission'],
                sfuel = request.POST['sfuel'],
                cname = request.POST['cname'],
                mileage = request.POST['mileage'],
                seats = request.POST['seats'],
                luggage = request.POST['luggage'],
                desc = request.POST['desc'],
                air='air' in request.POST,
                gps='gps' in request.POST,
                Child_Seat='Child_Seat' in request.POST,
                Music='Music' in request.POST,
                Bluetooth='Bluetooth' in request.POST,
                Car_Kit='Car_Kit' in request.POST,
                Climate_control='Climate_control' in request.POST,
                Seat_Belt='Seat_Belt' in request.POST,
                ABS='ABS' in request.POST,
                Airbag='Airbag' in request.POST,
                Parking_Sensor='Parking_Sensor' in request.POST,
                Camera='Camera' in request.POST,
                Cruise_Control='Cruise_Control' in request.POST,
                cimage = request.FILES['cimage'],
                hprice = request.POST['hprice'],
                dprice = request.POST['dprice'],
                mprice = request.POST['mprice']
            )
            return redirect('lcar')
        
        except Exception as e:
            print("********************",e)
            msg = "Car not added !"
            return render(request,'add.html',{'msg':msg})
    else:
        return render(request,'add.html')





def services(request):
    return render(request,'services.html')

def about(request):
    return render(request,'about.html')

def labout(request):
    return render(request,'labout.html')


def lchangepass(request):
    if request.method =="POST":
        try:
            user=User.objects.get(email=request.session['email'])
            if request.POST['opassword']==user.password:
                if request.POST['npassword']==request.POST['cnpassword']:
                    user.password=request.POST['npassword']
                    user.save()
                    msg="Password changed successfully !"
                    return render(request,'lchangepass.html',{'msg':msg})
                else:
                    msg="New Password and Confirm New Password does not match !"
                    return render(request,'lchangepass.html',{'msg':msg})
            else:
                msg="Old Password is incorrect !"
                return render(request,'lchangepass.html',{'msg':msg})
        except:
            return redirect('login')
        
    else:
        return render(request,'lchangepass.html')
    


def luprofile(request):
    user=User.objects.get(email=request.session['email'])

    if request.method=="POST":
        user.name=request.POST['name']
        user.email=request.POST['email']
        user.mobile=request.POST['mobile']
        user.profile=request.FILES['profile']
        user.save()
        request.session['profile']=user.profile.url
        return redirect('lindex')
    
    else:
        return render(request,'luprofile.html',{'user':user})



def lcar(request):
    lessor = User.objects.get(email=request.session['email'])
    car_list = Car.objects.filter(lessor=lessor)
    
    # Pagination
    paginator = Paginator(car_list, 6)  # Show 6 cars per page
    page = request.GET.get('page', 1)
    
    try:
        cars = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        cars = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        cars = paginator.page(paginator.num_pages)
    
    return render(request, 'lcar.html', {
        'car': cars,
        'paginator': paginator
    })


def details(request,pk):
    lessor = User.objects.get(email=request.session['email'])
    car = Car.objects.get(pk=pk)
    return render(request,'details.html',{'car':car})



def lpricing(request):
    try:
        lessor = User.objects.get(email=request.session['email'])
        car = Car.objects.filter(lessor=lessor)
        return render(request,'lpricing.html',{'car':car})
    except Exception as e:
        print("*****************",e)
        msg ="You are not logged in !"
        return render(request,'login.html',{'msg':msg})


def updatee(request,pk):
    lessor = User.objects.get(email=request.session['email'])
    car = Car.objects.get(pk=pk)

    if request.method=="POST":
        car.stransmission = request.POST['stransmission']
        car.sfuel = request.POST['sfuel']
        car.cname = request.POST['cname']
        car.mileage = request.POST['mileage']
        car.seats = request.POST['seats']
        car.luggage = request.POST['luggage']
        car.hprice = request.POST['hprice']
        car.dprice = request.POST['dprice']
        car.mprice = request.POST['mprice']
        car.desc = request.POST['desc']
        car.air='air' in request.POST
        car.gps='gps' in request.POST
        car.Child_Seat='Child_Seat' in request.POST
        car.Music='Music' in request.POST
        car.Bluetooth='Bluetooth' in request.POST
        car.Car_Kit='Car_Kit' in request.POST
        car.Climate_control='Climate_control' in request.POST
        car.Seat_Belt='Seat_Belt' in request.POST
        car.ABS='ABS' in request.POST
        car.Airbag='Airbag' in request.POST
        car.Parking_Sensor='Parking_Sensor' in request.POST
        car.Camera='Camera' in request.POST
        car.Cruise_Control='Cruise_Control' in request.POST
        car.save()

        try:
            car.cimage = request.FILES['cimage']
            car.save()

        except:
            pass

        return redirect('lcar')
    else:
        return render(request,'updatee.html', {'car':car})



def delete(request,pk):
    lessor = User.objects.get(email=request.session['email']) 
    car = Car.objects.get(pk=pk)
    car.delete()
    return redirect('lcar')


def lindex(request):
    try:
        lessor = User.objects.get(email=request.session['email'])
        cars = Car.objects.filter(lessor=lessor)
        return render(request,'lindex.html',{'cars':cars})
    
    except Exception as e:
        print("**********",e)
        msg = "Please Login First !"
        return render(request,'login.html',{'msg':msg})



def car(request):
    try:
        query = request.GET.get('q', '') 
        print("Received Query:", query)     
        if query:
            cars = Car.objects.filter(cname__icontains=query)
        else:
            cars = Car.objects.all()
            
        # Set up pagination - show 6 cars per page
        # You can change this number to determine how many cars appear on each page
        per_page = 6
        paginator = Paginator(cars, per_page)
        page_number = request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        # We're only sending page_obj to the template
        return render(request, 'car.html', {'car': page_obj})
    except Exception as e:
        print("Error:", e)
        msg = "Please Login First!"
        return render(request, 'login.html', {'msg': msg})

      

def pricing(request):
    try:
        car_list = Car.objects.all()
        paginator = Paginator(car_list, 4)  
        page = request.GET.get('page', 1)
        
        try:
            cars = paginator.page(page)
        except PageNotAnInteger:
            cars = paginator.page(1)
        except EmptyPage:
            cars = paginator.page(paginator.num_pages)
        
        return render(request, 'pricing.html', {
            'car': cars,  
            'paginator': paginator
        })
    
    except Exception as e:
        print("*****************", e)
        msg = "Please Login First!"
        return render(request, 'login.html', {'msg': msg})



def index(request):
    car = Car.objects.all()
    return render(request,'index.html',{'car':car})

def idetails(request, pk):
    try:
        lessor = User.objects.get(email=request.session['email'])
        car = Car.objects.get(pk=pk)
        related_cars = Car.objects.exclude(pk=pk)[:3]  # Example: showing 3 related cars
        related_reviews = Review.objects.filter(car=car)
        print(related_cars)
        print(related_reviews)

        if request.method == 'POST':
            lessor = User.objects.get(email=request.session['email'])
            car = Car.objects.get(pk=pk)
            review = request.POST['review']
            rating = request.POST['rating']
            Review.objects.create(
                user = lessor,
                car = car,
                review = review,
                rating = rating
            )
            return redirect('idetails', pk=pk)
        else:
            return render(request,'idetails.html',{'car':car,'lessor':lessor, 'related_cars': related_cars})

    except Exception as e:
        print("*****************",e)
        msg = "Please Login First !"
        return render(request,'login.html',{'msg':msg})
    
      


def cart(request, pk):
    try:
        user = User.objects.get(email=request.session['email'])
        car = Car.objects.get(pk=pk)

        if request.method == 'POST':
            user = User.objects.get(email=request.session['email'])
            car = Car.objects.get(pk=pk)

            Booking.objects.create(
                user=user,
                car=car,
                pickup_address=request.POST['pickup_address'],
                drop_address=request.POST['drop_address'],
                start_date=request.POST['start_date'],
                end_date=request.POST['end_date'],
                pick_time=request.POST['pick_time'],
                total_days=int(request.POST['total_days']),  
                total_amount=int(request.POST['total_days']) * car.dprice  
            )
            return redirect('summary',pk=pk)
        else:
            return render(request, 'cart.html', {'car': car, 'user': user})

    except Exception as e:
        print("*****************",e)
        msg = "Please Login First !"
        return render(request,'login.html',{'msg':msg})
    
def summary(request, pk):
    try:
        user = User.objects.get(email=request.session['email'])
        car = Car.objects.get(pk=pk)
        booking = Booking.objects.get(user=user, car=car)
        net = booking.total_amount


       
        client = razorpay.Client(auth = (settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
        payment = client.order.create({'amount':  net* 100, 'currency': 'INR', 'payment_capture': 1})
        
        context = {
                        'payment': payment,
                        #'book':book,  # Ensure the amount is in paise
                    }
    


        return render(request, 'summary.html', {'car': car, 'user': user, 'booking': booking,'net':net,'context':context})
    except Exception as e:
        print("*****************",e)
        msg = "Please Login First !"
        return render(request,'login.html',{'msg':msg})
    

def success(request):
    try:
        payment_id = request.GET.get('razorpay_payment_id')
        user = User.objects.get(email=request.session['email'])
        booking = Booking.objects.filter(user=user).order_by('-id')[0]  # Get the latest booking

        
        # You might want to store the payment_id with the booking
        booking.payment_id = payment_id  # Add this field to your model
        booking.payment_status = True
        booking.save()
        
        return render(request, 'success.html', {'booking': booking})
    
    except Exception as e:
        print(e)
        return render(request, 'index.html')



def mybooking(request):
    try:
        user = User.objects.get(email=request.session['email'])
        booking = Booking.objects.filter(user=user).order_by('-id')
        return render(request, 'mybooking.html',{'booking':booking})
    except Exception as e:
        print("*****************",e)
        msg = "Please Login First !"
        return render(request,'login.html',{'msg':msg})
    
from django.shortcuts import render, get_object_or_404
from .models import User, Booking, Car  # Ensure models are imported

def bookdetail(request, booking_id): 
    try:
        booking = get_object_or_404(Booking, pk=booking_id)
        return render(request, 'bookdetail.html', {'booking': booking})
    except Exception as e:
        print("*****************",e)
        msg = "Please Login First !"
        return render(request,'login.html',{'msg':msg})

def bookreq(request):
    try:
        lessor = User.objects.get(email=request.session['email'])
        cars = Car.objects.filter(lessor=lessor)  # Get all cars owned by the user
        bookings = Booking.objects.filter(car__in=cars).order_by('-id')  # Filter bookings for user's cars
        print(bookings)
        return render(request, 'bookreq.html', {'bookings': bookings})
    except Exception as e:
        print("*****************", e)
        msg = "Please Login First !"
        return render(request, 'login.html', {'msg': msg}) 

def approve_req(request):
    try:
        booking_id = request.GET.get('booking_id')
        booking = Booking.objects.get(pk=booking_id)
        booking.status = True
        booking.save()
        return redirect('bookreq')
    except Exception as e:
        print("*****************", e)
        msg = "Please Login First !"
        return render(request, 'login.html', {'msg': msg})
    

def decline_req(request):
    try:
        booking_id = request.GET.get('booking_id')
        booking = Booking.objects.get(pk=booking_id)
        booking.reject_status = True
        booking.save()
        return redirect('bookingreq')
    except Exception as e:
        print("*****************", e)
        msg = "Please Login First !"
        return render(request, 'login.html', {'msg': msg})
    


def download_invoice(request,booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    print(booking)
    return generate_invoice_pdf(booking)


def earning(request):
    if 'email' in request.session:  # Ensure user is logged in
        try:
            lessor = User.objects.get(email=request.session['email'])
            
            # Get all bookings for cars owned by this lessor
            bookings = Booking.objects.filter(car__lessor=lessor, payment_status=True)
           

            # Total earnings
            total_earnings = bookings.aggregate(total=Sum('total_amount'))['total'] or 0

            # Total number of rentals
            total_rentals = bookings.count()

            # Average rental duration (in days)
            avg_duration = bookings.aggregate(avg_days=Avg('total_days'))['avg_days'] or 0

            # Utilization Rate (Percentage of rented days vs total available days)
            total_cars = Car.objects.filter(lessor=lessor).count()
            total_days_rented = bookings.aggregate(days=Sum('total_days'))['days'] or 0
            total_available_days = total_cars * 30  # Assuming a 30-day month

            utilization_rate = (total_days_rented / total_available_days * 100) if total_available_days else 0

            context = {
                'total_earnings': total_earnings,
                'total_rentals': total_rentals,
                'avg_duration': round(avg_duration, 2),
                'utilization_rate': round(utilization_rate, 2)
            }

  

            return render(request, 'earning.html', context)

        except User.DoesNotExist:
            return redirect('login')  #
    else:
        return redirect('login')  