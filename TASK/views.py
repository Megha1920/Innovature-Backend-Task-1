from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import TaskSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Task
class TaskView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    
    def get(self,request):
        try:
            tasks=Task.objects.filter(user=request.user)
            serializer=TaskSerializer(tasks,many=True)
            
            return Response({
                    'data': serializer.data,   
                    'message':'task fetched succesfully'},status=status.HTTP_201_CREATED)
        except Exception as e:
           print(e)
           return Response({
               'data': {},   
               'message':'something went wrong'},status=status.HTTP_400_BAD_REQUEST)      
            
    
    def post(self, request):
        try:
            data = request.data
            data['user'] = request.user.id
            print('user')
            print("Received task data:", data)
            serializer = TaskSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print("Validation errors:", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        
        except Exception as e:
           print(e)
           return Response({
               'data': {},   
               'message':'something went wrong'},status=status.HTTP_400_BAD_REQUEST)  
    
    def patch(self,request):
        try:
            data=request.data
            task=Task.objects.filter(uid=data.get('uid'))
            
            if not task.exists():
                return Response({
                    'data': {},   
                    'message':'invalid task uid'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
            if request.user != task[0].user:
               return Response({
                    'data': {},   
                    'message':'you are not authorized to this'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = TaskSerializer(task[0],data=data,partial=True)
            
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,   
                    'message':'something went wrong'},status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                            'data': serializer.data,   
                            'message':'task updated succesfully'},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
           print(e)
           return Response({
               'data': {},   
               'message':'something went wrong'},status=status.HTTP_400_BAD_REQUEST)  
           
    
    def delete(self,request):
        try:
            data=request.data
            
            task=Task.objects.filter(uid=data.get('uid'))
            print(task)
            print(task[0].user)
            if not task.exists():
                return Response({
                    'data': {},   
                    'message':'invalid task uid'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
            if request.user != task[0].user:
               return Response({
                    'data': {},   
                    'message':'you are not authorized to this'
                    }, status=status.HTTP_400_BAD_REQUEST)   
            
            task[0].delete()
            return Response({
                            'data': {},   
                            'message':'task deleted succesfully'},
                            status=status.HTTP_201_CREATED)
            
        except Exception as e:
           print(e)
           return Response({
               'data': {},   
               'message':'something went wrong'},status=status.HTTP_400_BAD_REQUEST)  
               
    
           
           
