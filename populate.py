import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hangarin.settings')
django.setup()

from faker import Faker
from django.utils import timezone
from tasks.models import Task, Note, SubTask, Priority, Category

fake = Faker()

statuses = ["Pending", "In Progress", "Completed"]

priorities = list(Priority.objects.all())
categories = list(Category.objects.all())

for _ in range(10):
    task = Task.objects.create(
        title=fake.sentence(nb_words=5),
        description=fake.paragraph(nb_sentences=3),
        deadline=timezone.make_aware(fake.date_time_this_month()),
        status=fake.random_element(elements=statuses),
        priority=random.choice(priorities),
        category=random.choice(categories),
    )

    for _ in range(random.randint(1, 3)):
        SubTask.objects.create(
            parent_task=task,
            title=fake.sentence(nb_words=4),
            status=fake.random_element(elements=statuses),
        )

    for _ in range(random.randint(1, 2)):
        Note.objects.create(
            task=task,
            content=fake.paragraph(nb_sentences=2),
        )

print("Fake data inserted successfully.")