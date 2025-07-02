import hashlib


# Функция для хэширования ip
def hash_ip(ip):
    return hashlib.sha256(ip.encode('utf-8')).hexdigest()

# Функция для получения IP из запроса
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return hash_ip(ip)