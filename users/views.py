from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from .forms import UserRegisterForm, OTPVerificationForm
from .models import OTPVerification

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Save the user instance but don't commit to DB yet
            user = form.save(commit=False)
            user.is_active = False  # Deactivate user until email is verified
            user.save()

            # Generate and send OTP
            otp = get_random_string(length=6, allowed_chars='0123456789')
            OTPVerification.objects.create(user=user, otp=otp)

            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}. Use it to verify your email.',
                'noreply@yourdomain.com',  # Replace with your sender email
                [user.email],
                fail_silently=False,
            )
            # messages.info(request, f'OTP sent to {user.email}. Verify to activate your account.')
            return redirect('verify_otp', user_id=user.id)
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def verify_otp(request, user_id):
    user = OTPVerification.objects.get(user_id=user_id).user
    email = user.email
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data.get('otp')
            try:
                otp_entry = OTPVerification.objects.get(user_id=user_id, otp=otp)
                user = otp_entry.user
                user.is_active = True
                user.save()
                otp_entry.delete()  # Clean up OTP entry after successful verification
                messages.success(request, 'Email verified successfully! Please log in.')
                return redirect('login')
            except OTPVerification.DoesNotExist:
                messages.error(request, 'Invalid OTP. Please try again.')
    else:
        form = OTPVerificationForm()
    return render(request, 'users/verify_otp.html', {'form': form})
