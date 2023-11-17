from django import forms


class ComparisonProfessionsForm(forms.Form):
    first_profession = forms.RegexField(required=True, help_text="Название первой профессии", regex=r'^[А-Яа-яЁё]+$')
    second_profession = forms.CharField(required=True, help_text="Название второй профессии", regex=r'[А-Яа-яЁё]')
