from django.test import TestCase

from tenancy.models import AdministrativeUnit, ManagementGroup
from accounts.models import User


class UserModelTests(TestCase):
    databases = {'default'}

    def setUp(self):
        self.group = ManagementGroup.objects.create(name='Test Group')
        self.national = AdministrativeUnit.objects.create(
            name='Country', level=AdministrativeUnit.NATIONAL, code='NAT', management_group=self.group
        )
        self.region = AdministrativeUnit.objects.create(
            name='Region 1', level=AdministrativeUnit.REGION, code='REG1', parent=self.national, management_group=self.group
        )

    def test_has_unit_access_for_assigned_unit(self):
        user = User.objects.create_user(username='user1', password='secret', role=User.NON_TEACHING_STAFF)
        user.assigned_units.add(self.region)
        self.assertTrue(user.has_unit_access(self.region))

    def test_has_unit_access_for_parent_unit(self):
        user = User.objects.create_user(username='user2', password='secret', role=User.NON_TEACHING_STAFF)
        user.assigned_units.add(self.national)
        self.assertTrue(user.has_unit_access(self.region))

    def test_has_unit_access_for_unrelated_unit(self):
        other_group = ManagementGroup.objects.create(name='Other Group')
        other_national = AdministrativeUnit.objects.create(
            name='Other', level=AdministrativeUnit.NATIONAL, code='OTH', management_group=other_group
        )
        user = User.objects.create_user(username='user3', password='secret', role=User.NON_TEACHING_STAFF)
        user.assigned_units.add(other_national)
        self.assertFalse(user.has_unit_access(self.region))
