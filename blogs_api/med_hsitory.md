Certainly! Let's address the issues you've outlined for your **MedicationHistory** model and 
views in your Django app. I'll provide guidance on how to achieve the desired behavior.

1. **Isolating Patients for Pharmacist and Organizer**:
   To ensure that the **patients** field is isolated from the pharmacist and organizer, 
   you can override the form field for the **patients** ForeignKey. 
   Specifically, you'll customize the queryset to exclude previously selected patients
    for each user. Here's how you can modify your **MedicationHistoryForm**:

    ```python
    class MedicationHistoryForm(forms.ModelForm):
        class Meta:
            model = MedicationHistory
            fields = ['vital_signs', 'patients', ...]  # Add other fields as needed

        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user')  # Get the current user
            super().__init__(*args, **kwargs)
            # Customize the queryset for patients based on user type
            if user.is_organizer or user.is_pharmacist:
                # Exclude previously selected patients for the current user
                self.fields['patients'].queryset = PatientDetail.objects.exclude(
                    medicationhistory__user=user
                )
            else:
                # Pharmacist-specific queryset (if needed)
                # Customize this based on your requirements
                self.fields['patients'].queryset = ...

    # Usage in views:
    form = MedicationHistoryForm(user=self.request.user)
    ```

2. **Ordering Patients by Recent Date and Limiting Selection**:
   To order patients by the most recent date and limit the selection to the first 5 patients, you can modify your **MedicationHistoryForm** queryset. Here's how:

    ```python
    class MedicationHistoryForm(forms.ModelForm):
        class Meta:
            model = MedicationHistory
            fields = ['vital_signs', 'patients', ...]  # Add other fields as needed

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Order patients by date_created (most recent first)
            self.fields['patients'].queryset = PatientDetail.objects.order_by('-date_created')[:5]
    ```

3. **Applying Changes to MedicationHistoryUpdateView**:
   You can apply the same modifications to the **MedicationHistoryUpdateView** by using the same form class and overriding the queryset as shown in your **MedicationHistoryCreateView**.

Remember to adjust the code snippets according to your specific requirements and relationships between models. If you have any further questions or need additional assistance, feel free to ask! 😊

It seems you're working on a Django application for managing patient medication history, and you want to address a couple of issues related to the `MedicationHistory` model and views. Let's break down your requirements and tackle them step by step:

1. **Isolating Patients in the Select-Option Icon**:
    - You want the `patients` field (which is a ForeignKey) in the `MedicationHistoryCreateView` to be isolated from both pharmacists and organizers. Specifically, you don't want users to see their previous input in the select-option icon for patients. Specifically, I don't want pharmacist to see the organizer patients input in the formfield and vice-versa, so filter their input field respectively in isolation
    - To achieve this, you can override the `formfield_for_foreignkey` method in your `MedicationHistoryCreateView`. This method allows you to customize the queryset for the `patients` field.
    - Here's an example of how you can do this:

    ```python
    class MedicationHistoryCreateView(OrganizerPharmacistLoginRequiredMixin, CreateView):
        # ...

        def formfield_for_foreignkey(self, db_field, request, **kwargs):
            if db_field.name == 'patients':
                # Filter patients based on the user's role
                user = self.request.user
                if user.is_organizer or user.is_pharmacist:
                    kwargs['queryset'] = PatientDetail.objects.none()
                else:
                    kwargs['queryset'] = PatientDetail.objects.filter(
                        organization=user.pharmacist.organization
                    )
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
    ```

2. **Ordering Patients by Recent Date and Limiting Selection**:
    - You want the patients to be ordered by the most recent date and limit the selection to the first 5 patients.
    - To achieve this, you can modify the queryset for the `patients` field in the `MedicationHistoryForm`.
    - Here's an example:

    ```python
    class MedicationHistoryForm(forms.ModelForm):
        class Meta:
            model = MedicationHistory
            fields = ['vital_signs', 'patients', ...]  # Add other fields

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # Customize the queryset for the patients field
            self.fields['patients'].queryset = PatientDetail.objects.order_by('-date_created')[:5]
    ```

3. **Applying the Changes to the Update View**:
    - You can follow a similar approach in the `MedicationHistoryUpdateView` to achieve the same behavior for updating medication history.


