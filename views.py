from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import TaskSerializer
from .scoring import score_tasks

from django.shortcuts import render

def frontend(request):
    return render(request, "index.html")


# tasks/views.py
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import TaskSerializer
from .scoring import score_tasks

import json

def frontend(request):
    return render(request, "index.html")


class AnalyzeTasksView(APIView):
    """
    POST /api/tasks/analyze/?strategy=...
    Accepts list of tasks in POST body and returns them sorted with scores.
    """
    def post(self, request):
        # read strategy from query params (default to smart_balance)
        strategy = request.query_params.get("strategy", "smart_balance")

        serializer = TaskSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        tasks = serializer.validated_data

        scored = score_tasks(tasks, strategy=strategy)

        return Response(scored, status=status.HTTP_200_OK)


class SuggestTasksView(APIView):
    """
    GET /api/tasks/suggest/?tasks=[...]&strategy=...
    Returns top 3 tasks with explanations.
    """
    def get(self, request):
        tasks_param = request.query_params.get("tasks")
        strategy = request.query_params.get("strategy", "smart_balance")

        if not tasks_param:
            return Response({"error": "Please send tasks as ?tasks=[...] JSON"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tasks = json.loads(tasks_param)
        except Exception as e:
            return Response({"error": "Invalid JSON for tasks", "detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TaskSerializer(data=tasks, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        scored = score_tasks(serializer.validated_data, strategy=strategy)

        # return top 3
        return Response(scored[:3], status=status.HTTP_200_OK)





