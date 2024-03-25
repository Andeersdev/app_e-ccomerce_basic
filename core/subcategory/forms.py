from django import forms
from .models import Subcategory


class SubCategoryForm(forms.ModelForm):

    class Meta:
        model = Subcategory
        exclude = ['is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