Certainly! Let's address your requirements for isolating patient data and ordering it by the most recent date in your Django app. I'll provide guidance on how to achieve this.

1. **Isolating Patient Data**:
   To ensure that the `patients` field in the `MedicationHistoryCreateView` is isolated between the pharmacist and the organizer, you can override the form field queryset. Specifically, you want each user type to see only their relevant patients. We'll filter the patients based on the user's role.

   In your `MedicationHistoryForm`, override the `patients` field queryset as follows:

   ```python
   class MedicationHistoryForm(forms.ModelForm):
       class Meta:
           model = MedicationHistory
           fields = ['vital_signs', 'patients', ...]  # Other fields

       def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           user = self.request.user  # Assuming you have access to the request object
           if user.is_organizer:
               # Filter patients for organizers
               self.fields['patients'].queryset = PatientDetail.objects.filter(organization=user.userprofile)
           elif user.is_pharmacist:
               # Filter patients for pharmacists
               self.fields['patients'].queryset = PatientDetail.objects.filter(pharmacist__user=user)

   ```

   This way, the `patients` field will display only relevant patients based on the user's role.

2. **Ordering by Recent Date**:
   To order the data by the most recent date, you've already implemented it correctly in your views. The `get_queryset` method in both `MedicationHistoryCreateView` and `MedicationHistoryUpdateView` orders the queryset by `-date_created`, which sorts records in descending order (most recent first).

   You can keep your existing `get_queryset` methods as they are, and the data will be ordered correctly.

3. **Limiting Patients Selection**:
   To display only the first 5 patients in the selection field, you can modify the form field widget. You can use a `ModelChoiceField` with a custom widget that limits the number of displayed options. Here's an example:

   ```python
   from django.forms import ModelChoiceField, Select

   class LimitedSelect(Select):
       def __init__(self, limit_choices_to=5, *args, **kwargs):
           super().__init__(*args, **kwargs)
           self.limit_choices_to = limit_choices_to

       def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
           option = super().create_option(name, value, label, selected, index, subindex, attrs)
           if index >= self.limit_choices_to:
               option['attrs']['style'] = 'display:none;'
           return option

   class MedicationHistoryForm(forms.ModelForm):
       # ...

       patients = ModelChoiceField(
           queryset=PatientDetail.objects.none(),  # Empty queryset initially
           widget=LimitedSelect(limit_choices_to=5),
           # Other fields
       )

       def __init__(self, *args, **kwargs):
           # Same as before
           # ...

   ```

   In this example, the `LimitedSelect` widget hides options beyond the first 5. Adjust the `limit_choices_to` value as needed.

Remember to adjust the code snippets according to your specific project structure and any additional context you might have. If you encounter any issues or need further clarification, feel free to ask! 😊

Source: Conversation with Bing, 4/22/2024
(1) How to isolate detail data - Forms & APIs - Django Forum. https://forum.djangoproject.com/t/how-to-isolate-detail-data/30364.
(2) django - Health App : Data saved for a specific patient is being shown .... https://stackoverflow.com/questions/47276589/health-app-data-saved-for-a-specific-patient-is-being-shown-in-detail-view-for.
(3) Building a Python-based System for Managing Patient Records .... https://itcertifications.medium.com/building-a-python-based-system-for-managing-patient-records-appointments-and-medical-history-4c8e40f48e35.








Certainly! Let's address your requirements step by step for the `MedicationHistoryCreateView` and `MedicationHistoryUpdateView`.

1. **Isolating Patients for Pharmacist and Organizer**:
    - To ensure that the `patients` field is isolated for pharmacists and organizers, we can override the form field in the `MedicationHistoryForm`.
    - We'll filter the patients based on the user's role (pharmacist or organizer) to display only relevant options.
    - Additionally, we'll order the patients by the most recent date.

2. **Limiting Patients Selection to First 5**:
    - We'll modify the form field to display only the first 5 patients.
    - This will prevent the user from seeing all patients at once.

Let's start by updating the `MedicationHistoryForm`. Below is the modified form:

