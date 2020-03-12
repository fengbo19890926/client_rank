from django import forms


class ClientScoresForm(forms.Form):
    client_name = forms.CharField(max_length=30)
    score = forms.IntegerField(min_value=1, max_value=10000000)


class ClientScoresGetForm(forms.Form):
    client_name = forms.CharField(max_length=30)
    start = forms.IntegerField(min_value=1, required=False)
    end = forms.IntegerField(min_value=1, required=False)

    def clean_start(self):
        if not self.cleaned_data['start']:
            return 0
        else:
            return self.cleaned_data['start']

    def clean_end(self):
        if not self.cleaned_data['end']:
            return -1
        else:
            return self.cleaned_data['end']
