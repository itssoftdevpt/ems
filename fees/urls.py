from rest_framework.routers import DefaultRouter

from fees.views import (
    BankAccountViewSet,
    DiscountPolicyViewSet,
    FeeComponentViewSet,
    FeeScheduleViewSet,
    FeeStructureViewSet,
    InvoiceViewSet,
    PaymentViewSet,
    ScholarshipViewSet,
)

router = DefaultRouter()
router.register('structures', FeeStructureViewSet, basename='fee-structure')
router.register('components', FeeComponentViewSet, basename='fee-component')
router.register('schedules', FeeScheduleViewSet, basename='fee-schedule')
router.register('bank-accounts', BankAccountViewSet, basename='bank-account')
router.register('discounts', DiscountPolicyViewSet, basename='discount-policy')
router.register('scholarships', ScholarshipViewSet, basename='scholarship')
router.register('invoices', InvoiceViewSet, basename='invoice')
router.register('payments', PaymentViewSet, basename='payment')

urlpatterns = router.urls
