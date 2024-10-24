from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, DeleteView, View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Event, EventDate, Participant, Availability
from .forms import EventForm, EventDateForm, ParticipantForm
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.shortcuts import redirect
# Create your views here.
class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'scheduler/event_create.html'

    def form_valid(self, form):
        # 日程候補の取得
        dates = self.request.POST.get('dates')

        # 日程候補が選択されていない場合の処理
        if not dates or dates == '':
            messages.error(self.request, "日程候補を選択してください。")
            return self.form_invalid(form)
        form.instance.creator = self.request.user

        # ランダムなslugを生成
        form.instance.slug = slugify(form.instance.title + '-' + get_random_string(length=5))
        response = super().form_valid(form)

        # 日程候補の登録
        for date_with_time in self.request.POST.get('dates').split(','):
            if date_with_time:
                date, time = date_with_time.split(' ')  # 日付と時間を分割
                EventDate.objects.create(event=self.object, date=date, time=time)
        return response

    def get_success_url(self):
        return reverse('event_detail', kwargs={'slug': self.object.slug})

class EventDetailView(DetailView):
    model = Event
    template_name = "scheduler/event_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = self.object
        # イベントに関連する参加者を取得
        participants = Participant.objects.filter(event=event)
        context['participants'] = participants

        event_url = self.request.build_absolute_uri(reverse('event_detail', kwargs={'slug': event.slug}))
        context['participants'] = participants
        context['event_url'] = event_url  # URLをコンテキストに追加

        return context


class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = "scheduler/my_page.html"
    context_object_name = 'object_list'
    paginate_by = 6  # 1ページに表示するイベント数

    def get_queryset(self):
        return Event.objects.filter(creator=self.request.user)

class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    success_url = reverse_lazy('my_page')  # 削除後にリダイレクトするURL
    template_name = 'scheduler/event_delete.html'

    def get_object(self):
        event = super().get_object()
        # 削除できるのは作成者本人のみ
        if event.creator != self.request.user:
            raise PermissionDenied
        return event

class ParticipantCreateView(View):

    def get(self, request, slug):
        event = get_object_or_404(Event, slug=slug)
        event_dates = event.dates.all()
        return render(request, 'scheduler/event_participate.html', {'event': event, 'event_dates': event_dates})

    def post(self, request, slug):
        event = get_object_or_404(Event, slug=slug)
        name = request.POST.get('name', '匿名')  # 名前がなければ「匿名」を使用
        comment = request.POST.get('comment', '')  # コメントを取得

        participant = Participant.objects.create(event=event, name=name, comment=comment)

        error_messages = []
        all_selected = True

        for date in event.dates.all():
            availability = request.POST.get(f'availability_{date.id}')
            if not availability:  # 未選択の日程があった場合
                all_selected = False
            else:
                Availability.objects.create(participant=participant, event_date=date, availability=availability)

        # 全ての日程で参加可否が選ばれていない場合、エラーメッセージを表示
        if not all_selected:
            error_messages.append("全ての日程について参加可否を選択してください。")
            return render(request, 'scheduler/event_participate.html', {
                'event': event,
                'event_dates': event.dates.all(),
                'error_messages': error_messages
            })
        return redirect('event_detail', slug=slug)


# class ParticipantCreateView(CreateView):
#     model = Participant
#     form_class = ParticipantForm
#     template_name = 'scheduler/event_participate.html'

#     def form_valid(self, form):
#         event = get_object_or_404(Event, slug=self.kwargs['slug'])
#         form.instance.event = event
#         form.instance.availability = self.request.POST.get('availability')
#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse('event_detail', kwargs={'slug': self.object.event.slug})
