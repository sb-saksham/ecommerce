from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=264)
    email = forms.EmailField(max_length=264)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), max_length=264)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), max_length=264)

    def clean(self):
        password1 = self.cleaned_data.get('password')
        password3 = self.cleaned_data.get('password2')
        if password1 != password3:
            raise forms.ValidationError('Password not same')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=264)
    password = forms.CharField(widget=forms.PasswordInput)
