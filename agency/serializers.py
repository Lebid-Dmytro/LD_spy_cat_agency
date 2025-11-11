from typing import Any

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework import serializers

from .models import Cat, Mission, Target
from .services import fetch_valid_breeds


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = ["id", "name", "years_of_experience", "breed", "salary", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_breed(self, value: str) -> str:
        breeds = fetch_valid_breeds()
        if value not in breeds:
            raise serializers.ValidationError("Unknown cat breed (TheCatAPI).")
        return value


class TargetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ["name", "country", "notes"]


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ["id", "mission", "name", "country", "notes", "is_completed", "created_at", "updated_at"]
        read_only_fields = ["id", "mission", "is_completed", "created_at", "updated_at"]


class MissionCreateSerializer(serializers.ModelSerializer):
    targets = TargetCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Mission
        fields = ["id", "name", "cat", "is_completed", "targets", "created_at", "updated_at"]
        read_only_fields = ["id", "is_completed", "created_at", "updated_at"]

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        cat = attrs.get("cat")
        if cat and Mission.objects.filter(cat=cat, is_completed=False).exists():
            raise serializers.ValidationError("This cat already has an active mission.")

        targets_data = self.initial_data.get("targets", [])
        if not isinstance(targets_data, list) or not targets_data:
            raise serializers.ValidationError("Mission must have at least 1 target.")
        if len(targets_data) > 3:
            raise serializers.ValidationError("Mission can have at most 3 targets.")
        return attrs

    def create(self, validated_data: dict[str, Any]) -> Mission:
        targets_data = validated_data.pop("targets", [])
        with transaction.atomic():
            mission = Mission.objects.create(**validated_data)
            Target.objects.bulk_create(
                [Target(mission=mission, **t) for t in targets_data]
            )
        return mission


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True, read_only=True)

    class Meta:
        model = Mission
        fields = ["id", "name", "cat", "is_completed", "targets", "created_at", "updated_at"]
        read_only_fields = ["id", "is_completed", "created_at", "updated_at", "targets"]

    def validate_cat(self, value: Cat | None) -> Cat | None:
        if value and Mission.objects.filter(cat=value, is_completed=False).exists():
            raise serializers.ValidationError("This cat already has an active mission.")
        return value

    def update(self, instance: Mission, validated_data: dict[str, Any]) -> Mission:
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        try:
            instance.full_clean()
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.message_dict or exc.messages)
        instance.save()
        return instance


class TargetNotesSerializer(serializers.Serializer):
    notes = serializers.CharField(allow_blank=True, required=True)
