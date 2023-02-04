from django import forms

from .models import Customer


class CustomerForm(forms.ModelForm):
    file = forms.FileField(required=False)

    class Meta:
        model = Customer
        fields = '__all__'


class EmailForm(forms.Form):
    email = forms.EmailField()
    cc = forms.EmailField(required=False)
    subject = forms.CharField(max_length=100)

    # Permitir la subida de multiples archivos
    attach = forms.FileField(
        required=False,
        widget= forms.ClearableFileInput(
            attrs= {
                'multiple': True
            }
        )
    )
    message = forms.CharField(widget = forms.Textarea)
    customer_status = forms.HiddenInput()
    customer_id = forms.HiddenInput()