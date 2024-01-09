from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from users.models import User

@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Cari pengguna berdasarkan email
            users = User.objects.filter(email=email)

            if users.exists():
                user = users.first()

                if user and user.check_password(password):
                    # Buat token JWT
                    payload = {
                        'user_id': user.id_user,
                        'exp': datetime.utcnow() + timedelta(days=1),
                    }
                    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

                    return JsonResponse({'token': token})
                else:
                    print(f"Invalid credentials for email: {email}")
                    return JsonResponse({'error': 'Invalid credentials'}, status=401)

            else:
                print(f"User not found for email: {email}")
                return JsonResponse({'error': 'User not found'}, status=404)

        except Exception as e:
              print(f"Error during login: {str(e)}")
              return JsonResponse({'error': f'Internal Server Error: {str(e)}'}, status=500)


    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
