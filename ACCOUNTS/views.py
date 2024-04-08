from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerialzer,LoginSerialzer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

class Registerview(APIView):
    
    def post(self,request):
        try:
            
            data=request.data
            serializer= RegisterSerialzer(data=data)
            
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,   
                    'message':'something went wrong'},status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            
            return Response({
                    'data': serializer.data,   
                    'message':'your account created'},status=status.HTTP_201_CREATED)
        
        except Exception as e:
        
            return Response({
               'data': {},   
               'message':'something wents wrong'},status=status.HTTP_400_BAD_REQUEST) 

class Loginview(APIView): 
    def post(self,request):
        try:
            
            data=request.data
            serializer= LoginSerialzer(data=data)
            
            if not serializer.is_valid():
                    return Response({
                                'data': serializer.errors,   
                               'message':'somethissng went wrong'},status=status.HTTP_400_BAD_REQUEST) 
            response=serializer.get_jwt_token(serializer.data)     
            
            return Response( response,status=status.HTTP_201_CREATED)
                       
                
        except Exception as e:
            print(e)
            return Response({
               'data': {},   
               'message':'something wents wrong'},status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')

            if not refresh_token:
                return Response({
                    'message': 'Refresh token is required.',
                    'data': {}
                }, status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken(refresh_token)

            new_access_token = str(refresh.access_token)
            
            return Response({
                'message': 'Token refreshed successfully.',
                'data': {'access_token': new_access_token}
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'message': 'Something went wrong while refreshing token.',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)
