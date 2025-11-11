from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator, RegexValidator

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    college_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    middle_name = models.CharField(max_length=30, blank=True, null=True)
    mobile_no = models.CharField(max_length=15, validators=[RegexValidator(r'^\+?1?\d{9,15}$')], blank=True, null=True)
    aadhar_no = models.CharField(max_length=12, unique=True, blank=True, null=True, validators=[RegexValidator(r'^\d{12}$')])
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

class ExamForm(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    EXAM_TYPE_CHOICES = [
        ('winter', 'Winter'),
        ('summer', 'Summer'),
    ]
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='exam_forms')
    branch = models.CharField(max_length=100, blank=True, null=True)
    semester = models.CharField(max_length=50, blank=True, null=True)
    subjects = models.TextField(blank=True, null=True)  # Can be a comma-separated list or JSON
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE_CHOICES, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.username} - {self.branch} - {self.status}"

class Payment(models.Model):
    exam_form = models.OneToOneField(ExamForm, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_order_id = models.CharField(max_length=100, unique=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Payment for {self.exam_form} - {self.status}"

class Attendance(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    status = models.BooleanField(default=False)  # True for present, False for absent

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.username} - {self.date} - {'Present' if self.status else 'Absent'}"
