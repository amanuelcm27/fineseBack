
from django.utils.timezone import make_aware
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import *
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import generics, permissions
from django.utils import timezone
from django.db.models import F
from datetime import datetime
from django.utils.timezone import timedelta


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/token',
        '/api/token/refresh'
    ]
    return Response(routes)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(["POST"])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "Username and password are required."})

    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."})

    try:
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return Response({"success": "User created successfully", "user_id": user.id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(["POST"])
# def set_goal(request,user_pk):
#     income = request.data.get("income")
#     save = request.data.get("save")

#     if income is None or save is None :
#         return Response({"error": "Income and Save must be filled. "}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         user = User.objects.get(id=user_pk)
#     except User.DoesNotExist:
#         return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         income = float(income)
#         save = float(save)
#     except ValueError:
#         return Response({"error": "Invalid input for income or save"}, status=status.HTTP_400_BAD_REQUEST)

#     data = {"user_id": user.id, "income": income, "save": save}

#     # Debugging prints
#     print(f"Request Data: {request.data}")
#     print(f"Processed Data: {data}")

#     serializer = GoalSerializer(data=data)
#     print('exec 1')
#     if serializer.is_valid():
#         print("Serializer is valid")
#         serializer.save(user=user)
#         print('exec 2')

#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     else:
#         print("Serializer errors:", serializer.errors)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GoalCreateView(generics.CreateAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)


class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseListView (generics.ListCreateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).order_by("-date_created")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CurrentMonthExpenseView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        current_month = timezone.now().month
        user = request.user
        total_expense = Expense.objects.filter(user=user, date_created__month=current_month).aggregate(
            total_amount=models.Sum('amount'))['total_amount'] or 0

        return Response({"this_month_expense": total_expense})


class UpdateExpenseView(generics.UpdateAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)


class DeleteExpenseView (generics.DestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)


class GoalListApiView (generics.ListAPIView):
    serializer_class = GoalSerializer
    queryset = Goal.objects.all()

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)


class UpdateGoalView(generics.UpdateAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)


class AveragesListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        year = kwargs.get("year")
        print(year)
        if not year:
            return Response({"error": "Year field is required. "}, status=400)
        total_expense_year = Expense.objects.filter(user=user, date_created__year=year).aggregate(
            total_amount=models.Sum('amount'))['total_amount'] or 0
        avg_monthly = total_expense_year / 12
        avg_weekly = total_expense_year / 52
        avg_daily = total_expense_year / 365

        return Response({'avg_daily': avg_daily, 'avg_weekly': avg_weekly, 'avg_monthly': avg_monthly, 'yearly_expense': total_expense_year})


class AchievementView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        current_month = timezone.now().month
        this_month_expense = Expense.objects.filter(
            user=user, date_created__month=current_month).aggregate(
            total_amount=models.Sum('amount'))['total_amount'] or 0
        goal_list = list(Goal.objects.filter(
            user=user).values("income", "saving"))
        income = goal_list[0].get("income")
        goal = goal_list[0].get("saving")
        netIncome = income - this_month_expense
        percentage_spend = (this_month_expense / income) * \
            100 if netIncome else 0
        achieved = None
        saving = income * (goal / 100)
        if (netIncome <= 0):
            # means user is spending more than they earn
            achieved = False
        else:
            # means user is not spending more than they earn
            achieved = True if (netIncome > saving) else False

        return Response({"netIncome": netIncome, "current_income": income, "achieved": achieved, "percentage_spend": percentage_spend, "saving": saving, "this_month_expense": this_month_expense})


class SuggestionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        current_month = timezone.now().month
        user = self.request.user
        goal_data = Goal.objects.filter(
            user=user).values("income", "saving").first()
        if not goal_data:
            return Response({"error": "No goal data found."}, status=400)

        income = goal_data["income"]
        goal_percentage = goal_data["saving"]
        saving_goal = income * (goal_percentage / 100)

        this_month_expense = Expense.objects.filter(
            user=user, date_created__month=current_month).aggregate(
            total_amount=models.Sum('amount'))['total_amount'] or 0
        deficit = this_month_expense - income  # excess spending amount
        # the total reduction needed to cover the deficit and achieve the saving goal.
        total_reduction_needed = deficit + saving_goal
        spendable_income = income - saving_goal
        all_categories = list(
            Expense.objects.filter(
                user=user, date_created__month=current_month)
            .values(category_name=F("category__name"))
            .annotate(total_amount=models.Sum('amount'))
            .order_by('-total_amount'))
        top_3 = all_categories[:3]
        for category in all_categories:
            proportion = category["total_amount"] / this_month_expense
            reduction_needed = total_reduction_needed * proportion
            category["reduction_needed"] = reduction_needed
            print(category["total_amount"], proportion)

        return Response({"saving_goal": saving_goal, "all_categories": all_categories, "spendable_income": spendable_income, "top_3": top_3})


class FilteredListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        currentDay = timezone.now().day
        user = self.request.user
        day = request.data.get("day")
        month = request.data.get("month")
        year = request.data.get("year")
        order = request.data.get("order")
        category = request.data.get("category")

        if (category):
            category = Category.objects.get(user=user ,id=category.get("id"))
            expenses = Expense.objects.filter(
                category=category,
                user=user,
                date_created__day=day,
                date_created__month=month,
                date_created__year=year
            ).values().order_by("-amount" if order == "High-to-Low" else "amount")
        else:
            expenses = Expense.objects.filter(user=user,date_created__day = currentDay).values().order_by("-amount")

        print(f"Expenses: {list(expenses)}")

        return Response(list(expenses), status=200)
 