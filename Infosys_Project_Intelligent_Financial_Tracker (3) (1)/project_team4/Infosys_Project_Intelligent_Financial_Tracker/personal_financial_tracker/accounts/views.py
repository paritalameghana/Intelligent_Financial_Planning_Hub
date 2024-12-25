# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# from django.contrib import messages
# from .forms import UserRegistrationForm, ExpenseForm
# from .models import Expense
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.messages import get_messages
# from django.db.models import Sum
# import json
# from django.middleware import csrf as CsrfViewMiddleware

# # Helper function to clear stale messages
# def clear_stale_messages(request):
#     storage = get_messages(request)
#     for _ in storage:
#         pass

# def home(request):
#     return render(request, 'accounts/home.html')

# @login_required
# def profile(request):
#     if request.GET.get('first_login'):
#         messages.success(request, f"Welcome once more!, {request.user.username}!")
#     return render(request, 'accounts/profile.html')

# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             messages.success(request, 'Registration successful! Please log in.')
#             return redirect('login')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'accounts/register.html', {'form': form})

# def login_view(request):
#     clear_stale_messages(request)

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         try:
#             if not User.objects.filter(username=username).exists():
#                 messages.error(request, 'Username is incorrect. Please try again.')
#                 return render(request, 'accounts/login.html')

#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, f'Welcome back, {user.username}!')
#                 return redirect('/profile?first_login=true')
#             else:
#                 messages.error(request, 'Password is incorrect. Please try again.')

#         except CsrfViewMiddleware.CsrfTokenMissing:
#             messages.error(request, 'Something went wrong. Please refresh the page and try again.')

#     return render(request, 'accounts/login.html')

# @login_required
# def add_expenses(request):
#     if request.method == 'POST':
#         form = ExpenseForm(request.POST)
#         if form.is_valid():
#             expense = form.save(commit=False)
#             expense.user = request.user
#             expense.save()
#             messages.success(request, 'Expense added successfully!')
#             return redirect('add_expenses')
#     else:
#         form = ExpenseForm()

#     return render(request, 'accounts/add_expenses.html', {'form': form})

# @login_required
# def view_expenses(request):
#     clear_stale_messages(request)

#     expenses = Expense.objects.filter(user=request.user)
#     return render(request, 'accounts/view_expenses.html', {'expenses': expenses})

# @login_required
# def financial_reports(request):
#     # Filter expenses for the logged-in user
#     user_expenses = Expense.objects.filter(user=request.user)

#     # Aggregate total amounts per category
#     expenses_by_category = user_expenses.values('category').annotate(total=Sum('amount'))

#     # Extract categories and amounts
#     categories = []
#     amounts = []

#     for expense in expenses_by_category:
#         category = expense['category']
#         total = expense['total']

#         # Include all valid categories; handle "Others" separately
#         if category in ['Food', 'Utilities', 'Entertainment', 'Others']:
#             categories.append(category)
#             amounts.append(float(total))  # Convert Decimal to float

#     # Calculate totals and averages
#     total_expense = user_expenses.aggregate(Sum('amount'))['amount__sum'] or 0

#     # Get the count of unique dates
#     distinct_dates = user_expenses.values('date').distinct().count()

#     # Calculate average as sum of amounts / number of unique dates
#     average_daily_expense = total_expense / distinct_dates if distinct_dates > 0 else 0

#     context = {
#         'categories': json.dumps(categories),  # Serialize categories for JavaScript
#         'amounts': json.dumps(amounts),        # Serialize amounts for JavaScript
#         'total_expense': total_expense,
#         'average_daily_expense': average_daily_expense,
#     }
#     return render(request, 'accounts/financial_reports.html', context)

# @login_required
# def edit_expense(request, expense_id):
#     expense = get_object_or_404(Expense, id=expense_id, user=request.user)

#     if request.method == 'POST':
#         form = ExpenseForm(request.POST, instance=expense)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Expense updated successfully!")
#             return redirect('view_expenses')
#     else:
#         form = ExpenseForm(instance=expense)

#     return render(request, 'accounts/edit_expense.html', {'form': form, 'expense': expense})

# @login_required
# @csrf_exempt
# def delete_expense(request, expense_id):
#     try:
#         expense = Expense.objects.get(id=expense_id, user=request.user)
#         expense.delete()
#         return JsonResponse({"success": True}, status=200)
#     except Expense.DoesNotExist:
#         return JsonResponse({"success": False, "error": "Expense not found"}, status=404)





# from django.shortcuts import get_object_or_404, redirect
# from django.http import JsonResponse
# from django.contrib import messages

# @login_required
# def delete_expense(request, expense_id):
#     """
#     Deletes an expense entry if it belongs to the logged-in user.
#     """
#     try:
#         expense = get_object_or_404(Expense, id=expense_id, user=request.user)

#         if request.method == 'POST':
#             expense.delete()
#             if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                 return JsonResponse({'success': True, 'message': 'Expense deleted successfully!'}, status=200)
#             messages.success(request, 'Expense deleted successfully!')
#             return redirect('view_expenses')

#         return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)
#     except Expense.DoesNotExist:
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             return JsonResponse({'success': False, 'error': 'Expense not found.'}, status=404)
#         messages.error(request, 'Expense not found.')
#         return redirect('view_expenses')




# @login_required
# def view_expenses(request):
#     """
#     Displays a list of expenses for the logged-in user.
#     """
#     expenses = Expense.objects.filter(user=request.user)
#     return render(request, 'accounts/view_expenses.html', {'expenses': expenses})



