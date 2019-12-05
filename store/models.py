from django.db import models

# Create your models here.
ARTISTS = {
    'js-ondara': {'name': 'J.S Ondara'},
    'kery-james': {'name': 'Kery James'},
    'youssof': {'name': 'Youssoupha'}
}

ALBUMS = [
    {'name': 'Dieu est grand', 'artists': [ARTISTS['youssof']]},
    {'name':'Le combat continue', 'artists': [ARTISTS['kery-james']]},
    {'name': 'Tales of America', 'artists': [ARTISTS['js-ondara']]},
]



class Artist(models.Model):
    name = models.CharField('Nom',max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Artiste"
    

class Contact(models.Model):
    email = models.EmailField('Adresse mail', max_length=100)
    name = models.CharField('Nom', max_length=200)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Propect"


class Album(models.Model):
    reference = models.IntegerField('Référence', null=True)
    created_at = models.DateTimeField('Date de création', auto_now_add=True)
    available = models.BooleanField('Disponible', default=True)
    title = models.CharField('Titre', max_length=200)
    picture = models.URLField('URL de l\'image')
    artists = models.ManyToManyField(Artist, related_name='albums', blank=True)

    def __str__(self):
        return self.title


class Booking(models.Model):
    created_at = models.DateTimeField('Date de création', auto_now_add=True)
    contacted = models.BooleanField('demandé traitée',default=False)
    album = models.OneToOneField(Album, on_delete=models.PROTECT)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)

    def __str__(self):
        return self.contact.name

    class Meta:
        verbose_name = "Réservation"
    