
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.urls import reverse
import razorpay
import json
from .models import CustomUser, ExamForm, Payment, Attendance
from .forms import ExamFormForm, CustomUserCreationForm, CustomUserEditForm, get_subjects_by_semester, get_subjects_by_branch_and_semester

def home(request):
    # Redirect authenticated users to their dashboard
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return redirect('admin_dashboard')
        else:
            return redirect('student_dashboard')
    return render(request, 'exam_app/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            # Try to authenticate using college_id
            try:
                user_obj = CustomUser.objects.get(college_id=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except CustomUser.DoesNotExist:
                pass
        if user is not None:
            # Force logout any existing user before login
            if request.user.is_authenticated:
                logout(request)

            login(request, user)
            # Set session expiry to 30 minutes after successful login
            request.session.set_expiry(1800)  # 30 minutes in seconds
            messages.success(request, 'Login successful!')
            if user.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('student_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'exam_app/login.html')



def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('admin_dashboard')
    exam_forms = ExamForm.objects.filter(student=request.user)
    # Get session expiry time
    session_expiry = request.session.get_expiry_date()
    session_expiry_timestamp = int(session_expiry.timestamp() * 1000) if session_expiry else 0

    # Calculate counts
    approved_count = exam_forms.filter(status='approved').count()
    pending_count = exam_forms.filter(status='pending').count()

    return render(request, 'exam_app/student_dashboard.html', {
        'exam_forms': exam_forms,
        'session_expiry_timestamp': session_expiry_timestamp,
        'approved_count': approved_count,
        'pending_count': pending_count
    })

@login_required
def fill_exam_form(request):
    if request.user.role != 'student':
        return redirect('admin_dashboard')
    if request.method == 'POST':
        form = ExamFormForm(request.POST)
        if form.is_valid():
            # Store form data in session instead of saving to database
            form_data = {
                'branch': form.cleaned_data['branch'],
                'semester': form.cleaned_data['semester'],
                'subjects': ','.join(form.cleaned_data['subjects']),
                'exam_type': form.cleaned_data['exam_type']
            }
            request.session['exam_form_data'] = form_data

            # Send HTML email notification after form submission
            from django.template.loader import render_to_string
            from django.core.mail import EmailMessage

            context = {
                'user_name': request.user.get_full_name() or request.user.username,
                'branch': form_data['branch'],
                'semester': form_data['semester'],
                'exam_type': form_data['exam_type'],
                'subjects': form_data['subjects'],
                'payment_url': request.build_absolute_uri('/payment/'),
            }

            html_content = render_to_string('exam_app/email_form_submitted.html', context)

            email = EmailMessage(
                '📝 Exam Form Submitted Successfully',
                html_content,
                settings.DEFAULT_FROM_EMAIL,
                [request.user.email],
            )
            email.content_subtype = 'html'
            email.send(fail_silently=True)

            messages.success(request, 'Form details saved. Proceed to payment.')
            return redirect('payment')
    else:
        # Check if there's existing form data in session (for editing)
        existing_data = request.session.get('exam_form_data')
        if existing_data:
            form = ExamFormForm(initial=existing_data)
        else:
            form = ExamFormForm(initial={'branch': 'cse', 'semester': '1'})
    return render(request, 'exam_app/fill_form.html', {'form': form})

@login_required
def payment(request):
    if request.user.role != 'student':
        return redirect('admin_dashboard')

    # Check if form data exists in session
    form_data = request.session.get('exam_form_data')
    if not form_data:
        messages.error(request, 'No form data found. Please fill the exam form first.')
        return redirect('fill_exam_form')

    # Create Razorpay order
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    amount = 10000  # Amount in paisa (100 INR)
    order_data = {
        'amount': amount,
        'currency': 'INR',
        'payment_capture': '1'
    }
    order = client.order.create(data=order_data)

    # Store payment order ID in session for later use
    request.session['razorpay_order_id'] = order['id']

    return render(request, 'exam_app/payment.html', {
        'form_data': form_data,
        'amount': amount / 100,
        'razorpay_order_id': order['id'],
        'razorpay_key_id': settings.RAZORPAY_KEY_ID
    })

@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_signature = data.get('razorpay_signature')

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })

            # Get form data from session
            form_data = request.session.get('exam_form_data')
            if not form_data:
                return JsonResponse({'status': 'failed', 'message': 'Form data not found'})

            # Create exam form only after successful payment
            exam_form = ExamForm.objects.create(
                student=request.user,
                branch=form_data['branch'],
                semester=form_data['semester'],
                subjects=form_data['subjects'],
                exam_type=form_data['exam_type'],
                status='pending'  # Set to pending for admin approval
            )

            # Create payment record
            payment = Payment.objects.create(
                exam_form=exam_form,
                amount=100.00,  # Amount in rupees
                razorpay_order_id=razorpay_order_id,
                razorpay_payment_id=razorpay_payment_id,
                status='paid',
                paid_at=timezone.now()
            )

            # Clear session data
            del request.session['exam_form_data']
            del request.session['razorpay_order_id']

            # Send HTML email notification for payment success
            from django.template.loader import render_to_string
            from django.core.mail import EmailMessage

            context = {
                'user_name': request.user.get_full_name() or request.user.username,
                'form_id': exam_form.id,
                'amount': '100.00',
                'payment_id': razorpay_payment_id,
                'payment_date': payment.paid_at.strftime('%d %B %Y, %I:%M %p'),
                'dashboard_url': request.build_absolute_uri('/student/dashboard/'),
            }

            html_content = render_to_string('exam_app/email_payment_success.html', context)

            email = EmailMessage(
                '💳 Payment Successful - Form Submitted',
                html_content,
                settings.DEFAULT_FROM_EMAIL,
                [exam_form.student.email],
            )
            email.content_subtype = 'html'
            email.send(fail_silently=True)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'failed', 'message': str(e)})
    return JsonResponse({'status': 'invalid'})

