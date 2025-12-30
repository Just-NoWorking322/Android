from django.db import models


class MotivationItem(models.Model):
    SMART_HINT = "SMART_HINT"      # Умные подсказки
    FIN_TIP = "FIN_TIP"            # Финансовые советы
    REMEMBER = "REMEMBER"          # Помните
    QUOTE = "QUOTE"                # Цитата дня
    WISH = "WISH"                  # Пожелание дня (если нужно)

    TYPE_CHOICES = (
        (SMART_HINT, "Умная подсказка"),
        (FIN_TIP, "Финансовый совет"),
        (REMEMBER, "Помните"),
        (QUOTE, "Цитата дня"),
        (WISH, "Пожелание дня"),
    )

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Тип")
    title = models.CharField(max_length=120, verbose_name="Заголовок")
    subtitle = models.CharField(max_length=160, blank=True, default="", verbose_name="Подзаголовок")
    short_text = models.TextField(blank=True, default="", verbose_name="Короткий текст")
    content = models.TextField(blank=True, default="", verbose_name="Полный текст (для Подробнее)")

    icon = models.CharField(max_length=50, blank=True, default="", verbose_name="Иконка (ключ/название)")
    color = models.CharField(max_length=30, blank=True, default="", verbose_name="Цвет (ключ)")

    action_label = models.CharField(max_length=40, blank=True, default="", verbose_name="Текст кнопки (Подробнее)")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    priority = models.PositiveIntegerField(default=100, verbose_name="Приоритет (меньше = выше)")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Мотивация"
        verbose_name_plural = "Мотивация"
        ordering = ("priority", "-created_at")

    def __str__(self):
        return f"{self.type}: {self.title}"