```python
# forms.py
from django import forms
from .models import MedicationHistory

class MedicationHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicationHistory
        fields = ['vital_signs', 'patients']  # Add other fields as needed

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Get the user from the view
        super().__init__(*args, **kwargs)

        # Filter patients based on user role (pharmacist or organizer)
        if user.is_pharmacist:
            self.fields['patients'].queryset = user.pharmacist.organization.patientdetail_set.all()
        elif user.is_organizer:
            self.fields['patients'].queryset = user.userprofile.patientdetail_set.all()

        # Order patients by most recent date
        self.fields['patients'].queryset = self.fields['patients'].queryset.order_by('-date_created')

        # Limit patients selection to first 5
        self.fields['patients'].widget.attrs['size'] = 5
```

Next, update your views to pass the user to the form:

```python
# views.py
from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from .models import MedicationHistory
from .forms import MedicationHistoryForm

class MedicationHistoryCreateView(OrganizerPharmacistLoginRequiredMixin, CreateView):
    # ...

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user to the form
        return kwargs

    # ...

class MedicationHistoryUpdateView(OrganizerPharmacistLoginRequiredMixin, UpdateView):
    # ...

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the user to the form
        return kwargs

    # ...
```

With these changes, the `patients` field in the form will be isolated based on the user's role, ordered by date, and limited to the first 5 patients. Feel free to adjust the code according to your specific requirements. If you have any further questions or need additional assistance, feel free to ask! 😊

Source: Conversation with Bing, 4/22/2024
(1) How to isolate detail data - Forms & APIs - Django Forum. https://forum.djangoproject.com/t/how-to-isolate-detail-data/30364.
(2) Django : One model has two foreign keys is this the right approach in .... https://stackoverflow.com/questions/41715273/django-one-model-has-two-foreign-keys-is-this-the-right-approach-in-this-case.
(3) Building a Python-based System for Managing Patient Records .... https://itcertifications.medium.com/building-a-python-based-system-for-managing-patient-records-appointments-and-medical-history-4c8e40f48e35.





```py

        # Filter patients based on user role (pharmacist or organizer)
        if user.is_organizer:
            self.fields['patients'].queryset = user.userprofile\
                .patientdetail_set.all() 
            
        elif user.is_pharmacist:
            #self.fields['patients'].queryset = user.pharmacist.organization.patientdetail_set.all()
            self.fields['patients'].queryset = user.userprofile.patientdetail_set.all() 
            

        # Order patients by most recent date  pharmacist__user=user
        self.fields['patients'].queryset = self.fields['patients'].queryset.order_by(
            '-date_created')

        # Limit patients selection to first 5
        self.fields['patients'].widget.attrs['size'] = 5

class MedicationHistoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Get the user from the view
        super().__init__(*args, **kwargs)
        if user.is_organizer:
            # Filter patients for organizers
            self.fields['patients'].queryset = PatientDetail.objects.filter(organization=user.userprofile)
        elif user.is_pharmacist:
            # Filter patients for pharmacists
            self.fields['patients'].queryset = PatientDetail.objects.filter(pharmacist__user=user)

    class Meta:
        model = MedicationHistory
        fields = ['patients', 'vital_signs']  # Adjust fields as needed


```

















### IBW

The **Devine Formula**, established in 1974, is used to promptly calculate the **ideal body weight** for dosages of medications. It relies solely on height and is commonly applied in both scholarly and medical contexts. Here's how it works:

1. **Men**:
   - Ideal Body Weight (in kg) = 50 kg + 2.3 kg per inch over 5 feet.
   - For example, a 6-foot tall man should have an ideal body weight of approximately **77.6 kilograms**¹. 60 * 30.88

2. **Women**:
   - Ideal Body Weight (in kg) = 45.5 kg + 2.3 kg per inch over 5 feet.
   - For instance, a 6-foot tall woman should aim for an ideal weight of around **73.1 kilograms**¹.

Remember that **1 kilogram (kg)** is equivalent to **2.2 pounds (lb)**, and **1 meter** equals approximately **3.28084 feet**. If you're using metric units, this formula can be quite handy! 🌟


