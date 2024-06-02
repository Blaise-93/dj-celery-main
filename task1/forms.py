from django import forms
from task1.tasks import send_review_email_task

class ReviewForm(forms.Form):

    name = forms.CharField(label='Enter your first name', min_length=4, max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3',
               'placeholder': 'John Doe', 'id': 'form-firstname'}
    ))

    email = forms.CharField(label='Enter your email',
                            min_length=4, max_length=100, widget=forms.TextInput(
                                attrs={'class': 'form-control mb-3',
                                       'placeholder': 'Johndoe@gmail.com', 'id': 'form-email'}
                            ))

    review = forms.CharField(label='Review', widget=forms.Textarea(attrs={
        'class': 'form-control', 'rows': '5'
    }))

    def send_email(self):
        '''send_review_email_task'''

        send_review_email_task.delay(
            self.cleaned_data['name'], 
            self.cleaned_data.get('email'), self.cleaned_data['review']
            )
