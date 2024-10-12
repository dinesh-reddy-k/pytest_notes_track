from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import Note


class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = "index.html"
    context_object_name = "notes"

    def get_queryset(self):
        return Note.objects.filter(owner=self.request.user).order_by("-updated_at")
