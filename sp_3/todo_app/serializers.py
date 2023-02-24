from rest_framework import serializers
from todo_app.models import TodoList, Todo

class TodoListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(min_length=5, max_length=100, allow_null=False)

    def create(self, validated_data):
        todo_list = TodoList(**validated_data)
        todo_list.save()
        return todo_list

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()
        return instance


class TodoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(min_length=5, max_length=200, allow_null=False)
    todo_list = TodoListSerializer(required=False, read_only=True)
    todo_list_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        todo = Todo(**validated_data)
        todo.save()
        return todo

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.todo_list_id = validated_data.get('todo_list_id', instance.todo_list_id)

        instance.save()
        return instance