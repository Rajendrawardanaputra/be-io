# views.py
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from .models import DetailTimeline
from .serializers import (
    DetailTimelineSerializer, DetailTimelineListSerializer
)
from .models import User, ActivityLog
from be.middleware.token_middleware import CustomJWTAuthentication
import json
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404

class DetailTimelineListCreateAPIView(ListCreateAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = DetailTimeline.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST' and isinstance(self.request.data, list):
            return DetailTimelineListSerializer
        return DetailTimelineSerializer

    def get_queryset(self):
        id_project = self.request.query_params.get('id_project', None)
        if id_project is not None:
            queryset = DetailTimeline.objects.filter(id_project=id_project)
            return queryset
        return DetailTimeline.objects.all()

    def perform_create(self, serializer):
        detail_timeline_list = serializer.save()

        for detail_timeline in detail_timeline_list:
            user_id = detail_timeline.id_user.id_user
            self.log_activity(
                user_id, 'created', 'DetailTimeline', detail_timeline
            )

        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    def log_activity(
        self, user_id, action, name_table, detail_timeline,
        new_photo=None, old_photo=None
    ):
        user_instance = get_object_or_404(User, id_user=user_id)

        object_data = {
            'weeks': detail_timeline.weeks,
            'activity': detail_timeline.activity,
            # Saring old_Data jika tidak ada pada objek DetailTimeline
            # ... (kolom lainnya)
        }

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )

class DetailTimelineDetailAPIView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [CustomJWTAuthentication]
    queryset = DetailTimeline.objects.all()
    serializer_class = DetailTimelineSerializer

    def get_serializer(self, *args, **kwargs):
        if (
            'fields' not in kwargs and
            self.serializer_class == DetailTimelineListSerializer
        ):
            kwargs['context'] = {
                'fields': ['user', 'project_internal', 'weeks', 'activity']
            }
        return super().get_serializer(*args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_data = model_to_dict(instance)  
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, old_data)
        return Response(
            {"message": "Update berhasil"}, status=status.HTTP_200_OK
        )

    def perform_update(self, serializer, old_data):
        user_id = serializer.instance.id_user.pk
        serializer.save()
        self.log_activity(
            user_id, 'updated', 'DetailTimeline', old_data=old_data
        )

    def perform_destroy(self, instance):
        user_id = instance.id_user.pk
        old_data = model_to_dict(instance)
        instance.delete()
        self.log_activity(
            user_id, 'deleted', 'DetailTimeline', old_data=old_data
        )
        return Response(
            {"message": "DetailTimeline berhasil dihapus"},
            status=status.HTTP_204_NO_CONTENT
        )

    def log_activity(
        self, user_id, action, name_table, old_data, new_data=None
    ):
        user_instance = get_object_or_404(User, id_user=user_id)

        object_data = {
            'weeks': old_data['weeks'],
            'activity': old_data['activity'],
            # ... (kolom lainnya)
        }

        if new_data is not None:
            object_data.update({'changes': new_data})

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )

class DetailTimelinePublicListCreateAPIView(ListCreateAPIView):
    queryset = DetailTimeline.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST' and isinstance(self.request.data, list):
            return DetailTimelineListSerializer
        return DetailTimelineSerializer

    def get_queryset(self):
        id_project = self.request.query_params.get('id_project', None)
        if id_project is not None:
            queryset = DetailTimeline.objects.filter(id_project=id_project)
            return queryset
        return DetailTimeline.objects.all()

    def perform_create(self, serializer):
        detail_timeline_list = serializer.save()

        for detail_timeline in detail_timeline_list:
            user_id = detail_timeline.id_user.id_user
            self.log_activity(
                user_id, 'created', 'DetailTimeline', detail_timeline
            )

        return Response(
            serializer.data, status=status.HTTP_201_CREATED
        )

    def log_activity(
        self, user_id, action, name_table, detail_timeline,
        new_photo=None, old_photo=None
    ):
        user_instance = get_object_or_404(User, id_user=user_id)

        object_data = {
            'weeks': detail_timeline.weeks,
            'activity': detail_timeline.activity,
            # Saring old_Data jika tidak ada pada objek DetailTimeline
            # ... (kolom lainnya)
        }

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )

class DetailTimelinePublicDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = DetailTimeline.objects.all()
    serializer_class = DetailTimelineSerializer

    def get_serializer(self, *args, **kwargs):
        if (
            'fields' not in kwargs and
            self.serializer_class == DetailTimelineListSerializer
        ):
            kwargs['context'] = {
                'fields': ['user', 'project_internal', 'weeks', 'activity']
            }
        return super().get_serializer(*args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_data = model_to_dict(instance)  
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, old_data)
        return Response(
            {"message": "Update berhasil"}, status=status.HTTP_200_OK
        )

    def perform_update(self, serializer, old_data):
        user_id = serializer.instance.id_user.pk
        serializer.save()
        self.log_activity(
            user_id, 'updated', 'DetailTimeline', old_data=old_data
        )

    def perform_destroy(self, instance):
        user_id = instance.id_user.pk
        old_data = model_to_dict(instance)
        instance.delete()
        self.log_activity(
            user_id, 'deleted', 'DetailTimeline', old_data=old_data
        )
        return Response(
            {"message": "DetailTimeline berhasil dihapus"},
            status=status.HTTP_204_NO_CONTENT
        )

    def log_activity(
        self, user_id, action, name_table, old_data, new_data=None
    ):
        user_instance = get_object_or_404(User, id_user=user_id)

        object_data = {
            'weeks': old_data['weeks'],
            'activity': old_data['activity'],
            # ... (kolom lainnya)
        }

        if new_data is not None:
            object_data.update({'changes': new_data})

        ActivityLog.objects.create(
            id_user=user_instance,
            action=action,
            name_table=name_table,
            object=json.dumps(object_data),
        )
