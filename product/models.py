from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=50, null=False, blank=False)
    product_price = models.IntegerField(null=False)
    product_stock = models.IntegerField(null=False, default=0)


    class Meta:
        db_table = 'tbl_product'
