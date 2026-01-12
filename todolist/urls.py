from django.urls import path
from . import views

urlpatterns = [
    # HALAMAN UTAMA
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('gallery/', views.gallery, name='gallery'),

    # NOTE
    path('note/edit/<int:id>/', views.edit_note, name='edit_note'),
    path('note/pin/<int:id>/', views.pin_todolist, name='pin_todolist'),
    path('note/delete/<int:id>/', views.delete_todolist, name='delete_todolist'),

    # TASK
    path('task/add/<int:note_id>/', views.add_task, name='add_task'),
    path('task/toggle/<int:id>/', views.toggle_task, name='toggle_task'),
    path('task/edit/<int:id>/', views.edit_task, name='edit_task'),
    path('task/delete/<int:id>/', views.delete_task, name='delete_task'),

    # EXTRA
    path('task/reorder/', views.reorder_tasks, name='reorder_tasks'),
    path('task/add-ajax/<int:note_id>/', views.add_task_ajax, name='add_task_ajax'),
]
