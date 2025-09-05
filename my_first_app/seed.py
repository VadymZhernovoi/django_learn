import random
from faker import Faker
from .models import Category, Task

faker = Faker('ru_RU')

# print(faker.sentence(nb_words=5))
# print(faker.text(max_nb_chars=100))

def create_categories(count=100):
    for _ in range(count):
        Category.objects.create( name=faker.sentence(nb_words=5))
    print('Categories created.')

# def create_tasks(count=100):
#     for _ in range(count):
#         Task.objects.create(
#             title=faker.text(max_nb_chars=50),
#             description=faker.text(max_nb_chars=550),
#             status=random.choice(["New", "In Progress", "Pending", "Blocked", "Done"]),
#             created_at=faker.date_time(),
#             deadline=faker.date_time(),
#         )
#     print('Tasks created.')

