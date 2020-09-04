class DreamrealForm(forms.Form):
   website = forms.CharField(max_length = 100)
   name = forms.CharField(max_length = 100)
   phonenumber = forms.CharField(max_length = 50)
   email = forms.CharField(max_length = 100)