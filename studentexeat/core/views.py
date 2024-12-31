from django.shortcuts import render, redirect,get_object_or_404
from .models import ExeatRequest,UserRole,Student,Hod
from .forms import ExeatRequestForm,EmergencyForm
from google.cloud import speech_v1p1beta1 as speech
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required 

from django.contrib.auth import authenticate, login
from .forms import MatricNumberLoginForm, UpdateProfileForm,RejectionReasonForm
from django.contrib import messages
from django.utils import timezone



@login_required 
def home(request): 
    user_role = None 
    if request.user.is_authenticated: 
        try: 
            user_role = UserRole.objects.get(user=request.user) 
            print(f'Yo!!!!!!! {user_role.role}')
        except UserRole.DoesNotExist: 
            user_role = None 
    context = { 'user_role': user_role }
    return render(request, 'home.html',context)




@login_required
def create_exeat_request(request):
    user_role = UserRole.objects.get(user=request.user) 
    if request.method == 'POST':
        form = ExeatRequestForm(request.POST, request.FILES)
        form.instance.student = request.user.student
        if form.is_valid():
            exeat_request = form.save(commit=False)
            exeat_request.student = request.user.student
            exeat_request.approved_by_student_affairs = False
            exeat_request.approved_by_hod = False
            exeat_request.approved_by_warden = False
            
            if 'audio_file' in request.FILES:
                audio_file = request.FILES['audio_file']
                audio_file_path = os.path.join(settings.MEDIA_ROOT, audio_file.name)
                with open(audio_file_path, 'wb+') as destination:
                    for chunk in audio_file.chunks():
                        destination.write(chunk)

                # Transcribe the audio file directly
                exeat_request.reason = transcribe_audio(audio_file_path)

                # Remove the temporary file after transcription
                os.remove(audio_file_path)
            else:
                exeat_request.reason = form.cleaned_data['reason']
            
            exeat_request.save()

            # Send email notification to guardian
            send_guardian_notification(request.user.student, exeat_request)
            messages.success(request, "Your request has been submitted and will be processed by various officers")
            return redirect('home')
    else:
        form = ExeatRequestForm()
    return render(request, 'create_exeat_request.html', {'form': form,'user_role':user_role})





import os
from google.cloud import speech

def transcribe_audio(audio_file_path):
    client = speech.SpeechClient()
    with open(audio_file_path, 'rb') as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,  # Change to MP3 encoding
        sample_rate_hertz=16000,
        language_code='en-US'
    )
    response = client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript if response.results else ''




def hod_dashboard(request):
    user = request.user
    user_role = UserRole.objects.get(user=user)
    hoduser = Hod.objects.get(hod=user)
    
    if user_role.role == 'HeadOfDepartment':
        department = user_role.department
        requests = ExeatRequest.objects.filter(student__dept=department, approved_by_student_affairs=True).order_by('-created_at')
        return render(request, 'hod_dashboard.html', {'requests': requests,'hoduser':hoduser,'user_role':user_role})
    else:
        # Handle cases where the user is not an HoD
        return render(request, 'access_denied.html')


def female_hall_warden_dashboard(request):
    user = request.user
    user_role = UserRole.objects.get(user=user)
    if user_role.role == 'HallWarden':
        requests = ExeatRequest.objects.filter(student__gender='Female', approved_by_hod=True)
        return render(request, 'female_hall_warden_dashboard.html', {'requests': requests})
    

def male_hall_warden_dashboard(request):
    user = request.user
    user_role = UserRole.objects.get(user=user)
    if user_role.role == 'HallWarden':
        requests = ExeatRequest.objects.filter(student__gender='Male', approved_by_hod=True)
        return render(request, 'male_hall_warden_dashboard.html', {'requests': requests})




