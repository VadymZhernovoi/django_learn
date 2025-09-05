from django.db import models

class Status(models.TextChoices):
    NEW = 'New', "New"
    IN_PROGRESS = 'In Progress', "In Progress"
    PENDING = 'Pending', "Pending"
    BLOCKED = 'Blocked', "Blocked"
    DONE = 'Done', "Done"