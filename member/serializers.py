from rest_framework import serializers
from member.models import Member


# 직렬화 (sesstion에 객체를 담는 법)
class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'