def send_guardian_notification(student, exeat_request):
    subject = 'Exeat Request Notification'
    message = f'Dear Guardian,\n\nYour ward, {student.user.student_id}, has initiated an exeat request. \n\nReason: {exeat_request.reason}\nStart Date: {exeat_request.start_date}\nEnd Date: {exeat_request.end_date}\n\nPlease contact the University for further details.\n\nBest regards,\nStudent Affairs'
    recipient_list = [student.guardian_email]
    send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)




def custom_login_view(request):
    if request.method == 'POST':
        form = MatricNumberLoginForm(request.POST)
        if form.is_valid():
            matric_number = form.cleaned_data['matric_number']
            password = form.cleaned_data['password']
            user = authenticate(request, username=matric_number, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Invalid matric number or password.')
    else:
        form = MatricNumberLoginForm()
    return render(request, 'login.html', {'form': form})



@login_required
def student_dashboard(request):
    try: 
        student = request.user.student  # Retrieve the Student object 
    except Student.DoesNotExist:  # Handle the case where the CustomUser does not have a Student object 
        return render(request, 'error.html', {'message': 'Student profile not found.'})
    
    recent_activities = ExeatRequest.objects.filter(student=student).order_by('-created_at')[:5]  # Adjust number of activities as needed
    pending_requests = ExeatRequest.objects.filter(student=student, status='Pending').order_by('-created_at')[:5]
    approved_requests = ExeatRequest.objects.filter(student=student, status='Approved').order_by('-created_at')[:5]
    rejected_requests = ExeatRequest.objects.filter(student=student, status='Rejected').order_by('-created_at')[:5]

    context = {
        'recent_activities': recent_activities,
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'rejected_requests': rejected_requests
    }
    return render(request, 'studentDash.html', context)



@login_required 
def update_profile(request): 
    student = request.user 
    if request.method == 'POST': 
        form = UpdateProfileForm(request.POST, instance=student) 
        if form.is_valid(): 
            form.save() 
            return redirect('student_dashboard') 
    else: 
        form = UpdateProfileForm(instance=student) 
    return render(request, 'update_profile.html', {'form':form})




@login_required
def approve_exeat_request(request, request_id):
    exeat_request = get_object_or_404(ExeatRequest, id=request_id)

    # Check if the user is HOD and from the same department
    user_role = UserRole.objects.get(user=request.user)
    if user_role.role == 'HeadOfDepartment' and exeat_request.student.dept == user_role.department:
        exeat_request.status = 'Approved'
        exeat_request.save()
        messages.success(request, f"Exeat request for {exeat_request.student.user.student_id} has been approved.")
    else:
        messages.error(request, "You do not have permission to approve this request.")

    return redirect('hod_dashboard')




@login_required
def reject_exeat_request(request, request_id):
    exeat_request = get_object_or_404(ExeatRequest, id=request_id)
    user_role = UserRole.objects.get(user=request.user)

    # Initialize the appropriate redirect URL based on user role and gender
    redirect_url = 'home'
    if user_role.role == 'StudentAffairs':
        redirect_url = 'student_affairs_dashboard'
    elif user_role.role == 'HeadOfDepartment':
        if exeat_request.student.dept == user_role.department:
            redirect_url = 'hod_dashboard'
        else:
            messages.error(request, "You do not have permission to reject this request.")
            return redirect(redirect_url)
    elif user_role.role == 'HallWarden' and user_role.gender == 'Female':
        redirect_url = 'female_hall_warden_dashboard'
    elif user_role.role == 'HallWarden' and user_role.gender == 'Male':
        redirect_url = 'male_hall_warden_dashboard'
    else:
        messages.error(request, "You do not have permission to reject this request.")
        return redirect(redirect_url)
    
    # Handle form submission for rejection reason
    if request.method == 'POST':
        form = RejectionReasonForm(request.POST, instance=exeat_request)
        if form.is_valid():
            exeat_request = form.save(commit=False)
            exeat_request.status = 'Rejected'
            exeat_request.save()
            messages.success(request, f"Exeat request for {exeat_request.student.user.student_id} has been rejected.")
            return redirect(redirect_url)
    else:
        form = RejectionReasonForm(instance=exeat_request)

    return render(request, 'reject_exeat_request.html', {'form': form, 'exeat_request': exeat_request})





@login_required
def student_affairs_dashboard(request):
    user = request.user
    user_role = UserRole.objects.get(user=user)
    
    if user_role.role == 'StudentAffairs':
        # Retrieve all exeat requests that need to be processed by Student Affairs
        pending_exeat_requests = ExeatRequest.objects.filter(approved_by_student_affairs=False, status='Pending').order_by('-created_at') 
        rejected_requests = ExeatRequest.objects.filter(approved_by_student_affairs=False, status='Rejected').order_by('-created_at')
        
        context = {
            'pending_exeat_requests': pending_exeat_requests,
            'user_role':user_role,
            'rejected_requests':rejected_requests,
        }
        return render(request, 'student_affairs_dashboard.html', context)
    else:
        messages.error(request, "You do not have permission to view this page.")
        return render(request, 'access_denied.html')


@login_required
def approve_student_affairs_exeat_request(request, request_id):
    exeat_request = get_object_or_404(ExeatRequest, id=request_id)

    # Check if the user is in Student Affairs
    user_role = UserRole.objects.get(user=request.user)
    if user_role.role == 'StudentAffairs':
        exeat_request.approved_by_student_affairs = True
        exeat_request.status = 'Approved'
        exeat_request.save()
        messages.success(request, f"Exeat request for {exeat_request.student.user.student_id} has been approved by Student Affairs.")
    else:
        messages.error(request, "You do not have permission to approve this request.")

    return redirect('student_affairs_dashboard')

@login_required
def reject_student_affairs_exeat_request(request, request_id):
    exeat_request = get_object_or_404(ExeatRequest, id=request_id)

    # Check if the user is in Student Affairs
    user_role = UserRole.objects.get(user=request.user)
    if user_role.role == 'StudentAffairs':
        exeat_request.approved_by_student_affairs = False
        exeat_request.status = 'Rejected'
        exeat_request.save()
        messages.success(request, f"Exeat request for {exeat_request.student.user.student_id} has been rejected by Student Affairs.")
    else:
        messages.error(request, "You do not have permission to reject this request.")

    return redirect('student_affairs_dashboard')


@login_required
def approve_exeat_request_female_warden(request, request_id):
    exeat_request = get_object_or_404(ExeatRequest, id=request_id)

    user_role = UserRole.objects.get(user=request.user)
    if user_role.role == 'HallWarden' and user_role.gender == 'Female':
        exeat_request.approved_by_warden = True
        exeat_request.save()
        messages.success(request, f"Exeat request for {exeat_request.student.user.student_id} has been approved by the Female Hall Warden.")
    else:
        messages.error(request, "You do not have permission to approve this request.")

    return redirect('female_hall_warden_dashboard')

@login_required
def reject_exeat_request_female_warden(request, request_id):
    exeat_request = get_object_or_404(ExeatRequest, id=request_id)

    user_role = UserRole.objects.get(user=request.user)
    if user_role.role == 'HallWarden' and user_role.gender == 'Female':
        exeat_request.status = 'Rejected'
        exeat_request.save()
        messages.success(request, f"Exeat request for {exeat_request.student.user.student_id} has been rejected by the Female Hall Warden.")
    else:
        messages.error(request, "You do not have permission to reject this request.")

    return redirect('female_hall_warden_dashboard')

@login_required
def approve_exeat_request_male_warden(request, request_id):
    exeat_request = get_object_or_404(ExeatRequest, id=request_id)

    user_role = UserRole.objects.get(user=request.user)
    if user_role.role == 'HallWarden' and user_role.gender == 'Male':
        exeat_request.approved_by_warden = True
        exeat_request.save()
        messages.success(request, f"Exeat request for {exeat_request.student.user.student_id} has been approved by the Male Hall Warden.")
    else:
        messages.error(request, "You do not have permission to approve this request.")

    return redirect('male_hall_warden_dashboard')

@login_required
def reject_exeat_request_male_warden(request, request_id):
    exeat_request = get_object_or_404(ExeatRequest, id=request_id)

    user_role = UserRole.objects.get(user=request.user)
    if user_role.role == 'HallWarden' and user_role.gender == 'Male':
        exeat_request.status = 'Rejected'
        exeat_request.save()
        messages.success(request, f"Exeat request for {exeat_request.student.user.student_id} has been rejected by the Female Hall Warden.")
    else:
        messages.error(request, "You do not have permission to reject this request.")

    return redirect('male_hall_warden_dashboard')



@login_required
def create_emergency_exeat_by_officer(request):
    user_role = UserRole.objects.get(user=request.user)
    if user_role.role != 'StudentAffairs':
        messages.error(request, "You do not have permission to create emergency exeat requests.")
        return redirect('home')

    if request.method == 'POST':
        form = EmergencyForm(request.POST, request.FILES)
        if form.is_valid():
            exeat_request = form.save(commit=False)
            exeat_request.emergency = True  # Mark as emergency
            exeat_request.approved_by_student_affairs = True  # Automatically approve
            exeat_request.status = 'Approved'  # Set status to approved
            exeat_request.save()
            messages.success(request, "Emergency exeat request has been created and approved.")
            return redirect('student_affairs_dashboard')
    else:
        form = EmergencyForm()
    return render(request, 'create_emergency_exeat_by_officer.html', {'form': form,'user_role':user_role})



@login_required
def pending_returns_female_warden(request):
    user_role = UserRole.objects.get(user=request.user)
    
    if user_role.role == 'HallWarden' and user_role.gender == 'Female':
        pending_returns = ExeatRequest.objects.filter(
            student__gender='Female', 
            approved_by_student_affairs=True, 
            approved_by_hod=True, 
            approved_by_warden=True, 
            return_date__isnull=True
        ).order_by('-start_date')
        
        context = {
            'pending_returns': pending_returns,
        }
        return render(request, 'pending_returns_female_warden.html', context)
    else:
        messages.error(request, "You do not have permission to view this page.")
        return redirect('home')

@login_required
def pending_returns_male_warden(request):
    user_role = UserRole.objects.get(user=request.user)
    
    if user_role.role == 'HallWarden' and user_role.gender == 'Male':
        pending_returns = ExeatRequest.objects.filter(
            student__gender='Male', 
            approved_by_student_affairs=True, 
            approved_by_hod=True, 
            approved_by_warden=True, 
            return_date__isnull=True
        ).order_by('-start_date')
        
        context = {
            'pending_returns': pending_returns,
        }
        return render(request, 'pending_returns_male_warden.html', context)
    else:
        messages.error(request, "You do not have permission to view this page.")
        return redirect('home')


@login_required
def mark_return_female_warden(request, request_id):
    exeat_request = get_object_or_404(ExeatRequest, id=request_id)
    user_role = UserRole.objects.get(user=request.user)
    
    if user_role.role == 'HallWarden' and user_role.gender == 'Female':
        exeat_request.return_date = timezone.now()
        exeat_request.save()
        messages.success(request, f"Return date for {exeat_request.student.user.student_id} has been updated.")
        return redirect('pending_returns_female_warden')
    else:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('home')

@login_required
def mark_return_male_warden(request, request_id):
    exeat_request = get_object_or_404(ExeatRequest, id=request_id)
    user_role = UserRole.objects.get(user=request.user)
    
    if user_role.role == 'HallWarden' and user_role.gender == 'Male':
        exeat_request.return_date = timezone.now()
        exeat_request.save()
        messages.success(request, f"Return date for {exeat_request.student.user.student_id} has been updated.")
        return redirect('pending_returns_male_warden')
    else:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('home')

