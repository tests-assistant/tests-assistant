from django import forms

from .models import Test
from .models import Run


class EditTest(forms.ModelForm):
        class Meta:
		model = Test
		fields = ('title', 'description', 'tags')


class EditRun(forms.ModelForm):
	class Meta:
		model = Run
		fields = ('title', 'tags')
