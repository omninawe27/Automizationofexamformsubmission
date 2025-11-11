from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, ExamForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Enter your college email ending with @kdkce.edu.in")
    middle_name = forms.CharField(max_length=30, required=False)
    mobile_no = forms.CharField(max_length=15, required=True, help_text="Enter your mobile number")
    aadhar_no = forms.CharField(max_length=12, required=True, help_text="Enter your 12-digit Aadhar number")
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'college_id', 'first_name', 'middle_name', 'last_name', 'mobile_no', 'aadhar_no', 'date_of_birth', 'address', 'password1', 'password2', 'role')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@kdkce.edu.in'):
            raise forms.ValidationError("Email must end with @kdkce.edu.in")
        return email

class CustomUserEditForm(forms.ModelForm):
    profile_photo = forms.ImageField(required=False, help_text="Upload your profile photo")

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'college_id', 'first_name', 'middle_name', 'last_name', 'mobile_no', 'aadhar_no', 'date_of_birth', 'address', 'profile_photo')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@kdkce.edu.in'):
            raise forms.ValidationError("Email must end with @kdkce.edu.in")
        return email

def get_subjects_by_branch_and_semester(branch, semester):
    """
    Returns a list of subject choices for the given branch and semester.
    """
    # Common subjects for semesters 1 and 2
    common_subjects = {
        '1': [
            ('engineering_mathematics_i', 'Engineering Mathematics-I'),
            ('engineering_physics', 'Engineering Physics'),
            ('engineering_graphics', 'Engineering Graphics'),
            ('basic_electrical_engineering', 'Basic Electrical Engineering'),
            ('communication_skills', 'Communication Skills'),
        ],
        '2': [
            ('engineering_mathematics_ii', 'Engineering Mathematics-II'),
            ('engineering_chemistry', 'Engineering Chemistry'),
            ('engineering_mechanics', 'Engineering Mechanics'),
            ('basics_of_programming', 'Basics of Programming'),
            ('basic_electronics_engineering', 'Basic Electronics Engineering'),
        ],
    }

    # Branch-specific subjects
    branch_subjects = {
        'cse': {
            '3': [
                ('applied_mathematics_iii', 'Applied Mathematics-III'),
                ('object_oriented_programming', 'Object-Oriented Programming'),
                ('data_structures', 'Data Structures'),
                ('digital_electronics', 'Digital Electronics'),
                ('universal_human_values', 'Universal Human Values'),
            ],
            '4': [
                ('design_and_analysis_of_algorithms', 'Design and Analysis of Algorithms'),
                ('database_management_systems', 'Database Management Systems'),
                ('operating_systems', 'Operating Systems'),
                ('theory_of_computation', 'Theory of Computation'),
                ('computer_organization', 'Computer Organization'),
            ],
            '5': [
                ('artificial_intelligence', 'Artificial Intelligence'),
                ('software_engineering', 'Software Engineering'),
                ('computer_networks', 'Computer Networks'),
                ('pe_data_warehousing', 'Professional Elective-I: Data Warehousing'),
                ('pe_computer_graphics', 'Professional Elective-I: Computer Graphics'),
            ],
            '6': [
                ('compilers', 'Compilers'),
                ('web_technologies', 'Web Technologies'),
                ('pe_machine_learning', 'Professional Elective-II: Machine Learning'),
                ('pe_information_security', 'Professional Elective-II: Information Security'),
                ('oe_power_plant_engineering', 'Open Elective-I: Power Plant Engineering'),
                ('oe_industrial_safety', 'Open Elective-I: Industrial Safety'),
            ],
            '7': [
                ('cloud_computing', 'Cloud Computing'),
                ('cryptography_and_network_security', 'Cryptography and Network Security'),
                ('pe_deep_learning', 'Professional Elective-III: Deep Learning'),
                ('pe_natural_language_processing', 'Professional Elective-IV: Natural Language Processing'),
                ('oe_renewable_energy', 'Open Elective-II: Renewable Energy'),
                ('oe_project_management', 'Open Elective-II: Project Management'),
                ('project_i', 'Project-I'),
            ],
            '8': [
                ('project_ii', 'Project-II / Internship'),
                ('pe_big_data_analytics', 'Professional Elective-V: Big Data Analytics'),
                ('pe_internet_of_things', 'Professional Elective-VI: Internet of Things'),
                ('oe_entrepreneurship', 'Open Elective-III: Entrepreneurship'),
            ],
        },
        'it': {
            '3': [
                ('applied_mathematics_iii', 'Applied Mathematics-III'),
                ('data_structures', 'Data Structures'),
                ('object_oriented_programming', 'Object-Oriented Programming'),
                ('digital_electronics', 'Digital Electronics'),
                ('discrete_structures', 'Discrete Structures'),
            ],
            '4': [
                ('design_and_analysis_of_algorithms', 'Design and Analysis of Algorithms'),
                ('database_management_systems', 'Database Management Systems'),
                ('operating_systems', 'Operating Systems'),
                ('theory_of_computation', 'Theory of Computation'),
                ('computer_organization', 'Computer Organization'),
            ],
            '5': [
                ('software_engineering', 'Software Engineering'),
                ('computer_networks', 'Computer Networks'),
                ('artificial_intelligence', 'Artificial Intelligence'),
                ('pe_data_warehousing', 'Professional Elective-I: Data Warehousing'),
                ('pe_computer_graphics', 'Professional Elective-I: Computer Graphics'),
            ],
            '6': [
                ('web_technologies', 'Web Technologies'),
                ('compilers', 'Compilers'),
                ('pe_machine_learning', 'Professional Elective-II: Machine Learning'),
                ('pe_information_security', 'Professional Elective-II: Information Security'),
                ('oe_power_plant_engineering', 'Open Elective-I: Power Plant Engineering'),
                ('oe_industrial_safety', 'Open Elective-I: Industrial Safety'),
            ],
            '7': [
                ('cloud_computing', 'Cloud Computing'),
                ('mobile_application_development', 'Mobile Application Development'),
                ('pe_deep_learning', 'Professional Elective-III: Deep Learning'),
                ('pe_digital_forensics', 'Professional Elective-IV: Digital Forensics'),
                ('oe_renewable_energy', 'Open Elective-II: Renewable Energy'),
                ('oe_project_management', 'Open Elective-II: Project Management'),
                ('project_i', 'Project-I'),
            ],
            '8': [
                ('project_ii', 'Project-II / Internship'),
                ('pe_big_data_analytics', 'Professional Elective-V: Big Data Analytics'),
                ('pe_internet_of_things', 'Professional Elective-VI: Internet of Things'),
                ('oe_entrepreneurship', 'Open Elective-III: Entrepreneurship'),
            ],
        },
        'aids': {
            '3': [
                ('applied_mathematics_iii', 'Applied Mathematics-III'),
                ('data_structures', 'Data Structures'),
                ('object_oriented_programming', 'Object-Oriented Programming'),
                ('foundations_of_ai_and_data_science', 'Foundations of AI & Data Science'),
                ('discrete_mathematics', 'Discrete Mathematics'),
            ],
            '4': [
                ('design_and_analysis_of_algorithms', 'Design and Analysis of Algorithms'),
                ('database_management_systems', 'Database Management Systems'),
                ('operating_systems', 'Operating Systems'),
                ('probability_and_statistics_for_data_science', 'Probability & Statistics for Data Science'),
                ('computer_organization', 'Computer Organization'),
            ],
            '5': [
                ('machine_learning', 'Machine Learning'),
                ('computer_networks', 'Computer Networks'),
                ('big_data_analytics', 'Big Data Analytics'),
                ('pe_data_visualization', 'Professional Elective-I: Data Visualization'),
                ('pe_operations_research', 'Professional Elective-I: Operations Research'),
            ],
            '6': [
                ('deep_learning', 'Deep Learning'),
                ('software_engineering', 'Software Engineering'),
                ('pe_ai_for_games', 'Professional Elective-II: AI for Games'),
                ('pe_recommender_systems', 'Professional Elective-II: Recommender Systems'),
                ('oe_basics_of_civil_engg', 'Open Elective-I: Basics of Civil Engg.'),
                ('oe_control_systems', 'Open Elective-I: Control Systems'),
            ],
            '7': [
                ('natural_language_processing', 'Natural Language Processing'),
                ('cloud_computing', 'Cloud Computing'),
                ('pe_computer_vision', 'Professional Elective-III: Computer Vision'),
                ('pe_ai_in_healthcare', 'Professional Elective-IV: AI in Healthcare'),
                ('oe_electric_vehicles', 'Open Elective-II: Electric Vehicles'),
                ('oe_industrial_engg', 'Open Elective-II: Industrial Engg.'),
                ('project_i', 'Project-I'),
            ],
            '8': [
                ('project_ii', 'Project-II / Internship'),
                ('pe_ai_in_robotics', 'Professional Elective-V: AI in Robotics'),
                ('pe_audio_and_speech_processing', 'Professional Elective-VI: Audio & Speech Processing'),
                ('oe_business_intelligence', 'Open Elective-III: Business Intelligence'),
            ],
        },
        'electronics': {
            '3': [
                ('applied_mathematics_iii', 'Applied Mathematics-III'),
                ('electronic_devices_and_circuits', 'Electronic Devices & Circuits'),
                ('digital_system_design', 'Digital System Design'),
                ('network_theory', 'Network Theory'),
                ('electronic_measurements', 'Electronic Measurements'),
            ],
            '4': [
                ('analog_circuits', 'Analog Circuits'),
                ('signals_and_systems', 'Signals & Systems'),
                ('electromagnetic_waves', 'Electromagnetic Waves'),
                ('control_systems', 'Control Systems'),
                ('data_structures_and_algorithms', 'Data Structures & Algorithms'),
            ],
            '5': [
                ('linear_integrated_circuits', 'Linear Integrated Circuits'),
                ('digital_signal_processing', 'Digital Signal Processing'),
                ('computer_architecture', 'Computer Architecture'),
                ('pe_power_electronics', 'Professional Elective-I: Power Electronics'),
                ('oe_database_management', 'Open Elective-I: Database Management (DBMS)'),
                ('oe_ai_techniques', 'Open Elective-I: AI Techniques'),
            ],
            '6': [
                ('digital_communication', 'Digital Communication'),
                ('vlsi_design', 'VLSI Design'),
                ('computer_networks', 'Computer Networks'),
                ('pe_embedded_systems', 'Professional Elective-II: Embedded Systems'),
                ('oe_software_engineering', 'Open Elective-II: Software Engineering'),
                ('oe_renewable_energy', 'Open Elective-II: Renewable Energy'),
            ],
            '7': [
                ('microwave_and_radar_engineering', 'Microwave & Radar Engineering'),
                ('optical_communication', 'Optical Communication'),
                ('pe_wireless_communication', 'Professional Elective-III: Wireless Communication'),
                ('pe_satellite_communication', 'Professional Elective-IV: Satellite Communication'),
                ('oe_big_data_analytics', 'Open Elective-III: Big Data Analytics'),
                ('oe_project_management', 'Open Elective-III: Project Management'),
                ('project_i', 'Project-I'),
            ],
            '8': [
                ('project_ii', 'Project-II / Internship'),
                ('pe_advanced_vlsi', 'Professional Elective-V: Advanced VLSI'),
                ('pe_iot_and_sensor_networks', 'Professional Elective-VI: IoT & Sensor Networks'),
                ('oe_industrial_safety', 'Open Elective-IV: Industrial Safety'),
            ],
        },
        'electrical': {
            '3': [
                ('applied_mathematics_iii', 'Applied Mathematics-III'),
                ('network_analysis', 'Network Analysis'),
                ('electrical_machines_i', 'Electrical Machines-I'),
                ('electronic_devices_and_circuits', 'Electronic Devices & Circuits'),
                ('electrical_measurements', 'Electrical Measurements'),
            ],
            '4': [
                ('electrical_machines_ii', 'Electrical Machines-II'),
                ('power_system_i', 'Power System-I'),
                ('digital_electronics', 'Digital Electronics'),
                ('control_systems_i', 'Control Systems-I'),
                ('electromagnetic_fields', 'Electromagnetic Fields'),
            ],
            '5': [
                ('power_system_ii', 'Power System-II'),
                ('microprocessor_and_interfacing', 'Microprocessor & Interfacing'),
                ('power_electronics', 'Power Electronics'),
                ('pe_electrical_machine_design', 'Professional Elective-I: Electrical Machine Design'),
                ('oe_data_structures', 'Open Elective-I: Data Structures'),
                ('oe_ai_techniques', 'Open Elective-I: AI Techniques'),
            ],
            '6': [
                ('control_systems_ii', 'Control Systems-II'),
                ('power_system_stability', 'Power System Stability'),
                ('switchgear_and_protection', 'Switchgear & Protection'),
                ('pe_electric_drives', 'Professional Elective-II: Electric Drives'),
                ('oe_internet_of_things', 'Open Elective-II: Internet of Things (IoT)'),
                ('oe_web_technologies', 'Open Elective-II: Web Technologies'),
            ],
            '7': [
                ('high_voltage_engineering', 'High Voltage Engineering'),
                ('ehv_ac_transmission', 'EHV-AC Transmission'),
                ('pe_power_system_operation_and_control', 'Professional Elective-III: Power System Operation & Control'),
                ('pe_smart_grid_technology', 'Professional Elective-IV: Smart Grid Technology'),
                ('oe_cloud_computing', 'Open Elective-III: Cloud Computing'),
                ('oe_big_data', 'Open Elective-III: Big Data'),
                ('project_i', 'Project-I'),
            ],
            '8': [
                ('project_ii', 'Project-II / Internship'),
                ('pe_power_quality', 'Professional Elective-V: Power Quality'),
                ('pe_hvdc_transmission', 'Professional Elective-VI: HVDC Transmission'),
                ('oe_industrial_management', 'Open Elective-IV: Industrial Management'),
            ],
        },
        'mechanical': {
            '3': [
                ('applied_mathematics_iii', 'Applied Mathematics-III'),
                ('engineering_thermodynamics', 'Engineering Thermodynamics'),
                ('strength_of_materials', 'Strength of Materials'),
                ('manufacturing_processes_i', 'Manufacturing Processes-I'),
                ('engineering_metallurgy', 'Engineering Metallurgy'),
            ],
            '4': [
                ('fluid_mechanics', 'Fluid Mechanics'),
                ('theory_of_machines_i', 'Theory of Machines-I'),
                ('machine_drawing', 'Machine Drawing'),
                ('applied_thermal_engineering', 'Applied Thermal Engineering'),
            ],
            '5': [
                ('heat_transfer', 'Heat Transfer'),
                ('theory_of_machines_ii', 'Theory of Machines-II'),
                ('design_of_machine_elements_i', 'Design of Machine Elements-I'),
                ('pe_mechatronics', 'Professional Elective-I: Mechatronics'),
                ('oe_database_management', 'Open Elective-I: Database Management (DBMS)'),
                ('oe_web_design', 'Open Elective-I: Web Design'),
            ],
            '6': [
                ('control_systems', 'Control Systems'),
                ('design_of_machine_elements_ii', 'Design of Machine Elements-II'),
                ('finite_element_analysis', 'Finite Element Analysis (FEA)'),
                ('pe_robotics', 'Professional Elective-II: Robotics'),
                ('oe_ai_techniques', 'Open Elective-II: AI Techniques'),
                ('oe_internet_of_things', 'Open Elective-II: Internet of Things (IoT)'),
            ],
            '7': [
                ('refrigeration_and_air_conditioning', 'Refrigeration & Air Conditioning (RAC)'),
                ('cad_cam', 'CAD/CAM'),
                ('pe_automobile_engineering', 'Professional Elective-III: Automobile Engineering'),
                ('pe_computational_fluid_dynamics', 'Professional Elective-IV: Computational Fluid Dynamics (CFD)'),
                ('oe_cloud_computing', 'Open Elective-III: Cloud Computing'),
                ('oe_project_management', 'Open Elective-III: Project Management'),
                ('project_i', 'Project-I'),
            ],
            '8': [
                ('project_ii', 'Project-II / Internship'),
                ('pe_power_plant_engineering', 'Professional Elective-V: Power Plant Engineering'),
                ('pe_advanced_manufacturing_processes', 'Professional Elective-VI: Advanced Manufacturing Processes'),
                ('oe_entrepreneurship', 'Open Elective-IV: Entrepreneurship'),
            ],
        },
        'civil': {
            '3': [
                ('applied_mathematics_iii', 'Applied Mathematics-III'),
                ('strength_of_materials', 'Strength of Materials'),
                ('fluid_mechanics_i', 'Fluid Mechanics-I'),
                ('surveying_i', 'Surveying-I'),
                ('building_construction_and_materials', 'Building Construction & Materials'),
            ],
            '4': [
                ('structural_analysis_i', 'Structural Analysis-I'),
                ('fluid_mechanics_ii', 'Fluid Mechanics-II'),
                ('surveying_ii', 'Surveying-II'),
                ('concrete_technology', 'Concrete Technology'),
                ('geotechnical_engineering_i', 'Geotechnical Engineering-I'),
            ],
            '5': [
                ('structural_analysis_ii', 'Structural Analysis-II'),
                ('geotechnical_engineering_ii', 'Geotechnical Engineering-II'),
                ('transportation_engineering_i', 'Transportation Engineering-I'),
                ('hydrology_and_water_resources', 'Hydrology & Water Resources'),
                ('pe_advanced_surveying', 'Professional Elective-I: Advanced Surveying'),
                ('oe_ai_techniques', 'Open Elective-I: AI Techniques'),
                ('oe_basics_of_electrical_engg', 'Open Elective-I: Basics of Electrical Engg.'),
            ],
            '6': [
                ('design_of_rcc_structures_i', 'Design of RCC Structures-I'),
                ('design_of_steel_structures_i', 'Design of Steel Structures-I'),
                ('transportation_engineering_ii', 'Transportation Engineering-II'),
                ('pe_town_planning', 'Professional Elective-II: Town Planning'),
                ('oe_internet_of_things', 'Open Elective-II: Internet of Things (IoT)'),
                ('oe_robotics', 'Open Elective-II: Robotics'),
            ],
            '7': [
                ('design_of_rcc_structures_ii', 'Design of RCC Structures-II'),
                ('quantity_surveying_and_costing', 'Quantity Surveying & Costing'),
                ('pe_earthquake_engineering', 'Professional Elective-III: Earthquake Engineering'),
                ('pe_advanced_water_treatment', 'Professional Elective-IV: Advanced Water Treatment'),
                ('oe_cloud_computing', 'Open Elective-III: Cloud Computing'),
                ('oe_industrial_safety', 'Open Elective-III: Industrial Safety'),
                ('project_i', 'Project-I'),
            ],
            '8': [
                ('construction_management', 'Construction Management'),
                ('project_ii', 'Project-II / Internship'),
                ('pe_finite_element_method', 'Professional Elective-V: Finite Element Method (FEM)'),
                ('pe_advanced_structural_design', 'Professional Elective-VI: Advanced Structural Design'),
                ('oe_project_management_and_finance', 'Open Elective-IV: Project Management & Finance'),
            ],
        },
    }

    # Return common subjects for semesters 1 and 2
    if semester in ['1', '2']:
        return common_subjects.get(semester, [])

    # Return branch-specific subjects for semesters 3-8
    branch_data = branch_subjects.get(branch.lower(), {})
    return branch_data.get(semester, [])