# from django.contrib import messages

# @login_required
# def edit_expense(request, expense_id):
#     expense = get_object_or_404(Expense, id=expense_id, user=request.user)

#     if request.method == 'POST':
#         form = ExpenseForm(request.POST, instance=expense)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Expense updated successfully!")
#             return redirect('view_expenses')  # Redirect to view expenses page after updating
#     else:
#         form = ExpenseForm(instance=expense)

#     return render(request, 'accounts/edit_expense.html', {'form': form, 'expense': expense})



# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required

# @login_required
# def financial_dashboard(request):
#     """
#     View to display the financial dashboard with key metrics and charts.
#     """
#     # Example data (replace with real data from your database)
#     categories = ['Food', 'Utilities', 'Other']
#     amounts = [300, 200, 100]  # Corresponding amounts for each category
#     total_expense = sum(amounts)
#     average_daily_expense = total_expense / 30  # Example: Average for a month

#     context = {
#         'categories': categories,
#         'amounts': amounts,
#         'total_expense': total_expense,
#         'average_daily_expense': average_daily_expense,
#     }
#     return render(request, 'accounts/financial_dashboard.html', context)




# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.db.models import Sum
# import json

# @login_required
# def financial_dashboard(request):
#     """
#     View to display the financial dashboard with key metrics and charts.
#     """
#     # Fetch user expenses
#     user_expenses = Expense.objects.filter(user=request.user)

#     # Aggregate data for charts
#     expenses_by_category = user_expenses.values('category').annotate(total=Sum('amount'))
#     categories = [item['category'] for item in expenses_by_category]
#     amounts = [float(item['total']) for item in expenses_by_category]

#     # Total budget and total expenses
#     total_budget = 10000  # Example budget (replace with user-specific budget if available)
#     total_expenses = user_expenses.aggregate(total=Sum('amount'))['total'] or 0

#     # Latest transactions (limit to last 5)
#     latest_expenses = user_expenses.order_by('-date')[:5]

#     context = {
#         'categories': json.dumps(categories),  # Pass JSON-serialized data for JavaScript
#         'amounts': json.dumps(amounts),        # Pass JSON-serialized data for JavaScript
#         'total_budget': total_budget,
#         'total_expenses': total_expenses,
#         'latest_expenses': latest_expenses,
#     }
#     return render(request, 'accounts/financial_dashboard.html', context)










# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .forms import BudgetForm
# from .models import UserProfile

# @login_required
# def update_budget(request):
#     profile, created = UserProfile.objects.get_or_create(user=request.user)
#     if request.method == 'POST':
#         form = BudgetForm(request.POST, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('financial_dashboard')  # Redirect to the dashboard after saving
#     else:
#         form = BudgetForm(instance=profile)
    
#     return render(request, 'accounts/update_budget.html', {'form': form})







# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.db.models import Sum
# import json
# from .models import Expense, UserProfile

# @login_required
# def financial_dashboard(request):
#     # Fetch user expenses
#     user_expenses = Expense.objects.filter(user=request.user)

#     # Aggregate data for charts
#     expenses_by_category = user_expenses.values('category').annotate(total=Sum('amount'))
#     categories = [item['category'] for item in expenses_by_category]
#     amounts = [float(item['total']) for item in expenses_by_category]

#     # Fetch user's budget
#     profile, created = UserProfile.objects.get_or_create(user=request.user)
#     total_budget = profile.total_budget

#     # Total expenses
#     total_expenses = user_expenses.aggregate(total=Sum('amount'))['total'] or 0

#     # Latest transactions (limit to last 5)
#     latest_expenses = user_expenses.order_by('-date')[:5]

#     context = {
#         'categories': json.dumps(categories),  # Pass JSON-serialized data for JavaScript
#         'amounts': json.dumps(amounts),        # Pass JSON-serialized data for JavaScript
#         'total_budget': total_budget,
#         'total_expenses': total_expenses,
#         'latest_expenses': latest_expenses,
#     }
#     return render(request, 'accounts/financial_dashboard.html', context)







# # from django.contrib import messages
# # from django.shortcuts import render, redirect, get_object_or_404
# # from .models import Expense
# # from .forms import ExpenseForm
# # from django.contrib.auth.decorators import login_required

# # @login_required
# # def edit_expense(request, expense_id):
# #     expense = get_object_or_404(Expense, id=expense_id, user=request.user)

# #     if request.method == 'POST':
# #         form = ExpenseForm(request.POST, instance=expense)
# #         if form.is_valid():
# #             form.save()
# #             messages.success(request, "Expense updated successfully!")
# #             return redirect('view_expenses')  # Redirect back to the list of expenses
# #     else:
# #         form = ExpenseForm(instance=expense)

# #     return render(request, 'edit_expense.html', {'form': form, 'expense': expense})







# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.contrib.auth import update_session_auth_hash

# @login_required
# def change_password(request):
#     if request.method == 'POST':
#         old_password = request.POST.get('old_password')
#         new_password = request.POST.get('new_password')
#         confirm_password = request.POST.get('confirm_password')

#         if not request.user.check_password(old_password):
#             messages.error(request, 'The current password is incorrect.')
#         elif new_password != confirm_password:
#             messages.error(request, 'The new passwords do not match.')
#         else:
#             request.user.set_password(new_password)
#             request.user.save()
#             update_session_auth_hash(request, request.user)  # Keeps the user logged in
#             messages.success(request, 'Password updated successfully.')
#             return redirect('profile')

