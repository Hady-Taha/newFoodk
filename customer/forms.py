from django import forms
from allauth.account.forms import SignupForm
from .models import Customer,Region
from django.contrib.auth.models import User


class CustomerProfile(forms.ModelForm):
    full_name = forms.CharField(label='الاسم كامل')
    phone = forms.CharField(label='رقم التليفون')
    region = forms.ModelChoiceField(queryset=Region.objects.all(), label='اختار منطقتك ')
    address = forms.CharField(label='العنوان')
    class Meta:
        model = Customer
        fields = ('full_name','phone','region',"address",)

    def clean_phone(self):
        cd = self.cleaned_data
        if cd["phone"][:3] not in ["012", "011", "015", "010"]:
            raise forms.ValidationError('الرقم الذي ادخلته غير صحيح')
        elif Customer.objects.filter(phone=cd["phone"]).exists():
            raise forms.ValidationError('الرقم الذي ادخلته موجد مسبقا')
        return cd['phone']


class UserForm(SignupForm, CustomerProfile):
    username = forms.CharField(label='اسم المستخدم', max_length=30,help_text='اسم المستخدم يجب ألا يحتوي على مسافات.')
    
    def save(self, request):
        user = super(UserForm, self).save(request)
        if request.method == "POST":
            form = CustomerProfile(request.POST)
            if form.is_valid():
                newuser = form.save(commit=False)
                newuser.user = User.objects.get(username=user)
                newuser.save()
        return user


class EditCustomer(forms.ModelForm):
    full_name = forms.CharField(label='الاسم كامل')
    phone = forms.CharField(label='رقم التليفون')
    address = forms.CharField(label='العنوان')
    region = forms.ModelChoiceField(queryset=Region.objects.all(),label=' منطقتك')
    class Meta:
        model = Customer
        fields = ('full_name', 'phone', "region","address",)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(EditCustomer, self).__init__(*args, **kwargs)

    


    def clean_phone(self):
        cd = self.cleaned_data
        if cd["phone"][:3] not in ["012", "011", "015", "010"]:
            raise forms.ValidationError('الرقم الذي ادخلته غير صحيح')
        elif Customer.objects.filter(phone=cd["phone"]).exclude(phone=self.request.user.customer.phone).exists():
            raise forms.ValidationError('الرقم الذي ادخلته موجد مسبقا')
        return cd['phone']