def ibw(height, gender, unit_choice) 
        """Devine formular""":
         if gender == 'male'.lower():
          # 100cm == 1m  
            50 kg + 2.3 kg * (height in inches - 60 inches) men_ibw = round(50 + 2.3 * (height + 10.17), 2) 
            mass_in_lb = round(men_ibw * 2.2, 1) ibw.append(f"Ideal Body Weight: {men_ibw:.2f} kg ({mass_in_lb}pounds)") elif gender == 'female'.lower(): female_ibw = round(45.5 + 2.3 * (height + 10.17), 2) mass_in_lb = round(female_ibw * 2.2, 1) ibw.append(f"Ideal Body Weight: {female_ibw:.2f} kg ({mass_in_lb}pounds)") 
            else: raise ValueError("Invalid gender. Please specify 'male' or 'female'.") -> the answer is not correct, it returned a list of  [Ideal Body Weight: 72.40 kg (159.3pounds)] instead of [Ideal Body Weight: 45.50 kg (100.1pounds)] for female -> please where am i getting the error, and I don't want to use inch or cm to solve it 

Source: Conversation with Bing, 4/22/2024
(1) Ideal Body Weight - B. J. Devine Formula (1974) - BMI Calculator. https://www.bmi-calculator.net/ideal-weight-calculator/devine-formula/.
(2) Devine Formula for estimating ideal body weight - Topend Sports. https://www.topendsports.com/testing/tests/devine-formula.htm.











from typing import Any, Sequence
from django import forms
from pharmcare.models import *
from tinymce.widgets import TinyMCE
from django.contrib.auth import get_user_model
from django.forms import ModelChoiceField, Select
User = get_user_model()


