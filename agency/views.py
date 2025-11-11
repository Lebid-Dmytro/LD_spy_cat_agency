from django.db.models import QuerySet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Cat, Mission, Target
from .serializers import (
    CatSerializer,
    MissionCreateSerializer,
    MissionSerializer,
    TargetNotesSerializer,
    TargetSerializer,
)


class CatViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[Cat] = Cat.objects.all().order_by("id")
    serializer_class = CatSerializer


class MissionViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[Mission] = Mission.objects.all().order_by("-created_at")

    def get_serializer_class(self):
        if self.action == "create":
            return MissionCreateSerializer
        return MissionSerializer

    @action(detail=True, methods=["post"], url_path="assign-cat")
    def assign_cat(self, request: Request, pk: str | None = None) -> Response:
        mission: Mission = self.get_object()
        cat_id = request.data.get("cat")
        try:
            cat = Cat.objects.get(pk=cat_id)
        except Cat.DoesNotExist:
            return Response({"detail": "Cat not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = MissionSerializer(instance=mission, data={"cat": cat.id}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(MissionSerializer(mission).data)

    def destroy(self, request: Request, *args, **kwargs) -> Response:
        mission: Mission = self.get_object()
        if mission.cat_id:
            return Response(
                {"detail": "Cannot delete a mission assigned to a cat."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        mission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TargetViewSet(viewsets.GenericViewSet):
    queryset: QuerySet[Target] = Target.objects.select_related("mission").all()
    serializer_class = TargetSerializer

    @action(detail=True, methods=["post"], url_path="complete")
    def complete(self, request: Request, pk: str | None = None) -> Response:
        target: Target = self.get_object()
        if not target.is_completed:
            target.is_completed = True
            target.save(update_fields=["is_completed"])
            mission = target.mission
            if not mission.is_completed and not mission.targets.filter(
                is_completed=False
            ).exists():
                mission.is_completed = True
                mission.save(update_fields=["is_completed"])
        return Response(TargetSerializer(target).data)

    @action(detail=True, methods=["post"], url_path="notes")
    def update_notes(self, request: Request, pk: str | None = None) -> Response:
        target: Target = self.get_object()
        serializer = TargetNotesSerializer(data=request.data, context={"target": target})
        serializer.is_valid(raise_exception=True)
        if target.is_completed or target.mission.is_completed:
            return Response(
                {"detail": "Notes are frozen: target or mission completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        target.notes = serializer.validated_data["notes"]
        target.save(update_fields=["notes"])
        return Response(TargetSerializer(target).data)
