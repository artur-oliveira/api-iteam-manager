from django.db import models


class Categoria(models.Model):
    nome = models.CharField(max_length=255, unique=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.nome = str(self.nome).upper().strip()
        super(Categoria, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return str(self.nome).capitalize()

    def __repr__(self):
        return self.__str__()
