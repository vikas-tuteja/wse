from django import forms
from models import MetaData
from django.template import Template, TemplateSyntaxError

class MyModelForm(forms.ModelForm):
    def clean(self, *args, **kwargs):
        cleaned_data = super(MyModelForm, self).clean()
        cleaned_data.update({
            'path':self.data['path']
        })
        for i in cleaned_data:
            try:
                Template(cleaned_data[i])
            except TemplateSyntaxError:
                self._errors[i] = ErrorList()
                self._errors[i].append('SYNTAX ERROR: Please check your syntax')
        return cleaned_data


    class Meta:
        model = MetaData
        widgets = {
            'regular_expression': forms.RadioSelect
        }
        fields = '__all__'

