from django.shortcuts import render , redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UploadedFile
import json
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

 

# Create your views here.
def index_view(request):
    files = UploadedFile.objects.all().order_by('-uploaded_at')[:10]  
    return render(request, 'index.html', {'files': files})


@csrf_exempt
def admin_view(request):
    if request.method == 'GET':
        files = UploadedFile.objects.all().order_by('-uploaded_at')
        return render(request, 'Dashboard.html', {'files': files})

    elif request.method == 'POST':
        # Check if this is an upload or an update based on presence of ID
        file_id = request.POST.get('id')
        if file_id:
            # File update logic via POST (to avoid PUT limitations)
            try:
                uploaded_file = UploadedFile.objects.get(id=file_id)
                if 'file' not in request.FILES:
                    return JsonResponse({'status': 'error', 'message': 'No file provided for update'}, status=400)

                uploaded_file.file = request.FILES['file']
                uploaded_file.updated_at = timezone.now()
                uploaded_file.save()

                return JsonResponse({'status': 'success', 'message': 'File updated successfully!'})
            except UploadedFile.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'File not found'}, status=404)

        # Handle new file upload
        if 'file' in request.FILES:
            files = request.FILES.getlist('file')
            for file in files:
                uploaded_file = UploadedFile(
                    file=file,
                    uploaded_at=timezone.now(),
                    updated_at=timezone.now()
                )
                uploaded_file.save()
            return JsonResponse({'status': 'success', 'message': f'{len(files)} file(s) uploaded successfully!'})
        else:
            return JsonResponse({'status': 'error', 'message': 'No files selected'}, status=400)

    elif request.method == 'PUT':
        # Avoid trying to read binary data as JSON
        if request.content_type.startswith('multipart/form-data'):
            return JsonResponse({
                'status': 'error',
                'message': 'PUT requests with files are not supported. Use POST instead.'
            }, status=400)

        try:
            body_data = request.body.decode('utf-8')
            data = json.loads(body_data)
            file_id = data.get('id')
            if not file_id:
                return JsonResponse({'status': 'error', 'message': 'File ID missing'}, status=400)

            uploaded_file = UploadedFile.objects.get(id=file_id)
            uploaded_file.updated_at = timezone.now()
            uploaded_file.save()

            return JsonResponse({'status': 'success', 'message': 'Metadata updated (no file change)'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'}, status=400)
        except UploadedFile.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'File not found'}, status=404)

    elif request.method == 'DELETE':
        try:
            body_data = request.body.decode('utf-8')
            data = json.loads(body_data)
            file_id = data.get('id')
            if not file_id:
                return JsonResponse({'status': 'error', 'message': 'File ID missing'}, status=400)

            uploaded_file = UploadedFile.objects.get(id=file_id)
            uploaded_file.file.delete()
            uploaded_file.delete()
            return JsonResponse({'status': 'success', 'message': 'File deleted successfully!'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except UploadedFile.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'File not found'}, status=404)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)



