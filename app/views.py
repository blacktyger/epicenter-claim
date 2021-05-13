import datetime
import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from app.forms import EIOUForm
from django.views import generic

from app.manager import ClaimManager
from app.models import Claim, ClaimFile
from django.views.generic import CreateView
from .models import ClaimFile


class EIOUClaimViews(generic.TemplateView):
    fields = ['telegram', 'vitex_address', 'details']
    template_name = "eiou_claim_app.html"
    success_url = "eiou_confirm_form.html"
    form_class = EIOUForm
    model = Claim

    def post(self, request, *args, **kwargs):
        claim_id = request.session['active_claim'] or None
        if claim_id:
            claim = Claim.objects.get(id=claim_id)

            for field in self.fields:
                value = request.POST.get(field) or None
                setattr(claim, field, value)

            claim.status = claim.STATUS.submitted
            claim.save()
            del request.session['active_claim']
            print('Yay!')

            context = self.get_context_data(
                claim_id=claim.id,
                claim_status=claim.status)

            return render(request, self.success_url, context)
        else:
            return render(request, self.template_name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get(self, request, *args, **kwargs):
        """Start new claim or continue already started one"""
        claim = ClaimManager()

        # Check if there is already started claim saved in session,
        # if yes continue started one, if no start new
        if 'active_claim' not in request.session:
            claim.start()
            # TODO: remove this from session after successful submission
            request.session['active_claim'] = str(claim.data.id)
        else:
            claim.data = Claim.objects.get(id=request.session['active_claim'])

        context = self.get_context_data(claim_id=claim.data.id)
        response = render(request, self.template_name, context)

        # Check for cookie, we will save number of sent claims there (anti-flood)
        if not request.COOKIES.get('eiou_claim_visits'):
            response.set_cookie('eiou_claim_visits', '1')
            print(request.COOKIES)
        else:
            visits = int(request.COOKIES.get('eiou_claim_visits'))
            print(visits)
            response.set_cookie('eiou_claim_visits', visits + 1)

        return response


class HomeView(generic.TemplateView):
    template_name = "home.html"


def upload(request):
    def generate_file_name(file):
        """Add date to name files"""
        now = datetime.datetime.now()
        now = now.strftime("%Y%m%d%H")
        print(f"{str(file)[:-4]}_{now}{str(file)[-4:]}")
        return f"{str(file)[:-4]}_{now}{str(file)[-4:]}"

    if request.method == 'POST':
        if request.is_ajax():
            file = request.FILES.get('file')
            print('--------------------------------')
            print(file)
            new, created = ClaimFile.objects.\
                get_or_create(name=generate_file_name(file))
            new.file = file
            new.save()
            claim_id = request.session['active_claim']
            active_claim = Claim.objects.get(id=claim_id)
            active_claim.files.add(new)
            active_claim.save()
            print(new)
            print('--------------------------------')
            response_data = {
                'url': new.file.url,
                'status': 'success'
                }
            return JsonResponse(response_data)

