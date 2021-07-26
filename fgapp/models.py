from django.db import models

class fgitem(models.Model):
    matno = models.TextField()


class users(models.Model):
    name = models.TextField()
    password = models.TextField()
    detail = models.TextField()
    def __unicode__(self):
        return self.name

class todayfg(models.Model):
    matno = models.TextField()
    matdes = models.TextField()
    plant = models.TextField()
    batch = models.TextField()
    platform = models.TextField()
    cus_name = models.TextField()
    kam_name = models.TextField()
    qty = models.TextField()
    value1 = models.TextField()
    concat = models.TextField(default='None')
    age = models.TextField()
    log_remarks = models.TextField()
    log_des_advice = models.CharField(max_length=200)
    kam_qty_clear = models.TextField()
    kam_des_adv = models.TextField(default='No')
    kam_remarks = models.CharField(max_length=200)
    kam_des_date = models.TextField()


    def __unicode__(self):
        return self.cus_name

class todayfg_old(models.Model):
    matno = models.TextField()
    matdes = models.TextField()
    plant = models.TextField()
    batch = models.TextField()
    platform = models.TextField()
    cus_name = models.TextField()
    kam_name = models.TextField()
    qty = models.TextField()
    value1 = models.TextField()
    concat = models.TextField(default='None')
    age = models.TextField()
    log_remarks = models.TextField()
    log_des_advice = models.CharField(max_length=200)
    kam_qty_clear = models.TextField()
    kam_remarks = models.CharField(max_length=200)
    kam_des_adv = models.TextField(default='No')
    kam_des_date = models.TextField()


    def __unicode__(self):
        return self.cus_name


# Create your models here.