@login_required
def download_receipt(request, form_id):
    exam_form = get_object_or_404(ExamForm, id=form_id, student=request.user)
    if exam_form.status != 'approved' or not hasattr(exam_form, 'payment') or exam_form.payment.status != 'paid':
        messages.error(request, 'Receipt not available.')
        return redirect('student_dashboard')
    return render(request, 'exam_app/receipt.html', {'exam_form': exam_form})

@login_required
def receipts(request):
    if request.user.role != 'student':
        return redirect('admin_dashboard')
    exam_forms = ExamForm.objects.filter(student=request.user, status='approved').prefetch_related('payment')
    return render(request, 'exam_app/receipts.html', {'exam_forms': exam_forms})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('admin_dashboard' if request.user.role == 'admin' else 'student_dashboard')
    else:
        form = CustomUserEditForm(instance=request.user)
    return render(request, 'exam_app/edit_profile.html', {'form': form})

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return redirect('student_dashboard')
    exam_forms = ExamForm.objects.all().order_by('-submitted_at')

    # Calculate statistics
    total_forms = exam_forms.count()
    pending_forms = exam_forms.filter(status='pending').count()
    approved_forms = exam_forms.filter(status='approved').count()
    rejected_forms = exam_forms.filter(status='rejected').count()

    context = {
        'exam_forms': exam_forms,
        'total_forms': total_forms,
        'pending_forms': pending_forms,
        'approved_forms': approved_forms,
        'rejected_forms': rejected_forms,
    }
    return render(request, 'exam_app/admin_dashboard.html', context)

