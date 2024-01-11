# views.py
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
import json
from .models import Approvedby, User, ActivityLog
from .serializers import ApprovedbySerializer
from be.middleware.token_middleware import CustomJWTAuthentication

class ApprovedbyListCreateAPIView(ListCreateAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = Approvedby.objects.all()
    serializer_class = ApprovedbySerializer

    def perform_create(self, serializer):
        approvedby = serializer.save()

        # Pastikan nilai-nilai yang ingin dicatat tidak None
        nama = approvedby.nama if approvedby.nama is not None else "N/A"
        cc_to = approvedby.cc_to if approvedby.cc_to is not None else "N/A"
        note = approvedby.note if approvedby.note is not None else "N/A"
        # ... (lakukan hal yang sama untuk atribut lainnya)

        # Logging activity for each approvedby creation
        user_id = approvedby.id_user.id_user
        self.log_activity(
            user_id, 'created', 'approvedBy', approvedby,
            nama=nama, cc_to=cc_to, note=note, title=approvedby.title,
            nama1=approvedby.nama1, title1=approvedby.title1, cc_to1=approvedby.cc_to1
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def log_activity(self, user_id, action, name_table, approvedby, **kwargs):
        user_instance = get_object_or_404(User, id_user=user_id)

        object_data = {
            'nama': approvedby.nama,
            'cc_to': approvedby.cc_to,
            'note': approvedby.note,
            'title': approvedby.title,
            'nama1': approvedby.nama1,
            'title1': approvedby.title1,
            'cc_to1': approvedby.cc_to1,
            # ... (kolom lainnya)
        }

        # Tambahkan nilai-nilai lain yang ingin dicatat
        for key, value in kwargs.items():
            object_data[key] = value

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )

class ApprovedbyDetailAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = Approvedby.objects.all()
    serializer_class = ApprovedbySerializer

    def perform_update(self, serializer):
        approvedby = serializer.save()

        # Logging activity for each approvedby update
        user_id = approvedby.id_user.id_user
        self.log_activity(user_id, 'updated', 'approvedBy', approvedby)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        # Logging activity for each approvedby deletion
        user_id = instance.id_user.id_user
        self.log_activity(user_id, 'deleted', 'approvedBy', instance)

        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def log_activity(self, user_id, action, name_table, approvedby):
        user_instance = get_object_or_404(User, id_user=user_id)

        object_data = {
            'nama': approvedby.nama,
            'cc_to': approvedby.cc_to,
            'note': approvedby.note,
            'title': approvedby.title,
            'nama1': approvedby.nama1,
            'title1': approvedby.title1,
            'cc_to1': approvedby.cc_to1,
            # ... (kolom lainnya)
        }

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )
