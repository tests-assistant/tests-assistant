from django import forms


class EditTest(forms.Form):
    title = forms.CharField(max_length=255)
    description = forms.CharField()
    tags = forms.CharField(max_length=255)


class EditRun(forms.Form):
    title = forms.CharField(max_length=255)
