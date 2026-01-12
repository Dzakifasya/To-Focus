from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=200)
    pinned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def is_completed(self):
        return self.tasks.exists() and not self.tasks.filter(completed=False).exists()

    def __str__(self):
        return self.title


class Task(models.Model):
    note = models.ForeignKey(
        Note,
        related_name='tasks',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return self.title
