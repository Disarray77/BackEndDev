
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from todo_app.models import TodoList, Todo
from todo_app.serializers import TodoListSerializer, TodoSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser
import json


@api_view(['GET', 'POST'])
@csrf_exempt
def todo_lists_handler(request):
    if request.method == 'GET':
        categories = TodoList.objects.all()
        serializer = TodoListSerializer(categories, many=True)
        return JsonResponse(serializer.data, status=200, safe=False)
    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = TodoListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data=serializer.data, status=200)
        return JsonResponse(data=serializer.errors, status=400)
    return JsonResponse({'message': 'Request is not supported'}, status=400)


def get_todo_list(pk):
    try:
        todo_list = TodoList.objects.get(id=pk)
        return {
            'status': 200,
            'todo_list': todo_list
        }
    except TodoList.DoesNotExist as e:
        return {
            'status': 404,
            'todo_list': None
        }


@csrf_exempt
def todo_list_handler(request, pk):
    result = get_todo_list(pk)

    if result['status'] == 404:
     return JsonResponse({'message': 'TodoList not found'}, status=404)


    todo_list = result['todo_list']

    if request.method == 'GET':
        serializer = TodoListSerializer(todo_list)
        return JsonResponse(serializer.data, status=200)
    if request.method == 'PUT':
        data = json.loads(request.body)
        serializer = TodoListSerializer(data=data, instance=todo_list)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(data=serializer.data)
        return JsonResponse(data=serializer.errors, status=400)
    if request.method == 'DELETE':
        todo_list.delete()
        return JsonResponse({'message': 'TodoList deleted successfully!'})
    return JsonResponse({'message': 'Request is not supported'}, status=400)


@csrf_exempt
def todo_list_todos_handler(request, pk):
    result = get_todo_list(pk)

    if result['status'] == 404:
        return JsonResponse({'message': 'TodoList not found'}, status=404)

    todo_list = result['todo_list']

    if request.method == 'GET':
        todos = todo_list.todo_set.all()
        serializer = TodoSerializer(todos, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == 'POST':
        data = json.loads(request.body)
        data['todo_list_id'] = pk
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    return JsonResponse({'message': 'Request is not supported'}, status=400)


def get_todo(pk):
    try:
        todo = Todo.objects.get(id=pk)
        return {
            'status': 200,
            'todo': todo
        }
    except Todo.DoesNotExist as e:
        return {
            'status': 404,
            'todo': None
        }


@csrf_exempt
def todos_handler(request):
    if request.method == 'GET':
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == 'POST':
        data = json.loads(request.body)
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    return JsonResponse({'message': 'Request is not supported'}, status=400)



@csrf_exempt
def todo_handler(request, pk):
    result = get_todo(pk)

    if result['status'] == 404:
        return JsonResponse({'message': 'Todo not found'}, status=404)

    todo = result['todo']

    if request.method == 'GET':
        serializer = TodoSerializer(todo)
        return JsonResponse(serializer.data)
    if request.method == 'PUT':
        data = json.loads(request.body)
        serializer = TodoSerializer(instance=todo, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        return JsonResponse(serializer.errors, safe=False, status=400)
    if request.method == 'DELETE':
        todo.delete()
        serializer = TodoSerializer(todo)
        return JsonResponse(serializer.data, status=200, safe=False)
    return JsonResponse({'message': 'Request is not supported'}, status=400)