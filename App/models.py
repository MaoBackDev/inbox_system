from django.db import models
from django.utils.html import format_html


class Customer(models.Model):
    STATUS = (
        ('Pending', 'pending'),
        ('Read', 'read'),
    )
    name = models.CharField('Nombre', max_length=50)
    phone = models.CharField('Teléfono', max_length=20)
    email = models.EmailField('Email', max_length=254)
    subject = models.CharField('Asunto', max_length=20)
    message = models.TextField('Mensaje')
    file = models.FileField('Archivos')
    created_at = models.DateTimeField('Enviado', auto_now=False, auto_now_add=True)
    status = models.CharField('Estado', max_length=50, choices=STATUS)

    # CONTROL READ/UNREAD MESSAGE ON ADMIN.PY
    def situation(self):
        if self.status == 'Read':
            return format_html('<span style="color:black">{0}</span>', self.status)
        else:
            return format_html('<span style="color:red">{0}</span>', self.status)
    situation.allow_tags = True

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Inbox'