from django.db import models
from doctor.models import Doctordata

# Create your models here.
class Response(models.Model):
    ack = (
            ('approved', 'Approved'),
            ('declined', 'Declined'),
            ('Pending', 'Pending'),
        )
    ack1 = (
            ('approved', 'Approved'),
            ('declined', 'Declined'),
            ('Pending', 'Pending'),
        )
    responseid = models.AutoField
    doctorack = models.CharField(max_length= 30, blank = True, null = True, choices= ack)
    userack = models.CharField(max_length= 30, blank = True, null = True, choices= ack1)
    patientid = models.CharField(max_length= 30, blank = True, null = True)
    userid = models.CharField(max_length= 30, blank = True, null = True)
    doctorid = models.ForeignKey(Doctordata, on_delete=models.CASCADE)
    