from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from accounts.models import User
from accounts.permissions import IsNonTeachingStaff
from fees.models import (
    BankAccount,
    DiscountPolicy,
    FeeComponent,
    FeeSchedule,
    FeeStructure,
    Invoice,
    Payment,
    Scholarship,
)
from fees.serializers import (
    BankAccountSerializer,
    DiscountPolicySerializer,
    FeeComponentSerializer,
    FeeScheduleSerializer,
    FeeStructureSerializer,
    InvoiceSerializer,
    PaymentSerializer,
    ScholarshipSerializer,
)


class FeeStructureViewSet(viewsets.ModelViewSet):
    queryset = FeeStructure.objects.prefetch_related('components')
    serializer_class = FeeStructureSerializer

    def get_permissions(self):
        if self.request.method in {'GET', 'HEAD', 'OPTIONS'}:
            return [IsAuthenticated()]
        return [IsNonTeachingStaff()]


class FeeComponentViewSet(viewsets.ModelViewSet):
    queryset = FeeComponent.objects.select_related('structure')
    serializer_class = FeeComponentSerializer

    def get_permissions(self):
        if self.request.method in {'GET', 'HEAD', 'OPTIONS'}:
            return [IsAuthenticated()]
        return [IsNonTeachingStaff()]


class FeeScheduleViewSet(viewsets.ModelViewSet):
    queryset = FeeSchedule.objects.select_related('structure', 'component', 'level')
    serializer_class = FeeScheduleSerializer

    def get_permissions(self):
        if self.request.method in {'GET', 'HEAD', 'OPTIONS'}:
            return [IsAuthenticated()]
        return [IsNonTeachingStaff()]


class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.select_related('administrative_unit', 'management_group')
    serializer_class = BankAccountSerializer

    def get_permissions(self):
        if self.request.method in {'GET', 'HEAD', 'OPTIONS'}:
            return [IsAuthenticated()]
        return [IsNonTeachingStaff()]


class DiscountPolicyViewSet(viewsets.ModelViewSet):
    queryset = DiscountPolicy.objects.all()
    serializer_class = DiscountPolicySerializer
    permission_classes = (IsAuthenticated, IsNonTeachingStaff)


class ScholarshipViewSet(viewsets.ModelViewSet):
    queryset = Scholarship.objects.select_related('student', 'discount_policy')
    serializer_class = ScholarshipSerializer

    def get_permissions(self):
        if self.request.method in {'GET', 'HEAD', 'OPTIONS'}:
            return [IsAuthenticated()]
        return [IsNonTeachingStaff()]


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.select_related('student', 'structure').prefetch_related('line_items')
    serializer_class = InvoiceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_superuser or user.role in {User.ADMINISTRATOR, User.NON_TEACHING_STAFF}:
            return qs
        if user.role == User.PARENT:
            return qs.filter(student__guardians=user)
        if user.role == User.STUDENT:
            return qs.filter(student__user=user)
        return qs.none()

    def perform_create(self, serializer):
        serializer.save()


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('invoice', 'received_by', 'bank_account').prefetch_related('allocations')
    serializer_class = PaymentSerializer

    def get_permissions(self):
        if self.request.method in {'GET', 'HEAD', 'OPTIONS'}:
            return [IsAuthenticated()]
        if self.request.method == 'POST':
            return [IsNonTeachingStaff()]
        return [IsNonTeachingStaff()]

    def perform_create(self, serializer):
        serializer.save(received_by=self.request.user)
