from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import TaskSerializer
from .models import Task

class TaskView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            tasks = Task.objects.filter(user=request.user)
            serializer = TaskSerializer(tasks, many=True)
            return Response({
                'data': serializer.data,
                'message': 'Tasks fetched successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            data = request.data
            data['user'] = request.user.id
            print('Received task data:', data)
            serializer = TaskSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print('Validation errors:', serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        try:
            data = request.data
            task = Task.objects.filter(uid=data.get('uid')).first()
            
            if not task:
                return Response({
                    'data': {},
                    'message': 'Invalid task UID'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            if request.user != task.user:
                return Response({
                    'data': {},
                    'message': 'You are not authorized to update this task'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = TaskSerializer(task, data=data, partial=True)
            
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Something went wrong'
                }, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'data': serializer.data,
                'message': 'Task updated successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        try:
            data = request.data
            task = Task.objects.filter(uid=data.get('uid')).first()
            
            if not task:
                return Response({
                    'data': {},
                    'message': 'Invalid task UID'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            if request.user != task.user:
                return Response({
                    'data': {},
                    'message': 'You are not authorized to delete this task'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            task.delete()
            return Response({
                'data': {},
                'message': 'Task deleted successfully'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)
