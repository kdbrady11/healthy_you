from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Medication, MedicationDoseTime, MedicationLog
from .forms import MedicationForm, MedicationDoseTimeForm
import datetime


class MedicationModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')

        # Create a test medication
        self.medication = Medication.objects.create(
            user=self.user,
            name='Test Medication',
            description='Some description',
            frequency='daily',
            start_date=datetime.date.today(),
        )

    def test_medication_creation(self):
        self.assertEqual(Medication.objects.count(), 1)
        self.assertEqual(self.medication.name, 'Test Medication')

    def test_medication_str(self):
        self.assertEqual(str(self.medication), 'Test Medication (daily)')


class MedicationDoseTimeModelTest(TestCase):
    def setUp(self):
        # Create a test user and medication
        self.user = User.objects.create_user(username='testuser', password='password')
        self.medication = Medication.objects.create(
            user=self.user,
            name='Test Medication',
            frequency='daily',
            start_date=datetime.date.today(),
        )
        # Create a dose time
        self.dose_time = MedicationDoseTime.objects.create(
            medication=self.medication,
            scheduled_time='08:00',
            recurring_days='Mon,Wed,Fri'
        )

    def test_dose_time_creation(self):
        self.assertEqual(MedicationDoseTime.objects.count(), 1)
        self.assertEqual(self.dose_time.scheduled_time.strftime('%H:%M'), '08:00')

    def test_dose_time_str(self):
        self.assertEqual(str(self.dose_time), 'Test Medication at 08:00:00')


class MedicationLogModelTest(TestCase):
    def setUp(self):
        # Create a test user, medication, and dose time
        self.user = User.objects.create_user(username='testuser', password='password')
        self.medication = Medication.objects.create(
            user=self.user,
            name='Test Medication',
            frequency='daily',
            start_date=datetime.date.today(),
        )
        self.dose_time = MedicationDoseTime.objects.create(
            medication=self.medication,
            scheduled_time='08:00',
            recurring_days='Mon,Wed,Fri'
        )
        # Create a medication log
        self.log = MedicationLog.objects.create(
            medication=self.medication,
            date=datetime.date.today(),
            dose_time=self.dose_time,
            status='taken'
        )

    def test_log_creation(self):
        self.assertEqual(MedicationLog.objects.count(), 1)
        self.assertEqual(self.log.status, 'taken')

    def test_log_str(self):
        self.assertEqual(
            str(self.log),
            f'Test Medication on {datetime.date.today()} at 08:00:00: taken'
        )


class MedicationViewsTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')

        # Log the user in
        self.client.login(username='testuser', password='password')

        # Create medication and dose time
        self.medication = Medication.objects.create(
            user=self.user,
            name='Test Medication',
            frequency='daily',
            start_date=datetime.date.today()
        )
        self.dose_time = MedicationDoseTime.objects.create(
            medication=self.medication,
            scheduled_time='08:00',
            recurring_days='Mon,Wed,Fri'
        )

    def test_medications_dashboard_view(self):
        response = self.client.get(reverse('medications_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'medications/medications_dashboard.html')
        self.assertContains(response, 'Test Medication')

    def test_medication_create_view(self):
        response = self.client.post(reverse('medication_create'), {
            'name': 'New Medication',
            'description': 'Description of medication',
            'frequency': 'weekly',
            'start_date': datetime.date.today()
        })
        self.assertEqual(response.status_code, 302)  # Redirect after form submission
        self.assertEqual(Medication.objects.count(), 2)  # Medication created successfully

    def test_medication_edit_view(self):
        response = self.client.get(reverse('medication_edit', args=[self.medication.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'medications/medication_form.html')

    def test_add_dose_time_view(self):
        response = self.client.post(reverse('add_dose_time', args=[self.medication.id]), {
            'scheduled_time': '10:00',
            'recurring_days': 'Tue,Thu'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after form submission
        self.assertEqual(self.medication.dose_times.count(), 2)

    def test_update_medication_log_view(self):
        log = MedicationLog.objects.create(
            medication=self.medication,
            date=datetime.date.today(),
            dose_time=self.dose_time,
            status='not_recorded'
        )
        response = self.client.post(reverse('update_medication_log', args=[log.id]), {
            'status': 'taken'
        })
        log.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(log.status, 'taken')


class MedicationFormsTest(TestCase):
    def test_medication_form_valid(self):
        form = MedicationForm(data={
            'name': 'Medication Name',
            'description': 'Description',
            'frequency': 'daily',
            'start_date': datetime.date.today(),
            'dosing_schedule': 'Take with food',
        })
        self.assertTrue(form.is_valid())

    def test_medication_dose_time_form_valid(self):
        form = MedicationDoseTimeForm(data={
            'scheduled_time': '09:00',
            'recurring_days': 'Mon,Wed,Fri',
        })
        self.assertTrue(form.is_valid())

    def test_medication_form_invalid(self):
        form = MedicationForm(data={
            'name': '',  # Missing required name
            'start_date': ''  # Missing required start_date
        })
        self.assertFalse(form.is_valid())