class LimitedSelectOption(Select):
    """ a customized class to override the limit choice attrs thus limiting the
        widget to 5 patient's options."""

    def __init__(self, limit_choices_to=5, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.limit_choices_to = limit_choices_to

    def create_option(
            self, name,
            value, label,
            selected, index,
            subindex=None,
            attrs=None
    ):

        option = super().create_option(
            name, value, label, selected,
            index, subindex, attrs
        )

        if index >= self.limit_choices_to:
            option['attrs']['style'] = 'display:none;'

        return option


class PatientDetailModelForm(forms.ModelForm):
    """ Patient detail form is a form class that helps us to input, check the validility
        of the form prior to it's submission of our patient's details given. """
    class Meta:

        model = PatientDetail
        fields = [
            'first_name',
            'last_name',
            'email',
            'marital_status',
            'patient_class',
            'gender',
            'age',
            "ethnicity_or_race",
            "weight",
            'unit_choice',
            'height',
            'patient_history',
            'past_medical_history',
            'social_history',
            # 'slug',
            'phone_number',
            'consultation'

        ]

        labels = {
            'first_name': 'Enter your patient\'s first name',
            'last_name': 'Enter your patient\'s last name',
            'email': ' Enter your patient\'s email if any',
            'age': ' Enter your patient\'s age',
            'unit_choice': "Select the unit you would want to work with for the\
                             patient's height conversion.",
            'height': "Enter your patient's height either in \
                                (centimeters,inches, feet, meters)",
            'weight': "Enter your patient's weight in (kg)",
            'patient_history':  "Enter your patient's medical history",
            'past_medical_history': "Enter your patient's past medical history",
            'social_history': 'Enter the social history of your patient if any',
            'slug': "Enter your patient's first name as the slug",
            'phone_number': 'Enter your patient\'s phone number',
            'consultation': 'Enter the consultation fee if any'
        }


class MedicationHistoryForm(forms.ModelForm):
    """ patients form for medication history """

    class Meta:
        model = MedicationHistory
        ordering = "-date_created"

        fields = [
            'medication_list',
            'patients',
            'notes',
            'indication_and_evidence',
            'goal_of_therapy'
        ]
        labels = {
            'medication_list': " Enter your patient's medication list",
            'indication_and_evidence': "Enter your patient's indication",
            'goal_of_therapy': "State the therapeutic goals you want \
            achieve with your patient",
            'vital_signs': "Enter your patient's vital signs you have assessed.",
            'notes': "Enter the necessary notes you gathered if any for the patient",
            'review_of_system': "Enter the patient review of system",
            "patients": "Select the specific patient detail"

        }

    def __init__(self, *args, **kwargs):
        """ override and manipulate the form field rendering of the patient
        detail field, as well as its date created ordering. """
        # get the current user
        user = kwargs.pop('user')

        super(MedicationHistoryForm, self).__init__(*args, **kwargs)

        # Filter patients based on user role (pharmacist or organizer)
        if user.is_organizer:
            self.fields['patients'].queryset = user.userprofile\
                .patientdetail_set.all()

        elif user.is_pharmacist:
            # self.fields['patients'].queryset = user.pharmacist.organization.patientdetail_set.all()
            self.fields['patients'].queryset = user.userprofile.patientdetail_set.all()

        # Order patients by most recent date  pharmacist__user=user
        self.fields['patients'].queryset = self.fields['patients'].queryset.order_by(
            '-date_created')

        # Limit patients selection to first 5
        self.fields['patients'].widget.attrs['size'] = 5

        # placeholder to the fields to guide pharmacist input needed
        self.fields['goal_of_therapy'].widget.attrs['placeholder'] = \
            f"""
            Establish the goal of the therapy you want for this patient throughout the course of treatment.
        """

        self.fields['notes'].widget.attrs['placeholder'] = \
            f"""
            State the different vital signs you gathered throughout the course of your interaction
            with the patient on his first visit for start. For example, vital signs (pulse, blood pressure,
            respiratory rate and body temperature).
        """


class ProgressNoteForm(forms.ModelForm):
    """ patients form for medication history """

    class Meta:
        model = ProgressNote

        fields = [
            'patient',
            'notes',
            'goal_of_therapy',
        ]
        labels = {
            'notes': "Enter your patient's medical notes ",
            'goal_of_therapy': "State the therapeutic goals you want to achieve further with your patient"
        }
        error_messages = {
            'error': "Kindly input the patient note, Pharm."
        }

    def __init__(self, *args, **kwargs):
        """ override and manipulate the form field rendering of the patient 
        detail field, as well as its date created ordering. """

        # get the user from the view
        user = kwargs.pop('user')

        super(ProgressNoteForm, self).__init__(*args, **kwargs)

        # Filter patients based on user role (pharmacist or organizer)
        if user.is_organizer:
            self.fields['patient'].queryset = user.userprofile\
                .patientdetail_set.all()
        elif user.is_pharmacist:
            self.fields['patient'].queryset = user.userprofile\
                .patientdetail_set.all()

        # Order patients by most recent date
        self.fields['patient'].queryset = self.fields['patient']\
            .queryset.order_by('-date_created')

        # Limit patients selection to first 5
        self.fields['patient'].widget.attrs['size'] = 5


class MedicationChangesForm(forms.ModelForm):
    """ Medication changes form is a form class that handles all the
      form field and submissions made by the pharmacist wrt patient 
      posology/changes due to the mediactions that s/he is placed on."""

    class Meta:
        model = MedicationChanges

        fields = [
            'patient',
            'medication_list',
            'dose',
            'frequency',
            'route',
            'indication',
            "stop_date",

        ]

        labels = {
            'medication_list': "Enter the list of medications you\
                  want to dispense to your patient",
            'dose': "Enter the dose of the medication",
            'frequency': " Enter the frequency of the dose",
            'route': " Enter the route of administration of the drug ",
            'indication': " Enter the drug(s) indication",
            'start_or_continued_date': " (Optional) If the time is left blank, \
                it will automatically generated",
            'stop_date': " Enter the time the patient is meant to stop the drug",

        }
        error_messages = {
            'error': "Kindly input the patient fields, Pharm."
        }

    def __init__(self, *args, **kwargs):
        """ override and manipulate the form field rendering of the patient
           detail field, as well as its date created ordering. 
        """
        # get the current user
        user = kwargs.pop('user')

        super(MedicationChangesForm, self).__init__(*args, **kwargs)

        # Filter patients based on user role (pharmacist or organizer)
        if user.is_organizer:
            self.fields['patient'].queryset = user.userprofile\
                .patientdetail_set.all()

        elif user.is_pharmacist:
            self.fields['patient'].queryset = user.userprofile\
                .patientdetail_set.all()

        # Order patients by most recent date  pharmacist__user=user
        self.fields['patient'].queryset = self.fields['patient']\
            .queryset.order_by(
            '-date_created'
        )

        # Limit patients selection to first 5
       # self.fields['patient'].widget.attrs['size'] = 5

    patients = ModelChoiceField(
        queryset=PatientDetail.objects.none(),
        widget=LimitedSelectOption(limit_choices_to=5)
    )


class AnalysisOfClinicalProblemForm(forms.ModelForm):
    """ Analysis of Clinical Problem form is a form class that helps us 
        to input, check the validility of the form prior to it's submission 
        of our patient's clinical problems retrieved from the model. """
    class Meta:
        model = AnalysisOfClinicalProblem

        fields = [
            'patient',
            "clinical_problem",
            "assessment",
            "priority",
            "action_taken_or_future_plan",
        ]

        labels = {
            "clinical_problem": " Enter the patient's clinical problem(s)",
            "assessment": 'Enter your clinical assessment about patient',
            "priority": "Choose the priority",
            "action_taken_or_future_plan": "Enter action to be taken\
             concerning the patient",

        }
        error_messages = {
            'error': f"Kindly input the patient fields, Pharm."
        }

    def __init__(self, *args, **kwargs):
        """ override and manipulate the form field rendering of the patient 
        detail field, as well as its date created ordering. """

        # get the user from the view
        user = kwargs.pop('user')

        super(AnalysisOfClinicalProblemForm, self).__init__(*args, **kwargs)

        # Filter patients based on user role (pharmacist or organizer)
        if user.is_organizer:
            self.fields['patient'].queryset = user.userprofile\
                .patientdetail_set.all()
        elif user.is_pharmacist:
            self.fields['patient'].queryset = user.userprofile\
                .patientdetail_set.all()

        # Order patients by most recent date
        self.fields['patient'].queryset = self.fields['patient']\
            .queryset.order_by('-date_created')

        # Limit patients selection to first 5
        self.fields['patient'].widget.attrs['size'] = 5


class MonitoringPlanForm(forms.ModelForm):
    """ Monitoring plan form is a form class that helps us to input,
        check the validility of the form prior to it's submission of our 
        patient's monitoring plan retrieved from the model. """

    class Meta:
        model = MonitoringPlan
        fields = [
            'patient',
            'parameter_used',
            'justification',
            'frequency',
            'results_and_action_plan'
        ]

    def __init__(self, *args, **kwargs):
        """ override and manipulate the form field rendering of the patient 
        detail field, as well as its date created ordering. """

        # get the user from the view
        user = kwargs.pop('user')

        super(MonitoringPlanForm, self).__init__(*args, **kwargs)

        # Filter patients based on user role (pharmacist or organizer)
        if user.is_organizer:
            self.fields['patient'].queryset = user.userprofile\
                .patientdetail_set.all()
        elif user.is_pharmacist:
            self.fields['patient'].queryset = user.userprofile\
                .patientdetail_set.all()

        # Order patients by most recent date
        self.fields['patient'].queryset = self.fields['patient']\
            .queryset.order_by('-date_created')

        # Limit patients selection to first 5
        self.fields['patient'].widget.attrs['size'] = 5


class FollowUpPlanForm(forms.ModelForm):
    """ Follow up form is a form class that helps us to input, 
        check the validility of the form prior to it's submission of our 
        patient's follow up retrieved from the model. """

    class Meta:
        model = FollowUpPlan

        fields = [
            'patient',
            'follow_up_requirement',
            'action_taken_and_future_plan',
            'state_of_improvement_by_score',
            'has_improved_than_before',
            'adhered_to_medications_given',
            'patient_education',
            'referral'
        ]

        labels = {
            'user': "Enter the user ( Optional )",
            'follow_up_requirement': " Enter the follow up requirement for the patient",
            "action_taken_or_future_plan": "Enter action to be taken concerning the patient",
            'state_of_improvement_by_score': "Score the patient's medical \
                improvement by percent ",
            'referral': " Enter the referral's name if any. "
        }
        error_messages = {
            'error': f"Kindly input the patient fields, Pharm."
        }

    def __init__(self, *args, **kwargs):
        """ override and manipulate the form field rendering of the patient 
        detail field, as well as its date created ordering. """

        # get the user from the view
        user = kwargs.pop('user')
        super(FollowUpPlanForm, self).__init__(*args, **kwargs)

        # Filter patients based on user role (pharmacist or organizer)
        if user.is_organizer:
            self.fields['patient'].queryset = user.userprofile\
                .patientdetail_set.all()
        elif user.is_pharmacist:
            self.fields['patient'].queryset = user.userprofile\
                .patientdetail_set.all()

        # Order patients by most recent date
        self.fields['patient'].queryset = self.fields['patient']\
            .queryset.order_by('-date_created')

        # Limit patients selection to first 5
        self.fields['patient'].widget.attrs['size'] = 5

        # placeholder

        self.fields['state_of_improvement_by_score'].widget.attrs['placeholder'] = \
            'for example -> 70'


class PatientModelForm(forms.ModelForm):
    """ class that handles the patient form input and submission in our 
        db made by our pharmacist.  """
    class Meta:
        model = Patient
        fields = [
            'medical_charge',
            'notes',
            'patient',
            'medical_history',
            'discount',
        ]

        labels = {
            'medical_charge': "Enter medical charge",
            'notes': "Enter patient's notes to follow up on your next possible action ",
            'patient': "Select patient for this field which you had previously created",
            'medical_history': 'Select patient medical history for this field which you\
                                had previously created',
            'total_payment': 'Optional (the summation is done instantenously)',
        }

    def __init__(self, *args, **kwargs):
        """ customize and manipulate the form field rendering of the patient and
         medical history field, as well as their date created ordering. """
        # get the user from the view
        user = kwargs.pop('user')

        super(PatientModelForm, self).__init__(*args, **kwargs)

        # Filter patients, and medical_history based on user role (pharmacist or organizer)
        if user.is_organizer:
            self.fields['patient'].queryset = user.userprofile\
                .patientdetail_set.all()
            self.fields['medical_history'].queryset = user.userprofile.\
                medicationhistory_set.all()

        elif user.is_pharmacist:
            self.fields['patient'].queryset = user.userprofile.\
                patientdetail_set.all()
            self.fields['medical_history'].queryset = user.userprofile.\
                medicationhistory_set.all()

        # Order patients by most recent date
        self.fields["patient"].queryset = self.fields['patient'].\
            queryset.order_by('-date_created')
        self.fields["medical_history"].queryset = self.fields['medical_history'].\
            queryset.order_by('-date_created')

        # Limit patients, and medicationhistory field to first 5
        self.fields['patient'].widget.attrs['size'] = 5
        self.fields['medical_history'].widget.attrs['size'] = 5


class PharmaceuticalCarePlanModelForm(forms.ModelForm):
    """ Pharmceutical care form that handles user input and validations """
    class Meta:
        model = PharmaceuticalCarePlan
        fields = [
            'patients',
            'has_improved',
            'progress_note',
            'medication_changes',
            'analysis_of_clinical_problem',
            'monitoring_plan',
            'follow_up_plan',

        ]

    def __init__(self, *args, **kwargs):
        """ override and manipulate the form field rendering of the patient 
        detail field, as well as its date created ordering. """

        # get the user from the view
        user = kwargs.pop('user')

        super(PharmaceuticalCarePlanModelForm, self).__init__(*args, **kwargs)

        # Filter patients based on user role (pharmacist or organizer)
        if user.is_organizer:
            self.fields['progress_note'].queryset = user.userprofile\
                .progressnote_set.all()
            self.fields['medication_changes'].queryset = user.userprofile\
                .medicationchanges_set.all()
            self.fields['analysis_of_clinical_problem'].queryset = user.userprofile\
                .analysisofclinicalproblem_set.all()
            self.fields['monitoring_plan'].queryset = user.userprofile\
                .monitoringplan_set.all()
            self.fields['follow_up_plan'].queryset = user.userprofile\
                .followupplan_set.all()

        elif user.is_pharmacist:
            self.fields['progress_note'].queryset = user.userprofile\
                .progressnote_set.all()
            self.fields['medication_changes'].queryset = user.userprofile\
                .medicationchanges_set.all()
            self.fields['analysis_of_clinical_problem'].queryset = user.userprofile\
                .analysisofclinicalproblem_set.all()
            self.fields['monitoring_plan'].queryset = user.userprofile\
                .monitoringplan_set.all()
            self.fields['follow_up_plan'].queryset = user.userprofile\
                .followupplan_set.all()

        # Order patients by most recent date
        self.fields['progress_note'].queryset = self.fields['progress_note'].\
            queryset.order_by('-date_created')
        self.fields['medication_changes'].queryset = self.fields['medication_changes'].\
            queryset.order_by('-date_created')
        self.fields['analysis_of_clinical_problem'].queryset = \
            self.fields['analysis_of_clinical_problem'].queryset.order_by(
                '-date_created')
        self.fields['monitoring_plan'].queryset = self.fields['monitoring_plan']\
            .queryset.order_by('-date_created')
        self.fields['follow_up_plan'].queryset = self.fields['follow_up_plan']\
            .queryset.order_by('-date_created')

        # Limit patients selection to first 5
        self.fields['progress_note'].widget.attrs['size'] = 5
        self.fields['medication_changes'].widget.attrs['size'] = 5
        self.fields['analysis_of_clinical_problem'].widget.attrs['size'] = 5
        self.fields['monitoring_plan'].widget.attrs['size'] = 5
        self.fields['follow_up_plan'].widget.attrs['size'] = 5


# Pharmacist Forms


class PharmacistModelForm(forms.ModelForm):
    """ form class that handles organization pharmacist form for the patient
    if the user is granted access."""

    class Meta:
        model = User

        fields = [

            'username',
            'first_name',
            "last_name",
            'phone_number',
            'email',

        ]

        labels = {
            "username": "Enter your username",
            "first_name": "Enter your first name",
            "last_name": "Enter your last name",
            "phone_number": "Enter your phone number",
            'email': 'Enter your email',
        }


class PharmacistAssignedForm(forms.Form):
    pharmacist = forms.ModelChoiceField(queryset=Pharmacist.objects.none())

    def __init__(self, *args, **kwargs):

        request = kwargs.pop('request')
        pharmacist = Pharmacist.objects.filter(
            organization=request.user.userprofile)

        super(PharmacistAssignedForm, self).__init__(*args, **kwargs)

        self.fields['pharmacist'].queryset = pharmacist














Certainly! Let's dive into the world of asynchronous programming in Python and explore why functions need to be marked as `async def`.

1. **Concurrency and Blocking**:
   - In traditional synchronous programming, tasks are executed one after the other. The program waits for each task to complete before moving on to the next.
   - However, this approach can be inefficient when dealing with I/O-bound operations (such as reading/writing files, making network requests, or querying databases). Waiting for one task to complete before starting the next can lead to unnecessary delays.
   - Asynchronous programming allows us to run multiple tasks concurrently, without blocking the execution flow. This is especially useful for I/O-bound operations.

2. **Coroutines and `async def`**:
   - In Python, asynchronous functions are called **coroutines**. They allow us to write non-blocking code.
   - To define a coroutine, we use the `async def` syntax. For example:
     ```python
     async def fetch_data(url):
         # Perform some asynchronous operation (e.g., fetching data from a URL)
         ...
     ```
   - The `async` keyword indicates that this function is a coroutine and can yield control back to the event loop during its execution.

3. **`await` and Yielding Control**:
   - Inside a coroutine, we can use the `await` keyword to pause execution until a specific asynchronous operation completes.
   - When we `await` something (like an I/O operation), the event loop can switch to executing other coroutines while waiting for the result.
   - However, for a function to use `await`, it must be marked as `async`. Otherwise, it cannot yield control back to the event loop.

4. **Event Loop and Execution**:
   - The event loop manages the execution of coroutines. It schedules and runs them concurrently.
   - When you call an asynchronous function (marked with `async def`), it returns a coroutine object. You then execute it using the event loop.
   - The event loop ensures that coroutines yield control when they encounter an `await` expression, allowing other tasks to run.

5. **Example**:
   ```python
   import asyncio

   async def main():
       # Define two asynchronous tasks
       await fetch_data("https://example.com")
       await fetch_data("https://another-url.com")

   asyncio.run(main())  # Execute the event loop
   ```
   - In this example, `fetch_data` is an asynchronous function. The event loop runs both tasks concurrently.

In summary, marking functions as `async def` allows them to yield control back to the event loop, enabling efficient concurrency and non-blocking I/O operations. So, when you see `async def func()`, it's Python's way of saying, "This function can be paused and resumed during execution." 😊

For more details, you can refer to the [official Python documentation on asyncio](https://docs.python.org/3/library/asyncio.html).¹³

Remember, asynchronous programming can be powerful, but it requires understanding the event loop and the principles behind it. Happy coding! 🚀

