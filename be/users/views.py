# views.py
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from django.http import HttpResponseBadRequest
from django.core.files.storage import default_storage
from .models import User
from .serializers import UserSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.conf import settings
from datetime import datetime, timedelta
import boto3
import bcrypt
import jwt
import json
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from be.middleware.token_middleware import CustomJWTAuthentication
from jwt import ExpiredSignatureError, InvalidTokenError
from django.core.serializers.json import DjangoJSONEncoder
from be.middleware.token_middleware import CustomJWTAuthentication


class UserListCreateView(generics.ListCreateAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    
class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        # Gunakan partial=True untuk mendukung pembaruan sebagian
        serializer = UserSerializer(instance, data=request.data, partial=True)

        try:
            serializer.is_valid(raise_exception=True)
            # Ambil data profil dari instance yang ada
            existing_profile = instance.profile

            # Periksa apakah 'profile' ada dalam data yang dikirimkan
            if 'profile' in request.data:
                new_profile = request.data['profile']

                # Jika 'profile' diubah, simpan foto profil baru
                if new_profile != existing_profile:
                    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")

                    s3 = boto3.resource('s3', endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

                    photo_profile_name = f"profile/{current_datetime}_{new_profile.name}"
                    photo_profile_url = f"/internalorder/{photo_profile_name}"
                    serializer.save(profile=photo_profile_url)

                    s3.Bucket(settings.AWS_STORAGE_BUCKET_NAME).put_object(
                        Key=photo_profile_name, Body=new_profile, ContentType='image/jpeg')
                else:
                    # Jika 'profile' tidak diubah, lanjutkan dengan menyimpan data tanpa mengubah foto profil
                    serializer.save()
            else:
                # Jika 'profile' tidak ada dalam data yang dikirimkan, lanjutkan dengan menyimpan data tanpa mengubah foto profil
                serializer.save()

            return Response({'message': 'User updated successfully'})

        except serializers.ValidationError as e:
            return Response({'error': str(e)}, status=400)

        except Exception as e:
            return Response({'error': str(e)}, status=500)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()    
        self.perform_destroy(instance)
        return Response({'message': 'User deleted successfully.'})

@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        try:
            # Cek tipe konten yang diterima
            if request.content_type == 'application/json':
                data = json.loads(request.body)
            else:
                data = request.POST

            email = data.get('email')
            password = data.get('password')

            # Periksa apakah email atau password kosong
            if not email:
                return JsonResponse({'error': 'Email cannot be empty'}, status=400)
            if not password:
                return JsonResponse({'error': 'Password cannot be empty'}, status=400)

            # Retrieve user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return JsonResponse({'error': 'Email not found'}, status=401)

            # Check if the password is valid using bcrypt
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                # User berhasil diotentikasi, hasilkan token dan refresh token
                expiration_time = datetime.utcnow() + timedelta(hours=12)  # Token berlaku 3 jam
                refresh_expiration_time = datetime.utcnow() + timedelta(days=7)  # Refresh token berlaku 7 hari
                mobile_token_expiration_time = datetime.utcnow() + timedelta(days=365)  # Token akses mobile berlaku 1 tahun

                profile_url = user.profile.url if user.profile else None

                payload = {
                    'exp': expiration_time,
                    'id_user': user.id_user,
                    'email': user.email,
                    'hak_akses': user.hak_akses,
                    'nama': user.nama,
                    'phone': user.phone,
                    'jabatan': user.jabatan,
                    'profile': profile_url,
                }

                refresh_payload = {
                    'exp': refresh_expiration_time,
                    'id_user': user.id_user,
                    'hak_akses': user.hak_akses,
                    'nama': user.nama,
                    'phone': user.phone,
                    'jabatan': user.jabatan,
                    'profile': profile_url,
                }

                mobile_payload = {
                    'exp': mobile_token_expiration_time,
                    'id_user': user.id_user,
                    'email': user.email,
                    'hak_akses': user.hak_akses,
                    'nama': user.nama,
                    'phone': user.phone,
                    'jabatan': user.jabatan,
                    'profile': profile_url,
                }

                secret_key = settings.SECRET_KEY  # Pastikan settings.SECRET_KEY adalah kunci rahasia yang valid

                # Buat token akses
                token = jwt.encode(payload, secret_key, algorithm='HS256')

                # Buat refresh token
                refresh_token = jwt.encode(refresh_payload, secret_key, algorithm='HS256')

                # Simpan refresh token ke database atau tempat penyimpanan lainnya
                # ...
                mobile_token = jwt.encode(mobile_payload, secret_key, algorithm='HS256')

                return JsonResponse({'token': token, 'refresh_token': refresh_token, 'mobile_token': mobile_token})
            else:
                # User tidak berhasil diotentikasi
                return JsonResponse({'massage': 'Email/Password Tidak Sesuai'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    

def get_user_info(request):
    try:
        user, _ = CustomJWTAuthentication().authenticate(request)
        return JsonResponse(user.__dict__)
    except ExpiredSignatureError:
        return JsonResponse({'error': 'Token has expired'}, status=401)
    except InvalidTokenError:
        return JsonResponse({'error': 'Invalid token'}, status=401)
    except Exception as e:
        return JsonResponse({'error': str(e)},status=500)
    