#     return render(request, 'accounts/change_password.html')





# # from django.shortcuts import render, redirect
# # from django.contrib.auth.decorators import login_required
# # from django.contrib.auth.models import User
# # from django.contrib import messages

# # @login_required
# # def edit_username(request):
# #     if request.method == 'POST':
# #         new_username = request.POST.get('username')
# #         if User.objects.filter(username=new_username).exists():
# #             messages.error(request, 'This username is already taken.')
# #         else:
# #             request.user.username = new_username
# #             request.user.save()
# #             messages.success(request, 'Username updated successfully.')
# #             return redirect('profile')

# #     return render(request, 'accounts/edit_username.html', {'user': request.user})

















# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.db import IntegrityError

# @login_required
# def edit_username(request):
#     if request.method == 'POST':
#         new_username = request.POST.get('username')
#         if not new_username:
#             messages.error(request, 'Username cannot be empty.')
#             return redirect('edit_username')  # Redirect back to the form if username is empty
        
#         try:
#             # Update username if it does not already exist
#             request.user.username = new_username
#             request.user.save()
#             messages.success(request, 'Username updated successfully.')
#             return redirect('profile')  # Redirect to the profile page after successful update
#         except IntegrityError:
#             messages.error(request, 'This username is already taken.')
#             return redirect('edit_username')  # Redirect back to the form if username exists
    
#     # Render the edit username template with the current user
#     return render(request, 'accounts/edit_username.html', {'user': request.user})
















from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .forms import UserRegistrationForm, ExpenseForm, BudgetForm
from .models import Expense, UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages import get_messages
from django.db.models import Sum
from django.contrib.auth import update_session_auth_hash
import json
from django.db import IntegrityError

# Helper function to clear stale messages
def clear_stale_messages(request):
    storage = get_messages(request)
    for _ in storage:
        pass

def home(request):
    return render(request, 'accounts/home.html')

@login_required
def profile(request):
    if request.GET.get('first_login'):
        messages.success(request, f"Welcome back, {request.user.username}!")
    return render(request, 'accounts/profile.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
           # Check if Profile already exists, if not, create one
            if not hasattr(user, 'profile'):
                profile.objects.create(user=user)

            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    # Clear stale messages
    clear_stale_messages(request)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Check if username exists
            if not User.objects.filter(username=username).exists():
                messages.error(request, 'Username is incorrect. Please try again.')
                return render(request, 'accounts/login.html')

            # Authenticate user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Login the user
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('/profile?first_login=true')  # Redirect to profile page after login
            else:
                messages.error(request, 'Password is incorrect. Please try again.')

        except Exception as e:
            messages.error(request, 'Something went wrong. Please refresh the page and try again.')
            print(f"Error: {e}")

    return render(request, 'accounts/login.html')

@login_required
def add_expenses(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('add_expenses')
    else:
        form = ExpenseForm()

    return render(request, 'accounts/add_expenses.html', {'form': form})

@login_required
def view_expenses(request):
    clear_stale_messages(request)

    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'accounts/view_expenses.html', {'expenses': expenses})

@login_required
def financial_reports(request):
    user_expenses = Expense.objects.filter(user=request.user)

    expenses_by_category = user_expenses.values('category').annotate(total=Sum('amount'))

    categories = []
    amounts = []

    for expense in expenses_by_category:
        category = expense['category']
        total = expense['total']

        if category in ['Food', 'Utilities', 'Entertainment', 'Others']:
            categories.append(category)
            amounts.append(float(total))

    total_expense = user_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    distinct_dates = user_expenses.values('date').distinct().count()
    average_daily_expense = total_expense / distinct_dates if distinct_dates > 0 else 0

    context = {
        'categories': json.dumps(categories),
        'amounts': json.dumps(amounts),
        'total_expense': total_expense,
        'average_daily_expense': average_daily_expense,
    }
    return render(request, 'accounts/financial_reports.html', context)

@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated successfully!")
            return redirect('view_expenses')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'accounts/edit_expense.html', {'form': form, 'expense': expense})

@login_required
@csrf_exempt
def delete_expense(request, expense_id):
    try:
        expense = Expense.objects.get(id=expense_id, user=request.user)
        if request.method == 'POST':
            expense.delete()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Expense deleted successfully!'}, status=200)
            messages.success(request, 'Expense deleted successfully!')
            return redirect('view_expenses')
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)
    except Expense.DoesNotExist:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Expense not found.'}, status=404)
        messages.error(request, 'The expense you are trying to delete was not found.')
        return redirect('view_expenses')

@login_required
def financial_dashboard(request):
    user_expenses = Expense.objects.filter(user=request.user)

    expenses_by_category = user_expenses.values('category').annotate(total=Sum('amount'))
    categories = [item['category'] for item in expenses_by_category]
    amounts = [float(item['total']) for item in expenses_by_category]

    profile, created = UserProfile.objects.get_or_create(user=request.user)
    total_budget = profile.total_budget

    total_expenses = user_expenses.aggregate(total=Sum('amount'))['total'] or 0

    latest_expenses = user_expenses.order_by('-date')[:5]

    context = {
        'categories': json.dumps(categories),
        'amounts': json.dumps(amounts),
        'total_budget': total_budget,
        'total_expenses': total_expenses,
        'latest_expenses': latest_expenses,
    }
    return render(request, 'accounts/financial_dashboard.html', context)

