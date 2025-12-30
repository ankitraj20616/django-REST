from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest, JsonResponse, Http404
from students.models import Student
from employees.models import Employee
from .serializers import StudentSerializer, EmployeeSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import mixins, generics, viewsets
from blogs.models import Blog, Comment
from blogs.serializers import BlogSerializer, CommentSerializer
from .pagination import CustomPagination
from employees.filters import EmployeeFilter
from rest_framework.filters import SearchFilter, OrderingFilter

# Create your views here.

@api_view(["GET", "POST"])
def students_view(request: HttpRequest):
    # students = Student.objects.all()
    # students = list(students.values())
    # return JsonResponse(students, safe= False)

    if request.method == "GET":
        # Get all the data from the Student table
        students = Student.objects.all()
        serializer = StudentSerializer(students, many= True)
        return Response(serializer.data, status= status.HTTP_200_OK )
    elif request.method == "POST":
        serializer = StudentSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET", "PUT", "DELETE"])
def particular_student_view(request: HttpRequest, student_id: int):
    try:
        student = Student.objects.get(student_id= student_id)
    except Student.DoesNotExist:
        return Response("Invalide Student ID!", status= status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = StudentSerializer(student)
        return Response(serializer.data, status= status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = StudentSerializer(student, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        student.delete()
        return Response("Deleted this Student.", status= status.HTTP_204_NO_CONTENT)
    

# class Employees(APIView):
#     def get(self, request: HttpRequest):
#         employees = Employee.objects.all()
#         serializer = EmployeeSerializer(employees, many= True)
#         return Response(serializer.data, status= status.HTTP_200_OK)
    
#     def post(self, request: HttpRequest):
#         serializer = EmployeeSerializer(data= request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status= status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


# class EmployeeDetails(APIView):
#     def get_object(self, emp_id: int):
#         try:
#             employee = Employee.objects.get(emp_id= emp_id)
#             return employee
#         except Employee.DoesNotExist:
#             # return Response("Invalid emp_id!", status= status.HTTP_400_BAD_REQUEST)
#             raise Http404("Invalid emp_id!")
        
#     def get(self, request: HttpRequest, emp_id: int):
#         employee = self.get_object(emp_id)
        
#         serializer = EmployeeSerializer(employee)
#         return Response(serializer.data, status= status.HTTP_200_OK)
#     def put(self, request: HttpRequest, emp_id: int):
#         employee = self.get_object(emp_id)
#         serializer = EmployeeSerializer(employee, data= request.data)
#         if serializer.is_valid():
#             serializer.save()
    
#             return Response(request.data, status = status.HTTP_202_ACCEPTED)
#         return Response("Invalid Updated Data!", status= status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request: HttpRequest, emp_id: int):
#         employee = self.get_object(emp_id)
#         employee.delete()
#         return Response("Employee Record Deleted!", status= status.HTTP_204_NO_CONTENT)


## Using Mixins
'''
class Employees(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request: HttpRequest):
        return self.list(request)
    
    def post(self, request: HttpRequest):
        return self.create(request)
    
class EmployeeDetails(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field= "emp_id"
    lookup_url_kwarg= "emp_id"

    def get(self, request: HttpRequest, emp_id: int):
        return self.retrieve(request)
    
    def put(self, request: HttpRequest, emp_id: int):
        return self.update(request)
    
    def delete(self, request: HttpRequest, emp_id: int):
        return self.destroy(request)

'''

## Using Generics
'''
class Employees(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class EmployeeDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = "emp_id"
    lookup_url_kwarg = "emp_id"

'''

#  Using viewsets

# class EmployeesViewset(viewsets.ViewSet):
#     def list(self, request: HttpRequest):
#         queryset = Employee.objects.all()
#         serializer = EmployeeSerializer(queryset, many= True)
#         return Response(serializer.data, status= status.HTTP_200_OK)
#     def create(self, request: HttpRequest):
#         serializer = EmployeeSerializer(data= request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status= status.HTTP_201_CREATED)
#         return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
#     def retrieve(self, request: HttpRequest, pk: int= None):
#         queryset = get_object_or_404(Employee, emp_id= pk)
#         serializer = EmployeeSerializer(queryset)
#         return Response(serializer.data, status= status.HTTP_200_OK)
    
#     def update(self, request: HttpRequest, pk: int= None):
#         employee = Employee.objects.get(emp_id= pk)
#         serializer = EmployeeSerializer(employee, data= request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status= status.HTTP_202_ACCEPTED)
#         return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
#     def delete(self, request: HttpRequest, pk: int= None):
#         employee = get_object_or_404(Employee, emp_id= pk)
#         employee.delete()
#         return Response("Employee Record Deleted!", status= status.HTTP_204_NO_CONTENT)


class EmployeesViewset(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination
    # filterset_fields = ["designation"]
    filterset_class = EmployeeFilter



class BlogsView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["blog_title"]
    ordering_fields= ["id"]


class CommentsView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = "pk"


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "pk"


     