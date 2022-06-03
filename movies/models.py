from datetime import date

from django.db.models import (CharField, ImageField, ManyToManyField, Model,
                              PositiveSmallIntegerField, SlugField, TextField, DateField, BooleanField, ForeignKey,
                              SET_NULL, PositiveIntegerField, CASCADE, EmailField)
from django.urls import reverse


class Category(Model):
    """Категории"""
    name = CharField("Категория", max_length=150)
    description = TextField("Описание")
    url = SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Actor(Model):
    """Актёры и режиссёры"""
    name = CharField("Имя", max_length=100)
    age = PositiveSmallIntegerField("Возраст", default=0)
    description = TextField("Описание", )
    image = ImageField("Изображение", upload_to="actors/")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={'slug': self.name})

    class Meta:
        verbose_name = "Актёры и режиссёры"
        verbose_name_plural = "Актёры и режиссёры"


class Genre(Model):
    name = CharField("Название", max_length=100)
    description = TextField("Описание")
    url = SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Movie(Model):
    """Фильмы"""
    title = CharField("Название", max_length=100)
    tagline = CharField("Слоган", max_length=100, default="")
    description = TextField("Описание")
    poster = ImageField("Постер", upload_to="movies/")
    year = PositiveSmallIntegerField("Год выхода", default=2022)
    country = CharField("Страна", max_length=30)
    directors = ManyToManyField(Actor, verbose_name="Режиссёр", related_name="film_director")
    actors = ManyToManyField(Actor, verbose_name="Актёры", related_name="film_actor")
    genres = ManyToManyField(Genre, verbose_name="Жанры")
    world_premiere = DateField("Премьера в мире", default=date.today)
    budget = PositiveIntegerField("Бюджет", default=0, help_text="Указывать сумму в долларах")
    gross_usa = PositiveIntegerField(
        "Сборы в США", default=0, help_text="Указывать сумму в долларах"
    )
    gross_worldwide = PositiveIntegerField(
        "Сборы в мире", default=0, help_text="Указывать сумму в долларах"
    )
    category = ForeignKey(
        Category, verbose_name="Категория", on_delete=SET_NULL, null=True
    )
    url = SlugField(max_length=160, unique=True)
    draft = BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.url})

    def get_reviews(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class MovieShots(Model):
    """Кадры из фильма"""
    title = CharField("Название", max_length=100)
    description = TextField("Описание")
    image = ImageField("Изображение", upload_to="movie_shots/")
    movie = ForeignKey(Movie, verbose_name="Фильм", on_delete=CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"


class RatingStar(Model):
    """Звезда рейтинга"""
    value = PositiveSmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ['-value']


class Rating(Model):
    """Рейтинг"""
    ip = CharField("IP-адрес", max_length=15)
    star = ForeignKey(RatingStar, on_delete=CASCADE, verbose_name="Звезда")
    movie = ForeignKey(Movie, on_delete=CASCADE, verbose_name="Фильм")

    def __str__(self):
        return f"{self.star} - {self.movie}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Review(Model):
    """Отзывы"""
    email = EmailField()
    name = CharField("Имя", max_length=100)
    text = TextField("Сообщение", max_length=5000)
    parent = ForeignKey("self", verbose_name="Родитель", on_delete=SET_NULL, blank=True, null=True)
    movie = ForeignKey(Movie, verbose_name="Фильм", on_delete=CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
