from django.shortcuts import render, redirect
from django.views import View

from member.models import Member


class MainView(View):
    def get(self, request):
        # try:
        #     member = request.session.get('member')
        # except KeyError:
        #     member = None
        # return render(request, 'main/main.html', context={'member': member})
        return render(request, 'main/main.html')




