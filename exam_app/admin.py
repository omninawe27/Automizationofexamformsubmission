from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, ExamForm, Payment, Attendance

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'college_id', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'college_id')
    ordering = ('username',)
    actions = ['delete_selected']

    def has_delete_permission(self, request, obj=None):
        return True

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'college_id', 'middle_name', 'mobile_no', 'aadhar_no', 'date_of_birth', 'address', 'profile_photo')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('role', 'college_id', 'middle_name', 'mobile_no', 'aadhar_no', 'date_of_birth', 'address', 'profile_photo', 'email')
        }),
    )

@admin.register(ExamForm)
class ExamFormAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'branch', 'semester', 'exam_type', 'status', 'submitted_at', 'approved_at')
    list_filter = ('status', 'exam_type', 'branch', 'semester', 'submitted_at', 'approved_at')
    search_fields = ('student__username', 'student__email', 'student__college_id', 'branch', 'semester')
    ordering = ('-submitted_at',)
    readonly_fields = ('submitted_at', 'approved_at')

    fieldsets = (
        ('Student Information', {
            'fields': ('student',)
        }),
        ('Exam Details', {
            'fields': ('branch', 'semester', 'subjects', 'exam_type')
        }),
        ('Status', {
            'fields': ('status', 'submitted_at', 'approved_at')
        }),
    )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'exam_form', 'amount', 'status', 'razorpay_order_id', 'paid_at')
    list_filter = ('status', 'created_at', 'paid_at')
    search_fields = ('exam_form__student__username', 'exam_form__student__email', 'razorpay_order_id', 'razorpay_payment_id')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'paid_at')

    fieldsets = (
        ('Payment Information', {
            'fields': ('exam_form', 'amount', 'razorpay_order_id', 'razorpay_payment_id')
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'paid_at')
        }),
    )

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'date', 'status')
    list_filter = ('status', 'date')
    search_fields = ('student__username', 'student__email', 'student__college_id')
    ordering = ('-date',)

    fieldsets = (
        ('Attendance Information', {
            'fields': ('student', 'date', 'status')
        }),
    )