def get_subjects_by_semester(semester):
    """
    Returns a list of subject choices for the given semester.
    This function is kept for backward compatibility.
    """
    # Default to CSE branch for backward compatibility
    return get_subjects_by_branch_and_semester('cse', semester)

class ExamFormForm(forms.ModelForm):
    BRANCH_CHOICES = [
        ('cse', 'Computer Science Engineering'),
        ('aids', 'Artificial Intelligence and Data Science'),
        ('mechanical', 'Mechanical Engineering'),
        ('electrical', 'Electrical Engineering'),
        ('electronics', 'Electronics Engineering'),
        ('it', 'Information Technology'),
        ('civil', 'Civil Engineering'),
    ]

    SEMESTER_CHOICES = [
        ('1', '1st Semester'),
        ('2', '2nd Semester'),
        ('3', '3rd Semester'),
        ('4', '4th Semester'),
        ('5', '5th Semester'),
        ('6', '6th Semester'),
        ('7', '7th Semester'),
        ('8', '8th Semester'),
    ]

    branch = forms.ChoiceField(choices=BRANCH_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    semester = forms.ChoiceField(choices=[('', '-- Select Semester --')] + SEMESTER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    subjects = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        help_text="Select the subjects you want to appear for the exam"
    )
    exam_type = forms.ChoiceField(
        choices=[('winter', 'Winter'), ('summer', 'Summer')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set subjects choices based on POST data or initial data
        if self.data:
            # If form has POST data, use that
            branch = self.data.get('branch', 'cse')
            semester = self.data.get('semester', '1')
        else:
            # Otherwise use initial data
            branch = self.initial.get('branch', 'cse')
            semester = self.initial.get('semester', '1')
        self.fields['subjects'].choices = get_subjects_by_branch_and_semester(branch, semester)

    class Meta:
        model = ExamForm
        fields = ['branch', 'semester', 'subjects', 'exam_type']
