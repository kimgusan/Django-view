from random import randint

# 학생의 번호, 국어 점수, 영어, 수학 점수를 전달받은 뒤
# 총점과 평균을 화면에 출력한다.
from django.shortcuts import render, redirect
from django.views import View


# form태그는 get방식을 사용한다.
# 출력화면에서 다시 입력화면으로 돌아갈 수 있게 한다. (전송, 다시 입력)

# 입력: task/student/register.html
# 출력: task/student/result.html


class StudentRegisterFormView(View):
    def get(self, request):
        return render(request, 'task/student/register.html')


class StudentRegisterView(View):
    def get(self, request):
        data = request.GET
        data = {
            'id': data['student_id'],
            'kor': int(data['korean_score']),
            'eng': int(data['english_score']),
            'math': int(data['math_score'])
        }

        total = data['kor'] + data['eng'] + data['math']
        average = round(total / 3, 2)

        return redirect(f'/student/result?total={total}&average={average}')


class StudentResultView(View):
    def get(self, request):
        data = request.GET
        context = {
            'total': request.GET['total'],
            'average': request.GET['average']
        }
        return render(request, 'task/student/result.html', context)



# 회원의 이름과 나이를 전달받는다.
# 전달받은 이름과 나이를 아래와 같은 형식으로 변경 시킨다.
# "홍길동님은 20살!"
# 결과 화면으로 이동한다.

# 이름과 나이 작성: task/member/register.html
# 결과 출력: task/member/result.html


class MemberRegisterFormView(View):
    def get(self, request):
        return render(request, 'task/member/register.html')

class MemberRegisterView(View):
    def get(self,request):
        data = request.GET

        member_info = f'{data["member_name"]}님은 {data["member_age"]}살!'
        return redirect(f'/member/result?member_info={member_info}')

class MemberResultView(View):
    def get(self, request):
        context = {
            'member_info': request.GET['member_info']
        }
        return render(request, 'task/member/result.html', context)




############################################################################################################################################
# 회원의 이름과 나이를 전달 받은 후,
# 20살 미만이면 "지원님은 미성년자 입니다"
# 20살 이상이면 "지원님은 성인이시군요!"
# 결과 화면에 문구 출력하기

# 작성: task/user/register.html
# 출력: task/user/result.html

class UserRegisterFormView(View):
    def get(self, request):
        return render(request, 'task/user/register.html')

class UserRegisterView(View):
    def get(self, request):
        data = request.GET

        young_text = '김규산님은 미성년자 입니다.'
        old_text = '김규산님은 성인 입니다.'
        result = young_text
        if int(data['age']) >=20:
            result = old_text
        return redirect(f'/user/result/?result={result}')


class UserResultView(View):
    def get(self, request):
        data ={
            'result' : request.GET['result']
        }
        return render(request, 'task/user/result.html', data)


############################################################################################################################################
# 1~10사이의 숫자를 입력받아(input[type=number])
# 뷰에서 1~10사이의 랜덤한 숫자(random.randint())를 생성한 후
# 일치할 경우 "축하합니다! 정답입니다!"를 화면으로,
# 불일치할 경우 차이(절댓값)를 "아쉽네요... 정답과 [차이]만큼 차이가 나요!" 출력하기


class NumberInputFormView(View):
    def get(self, request):
        return render(request, 'task/number/input.html')

class NumberInputView(View):
    def get(self, request):
        number = int(request.GET['number'])

        text = f'{number}는 당첨입니다!!'
        random_number = randint(1,10)
        if (number != random_number):
            abs_number = abs(number-random_number)
            text = f'{number}는 꽝!꽝!꽝!꽝!꽝!,\n {abs_number}만큼 차이납니다.'
        return redirect(f'/number/result/?result={text}')

class NumberResultView(View):
    def get(self, request):
        datas = request.GET
        data = {
            'result': datas['result']
        }
        return render(request, 'task/number/result.html', data)