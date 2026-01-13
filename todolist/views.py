from django.shortcuts import render, redirect, get_object_or_404
from .models import Note, Task
from django.http import JsonResponse
import json
from django.utils import timezone
from datetime import timedelta

def home(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        if title:
            Note.objects.create(title=title)
        return redirect('home')

    # Pisahkan notes yang pinned dan tidak pinned
    pinned_notes = Note.objects.filter(pinned=True).order_by('-created_at')
    unpinned_notes = Note.objects.filter(pinned=False).order_by('-created_at')

    now = timezone.now()
    # Loop untuk pinned notes
    for note in pinned_notes:
        diff = now - note.updated_at
        note.show_time = diff < timedelta(hours=24)
        note.active_tasks = note.tasks.filter(completed=False).order_by('order')
        note.completed_tasks = note.tasks.filter(completed=True).order_by('order')
        note.completed_count = note.completed_tasks.count()

    # Loop untuk unpinned notes  
    for note in unpinned_notes:
        diff = now - note.updated_at
        note.show_time = diff < timedelta(hours=24)
        note.active_tasks = note.tasks.filter(completed=False).order_by('order')
        note.completed_tasks = note.tasks.filter(completed=True).order_by('order')
        note.completed_count = note.completed_tasks.count()

    return render(request, 'todolist/index.html', {
        'pinned_notes': pinned_notes,
        'unpinned_notes': unpinned_notes,
    })

def about(request):
    return render(request, 'todolist/about.html')

def gallery(request):
    return render(request, 'todolist/gallery.html')


# ==================== AJAX FUNCTIONS ====================

# ADD TASK - AJAX
def add_task(request, note_id):
    if request.method == 'POST':
        note = get_object_or_404(Note, id=note_id)
        title = request.POST.get('task_title')
        if title:
            # Cari order terakhir
            last_task = note.tasks.all().order_by('-order').first()
            new_order = (last_task.order + 1) if last_task else 0
            
            task = Task.objects.create(
                note=note, 
                title=title,
                order=new_order
            )
            note.save()
            
            return JsonResponse({
                'success': True,
                'task_id': task.id,
                'task_title': task.title,
                'completed': task.completed
            })
    return JsonResponse({'success': False})


# TOGGLE TASK - AJAX
def toggle_task(request, id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=id)
        task.completed = not task.completed
        task.save()
        task.note.save()
        
        return JsonResponse({
            'success': True,
            'completed': task.completed,
            'task_id': task.id
        })
    return JsonResponse({'success': False})


# EDIT TASK - AJAX
def edit_task(request, id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=id)
        title = request.POST.get('title')
        if title:
            task.title = title
            task.save()
            task.note.save()
            return JsonResponse({'success': True, 'title': title})
    return JsonResponse({'success': False})


# DELETE TASK - AJAX
def delete_task(request, id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=id)
        note = task.note
        task.delete()
        note.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


# EDIT NOTE - AJAX
def edit_note(request, id):
    if request.method == 'POST':
        note = get_object_or_404(Note, id=id)
        title = request.POST.get('title')
        if title:
            note.title = title
            note.save()
            return JsonResponse({'success': True, 'title': title})
    return JsonResponse({'success': False})


# PIN TODOLIST - AJAX
def pin_todolist(request, id):
    if request.method == 'POST':
        note = get_object_or_404(Note, id=id)
        note.pinned = not note.pinned
        note.save()
        return JsonResponse({
            'success': True,
            'pinned': note.pinned
        })
    return JsonResponse({'success': False})


# DELETE TODOLIST - AJAX
def delete_todolist(request, id):
    if request.method == 'POST':
        note = get_object_or_404(Note, id=id)
        note.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


# REORDER TASKS - AJAX
def reorder_tasks(request):
    if request.method == "POST":
        data = json.loads(request.body)
        order_list = data.get("order", [])

        for index, task_id in enumerate(order_list):
            Task.objects.filter(id=task_id).update(order=index)

        return JsonResponse({"success": True})
    return JsonResponse({"success": False})


# ADD TASK AJAX (alternative method)
def add_task_ajax(request, note_id):
    if request.method == "POST":
        note = get_object_or_404(Note, id=note_id)
        data = json.loads(request.body)
        title = data.get("title")
        
        if title:
            last_task = note.tasks.all().order_by("-order").first()
            new_order = (last_task.order + 1) if last_task else 0
            
            task = Task.objects.create(
                note=note, 
                title=title, 
                order=new_order
            )
            note.save()
            
            return JsonResponse({
                "id": task.id,
                "title": task.title,
                "completed": task.completed,
                "status": "success"
            })
    return JsonResponse({"status": "error"}, status=400)

