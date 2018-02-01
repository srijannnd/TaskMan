from django import forms
from datetime import datetime
from .models import Todo


class TodoForm(forms.ModelForm):
    title = forms.CharField(label='Task Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please Dont be Boring'}))
    deadline = forms.DateField(label='Deadline: (yyyy-mm-dd)',widget=forms.DateInput(format=('%Y-%m-%d'),
                                                  attrs={'class': 'form-control'},
                                                  ), initial=datetime.now().date
                           )
    # completed = forms.BooleanField(widget=forms.BooleanField)

    class Meta:
        model = Todo
        fields = ('title', 'deadline')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ['title', 'deadline']:
            self.fields[name].help_text = None
