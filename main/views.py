from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .services.handle_get_list_of_unfollowing_users import handle_get_list_of_unfollowing_users
from .services.handle_get_followers import handle_get_followers
import json
import datetime


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@csrf_exempt
@api_view(['GET'])
def get_current_time(request):
	print(get_client_ip(request))
	
	print(datetime.datetime.now())
	return Response( {"current_time": datetime.datetime.now()} , status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
def get_followers(request):
	"""
    Для работы с API необходимо отправить post запрос, в поле content необходимо вставить следующую информацию:

    {
		"sessionid" : "36059209189%3AqFBw0JXsMAzlbQ%3A21",
		"login": "aiur95_"
    }
    """
	request_attr = json.loads(request.body)
	sessionid = request_attr['sessionid']
	login = request_attr['login']

	msg, status_code = handle_get_followers(sessionid, login)
	if status_code == 200:
		return Response( {"msg": msg} , status=status.HTTP_200_OK)
	elif status_code == 429:
		return Response( {"msg": msg} , status=status.HTTP_400_BAD_REQUEST)
	else:
		return Response( {"msg": msg} , status=status.HTTP_204_NO_CONTENT)


@csrf_exempt
@api_view(['POST'])
def get_list_of_unfollowing_users(request):
	"""
    Для работы с API необходимо отправить post запрос, в поле content необходимо вставить следующую информацию:

    {
		"sessionid" : "36059209189%3AqFBw0JXsMAzlbQ%3A21",
		"login": "aiur95_"
    }
    """
	request_attr = json.loads(request.body)
	sessionid = request_attr['sessionid']
	login = request_attr['login']

	msg, status_code = handle_get_list_of_unfollowing_users(sessionid, login)
	if status_code == 200:
		print("ok")
		return Response( {"msg": msg} , status=status.HTTP_200_OK)
	elif status_code == 429:
		print(msg)
		return Response( {"msg": msg} , status=status.HTTP_400_BAD_REQUEST)
	else:
		print(msg)
		return Response( {"msg": msg} , status=status.HTTP_204_NO_CONTENT)
		
