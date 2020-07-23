from django import forms
from blog.models import Category, Post
from django.utils.text import slugify
from django.core.exceptions import ObjectDoesNotExist
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget
#from account.models import Profile

class ContactUsForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(required=False)
    phone_number = forms.RegexField(required=False, regex = "^[6-9]\d{9}$")

    def clean(self):
        cleaned_data = super().clean()
        if not (cleaned_data.get('email')) or (cleaned_data.get('phone_number')):
            raise forms.ValidationError("please enter email or phone number", code="invalid")

    def clean_email(self):
        data = self.cleaned_data['email']
        if "edyoda" not in data:
            raise forms.ValidationError("Invalid domain", code="invalid")
        return data

class RegisterForm(forms.Form):
    gender_choices = [("M", "Male"), ("F", "Female")]
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    username = forms.RegexField(r'^[A-Za-z]+[A-Za-z0-9@_]+$', min_length=8, max_length=16, help_text="Should start with Alphabet | Special character allowed (@, _)")
    email = forms.EmailField()
    password = forms.RegexField(r'((?=.*\d) (?=.*[a-z]) (?=.*[A-Z]) (?=.*[\S\D\W]).)', max_length=32, min_length=8, widget = forms.PasswordInput(attrs={'width':'100%','height':'30%', 'class':'login-fields'}))
    
    confirm_password = forms.CharField(max_length=32,min_length=8, widget = forms.PasswordInput)
    gender = forms.ChoiceField(choices = gender_choices, widget = forms.RadioSelect)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("password and confirm password does not match", code="mismatch")

    #def clean_username(self):
     #   data = self.cleaned_data['username']
        #special_char = ['@', '_']

      #  if ("@" not in data) or ("_" not in data):
       #     raise forms.ValidationError("enter valid username", code="mismatch")
        #return data


#class PostForm(forms.Form):
 #   statuses = [("D", "Draft"), ("P", "Published")]
  #  title = forms.CharField(max_length=250)
   # content = forms.CharField(widget= forms.Textarea)
    #status = forms.ChoiceField(choices=statuses)
    #category = forms.ModelChoiceField(queryset= Category.objects.all())
    #image = forms.ImageField(required=False)

class PostForm(forms.ModelForm):
    #content = forms.CharField(widget=SummernoteWidget())

    #author = forms.ModelChoiceField(queryset= Profile.objects.all(), disabled= True,required= False)
    class Meta:
        model = Post
        fields = ['title', 'content', 'status', 'category', 'image']

        widgets = {
            'content': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '530px'}}),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not self.initial:
            slug = slugify(title)
            try:
                post_obj = Post.objects.get(slug = slug)
                raise forms.ValidationError("Title already exists", code="Invalid")
            except ObjectDoesNotExist:
                return title
        return title

    # def clean_image(self):
    #     image = self.cleaned_data.get('image')
    #     return image


