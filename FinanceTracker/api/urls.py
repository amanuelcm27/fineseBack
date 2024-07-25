from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView,
)

from .views import MyTokenObtainPairView
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("",views.getRoutes),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("register/",views.register,name="register"),
    path("set_goal/",GoalCreateView.as_view(), name='set_goal'),
    path("list_category/",CategoryListView.as_view(),name="list_category"),
    path("create_category/",CategoryListView.as_view(),name="create_category"),
    path("list_expense/",ExpenseListView.as_view(),name="list_expense"),
    path("create_expense/",ExpenseListView.as_view(),name="create_expense"),
    path("thismonth/",CurrentMonthExpenseView.as_view(),name="this_month"),
    path("update_expense/<int:pk>/",UpdateExpenseView.as_view(),name="update_expense"),
    path("delete_expense/<int:pk>/",DeleteExpenseView.as_view(),name="delete_expense"),
    path("goal_stat/",GoalListApiView.as_view(),name="goal_stat"),
    path("update_goal/<int:pk>/",UpdateGoalView.as_view(),name="update_goal"),
    path("average_stat/<int:year>/",AveragesListView.as_view(),name="average_stat"),
    path("achievement/",AchievementView.as_view(),name="achievement"),
    path("suggestion/",SuggestionView.as_view(),name="suggestion"),
    path("filtered_list/",FilteredListView.as_view(),name="filtered_list")



]