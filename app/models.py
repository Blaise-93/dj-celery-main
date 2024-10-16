from django.db import models
from django_tenants.models import TenantMixin, DomainMixin


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Company name:{self.name[0:30]}...'

    class Meta:
        ordering = ['-date_created']
    
class Domain(DomainMixin):
    pass

class Subfolder(models.Model):
    name = models.CharField(max_length=100)
    tenant = models.ForeignKey(Client, related_name='subfolders', on_delete=models.CASCADE)


""" 

from clients.models import Client, Domain

# Create a tenant
tenant1 = Client(schema_name='tenant1', name='Tenant 1')
tenant1.save()
 
# Create a domain for the tenant
domain1 = Domain(domain='tenant1.yourdomain.com', tenant=tenant1)
domain1.save()

# Create a subfolder for the tenant (if required)
subfolder1 = Subfolder(name='tenant1', tenant=tenant1)
subfolder1.save()


subfolder = Subfolder(name="johnny", tenant=tenant) 

python manage.py migrate_schema --shared

domain=Domain(domain="bigvo.localhost", tenant=tenant, is_primary=True)
>>> domain.save()
>>> tenant = Client(schema_name="HealthPlus", name="HealthPlus Pharmaceuticals")
>>> tenant.save()

"""