from rest_framework import serializers
from .models import MotivationItem


class MotivationItemListSerializer(serializers.ModelSerializer):
    has_detail = serializers.SerializerMethodField()

    class Meta:
        model = MotivationItem
        fields = (
            "id", "type", "title", "subtitle", "short_text",
            "icon", "color", "action_label", "has_detail",
        )

    def get_has_detail(self, obj):
        return bool(obj.content and obj.content.strip())


class MotivationItemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MotivationItem
        fields = (
            "id", "type", "title", "subtitle", "short_text",
            "content", "icon", "color", "action_label",
            "created_at", "updated_at",
        )
