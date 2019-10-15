import requests
import datetime
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from django.contrib import messages
from django.shortcuts import render,redirect

class GetLogged(MiddlewareMixin):

    def process_request(self, request):

        print(datetime.datetime.now())
      
        if request.user.is_authenticated:
            print("User: " + request.user.username + " is logged in.")
        else:
            print("No one is logged in")

