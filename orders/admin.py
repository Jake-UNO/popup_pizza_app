import csv
import datetime
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from .views import admin_order_detail
from .models import Order, OrderItem, Event, PickupSlot
from django.urls import reverse
from django.utils.safestring import mark_safe

def order_detail(obj):
    return mark_safe('<a href="{}">View</a>'.format(
        reverse('orders:admin_order_detail', args=[obj.id])))

 
def export_to_csv(modeladmin, request, queryset): 
    opts = modeladmin.model._meta 
    response = HttpResponse(content_type='text/csv') 
    response['Content-Disposition'] = 'attachment;' \
        'filename={}.csv'.format(opts.verbose_name) 
    writer = csv.writer(response) 
     
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many] 
    # Write a first row with header information 
    writer.writerow([field.verbose_name for field in fields]) 
    # Write data rows 
    for obj in queryset: 
        data_row = [] 
        for field in fields: 
            value = getattr(obj, field.name) 
            if isinstance(value, datetime.datetime): 
                value = value.strftime('%d/%m/%Y') 
            data_row.append(value) 
        writer.writerow(data_row) 
    return response 
export_to_csv.short_description = 'Export to CSV' 


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'pickup_slot', 'payment_status', 'order_status',
                    'total_amount', 'created', 'updated', order_detail]
    list_display_links = ['id', 'first_name', 'last_name']
    list_filter = ['payment_status', 'order_status', 'created', 'updated']
    inlines = [OrderItemInline]

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:order_id>/',
                self.admin_site.admin_view(admin_order_detail),
                name='admin_order_detail',
            ),
        ]
        return custom_urls + urls
admin.site.register(Event)
admin.site.register(PickupSlot)