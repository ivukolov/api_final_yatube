from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Group(models.Model):
    title = models.CharField("Название группы", max_length=200)
    slug = models.SlugField("Слаг", unique=True)
    description = models.TextField("Описание")

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField("Текст поста")
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(
        "Автор", User, on_delete=models.CASCADE, related_name="posts"
    )
    image = models.ImageField(
        "Изображение", upload_to="posts/", null=True, blank=True
    )

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        "Автор", User, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(
        "Пост", Post, on_delete=models.CASCADE, related_name="comments"
    )
    group = models.ForeignKey(
        "Группа",
        Group,
        on_delete=models.SET_NULL,
        related_name="posts",
        blank=True,
        null=True,
    )
    text = models.TextField("Текст комментария")
    created = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following'
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers'
    )
