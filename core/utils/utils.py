

def get_client_ip(request):
    http_forward_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if http_forward_for:
        print( http_forward_for)
        ip = http_forward_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip