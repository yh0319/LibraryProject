from django.urls import path

from . import views

urlpatterns = [
    path('', views.BoardList.as_view(), name='Board_list'),
    path('view/<int:pk>', views.BoardView.as_view(), name='Board_view'),
    path('new', views.BoardCreate.as_view(), name='Board_new'),
    path('edit/<int:pk>', views.BoardUpdate.as_view(), name='Board_edit'),
    path('delete/<int:pk>', views.BoardDelete.as_view(), name='Board_delete'),
]
