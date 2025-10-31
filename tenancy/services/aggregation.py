from collections import defaultdict
from typing import Dict, Iterable, Optional

from django_tenants.utils import get_tenant_model, tenant_context

from tenancy.models import AdministrativeUnit


def iter_tenants_for_unit(unit: Optional[AdministrativeUnit] = None) -> Iterable:
    Tenant = get_tenant_model()
    queryset = Tenant.objects.select_related('administrative_unit')
    if unit is not None:
        descendant_ids = {unit.id}
        nodes = [unit]
        while nodes:
            node = nodes.pop()
            for child in node.children.all():
                descendant_ids.add(child.id)
                nodes.append(child)
        queryset = queryset.filter(administrative_unit_id__in=descendant_ids)
    return queryset


def student_counts(unit: Optional[AdministrativeUnit] = None) -> Dict[str, int]:
    totals = defaultdict(int)
    for tenant in iter_tenants_for_unit(unit):
        with tenant_context(tenant):
            try:
                from students.models import StudentProfile
            except Exception:
                continue
            totals['schools'] += 1
            totals['students'] += StudentProfile.objects.count()
            totals['active_enrollments'] += StudentProfile.objects.filter(status=StudentProfile.ACTIVE).count()
    return totals


def staff_counts(unit: Optional[AdministrativeUnit] = None) -> Dict[str, int]:
    totals = defaultdict(int)
    for tenant in iter_tenants_for_unit(unit):
        with tenant_context(tenant):
            try:
                from hr.models import StaffProfile
            except Exception:
                continue
            totals['schools'] += 1
            totals['teaching_staff'] += StaffProfile.objects.filter(role=StaffProfile.TEACHING).count()
            totals['non_teaching_staff'] += StaffProfile.objects.filter(role=StaffProfile.NON_TEACHING).count()
    return totals
