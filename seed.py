import os
import random
import django
from decimal import Decimal

from agency.models import Cat, Mission, Target 
from agency.services import fetch_valid_breeds 


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spycat.settings")

django.setup()


def run() -> None:
    random.seed(1)

    breeds = list(fetch_valid_breeds()) or ["Abyssinian", "Sphynx"]

    cats = [
        Cat.objects.create(
            name="Biri",
            years_of_experience=3,
            breed=breeds[0],
            salary=Decimal("1400.00"),
        ),
        Cat.objects.create(
            name="Tiger",
            years_of_experience=2,
            breed=breeds[1],
            salary=Decimal("1200.00"),
        ),
    ]

    m1 = Mission.objects.create(name="Operation Shadow", cat=cats[0])
    Target.objects.create(
        mission=m1, name="M-001", country="UA", notes="Initial surveillance"
    )

    m2 = Mission.objects.create(name="Night Watch")
    Target.objects.create(
        mission=m2, name="M-002", country="PL", notes="Data collection"
    )

    print("Seed done: 2 cats, 2 missions, 2 targets.")


if __name__ == "__main__":
    run()


