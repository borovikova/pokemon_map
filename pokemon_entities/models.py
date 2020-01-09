from django.db import models


class Pokemon(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='название покемона')
    en_title = models.CharField(
        max_length=255,
        verbose_name='название покемона на английском',
        blank=True)
    jp_title = models.CharField(
        max_length=255,
        verbose_name='название покемона на японском',
        blank=True)
    picture = models.ImageField(
        upload_to='pokemons',
        null=True,
        verbose_name='картинка покемона')
    description = models.TextField(
        verbose_name='описание',
        blank=True)
    parent = models.ForeignKey(
        "self",
        models.SET_NULL,
        null=True,
        related_name='parent_to',
        verbose_name='из кого эволюционировал',
        blank=True)

    def __str__(self):
        return f"{self.title}"


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        related_name='entities',
        verbose_name='покемон')
    lat = models.FloatField(
        verbose_name='широта')
    lon = models.FloatField(
        verbose_name='долгота')
    level = models.IntegerField(
        verbose_name='уровень',
        blank=True,
        default=0)
    health = models.IntegerField(
        verbose_name='здоровье',
        blank=True,
        default=0)
    strength = models.IntegerField(
        verbose_name='сила',
        blank=True,
        default=0)
    defence = models.IntegerField(
        verbose_name='защита',
        blank=True,
        default=0)
    stamina = models.IntegerField(
        verbose_name='выносливость',
        blank=True,
        default=0)
    appeared_at = models.DateTimeField(
        verbose_name='дата и время появления',
        blank=True,
        null=True)
    disappeared_at = models.DateTimeField(
        verbose_name='дата и время исчезновения',
        blank=True,
        null=True)
