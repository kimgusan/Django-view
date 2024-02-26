from django.shortcuts import render, redirect
from django.views import View


class MainView(View):
    def get(self, request):
        try:
            member = request.session.get('member')
        except:
            member = None
        return render(request, 'main/main.html', context={'member': member})

