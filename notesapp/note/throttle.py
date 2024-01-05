from rest_framework.throttling import BaseThrottle, UserRateThrottle
from datetime import datetime
from django.core.cache import cache
from django.conf import settings

class NoteListCreateThrottle(BaseThrottle):
    

    def allow_request(self, request, view):

        if request.method == 'GET':
            max_requests_per_day = 50 
        elif request.method == 'POST':
            max_requests_per_day = 20
        user = request.user
        path = request.path
        cache_key = f"{path}:{user.id}:{request.method}"
        cache_result = cache.get(cache_key,[])
        if cache_result:    
            if len(cache_result) < max_requests_per_day:
                cache_result.append(datetime.now())
                cache.set(cache_key, cache_result, settings.CACHES['default'].get('TIMEOUT', 43200))  # set a timeout (in seconds)
            else:
                return False
        else:
            cache_result.append(datetime.now())
            cache.set(cache_key, [datetime.now()], settings.CACHES['default'].get('TIMEOUT', 43200)) 
        
        return True        


class NoteDetailThrottle(BaseThrottle):
    def allow_request(self, request, view):

        if request.method == 'GET':
            max_requests_per_day = 30
        elif request.method == 'PUT':
            max_requests_per_day = 15
        elif request.method == 'DELETE':
            max_requests_per_day = 10
    
        user = request.user
        path = request.path
        cache_key = f"{path}:{user.id}:{request.method}"
        cache_result = cache.get(cache_key,[])
        if cache_result:    
            if len(cache_result) < max_requests_per_day:
                cache_result.append(datetime.now())
                cache.set(cache_key, cache_result, settings.CACHES['default'].get('TIMEOUT', 43200))  # set a timeout (in seconds)
            else:
                return False
        else:
            cache_result.append(datetime.now())
            cache.set(cache_key, [datetime.now()], settings.CACHES['default'].get('TIMEOUT', 43200)) 
        
        return True        
    

class NoteShareThrottle(UserRateThrottle):
    scope = 'note_share'

