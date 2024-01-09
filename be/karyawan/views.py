# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import User, ProjectStatus, ProjectInternal, DetailMainPower, ActivityLog

def tambah_internal_order(request):
    if request.method == 'POST':
        # Ambil data dari formulir atau request.POST sesuai kebutuhan Anda
        nama_order = request.POST.get('nama_order')
        deskripsi = request.POST.get('deskripsi')
        role = request.POST.get('role')
        
        # Simpan data baru ke model yang relevan
        user = get_object_or_404(User, nama=request.user.username)
        project = ProjectInternal.objects.create(
            status=ProjectStatus.ON_GOING,
            requester=request.user.username,
            application_name=nama_order,
            id_user=user
        )
        role_detail = DetailMainPower.objects.create(
            man_days_rate=0,  
            man_power=0,  
            days=0,  
            role=role,
            id_user=user,
            id_project=project
        )

        # Tambahkan entri ke ActivityLog
        ActivityLog.objects.create(
            detail_activity=f"Nama Order: {nama_order}, Deskripsi: {deskripsi}, Role: {role}",
            action_activity="Menambahkan Internal Order",
            id_user=user,
            id_project=project,
            id_role=role_detail
        )

        return HttpResponse("Internal Order berhasil ditambahkan.")
    else:
        # Logika untuk menampilkan formulir tambah internal order
        # ...
        return HttpResponse("GET request tidak diizinkan untuk halaman ini.")

def lihat_project_internal(request, id):
    project_internal = get_object_or_404(ProjectInternal, id=id)
    # Logika untuk menampilkan detail project_internal
    return render(request, 'lihat_project_internal.html', {'project_internal': project_internal})

def update_project_internal(request, id):
    project_internal = get_object_or_404(ProjectInternal, id=id)

    if request.method == 'POST':
        # Ambil data dari formulir atau request.POST sesuai kebutuhan Anda
        project_internal.status = request.POST.get('status')
        project_internal.requester = request.POST.get('requester')
        project_internal.application_name = request.POST.get('application_name')
        # Update data project_internal
        project_internal.save()

        # Tambahkan entri ke ActivityLog
        ActivityLog.objects.create(
            detail_activity=f"Project {project_internal.application_name} diupdate",
            action_activity="Mengubah Internal Order",
            id_user=request.user,
            id_project=project_internal,
        )

        return HttpResponse("Project Internal berhasil diupdate.")
    else:
        # Logika untuk menampilkan formulir update project_internal
        # ...
        return render(request, 'update_project_internal.html', {'project_internal': project_internal})

def hapus_project_internal(request, id):
    project_internal = get_object_or_404(ProjectInternal, id=id)

    if request.method == 'POST':
        # Tambahkan entri ke ActivityLog sebelum menghapus
        ActivityLog.objects.create(
            detail_activity=f"Project {project_internal.application_name} dihapus",
            action_activity="Menghapus Internal Order",
            id_user=request.user,
            id_project=project_internal,
        )

        # Hapus data project_internal
        project_internal.delete()

        return HttpResponse("Project Internal berhasil dihapus.")
    else:
        # Logika untuk menampilkan konfirmasi penghapusan project_internal
        # ...
        return render(request, 'hapus_project_internal.html', {'project_internal': project_internal})
