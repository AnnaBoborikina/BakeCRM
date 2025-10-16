from django.urls import path
from . import views

app_name = 'bakery'

urlpatterns = [
		# Продавец
		path('order/create-ajax/', views.order_create_ajax, name='order_create_ajax'),
		
  		# Админ: Заказы
		path('admin/orders/', views.order_list_admin, name='order_list_admin'),
		path('admin/order/<int:order_id>/detail/', views.order_detail_json, name='order_detail_json'),
		path('admin/order/<int:order_id>/update/', views.order_update, name='order_update'),
		path('admin/order/<int:order_id>/delete/', views.delete_order, name='delete_order'),
	
		# Админ: Товары
		path('admin/products/', views.product_list_admin, name='product_list_admin'),
		path('admin/product/save/', views.product_create_update, name='product_save'),
		path('admin/product/<int:product_id>/delete/', views.product_delete, name='product_delete'),

		# Админ: Пользователи
		path('admin/users/', views.user_list_admin, name='user_list_admin'),
		path('admin/user/save/', views.user_create_update, name='user_save'),
		path('admin/user/<int:user_id>/delete/', views.user_delete, name='user_delete'),
  
		# Админ: Отчеты
		path('admin/reports/', views.reports_view, name='reports'),
		path('admin/reports/data/', views.reports_data, name='reports_data'),
		path('admin/reports/export/xlsx/', views.export_xlsx, name='export_xlsx'),
		path('admin/reports/export/pdf/', views.export_pdf, name='export_pdf'),
]
