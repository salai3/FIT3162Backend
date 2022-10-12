from django.urls import path 
from back_end_application import views
from rest_framework_simplejwt import views as jwt_views
from .usersAPI.usersViews import UserAPIView, RegisterView
from . import views

urlpatterns = [
    path('', views.ApiOverview, name='home'),
    # URL for Products
    path('add_products/', views.add_products, name='add-products'),
    path('products/', views.view_products, name='view-products'),
    path('update_products/', views.update_products, name='update-products'),
    path('delete_products/', views.delete_product, name='delete-products'),
    path('low_stock/', views.view_low_on_stock, name='low_stock'),

    # URL for Batch
    path('add_batch/', views.add_batch, name='add-batches'),
    path('all_batch/', views.view_batch, name='view-batches'),
    path('update_batch/', views.update_batch, name='update-batches'),
    path('delete_batch/', views.delete_batch, name='delete-batches'),
    path('add_batch_status/', views.add_batch_status, name='add-batch_status'),
    path('all_batch_status/', views.view_batch_status, name='view-batch_status'),

    # URL for Stock
    path('add_stock/', views.add_stock, name='add-stock'),
    path('view_stock/', views.view_stock, name='view-stock'),
    path('update_stock/', views.update_stock, name='update-stock'),

    # URL for Order
    path('add_order/', views.add_order, name='add-order'),
    path('all_order/', views.view_order, name='view-order'),
    path('update_order/', views.update_order, name='update-order'),
    path('delete_order/', views.delete_order, name='delete-order'),
    path('add_order_status/', views.add_order_status, name='add-order-status'),
    path('all_order_status/', views.view_order_status, name='view-order-status'),
    path('test/<str:product_id>/', views.calculate_eta_for_supplier, name='test-order'),


    # URL for Order Content
    path('add_order_content/', views.add_order_content, name='add-order-content'),
    path('all_order_content/', views.view_order_content, name='view-order-content'),
    path('update_order_content/', views.update_order_content, name='update-order-content'),
    path('delete_order_content/', views.delete_order_content, name='delete-order-content'),

    # URL for Authentication
    path('auth/login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('user/', UserAPIView.as_view(), name='user'),
    path('customer/', views.view_customers, name='view-customer'),
    path('supplier/', views.view_suppliers, name='view-supplier'),

    # URL for Supplier Product
    path('add_supplier_product/', views.add_supplier_product, name='add-supplier-product'),
    path('supplier/<int:product_id>/', views.view_supplier_product_by_product, name='view_-supplier-product'),
    path('supplier/<int:supplier_id>/products/', views.view_supplier_product_by_supplier, name='view_-supplier-product')

]