@login_required
def update_budget(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Budget updated successfully!')
            return redirect('financial_dashboard')
    else:
        form = BudgetForm(instance=profile)

    return render(request, 'accounts/update_budget.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(old_password):
            messages.error(request, 'The current password you entered is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, 'The new passwords do not match. Please try again.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Your password has been updated successfully.')
            return redirect('profile')

    return render(request, 'accounts/change_password.html')

@login_required
def edit_username(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')
        if not new_username:
            messages.error(request, 'Username cannot be empty. Please provide a valid username.')
            return redirect('edit_username')

        try:
            request.user.username = new_username
            request.user.save()
            messages.success(request, 'Your username has been updated successfully.')
            return redirect('profile')
        except IntegrityError:
            messages.error(request, 'The username you entered is already taken. Please choose a different one.')
            return redirect('edit_username')

    return render(request, 'accounts/edit_username.html', {'user': request.user})






from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

@login_required
def change_password(request):
    """
    Handles the change password functionality.
    """
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'The passwords do not match. Please try again.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Keeps the user logged in after password change
            messages.success(request, 'Your password has been updated successfully.')
            return redirect('profile')

    return render(request, 'accounts/change_password.html')



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from .forms import BudgetForm

@login_required
def set_budget(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your monthly budget has been updated successfully!')
            return redirect('profile')  # Redirect to profile after saving
    else:
        form = BudgetForm(instance=profile)

    return render(request, 'accounts/set_budget.html', {'form': form})












# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
# from django.http import JsonResponse
# from django.contrib import messages
# from .forms import UserRegistrationForm, ExpenseForm
# from .models import Expense
# from django.views.decorators.csrf import csrf_exempt
# from django.contrib.messages import get_messages
# from django.db.models import Sum
# import json
# from django.middleware import csrf as CsrfViewMiddleware

# # Helper function to clear stale messages
# def clear_stale_messages(request):
#     storage = get_messages(request)
#     for _ in storage:
#         pass

# def home(request):
#     return render(request, 'accounts/home.html')

# @login_required
# def profile(request):
#     if request.GET.get('first_login'):
#         messages.success(request, f"Welcome once more!, {request.user.username}!")
#     return render(request, 'accounts/profile.html')

# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             messages.success(request, 'Registration successful! Please log in.')
#             return redirect('login')
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'accounts/register.html', {'form': form})

# def login_view(request):
#     clear_stale_messages(request)

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         try:
#             if not User.objects.filter(username=username).exists():
#                 messages.error(request, 'Username is incorrect. Please try again.')
#                 return render(request, 'accounts/login.html')

#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 messages.success(request, f'Welcome back, {user.username}!')
#                 return redirect('/profile?first_login=true')
#             else:
#                 messages.error(request, 'Password is incorrect. Please try again.')

#         except CsrfViewMiddleware.CsrfTokenMissing:
#             messages.error(request, 'Something went wrong. Please refresh the page and try again.')

#     return render(request, 'accounts/login.html')

# @login_required
# def add_expenses(request):
#     if request.method == 'POST':
#         form = ExpenseForm(request.POST)
#         if form.is_valid():
#             expense = form.save(commit=False)
#             expense.user = request.user
#             expense.save()
#             messages.success(request, 'Expense added successfully!')
#             return redirect('add_expenses')
#     else:
#         form = ExpenseForm()

#     return render(request, 'accounts/add_expenses.html', {'form': form})

# @login_required
# def view_expenses(request):
#     clear_stale_messages(request)

#     expenses = Expense.objects.filter(user=request.user)
#     return render(request, 'accounts/view_expenses.html', {'expenses': expenses})

# @login_required
# def financial_reports(request):
#     # Filter expenses for the logged-in user
#     user_expenses = Expense.objects.filter(user=request.user)

#     # Aggregate total amounts per category
#     expenses_by_category = user_expenses.values('category').annotate(total=Sum('amount'))

#     # Extract categories and amounts
#     categories = []
#     amounts = []

#     for expense in expenses_by_category:
#         category = expense['category']
#         total = expense['total']

#         # Include all valid categories; handle "Others" separately
#         if category in ['Food', 'Utilities', 'Entertainment', 'Others']:
#             categories.append(category)
#             amounts.append(float(total))  # Convert Decimal to float

#     # Calculate totals and averages
#     total_expense = user_expenses.aggregate(Sum('amount'))['amount__sum'] or 0

#     # Get the count of unique dates
#     distinct_dates = user_expenses.values('date').distinct().count()

#     # Calculate average as sum of amounts / number of unique dates
#     average_daily_expense = total_expense / distinct_dates if distinct_dates > 0 else 0

#     context = {
#         'categories': json.dumps(categories),  # Serialize categories for JavaScript
#         'amounts': json.dumps(amounts),        # Serialize amounts for JavaScript
#         'total_expense': total_expense,
#         'average_daily_expense': average_daily_expense,
#     }
#     return render(request, 'accounts/financial_reports.html', context)

# @login_required
# def edit_expense(request, expense_id):
#     expense = get_object_or_404(Expense, id=expense_id, user=request.user)

#     if request.method == 'POST':
#         form = ExpenseForm(request.POST, instance=expense)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Expense updated successfully!")
#             return redirect('view_expenses')
#     else:
#         form = ExpenseForm(instance=expense)

#     return render(request, 'accounts/edit_expense.html', {'form': form, 'expense': expense})

# @login_required
# @csrf_exempt
# def delete_expense(request, expense_id):
#     try:
#         expense = Expense.objects.get(id=expense_id, user=request.user)
#         expense.delete()
#         return JsonResponse({"success": True}, status=200)
#     except Expense.DoesNotExist:
#         return JsonResponse({"success": False, "error": "Expense not found"}, status=404)





# from django.shortcuts import get_object_or_404, redirect
# from django.http import JsonResponse
# from django.contrib import messages

# @login_required
# def delete_expense(request, expense_id):
#     """
#     Deletes an expense entry if it belongs to the logged-in user.
#     """
#     try:
#         expense = get_object_or_404(Expense, id=expense_id, user=request.user)

#         if request.method == 'POST':
#             expense.delete()
#             if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#                 return JsonResponse({'success': True, 'message': 'Expense deleted successfully!'}, status=200)
#             messages.success(request, 'Expense deleted successfully!')
#             return redirect('view_expenses')

#         return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)
#     except Expense.DoesNotExist:
#         if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#             return JsonResponse({'success': False, 'error': 'Expense not found.'}, status=404)
#         messages.error(request, 'Expense not found.')
#         return redirect('view_expenses')




# @login_required
# def view_expenses(request):
#     """
#     Displays a list of expenses for the logged-in user.
#     """
#     expenses = Expense.objects.filter(user=request.user)
#     return render(request, 'accounts/view_expenses.html', {'expenses': expenses})



# from django.contrib import messages

# @login_required
# def edit_expense(request, expense_id):
#     expense = get_object_or_404(Expense, id=expense_id, user=request.user)

#     if request.method == 'POST':
#         form = ExpenseForm(request.POST, instance=expense)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Expense updated successfully!")
#             return redirect('view_expenses')  # Redirect to view expenses page after updating
#     else:
#         form = ExpenseForm(instance=expense)

#     return render(request, 'accounts/edit_expense.html', {'form': form, 'expense': expense})



# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required

# @login_required
# def financial_dashboard(request):
#     """
#     View to display the financial dashboard with key metrics and charts.
#     """
#     # Example data (replace with real data from your database)
#     categories = ['Food', 'Utilities', 'Other']
#     amounts = [300, 200, 100]  # Corresponding amounts for each category
#     total_expense = sum(amounts)
#     average_daily_expense = total_expense / 30  # Example: Average for a month

#     context = {
#         'categories': categories,
#         'amounts': amounts,
#         'total_expense': total_expense,
#         'average_daily_expense': average_daily_expense,
#     }
#     return render(request, 'accounts/financial_dashboard.html', context)




# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.db.models import Sum
# import json

# @login_required
# def financial_dashboard(request):
#     """
#     View to display the financial dashboard with key metrics and charts.
#     """
#     # Fetch user expenses
#     user_expenses = Expense.objects.filter(user=request.user)

#     # Aggregate data for charts
#     expenses_by_category = user_expenses.values('category').annotate(total=Sum('amount'))
#     categories = [item['category'] for item in expenses_by_category]
#     amounts = [float(item['total']) for item in expenses_by_category]

#     # Total budget and total expenses
#     total_budget = 10000  # Example budget (replace with user-specific budget if available)
#     total_expenses = user_expenses.aggregate(total=Sum('amount'))['total'] or 0

#     # Latest transactions (limit to last 5)
#     latest_expenses = user_expenses.order_by('-date')[:5]

#     context = {
#         'categories': json.dumps(categories),  # Pass JSON-serialized data for JavaScript
#         'amounts': json.dumps(amounts),        # Pass JSON-serialized data for JavaScript
#         'total_budget': total_budget,
#         'total_expenses': total_expenses,
#         'latest_expenses': latest_expenses,
#     }
#     return render(request, 'accounts/financial_dashboard.html', context)










# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .forms import BudgetForm
# from .models import UserProfile

# @login_required
# def update_budget(request):
#     profile, created = UserProfile.objects.get_or_create(user=request.user)
#     if request.method == 'POST':
#         form = BudgetForm(request.POST, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('financial_dashboard')  # Redirect to the dashboard after saving
#     else:
#         form = BudgetForm(instance=profile)
    
#     return render(request, 'accounts/update_budget.html', {'form': form})







# from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.db.models import Sum
# import json
# from .models import Expense, UserProfile

# @login_required
# def financial_dashboard(request):
#     # Fetch user expenses
#     user_expenses = Expense.objects.filter(user=request.user)

#     # Aggregate data for charts
#     expenses_by_category = user_expenses.values('category').annotate(total=Sum('amount'))
#     categories = [item['category'] for item in expenses_by_category]
#     amounts = [float(item['total']) for item in expenses_by_category]

#     # Fetch user's budget
#     profile, created = UserProfile.objects.get_or_create(user=request.user)
#     total_budget = profile.total_budget

#     # Total expenses
#     total_expenses = user_expenses.aggregate(total=Sum('amount'))['total'] or 0

#     # Latest transactions (limit to last 5)
#     latest_expenses = user_expenses.order_by('-date')[:5]

#     context = {
#         'categories': json.dumps(categories),  # Pass JSON-serialized data for JavaScript
#         'amounts': json.dumps(amounts),        # Pass JSON-serialized data for JavaScript
#         'total_budget': total_budget,
#         'total_expenses': total_expenses,
#         'latest_expenses': latest_expenses,
#     }
#     return render(request, 'accounts/financial_dashboard.html', context)







# # from django.contrib import messages
# # from django.shortcuts import render, redirect, get_object_or_404
# # from .models import Expense
# # from .forms import ExpenseForm
# # from django.contrib.auth.decorators import login_required

# # @login_required
# # def edit_expense(request, expense_id):
# #     expense = get_object_or_404(Expense, id=expense_id, user=request.user)

# #     if request.method == 'POST':
# #         form = ExpenseForm(request.POST, instance=expense)
# #         if form.is_valid():
# #             form.save()
# #             messages.success(request, "Expense updated successfully!")
# #             return redirect('view_expenses')  # Redirect back to the list of expenses
# #     else:
# #         form = ExpenseForm(instance=expense)

# #     return render(request, 'edit_expense.html', {'form': form, 'expense': expense})







# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.contrib.auth import update_session_auth_hash

# @login_required
# def change_password(request):
#     if request.method == 'POST':
#         old_password = request.POST.get('old_password')
#         new_password = request.POST.get('new_password')
#         confirm_password = request.POST.get('confirm_password')

#         if not request.user.check_password(old_password):
#             messages.error(request, 'The current password is incorrect.')
#         elif new_password != confirm_password:
#             messages.error(request, 'The new passwords do not match.')
#         else:
#             request.user.set_password(new_password)
#             request.user.save()
#             update_session_auth_hash(request, request.user)  # Keeps the user logged in
#             messages.success(request, 'Password updated successfully.')
#             return redirect('profile')

#     return render(request, 'accounts/change_password.html')





# # from django.shortcuts import render, redirect
# # from django.contrib.auth.decorators import login_required
# # from django.contrib.auth.models import User
# # from django.contrib import messages

# # @login_required
# # def edit_username(request):
# #     if request.method == 'POST':
# #         new_username = request.POST.get('username')
# #         if User.objects.filter(username=new_username).exists():
# #             messages.error(request, 'This username is already taken.')
# #         else:
# #             request.user.username = new_username
# #             request.user.save()
# #             messages.success(request, 'Username updated successfully.')
# #             return redirect('profile')

# #     return render(request, 'accounts/edit_username.html', {'user': request.user})

















# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.db import IntegrityError

# @login_required
# def edit_username(request):
#     if request.method == 'POST':
#         new_username = request.POST.get('username')
#         if not new_username:
#             messages.error(request, 'Username cannot be empty.')
#             return redirect('edit_username')  # Redirect back to the form if username is empty
        
#         try:
#             # Update username if it does not already exist
#             request.user.username = new_username
#             request.user.save()
#             messages.success(request, 'Username updated successfully.')
#             return redirect('profile')  # Redirect to the profile page after successful update
#         except IntegrityError:
#             messages.error(request, 'This username is already taken.')
#             return redirect('edit_username')  # Redirect back to the form if username exists
    
#     # Render the edit username template with the current user
#     return render(request, 'accounts/edit_username.html', {'user': request.user})
















from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .forms import UserRegistrationForm, ExpenseForm, BudgetForm
from .models import Expense, UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.contrib.messages import get_messages
from django.db.models import Sum
from django.contrib.auth import update_session_auth_hash
import json
from django.db import IntegrityError

# Helper function to clear stale messages
def clear_stale_messages(request):
    storage = get_messages(request)
    for _ in storage:
        pass

def home(request):
    return render(request, 'accounts/home.html')

@login_required
def profile(request):
    if request.GET.get('first_login'):
        messages.success(request, f"Welcome back, {request.user.username}!")
    return render(request, 'accounts/profile.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
           # Check if Profile already exists, if not, create one
            if not hasattr(user, 'profile'):
                profile.objects.create(user=user)

            messages.success(request, 'Registration successful! Please log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    # Clear stale messages
    clear_stale_messages(request)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Check if username exists
            if not User.objects.filter(username=username).exists():
                messages.error(request, 'Username is incorrect. Please try again.')
                return render(request, 'accounts/login.html')

            # Authenticate user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Login the user
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('/profile?first_login=true')  # Redirect to profile page after login
            else:
                messages.error(request, 'Password is incorrect. Please try again.')

        except Exception as e:
            messages.error(request, 'Something went wrong. Please refresh the page and try again.')
            print(f"Error: {e}")

    return render(request, 'accounts/login.html')

@login_required
def add_expenses(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('add_expenses')
    else:
        form = ExpenseForm()

    return render(request, 'accounts/add_expenses.html', {'form': form})

@login_required
def view_expenses(request):
    clear_stale_messages(request)

    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'accounts/view_expenses.html', {'expenses': expenses})

@login_required
def financial_reports(request):
    user_expenses = Expense.objects.filter(user=request.user)

    expenses_by_category = user_expenses.values('category').annotate(total=Sum('amount'))

    categories = []
    amounts = []

    for expense in expenses_by_category:
        category = expense['category']
        total = expense['total']

        if category in ['Food', 'Utilities', 'Entertainment', 'Others']:
            categories.append(category)
            amounts.append(float(total))

    total_expense = user_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    distinct_dates = user_expenses.values('date').distinct().count()
    average_daily_expense = total_expense / distinct_dates if distinct_dates > 0 else 0

    context = {
        'categories': json.dumps(categories),
        'amounts': json.dumps(amounts),
        'total_expense': total_expense,
        'average_daily_expense': average_daily_expense,
    }
    return render(request, 'accounts/financial_reports.html', context)

@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated successfully!")
            return redirect('view_expenses')
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'accounts/edit_expense.html', {'form': form, 'expense': expense})

@login_required
@csrf_exempt
def delete_expense(request, expense_id):
    try:
        expense = Expense.objects.get(id=expense_id, user=request.user)
        if request.method == 'POST':
            expense.delete()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': 'Expense deleted successfully!'}, status=200)
            messages.success(request, 'Expense deleted successfully!')
            return redirect('view_expenses')
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)
    except Expense.DoesNotExist:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'error': 'Expense not found.'}, status=404)
        messages.error(request, 'The expense you are trying to delete was not found.')
        return redirect('view_expenses')

@login_required
def financial_dashboard(request):
    user_expenses = Expense.objects.filter(user=request.user)

    expenses_by_category = user_expenses.values('category').annotate(total=Sum('amount'))
    categories = [item['category'] for item in expenses_by_category]
    amounts = [float(item['total']) for item in expenses_by_category]

    profile, created = UserProfile.objects.get_or_create(user=request.user)
    total_budget = profile.total_budget

    total_expenses = user_expenses.aggregate(total=Sum('amount'))['total'] or 0

    latest_expenses = user_expenses.order_by('-date')[:5]

    context = {
        'categories': json.dumps(categories),
        'amounts': json.dumps(amounts),
        'total_budget': total_budget,
        'total_expenses': total_expenses,
        'latest_expenses': latest_expenses,
    }
    return render(request, 'accounts/financial_dashboard.html', context)

# @login_required
# def update_budget(request):
#     profile, created = UserProfile.objects.get_or_create(user=request.user)
#     if request.method == 'POST':
#         form = BudgetForm(request.POST, instance=profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Budget updated successfully!')
#             return redirect('financial_dashboard')
#     else:
#         form = BudgetForm(instance=profile)

#     return render(request, 'accounts/update_budget.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(old_password):
            messages.error(request, 'The current password you entered is incorrect.')
        elif new_password != confirm_password:
            messages.error(request, 'The new passwords do not match. Please try again.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Your password has been updated successfully.')
            return redirect('profile')

    return render(request, 'accounts/change_password.html')

@login_required
def edit_username(request):
    if request.method == 'POST':
        new_username = request.POST.get('username')
        if not new_username:
            messages.error(request, 'Username cannot be empty. Please provide a valid username.')
            return redirect('edit_username')

        try:
            request.user.username = new_username
            request.user.save()
            messages.success(request, 'Your username has been updated successfully.')
            return redirect('profile')
        except IntegrityError:
            messages.error(request, 'The username you entered is already taken. Please choose a different one.')
            return redirect('edit_username')

    return render(request, 'accounts/edit_username.html', {'user': request.user})






from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

@login_required
def change_password(request):
    """
    Handles the change password functionality.
    """
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, 'The passwords do not match. Please try again.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)  # Keeps the user logged in after password change
            messages.success(request, 'Your password has been updated successfully.')
            return redirect('profile')

    return render(request, 'accounts/change_password.html')



# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .models import UserProfile
# from .forms import BudgetForm

# @login_required
# def set_budget(request):
#     profile, created = UserProfile.objects.get_or_create(user=request.user)
#     if request.method == 'POST':
#         form = BudgetForm(request.POST, instance=profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Your monthly budget has been updated successfully!')
#             return redirect('profile')  # Redirect to profile after saving
#     else:
#         form = BudgetForm(instance=profile)

#     return render(request, 'accounts/set_budget.html', {'form': form})


from django.contrib import messages
from django.shortcuts import render, redirect

def set_budget(request):
    if request.method == 'POST':
        # Logic to save the budget
        category = request.POST.get('category')
        budget = request.POST.get(f'{category}_budget')
        
        # Example: Save the budget in the database
        # Assuming you have a model like Budget with fields: category and amount
        # Budget.objects.create(category=category, amount=budget)
        
        # After saving, show a success message
        messages.success(request, f'Your {category} budget has been successfully set!')
        return redirect('set_budget')  # Redirect to the same page to show the message
     
    return render(request, 'accounts/set_budget.html')


# from django.shortcuts import render, redirect
# from .models import CategoryBudget

# def update_budget(request):
#     if request.method == 'POST':
#         category_name = request.POST.get('category_name')
#         new_amount = request.POST.get('new_amount')

#         # Find the category and update the amount
#         category = CategoryBudget.objects.get(name=category_name)
#         category.amount = new_amount
#         category.save()

#         # Recalculate the total budget
#         total_budget = CategoryBudget.objects.aggregate(models.Sum('amount'))['amount__sum']

#         # Store the updated total budget (can be stored in session or database)
#         request.session['total_budget'] = total_budget

#         return redirect('financial_dashboard')

#     categories = CategoryBudget.objects.all()
#     return render(request, 'update_budget.html', {'categories': categories})




# from django.shortcuts import render, redirect
# from django.db.models import Sum
# from .models import CategoryBudget

# def update_budget(request):
#     if request.method == 'POST':
#         category_name = request.POST.get('category')
#         new_amount = request.POST.get('budget_amount')

#         # Check if category exists
#         category, created = CategoryBudget.objects.get_or_create(name=category_name)

#         # Update the budget amount for the selected category
#         category.amount = new_amount
#         category.save()

#         # Recalculate the total budget
#         total_budget = CategoryBudget.objects.aggregate(Sum('amount'))['amount__sum']

#         # Store the updated total budget in session
#         request.session['total_budget'] = total_budget

#         return redirect('financial_dashboard')

#     categories = CategoryBudget.objects.all()
#     return render(request, 'update_budget.html', {'categories': categories})

# def financial_dashboard(request):
#     categories = CategoryBudget.objects.all()
#     total_expenses = sum([category.amount for category in categories])

#     # Get the total budget from session or default to zero
#     total_budget = request.session.get('total_budget', 0)

#     # Prepare category names and amounts for the charts
#     category_names = [category.name for category in categories]
#     amounts = [category.amount for category in categories]

#     return render(request, 'financial_dashboard.html', {
#         'total_expenses': total_expenses,
#         'total_budget': total_budget,
#         'categories': category_names,
#         'amounts': amounts,
#         'latest_expenses': categories[:5]  # Example: Get the latest 5 expenses
#     })












# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .models import Budget, Expense

# @login_required
# def update_budget(request):
#     if request.method == 'POST':
#         category = request.POST.get('category')
#         budget_amount = float(request.POST.get('budget_amount'))
        
#         # Update or create the budget for the selected category
#         budget, created = Budget.objects.update_or_create(
#             user=request.user,
#             category=category,
#             defaults={'amount': budget_amount},
#         )
#         return redirect('financial_dashboard')  # Redirect to the dashboard after updating
#     return render(request, 'update_budget.html')

# @login_required
# def financial_dashboard(request):
#     budgets = Budget.objects.filter(user=request.user)
#     expenses = Expense.objects.filter(user=request.user)
    
#     # Calculate total budget and total expenses
#     total_budget = sum(budget.amount for budget in budgets)
#     total_expenses = sum(expense.amount for expense in expenses)
    
#     # Group expenses by category
#     category_totals = expenses.values('category').annotate(total=models.Sum('amount'))
#     categories = [item['category'] for item in category_totals]
#     amounts = [item['total'] for item in category_totals]

#     context = {
#         'total_budget': total_budget,
#         'total_expenses': total_expenses,
#         'categories': categories,
#         'amounts': amounts,
#         'latest_expenses': expenses.order_by('-date')[:5],  # Fetch latest 5 expenses
#     }
#     return render(request, 'financial_dashboard.html', context)




# @login_required
# def update_budget(request):
#     profile, created = UserProfile.objects.get_or_create(user=request.user)
#     if request.method == 'POST':
#         form = BudgetForm(request.POST, instance=profile)
#         if form.is_valid():
#             form.save()
            
#             # Calculate updated total expenses
#             user_expenses = Expense.objects.filter(user=request.user)
#             total_expenses = user_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
            
#             # Update total_budget dynamically
#             profile.total_budget = form.cleaned_data['total_budget']
#             profile.save()
            
#             messages.success(request, 'Budget updated successfully!')
#             return redirect('financial_dashboard')
#     else:
#         form = BudgetForm(instance=profile)

#     return render(request, 'accounts/update_budget.html', {'form': form})


# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.db.models import Sum
# from .forms import BudgetForm
# from .models import Expense, UserProfile
# import json

# @login_required
# def update_budget(request):
#     profile, created = UserProfile.objects.get_or_create(user=request.user)
#     if request.method == 'POST':
#         form = BudgetForm(request.POST, instance=profile)
#         if form.is_valid():
#             # Retrieve the category and new budget amount
#             category = request.POST.get('category')
#             new_amount = float(request.POST.get('budget_amount'))

#             # Calculate the old amount for the specific category
#             old_amount = Expense.objects.filter(user=request.user, category=category).aggregate(Sum('amount'))['amount__sum'] or 0

#             # Update the total budget
#             profile.total_budget = profile.total_budget - old_amount + new_amount
#             profile.save()

#             # Update the category budget
#             Expense.objects.filter(user=request.user, category=category).update(amount=new_amount)

#             messages.success(request, 'Budget updated successfully!')
#             return redirect('financial_dashboard')
#     else:
#         form = BudgetForm(instance=profile)

#     return render(request, 'accounts/update_budget.html', {'form': form})

# @login_required
# def financial_dashboard(request):
#     user_expenses = Expense.objects.filter(user=request.user)
#     expenses_by_category = user_expenses.values('category').annotate(total=Sum('amount'))

#     categories = [item['category'] for item in expenses_by_category]
#     amounts = [float(item['total']) for item in expenses_by_category]

#     profile, created = UserProfile.objects.get_or_create(user=request.user)
#     total_budget = profile.total_budget

#     total_expenses = user_expenses.aggregate(total=Sum('amount'))['total'] or 0
#     remaining_budget = total_budget - total_expenses

#     latest_expenses = user_expenses.order_by('-date')[:5]

#     context = {
#         'categories': json.dumps(categories),
#         'amounts': json.dumps(amounts),
#         'total_budget': total_budget,
#         'total_expenses': total_expenses,
#         'remaining_budget': remaining_budget,
#         'latest_expenses': latest_expenses,
#     }
#     return render(request, 'accounts/financial_dashboard.html', context)


# from django.db.models import Sum
# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .models import UserProfile, Expense


# @login_required
# def update_budget(request):
#     # Fetch the user profile and current budget
#     profile, created = UserProfile.objects.get_or_cr