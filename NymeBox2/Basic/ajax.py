from dajaxice.utils import deserialize_form
from myapp.form import DreamrealForm
from dajax.core import Dajax
from myapp.models import Dreamreal

@dajaxice_register
def send_form(request, form):
   dajax = Dajax()
   form = DreamrealForm(deserialize_form(form))
   
   if form.is_valid():
      dajax.remove_css_class('#my_form input', 'error')
      dr = Dreamreal()
      dr.website = form.cleaned_data.get('website')
      dr.name = form.cleaned_data.get('name')
      dr.phonenumber = form.cleaned_data.get('phonenumber')
      dr.save()
      
      dajax.alert("Dreamreal Entry %s was successfully saved." % 
         form.cleaned_data.get('name'))
   else:
      dajax.remove_css_class('#my_form input', 'error')
      for error in form.errors:
         dajax.add_css_class('#id_%s' % error, 'error')
			
   return dajax.json()