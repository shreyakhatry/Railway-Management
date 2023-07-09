# from django.shortcuts import render

# # Create your views here.
import jwt,json
from django.http import HttpResponse,JsonResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def signin(req):
    if req.method == 'POST':
        data = json.loads(req.body)
        username = data['username']
        password = data['password']
        print(username, password)
        user = authenticate(username = username,password = password)
        if user is not None:
            if user.is_active:
                payload = {
                    'id': user.id,
                    'username': user.username
                }
                jwt_token = jwt.encode(payload,'secret',algorithm ='HS256')
                return JsonResponse({'token':jwt_token,'user':user.username},status=200)
            else:
                return JsonResponse({'error':'Account is disabled'},status=403)
        else:
            return JsonResponse({'error':'Invalid Credentials'},status=403)

@csrf_exempt
def signup(req):
    print("--------------------")
    if req.method == 'POST':
        data = json.loads(req.body)
        username = data['username']
        password = data['password']
        email = data['email']
        print(data)
        try:
            user=User.objects.get(username=username)
            return JsonResponse({'error':'Username already registered'},status=403)
        except:
            try:
                user=User.objects.get(email=email)
                return JsonResponse({'error':'Email already registered'},status=403)
            except:
                user=User.objects.create_user(username,email,password)
                payload = {
                    'id':user.id,
                    'username':user.username
                }
                jwt_token = jwt.encode(payload,'secret',algorithm = 'HS256')
                return JsonResponse({'token':jwt_token,'user':user.username},status=201)

def authReq(token):
    try:
        reqUser = jwt.decode(token,'secret',algorithms = 'HS256')
    except Exception as e:
        return False
    user = User.objects.filter(id = reqUser.get('id', None)).values()
    if user:
        return True
    else:
        return False