@login_required
def register_view(request):
    if request.user.role != 'admin':
        return redirect('student_dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'User registration successful!')
            return redirect('login')
        else:
            # Add form errors as messages for notification
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        form = CustomUserCreationForm()

    return render(request, 'exam_app/register.html', {'form': form})

@login_required
def approve_form(request, form_id):
    if request.user.role != 'admin':
        return redirect('student_dashboard')
    exam_form = get_object_or_404(ExamForm, id=form_id)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            exam_form.status = 'approved'
            exam_form.approved_at = timezone.now()
            status_text = 'approved'
        elif action == 'reject':
            exam_form.status = 'rejected'
            status_text = 'rejected'
        exam_form.save()

        # Send HTML email notification for approval/rejection
        from django.template.loader import render_to_string
        from django.core.mail import EmailMessage

        if action == 'approve':
            context = {
                'user_name': exam_form.student.get_full_name() or exam_form.student.username,
                'form_id': exam_form.id,
                'branch': exam_form.branch,
                'semester': exam_form.semester,
                'exam_type': exam_form.exam_type,
                'subjects': exam_form.subjects,
                'approved_at': exam_form.approved_at.strftime('%d %B %Y, %I:%M %p'),
                'dashboard_url': request.build_absolute_uri('/student/dashboard/'),
            }

            html_content = render_to_string('exam_app/email_form_approved.html', context)

            email = EmailMessage(
                '🎉 Exam Form Approved - Action Required',
                html_content,
                settings.DEFAULT_FROM_EMAIL,
                [exam_form.student.email],
            )
            email.content_subtype = 'html'
            email.send(fail_silently=True)
        else:
            # Send simple rejection email (keeping it simple for now)
            send_mail(
                f'Exam Form {status_text.capitalize()}',
                f'Your exam form {exam_form.id} has been {status_text}.',
                settings.DEFAULT_FROM_EMAIL,
                [exam_form.student.email],
                fail_silently=True,
            )

        messages.success(request, f'Form {status_text}.')
        return redirect('admin_dashboard')
    return render(request, 'exam_app/approve_form.html', {'exam_form': exam_form})

@login_required
def view_status(request, form_id):
    exam_form = get_object_or_404(ExamForm, id=form_id)
    if request.user.role != 'admin' and exam_form.student != request.user:
        return redirect('student_dashboard')
    return render(request, 'exam_app/view_status.html', {'exam_form': exam_form})

@login_required
def get_subjects(request):
    branch = request.GET.get('branch')
    semester = request.GET.get('semester')
    if branch and semester:
        subjects_tuples = get_subjects_by_branch_and_semester(branch, semester)
        subjects = [{'value': value, 'label': label} for value, label in subjects_tuples]
        return JsonResponse({'subjects': subjects})
    return JsonResponse({'error': 'Branch and semester not provided'}, status=400)

@login_required
def extend_session(request):
    if request.method == 'POST':
        # Extend the session by updating the expiry time
        request.session.set_expiry(1800)  # 30 minutes from now
        return JsonResponse({'success': True, 'message': 'Session extended successfully'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'}, status=400)

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))
            subject = 'Password Reset Request'
            message = render_to_string('exam_app/password_reset_email.html', {
                'user': user,
                'reset_url': reset_url,
            })
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
            messages.success(request, 'Password reset email sent.')
            return redirect('password_reset_done')
        except User.DoesNotExist:
            messages.error(request, 'No user with this email address.')
    return render(request, 'exam_app/password_reset.html')

def password_reset_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password reset successful.')
                return redirect('password_reset_complete')
            else:
                messages.error(request, 'Passwords do not match.')
        return render(request, 'exam_app/password_reset_confirm.html')
    else:
        messages.error(request, 'Invalid reset link.')
        return redirect('password_reset')

def password_reset_done(request):
    return render(request, 'exam_app/password_reset_done.html')

def password_reset_complete(request):
    return render(request, 'exam_app/password_reset_complete.html')

@login_required
def check_username(request):
    if request.user.role != 'admin':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    username = request.GET.get('username', '')
    exists = CustomUser.objects.filter(username=username).exists()
    return JsonResponse({'available': not exists})

@login_required
def check_email(request):
    if request.user.role != 'admin':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    email = request.GET.get('email', '')
    exists = CustomUser.objects.filter(email=email).exists()
    return JsonResponse({'available': not exists})
