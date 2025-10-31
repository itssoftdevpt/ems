from rest_framework import serializers

from fees.models import (
    BankAccount,
    DiscountPolicy,
    FeeComponent,
    FeeSchedule,
    FeeStructure,
    Invoice,
    InvoiceLineItem,
    Payment,
    PaymentAllocation,
    Scholarship,
)


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = '__all__'


class FeeComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeComponent
        fields = ('id', 'name', 'description', 'is_mandatory')
        read_only_fields = ('id',)


class FeeStructureSerializer(serializers.ModelSerializer):
    components = FeeComponentSerializer(many=True, read_only=True)

    class Meta:
        model = FeeStructure
        fields = (
            'id',
            'name',
            'description',
            'applies_to_management_group',
            'is_independent',
            'components',
        )
        read_only_fields = ('id',)


class FeeScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeSchedule
        fields = ('id', 'structure', 'academic_year', 'term', 'component', 'amount', 'level')
        read_only_fields = ('id',)


class DiscountPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountPolicy
        fields = ('id', 'name', 'description', 'percentage', 'applies_to_level', 'applies_to_component')
        read_only_fields = ('id',)


class ScholarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholarship
        fields = ('id', 'student', 'name', 'discount_policy', 'amount', 'start_year', 'end_year')
        read_only_fields = ('id',)


class InvoiceLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceLineItem
        fields = ('id', 'component', 'description', 'amount')
        read_only_fields = ('id',)


class InvoiceSerializer(serializers.ModelSerializer):
    line_items = InvoiceLineItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = (
            'id',
            'student',
            'academic_year',
            'term',
            'structure',
            'status',
            'issued_on',
            'due_date',
            'total_amount',
            'discount_amount',
            'line_items',
        )
        read_only_fields = ('id', 'issued_on')

    def create(self, validated_data):
        line_items = validated_data.pop('line_items', [])
        invoice = Invoice.objects.create(**validated_data)
        total = 0
        for item in line_items:
            InvoiceLineItem.objects.create(invoice=invoice, **item)
            total += item.get('amount', 0)
        invoice.total_amount = total
        invoice.save(update_fields=['total_amount'])
        return invoice


class PaymentAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentAllocation
        fields = ('id', 'line_item', 'amount')
        read_only_fields = ('id',)


class PaymentSerializer(serializers.ModelSerializer):
    allocations = PaymentAllocationSerializer(many=True, required=False)

    class Meta:
        model = Payment
        fields = ('id', 'invoice', 'amount', 'paid_on', 'reference', 'received_by', 'bank_account', 'allocations')
        read_only_fields = ('id', 'received_by')

    def create(self, validated_data):
        allocations = validated_data.pop('allocations', [])
        payment = Payment.objects.create(**validated_data)
        for allocation in allocations:
            PaymentAllocation.objects.create(payment=payment, **allocation)
        return payment
