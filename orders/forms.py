from django import forms
from django.db.models import F
from .models import Order, PickupSlot


class OrderCreateForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'pickup_slot']
        widgets = {
            'pickup_slot': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # only show pickup slots that still have capacity
        self.fields['pickup_slot'].queryset = PickupSlot.objects.filter(
            current_orders__lt=F('max_orders')
        )