from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    mobile = models.BigIntegerField()
    password = models.CharField(max_length=20)
    profile = models.ImageField(default="")
    usertype = models.CharField(max_length=20,default="user")

    def __str__(self):
        return self.name

class Car(models.Model):

    lessor = models.ForeignKey(User,on_delete=models.CASCADE)

    transmission = (
        ('Manual','Manual'),
        ('Auto','Auto')
    )

    fuel = (
        ('Petrol','Petrol'),
        ('Diesel','Diesel'),
        ('Electric','Electric'),
        ('Hybrid','Hybrid'),
        ('CNG','CNG')
    )

    
    sfuel = models.CharField(max_length=50,choices=fuel)
    stransmission = models.CharField(max_length=50,choices=transmission)
    cname = models.CharField(max_length=100)
    mileage = models.IntegerField()
    seats = models.IntegerField()
    luggage = models.IntegerField()
    desc = models.TextField()   
    air  = models.BooleanField(default=False)
    gps = models.BooleanField(default=False)
    Child_Seat = models.BooleanField(default=False)
    Music = models.BooleanField(default=False)
    Bluetooth = models.BooleanField(default=False)
    Car_Kit = models.BooleanField(default=False)
    Climate_control = models.BooleanField(default=False)
    Seat_Belt = models.BooleanField(default=False)
    ABS = models.BooleanField(default=False)
    Airbag = models.BooleanField(default=False)
    Parking_Sensor = models.BooleanField(default=False)
    Camera = models.BooleanField(default=False)
    Cruise_Control = models.BooleanField(default=False)
    cimage = models.ImageField(default="user.png")

    hprice = models.IntegerField(default=0)
    dprice = models.IntegerField(default=0)
    mprice = models.IntegerField(default=0)


    def __str__(self):
        return self.cname
    



class Review(models.Model):
    STAR_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.IntegerField(choices=STAR_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} - {self.car.cname} ({self.rating} Stars)"
    


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    pickup_address = models.TextField()
    drop_address = models.TextField()
    pick_time = models.TimeField()
    total_days = models.IntegerField()
    total_amount = models.IntegerField()
    payment_status = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    reject_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name} - {self.car.cname} ({self.start_date} - {self.end_date})"

