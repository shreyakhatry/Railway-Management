from django.conf import settings
from django.db import models

# Create your models here. 

class Station(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    station_name = models.CharField(max_length=40, default="")
    station_code = models.CharField(max_length=10, default="")

    class Meta:
        verbose_name_plural = 'Stations'

    def __str__(self):
        return str(self.station_name)
    
    

class Train(models.Model):
    train_number = models.CharField(max_length=10, primary_key=True)
    train_name = models.CharField(max_length=30)
    train_source = models.ForeignKey('Station', related_name='start', on_delete=models.CASCADE)
    train_destination = models.ForeignKey('Station', related_name='end', on_delete=models.CASCADE)
    first_ac = models.IntegerField(default=10) # seats available in first ac
    second_ac = models.IntegerField(default=10) # seats available in second ac
    third_ac = models.IntegerField(default=10) # seats available in third ac
    sleeper = models.IntegerField(default=10) # seats available in sleeper
    days_availability = models.CharField(max_length=15) # availability of the train

    class Meta:
        verbose_name_plural = 'Trains'

    def __str__(self):
        return str(self.train_name) + ' - ' + str(self.train_number)

    def updateFirstAc(self):
        self.first_ac-=1
        self.save()
    def updateSecondAc(self):
        self.second_ac-=1
        self.save()
    def updateThirdAc(self):
        self.third_ac-=1
        self.save()
    def updateSleeper(self):
        self.sleeper-=1
        self.save()


class Route(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    source = models.ForeignKey('Station', related_name='source', on_delete=models.CASCADE)
    destination = models.ForeignKey('Station', related_name='destination', on_delete=models.CASCADE)
    train = models.ManyToManyField(Train)
    arrival = models.TimeField()
    departure = models.TimeField()

    class Meta:
        verbose_name_plural = 'Routes'

    def __str__(self):
        return str(self.source) + ' to ' + str(self.destination)


class Ticket(models.Model):
    pnr = models.CharField(max_length=10)
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    train = models.ForeignKey('Train', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    seatclass = models.CharField(max_length=5,default='Sl')
    doj=models.DateField()
    boarding_station = models.ForeignKey('Station', on_delete=models.CASCADE)

    def __str__(self):
        return (self.first_name + ' ' + self.last_name + ' '
                + self.seatclass + ' in ' + str(self.train))

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name