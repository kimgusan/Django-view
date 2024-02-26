from django.shortcuts import render, redirect
from django.views import View

from member.models import Member
from member.serializers import MemberSerializer


class MemberJoinView(View):

    def get(self, request):
        return render(request, 'member/join.html')

    def post(self, request):
        data = request.POST
        data = {
            'member_email': data['member-email'],
            'member_password': data['member-password'],
            'member_name': data['member-name']
        }

        Member.objects.create(**data)

        return redirect('member:login')


class MemberLoginView(View):

    def get(self, request):
        return render(request, 'member/login.html')

    def post(self, request):
        data = request.POST
        data = {
            'member_email': data['member-email'],
            'member_password': data['member-password']
        }

        member = Member.objects.filter(**data)
        url = 'member:login'
        if member.exists():
            # 성공
            request.session['member'] = MemberSerializer(member.first()).data
            url = '/'

        return redirect(url)

class MemberLogoutView(View):
    def get(self, request):
        request.session.clear()
        return redirect('/member/login')



