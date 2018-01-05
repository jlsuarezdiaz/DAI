# restaurants/forms.py

from django import forms
from .models import BoroughNY
from django.core.exceptions import ValidationError

def valida_codigo_postal(value):
    if value < 10000 or value > 99999:
        raise ValidationError('%s no es un código postal válido' % value)

def valida_coord_N(value):
    if value < -90.0 or value > 90.0:
        raise ValidationError('Las coordenadas de latitud deben tomar valores entre -90º y 90º')

def valida_coord_E(value):
    if value < -180.0 or value > 180.0:
        raise ValidationError('Las coordenadas de longitud deben tomar valores entre -180º y 180º')





class RestaurantForm(forms.Form):

    error_css_class = 'alert alert-danger'
    #required_css_class = 'alert alert-warning'

    name = forms.CharField(label='Nombre', widget = forms.TextInput(
                                                        attrs = {'class': 'form-control text-muted  col-xs-4',
                                                                'placeholder': 'Nombre'})
                                                        )

    cuisine = forms.CharField(label='Tipo', widget = forms.TextInput(
                                                        attrs = {'class': 'form-control text-muted col-md-4',
                                                                'placeholder': 'Tipo'})
                                                        )

    street = forms.CharField(label='Calle', widget = forms.TextInput(
                                                        attrs = {'class': 'form-control text-muted col-md-4',
                                                                'placeholder': 'Calle'})
                                                        )

    borough = forms.ChoiceField(label='Barrio', choices = BoroughNY.BOROUGH_CHOICES
        ,widget = forms.Select(
                                                        attrs = {'class': 'form-control text-muted col-md-4',
                                                                'placeholder': 'Barrio'})
                                                        )

    building = forms.IntegerField(label = 'Número', widget = forms.NumberInput(
                                                        attrs = {'class': 'form-control text-muted col-xs-4',
                                                                'placeholder': 'Número'})
                                                        )
                                                        

    zipcode = forms.IntegerField(label='Código Postal', validators=[valida_codigo_postal], widget = forms.NumberInput(
                                                        attrs = {'class': 'form-control text-muted col-md-4',
                                                                'placeholder': 'CP'}))

    n_coord = forms.DecimalField(label='Coordenada (latitud)',validators=[valida_coord_N], decimal_places = 8, widget = forms.NumberInput(
                                                        attrs = {'class': 'form-control text-muted col-xs-4',
                                                                 'placeholder': 'N' })
                                                        )

    e_coord = forms.DecimalField(label='Coordenada (longitud)',validators=[valida_coord_E], decimal_places = 8, widget = forms.NumberInput(
                                                        attrs = {'class': 'form-control text-muted col-xs-4',
                                                                 'placeholder': 'E' })
                                                        )