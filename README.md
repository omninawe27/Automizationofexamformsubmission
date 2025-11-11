
# Automation of Exam Form Submission System

## Overview
This is a Django-based web application designed to automate the exam form submission process for educational institutions. It allows students to register, fill out exam forms, make payments securely via Razorpay, and track their form status. Administrators can manage user registrations, approve/reject forms, and monitor overall system activity.

## Features
- **User Registration and Authentication**: Secure login/logout with role-based access (Student/Admin).
- **Exam Form Submission**: Students can fill and submit exam forms with details like branch, semester, subjects, and exam type.
- **Payment Integration**: Secure payment processing using Razorpay for form submission fees.
- **Admin Dashboard**: Administrators can view, approve, or reject submitted forms, and manage user registrations.
- **Student Dashboard**: Students can view their submitted forms, payment status, and download receipts upon approval.
- **Email Notifications**: Automated HTML emails for form submission, payment success, and approval/rejection.
- **Session Management**: Automatic session expiry and extension for security.
- **Password Reset**: Secure password reset functionality via email.
- **Attendance Tracking**: Basic attendance management for students.
- **Interactive UI**: Enhanced registration page with real-time validation, password strength indicators, and AJAX checks.

## Technologies Used
- **Backend**: Django (Python web framework)
- **Database**: SQLite (default; can be configured for PostgreSQL/MySQL)
- **Frontend**: HTML, CSS, JavaScript (with Bootstrap for styling)
- **Payment Gateway**: Razorpay
- **Email**: Django's built-in email system (configurable for SMTP)
- **Other**: AJAX for dynamic content, Django Forms for validation

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)

### Steps
1. **Clone the Repository**:
   ```
   git clone <repository-url>
   cd exam_form_system
   ```

2. **Create a Virtual Environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Configure Settings**:
   - Update `exam_form_system/settings.py` with your database, email, and Razorpay credentials.
   - Set environment variables for sensitive data (e.g., `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`, `EMAIL_HOST_PASSWORD`).

5. **Run Migrations**:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create Superuser (Admin)**:
   ```
   python manage.py createsuperuser
   ```

7. **Run the Server**:
   ```
   python manage.py runserver
   ```
   Access the application at `http://127.0.0.1:8000/`.

## Usage
- **Home Page**: Redirects authenticated users to their respective dashboards.
- **Student Workflow**:
  1. Register/Login.
  2. Fill and submit exam form.
  3. Make payment via Razorpay.
  4. View status and download receipts.
- **Admin Workflow**:
  1. Login as admin.
  2. View all submitted forms.
  3. Approve/Reject forms.
  4. Register new users if needed.
- **Password Reset**: Use the reset link sent to your email.

## Project Structure
```
exam_form_system/
├── exam_app/                 # Main Django app
│   ├── models.py            # Database models (CustomUser, ExamForm, Payment, Attendance)
│   ├── views.py             # View functions for handling requests
│   ├── forms.py             # Django forms for validation
│   ├── urls.py              # URL routing
│   ├── templates/           # HTML templates
│   ├── static/              # CSS, JS, images
│   └── admin.py             # Django admin configuration
├── exam_form_system/        # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/                   # Uploaded files (e.g., profile photos)
├── db.sqlite3               # Database file
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Contributing
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit changes: `git commit -am 'Add feature'`.
4. Push to branch: `git push origin feature-name`.
5. Submit a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or support, contact the development team at [your-email@example.com].
