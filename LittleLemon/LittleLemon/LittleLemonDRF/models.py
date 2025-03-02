from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    slugfield=models.SlugField()
    title=models.CharField(max_length=255,db_index=True)

class MenuItem(models.Model):
    title=models.CharField(max_length=255,db_index=True)
    price=models.DecimalField(max_digits=6, decimal_places=2,db_index=True)
    featured=models.BooleanField(db_index=True)
    category=models.ForeignKey(Category,on_delete=models.PROTECT)

class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem=models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity=models.SmallIntegerField()
    unit_price=models.DecimalField(max_digits=6,decimal_places=6)
    price=models.DecimalField(max_digits=6,decimal_places=6)

    class Meta:
        unique_together=('user', 'menuitem')


class Order(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew=models.ForeignKey(User, on_delete=models.SET_NULL,null=True,related_name='delivery_crew')
    status=models.BooleanField(db_index=True,default=0)
    total=models.DecimalField(max_digits=6,decimal_places=6)
    date=models.DateField(db_index=True)


class OrderItem(models.Model):
    order=models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem=models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity=models.DecimalField(max_digits=6,decimal_places=0)
    unit_price=models.DecimalField(max_digits=6,decimal_places=6)
    price=models.DecimalField(max_digits=6,decimal_places=6)


    class Meta:
        unique_together=('order','menuitem')






