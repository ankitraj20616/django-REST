from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("employees", views.EmployeesViewset, basename= "employee")


urlpatterns = [
    # Function Base Views
    path("students/", views.students_view),
    path("student/<int:student_id>/", views.particular_student_view),

    # Class Based Views
    # path("employees/", views.Employees.as_view()),
    # path("employee/<int:emp_id>/", views.EmployeeDetails.as_view()),

    # Includeing routers
    path("", include(router.urls)),

    path("blogs/", views.BlogsView.as_view()),
    path("comments/", views.CommentsView.as_view()),

    path("blogs/<int:pk>/", views.BlogDetailView.as_view()),
    path("comments/<int:pk>/", views.CommentDetailView.as_view()),
]