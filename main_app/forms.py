from django import forms
from .models import ItemRank

class RankForm(forms.ModelForm):
	
    class Meta:
        model = ItemRank
        fields = ('rk', 'title',)
