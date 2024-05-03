class PostOwnerMixin:

    def form_valid(self, form):
        if not form.instance.pk:
            form.instance.owner = self.request.user
        return super().form_valid(form)
    