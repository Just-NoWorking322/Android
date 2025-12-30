from rest_framework import serializers
from django.db.models import Sum
from decimal import Decimal

from .models import Account, Category, Transaction, Debt


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("id", "name", "currency", "created_at")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "type", "created_at")


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            "id", "account", "category", "type", "amount",
            "title", "note", "occurred_at", "created_at",
        )

    def validate(self, attrs):
        # аккаунт/категория должны принадлежать юзеру
        user = self.context["request"].user
        if attrs["account"].user_id != user.id:
            raise serializers.ValidationError("Нельзя использовать чужой account.")
        if attrs.get("category") and attrs["category"].user_id != user.id:
            raise serializers.ValidationError("Нельзя использовать чужую category.")
        return attrs


class DebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debt
        fields = (
            "id", "kind", "person_name", "amount",
            "due_date", "description", "is_closed", "closed_at", "created_at",
        )
        read_only_fields = ("is_closed", "closed_at")


class DebtCloseSerializer(serializers.Serializer):
    is_closed = serializers.BooleanField()
