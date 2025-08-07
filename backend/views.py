from django.shortcuts import render , redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UploadedFile
import json
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

 

# ============================ Index View ============================
# Display the latest 10 uploaded files on the homepage
def index_view(request):
    files = UploadedFile.objects.all().order_by('-uploaded_at')[:10]  
    return render(request, 'index.html', {'files': files})


# ============================ Admin Dashboard View ============================
# Handles GET for file listing, POST for upload/update, PUT for metadata update, DELETE for file deletion
@login_required(login_url='custom_error_view')
@csrf_exempt
def admin_view(request):
    # ---------- Handle GET: Show all uploaded files ----------
    if request.method == 'GET':
        files = UploadedFile.objects.all().order_by('-uploaded_at')
        return render(request, 'Dashboard.html', {'files': files})

    # ---------- Handle POST: Upload new file(s) or update existing file ----------
    elif request.method == 'POST':
        file_id = request.POST.get('id')
        
        # If 'id' is present, update the file
        if file_id:
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

        # If no 'id', handle new upload
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

    # ---------- Handle PUT: Update metadata only ----------
    elif request.method == 'PUT':
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

    # ---------- Handle DELETE: Delete the specified file ----------
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

    # ---------- Handle Unsupported Methods ----------
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)



# ============================ Login View ============================
# Handles login form + AJAX login and auto-creates a default superuser if missing
def login_view(request):
    # Create default user if it doesn't exist
    default_email = "admin@pioneersoftware.com"
    default_password = "Pioneer@Nepal"
    
    try:
        # Check if default user exists
        default_user = User.objects.get(email=default_email)
    except User.DoesNotExist:
        # Create default user
        default_user = User.objects.create_user(
            username=default_email,
            email=default_email,
            password=default_password,
            first_name="Admin",
            last_name="Pioneer Software",
            is_staff=True,
            is_superuser=True
        )
        print(f"Created default user: {default_email}")
    
    # Redirect authenticated users to admin
    if request.user.is_authenticated:
        return redirect('admin_view')
    
    if request.method == 'POST':
        # Handle AJAX login request
        if request.headers.get('Content-Type') == 'application/json':
            try:
                data = json.loads(request.body)
                username = data.get('username', '').strip()
                password = data.get('password', '').strip()
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False, 
                    'message': 'Invalid JSON data'
                }, status=400)
        else:
            # Handle form submission
            username = request.POST.get('username', '').strip()
            password = request.POST.get('password', '').strip()
        
        # Validation
        if not username or not password:
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({
                    'success': False, 
                    'message': 'Please fill in all fields'
                })
            else:
                messages.error(request, 'Please fill in all fields')
                return render(request, 'login.html')
        
        # Authenticate user (by username or email)
        user = authenticate(request, username=username, password=password)
        if user is None:
            try:
                user_by_email = User.objects.get(email=username)
                user = authenticate(request, username=user_by_email.username, password=password)
            except User.DoesNotExist:
                pass
        
        if user is not None:
            if user.is_active:
                login(request, user)
                if request.headers.get('Content-Type') == 'application/json':
                    return JsonResponse({
                        'success': True, 
                        'message': 'Login successful! Redirecting...',
                        'redirect_url': '/admin/'
                    })
                else:
                    messages.success(request, 'Login successful!')
                    return redirect('admin_view')
            else:
                message = 'Your account is disabled'
                if request.headers.get('Content-Type') == 'application/json':
                    return JsonResponse({
                        'success': False, 
                        'message': message
                    })
                else:
                    messages.error(request, message)
        else:
            message = 'Invalid username or password'
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({
                    'success': False, 
                    'message': message
                })
            else:
                messages.error(request, message)
    
    return render(request, 'login.html')


# ============================ Logout View ============================
# Logs out the current user and redirects to login page
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('login_view')




# ============================ Custom Error View ============================
# Handles custom error like 406 Not Acceptable and renders a specific template
def custom_error_view(request, exception=None):
    return render(request, 'unauth.html', status=406)