from django.db import models

class workQueue(models.Model):
    id_value = models.CharField(max_length=100)
    path_value = models.CharField(max_length=100)
    log = models.TextField(null=True, blank=True, default="No Ejecutado")
    status = models.TextField(default="Pendiente")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.id
