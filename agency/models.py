from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Cat(TimeStampedModel):
    name = models.CharField(max_length=120)
    years_of_experience = models.PositiveIntegerField(default=0)
    breed = models.CharField(max_length=120)
    salary = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.name} ({self.breed})"


class Mission(TimeStampedModel):
    name = models.CharField(max_length=200, default="Mission")
    cat = models.ForeignKey(
        Cat, related_name="missions", on_delete=models.SET_NULL, null=True, blank=True
    )
    is_completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Mission #{self.pk or 'new'}"


class Target(TimeStampedModel):
    mission = models.ForeignKey(
        Mission, related_name="targets", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=120)
    notes = models.TextField(blank=True, default="")
    is_completed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"Target {self.name}"
