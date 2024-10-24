from django import forms
from .models import Event, EventDate, Participant, Availability

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description"]
        labels = {
            "title" : "イベント名",
            "description" : "メモ(任意)"
        }
        def clean_dates(self):
            dates = self.cleaned_data.get('dates')
            if not dates:
                raise forms.ValidationError("日程候補を選択してください。")
            return dates


class EventDateForm(forms.ModelForm):
    date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = EventDate
        fields = ['date']

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'comment']  # コメントフィールドを追加

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            return "匿名"  # 名前が未入力の場合は「匿名」とする
        return name

    def clean_comment(self):
        comment = self.cleaned_data.get('comment')
        if comment and len(comment) > 500:
            raise forms.ValidationError("コメントは500文字以内で入力してください。")
        return comment

class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['availability']