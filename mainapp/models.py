from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, db_index=True, unique=True, verbose_name="Наименование категории")
    description = models.TextField(blank=True, verbose_name="Описание категории товара")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name="Наименование товара")
    image = models.ImageField(upload_to='product_images/%y/%m/%d', blank=True, verbose_name="Фото товара")
    description = models.TextField(blank=True, verbose_name="Описание товара")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена товара")
    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество на складе")
    color = models.CharField(max_length=50, verbose_name="Цвет товара", blank=True, unique=True)
    size = models.PositiveSmallIntegerField(verbose_name="Размер", blank=True, unique=True)
    created_at = models.DateField(auto_now_add=True, verbose_name="Дата поступления на склад")
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} | {self.category}'


"""
# цвет
class Color(models.Model):
    color_1 = models.CharField(max_length=50)
    category_1 = models.ForeignKey(Product, related_name="color_pr", to_field="color", on_delete=models.CASCADE)

    def __str__(self):
        return self.color_1


# размер
class Size(models.Model):
    size_1 = models.PositiveSmallIntegerField()
    category_2 = models.ForeignKey(Product, related_name="size_pr", to_field="size", on_delete=models.CASCADE)"""


