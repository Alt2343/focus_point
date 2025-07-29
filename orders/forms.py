from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'city', 
                'street', 'house', 'apartment', 'entrance', 'comment']
        
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+7 (___) ___-__-__'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Дополнительная информация для курьера'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'comment':
                self.fields[field].widget.attrs.update({'class': 'form-input'})
