from django.core.exceptions import ValidationError
from django.test import TestCase
from reports.models import Report, Profile

class ProfileAndReportModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        profile = Profile()
        profile.save()

        first_report = Report()
        first_report.text = 'The first report ever'
        first_report.profile = profile
        first_report.save()

        second_report = Report()
        second_report.text = 'Report number two'
        second_report.profile = profile
        second_report.save()

        saved_profile = Profile.objects.first()
        self.assertEqual(saved_profile, profile)

        saved_reports = Report.objects.all()
        self.assertEqual(saved_reports.count(), 2)

        first_saved_report = saved_reports[0]
        second_saved_report = saved_reports[1]
        self.assertEqual(first_saved_report.text, 'The first report ever')
        self.assertEqual(first_saved_report.profile, profile)
        self.assertEqual(second_saved_report.text, 'Report number two')
        self.assertEqual(second_saved_report.profile, profile)

    def test_cannot_save_empty_reports(self):
        profile = Profile.objects.create()
        report = Report(profile = profile, text='')
        with self.assertRaises(ValidationError):
            report.save()
            report.full_clean()

    def test_get_absolute_url(self):
        profile = Profile.objects.create()
        self.assertEqual(profile.get_absolute_url(), '/profiles/%d/' % (profile.id,))