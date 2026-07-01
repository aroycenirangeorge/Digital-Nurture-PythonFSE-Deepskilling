# ==========================================================
# Task 1: Understanding Django Request-Response Cycle
# ==========================================================


# 1. How does a GET /api/courses/ request work?

# Step 1:
# A user enters http://localhost:8000/api/courses/
# in the browser.

# Step 2:
# Django checks urls.py to find which view should
# handle this URL.

# Step 3:
# The matched view function in views.py is called.

# Step 4:
# The view asks the model for course data.
# Example:
# courses = Course.objects.all()

# Step 5:
# The model gets the data from the database.

# Step 6:
# The view sends the data back as a response
# (JSON or HTML).

# Step 7:
# The browser receives the response and displays it.



# ----------------------------------------------------------
# Implementation
# ----------------------------------------------------------

# urls.py
# path("api/courses/", views.course_list)

# views.py
# def course_list(request):
#     courses = Course.objects.all()
#     return JsonResponse(list(courses.values()), safe=False)

# models.py
# class Course(models.Model):
#     name = models.CharField(max_length=100)



# ==========================================================
# 2. Middleware
# ==========================================================

# Middleware is like a security guard.
# Every request passes through it before reaching the view.
# Every response also passes through it before reaching the browser.

# Example 1: AuthenticationMiddleware
# Checks who the logged-in user is.

# Example 2: SessionMiddleware
# Stores user session data like login information.



# ==========================================================
# 3. WSGI vs ASGI
# ==========================================================

# WSGI
# - Works one request at a time.
# - Best for normal websites.
# - Django uses this by default.

# ASGI
# - Can handle many requests at once.
# - Supports WebSockets and real-time apps.
# - Used for chat apps, live notifications, etc.

# Use WSGI:
# Normal websites and CRUD applications.

# Use ASGI:
# Chat applications, live updates, and real-time projects.



# ==========================================================
# 4. MVC vs Django MVT
# ==========================================================

# MVC
# Model -> Database
# View -> User Interface
# Controller -> Handles requests

# Django MVT

# Model
# Stores and retrieves data.

# View
# Handles requests and business logic.
# (Acts like the Controller in MVC.)

# Template
# Displays HTML to the user.
# (Acts like the View in MVC.)

# Mapping

# MVC Model      -> Django Model
# MVC View       -> Django Template
# MVC Controller -> Django View