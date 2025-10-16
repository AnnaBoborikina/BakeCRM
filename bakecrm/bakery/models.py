from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Product(models.Model):
	name = models.CharField('Название', max_length=200)
	description = models.TextField('Описание', blank=True)
	price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
	image = models.ImageField('Изображение', upload_to='products/', blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
 
	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Товар'
		verbose_name_plural = 'Товары'
  
class Order(models.Model):
	STATUS_CHOICES = [
		('pending', 'Ожидает оплаты'),
		('paid', 'Оплачен'),
		('completed', 'Завершен'),
		('canceled', 'Отменен'),
	]

	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_orders', verbose_name='Создан продавцом')
	
	created_at = models.DateTimeField('Создан', default=timezone.now)
	updated_at = models.DateTimeField('Обновлен', auto_now=True)
	status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
	total_amount = models.DecimalField('Итого', max_digits=10, decimal_places=2, default=0)
 
	def __str__(self):
		return f'Заказ №{self.id} от {self.created_at.strftime("%d.%m.%Y %H:%M")}'

	class Meta:
		verbose_name = 'Заказ'
		verbose_name_plural = 'Заказы'
		ordering = ['-created_at']
  
class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	quantity = models.PositiveIntegerField('Количество', default=1)
	price_at_time = models.DecimalField('Цена на момент покупки', max_digits=10, decimal_places=2)
 
	def __str__(self):
		return f'{self.quantity} x {self.product.name}'

	class Meta:
		verbose_name = 'Позиция заказа'
		verbose_name_plural = 'Позиции заказа'
# Create your models here.

