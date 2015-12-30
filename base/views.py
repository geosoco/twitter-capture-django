from django.contrib.auth.decorators import login_required


#
# Mixins
#

class LoginRequiredMixin(object):
    """A mixin that forces a login to view the CBTemplate."""

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        return JsonResponse(form.errors, status=400)


    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        logger.info("form is valid")

        # data = serializers.serialize('json', form)
        #logger.info("form data: %s"%(str(form.fields['text'])))
        response = super(AjaxableResponseMixin, self).form_valid(form)
        data = model_to_dict(self.object)
        return JsonResponse(data)

