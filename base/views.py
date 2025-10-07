# base/views.py
# REPLACE ENTIRE FILE WITH THIS CODE

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db import IntegrityError
from django.db.models import Count, Avg, Q
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .models import Topic, Subtopic, Question, Quiz, QuizAnswer, PDFDocument

# ==================== AUTHENTICATION VIEWS ====================

def home(request):
    """Home page view"""
    return render(request, 'home.html')

def register_view(request):
    """User registration view"""
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        contact = request.POST.get('contact', '').strip()
        gender = request.POST.get('gender', '')
        
        if not all([first_name, last_name, email, password, confirm_password, contact, gender]):
            messages.error(request, 'All fields are required!')
            return render(request, 'register.html')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'register.html')
        
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long!')
            return render(request, 'register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered! Please use a different email.')
            return render(request, 'register.html')
        
        username = email.split('@')[0]
        
        if User.objects.filter(username=username).exists():
            counter = 1
            original_username = username
            while User.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            messages.success(request, f'Registration successful! Your username is: {username}')
            messages.success(request, 'Please login to continue.')
            return redirect('login')
            
        except IntegrityError as e:
            messages.error(request, f'Registration failed: {str(e)}')
            return render(request, 'register.html')
        
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'register.html')
    
    return render(request, 'register.html')

def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.is_staff:
            return redirect('admin_dashboard')
        else:
            return redirect('user_dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        
        if not email or not password:
            messages.error(request, 'Please enter both email and password!')
            return render(request, 'login.html')
        
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                if user.is_superuser or user.is_staff:
                    messages.success(request, f'Welcome Admin {user.first_name}!')
                    return redirect('admin_dashboard')
                else:
                    messages.success(request, f'Welcome {user.first_name}!')
                    return redirect('user_dashboard')
            else:
                messages.error(request, 'Invalid password!')
                return render(request, 'login.html')
        
        except User.DoesNotExist:
            messages.error(request, 'No account found with this email!')
            return render(request, 'login.html')
        
        except Exception as e:
            messages.error(request, f'Login failed: {str(e)}')
            return render(request, 'login.html')
    
    return render(request, 'login.html')

def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('home')

# base/views.py
# KEEP YOUR EXISTING login_view, register_view, home_view at the top
# ADD these new views below your existing code

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count, Avg, Q
from .models import Topic, Subtopic, Question, Quiz, QuizAnswer, PDFDocument
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

# === ADD THESE NEW FUNCTIONS BELOW YOUR EXISTING VIEWS ===

# Helper function to check if user is admin
def is_admin(user):
    return user.is_superuser or user.is_staff

# ==================== QUIZ TAKING VIEWS ====================

@login_required
def select_quiz(request):
    """Quiz selection page - choose topic, subtopic, difficulty"""
    topics = Topic.objects.all()
    
    context = {
        'topics': topics,
    }
    
    return render(request, 'select_quiz.html', context)

@login_required
def get_subtopics(request, topic_id):
    """AJAX endpoint to get subtopics for a topic"""
    from django.http import JsonResponse
    
    subtopics = Subtopic.objects.filter(topic_id=topic_id).values('id', 'name')
    return JsonResponse(list(subtopics), safe=False)

@login_required
def start_quiz(request):
    """Start a new quiz with selected parameters"""
    if request.method == 'POST':
        topic_id = request.POST.get('topic')
        subtopic_id = request.POST.get('subtopic')
        difficulty = request.POST.get('difficulty')
        num_questions = int(request.POST.get('num_questions', 10))
        
        # Validate inputs
        if not topic_id or not difficulty:
            messages.error(request, 'Please select topic and difficulty')
            return redirect('select_quiz')
        
        # Get questions
        questions = Question.objects.filter(
            topic_id=topic_id,
            difficulty=difficulty
        )
        
        if subtopic_id:
            questions = questions.filter(subtopic_id=subtopic_id)
        
        # Check if enough questions available
        if questions.count() < num_questions:
            messages.warning(request, f'Only {questions.count()} questions available. Starting quiz with available questions.')
            num_questions = questions.count()
        
        if questions.count() == 0:
            messages.error(request, 'No questions available for selected criteria')
            return redirect('select_quiz')
        
        # Randomly select questions
        import random
        questions_list = list(questions)
        random.shuffle(questions_list)
        selected_questions = questions_list[:num_questions]
        
        # Store quiz data in session
        request.session['quiz_data'] = {
            'topic_id': topic_id,
            'subtopic_id': subtopic_id,
            'difficulty': difficulty,
            'question_ids': [q.id for q in selected_questions],
            'current_index': 0,
            'answers': {},
            'start_time': timezone.now().isoformat()
        }
        
        return redirect('take_quiz')
    
    return redirect('select_quiz')

@login_required
def take_quiz(request):
    """Take quiz - display questions one by one"""
    quiz_data = request.session.get('quiz_data')
    
    if not quiz_data:
        messages.error(request, 'No active quiz found')
        return redirect('select_quiz')
    
    question_ids = quiz_data['question_ids']
    current_index = quiz_data['current_index']
    
    # Check if quiz is complete
    if current_index >= len(question_ids):
        return redirect('submit_quiz')
    
    # Get current question
    question = Question.objects.get(id=question_ids[current_index])
    
    # Get user's previous answer if they're navigating back
    user_answer = quiz_data['answers'].get(str(question.id))
    
    context = {
        'question': question,
        'current_number': current_index + 1,
        'total_questions': len(question_ids),
        'user_answer': user_answer,
        'progress_percentage': int((current_index / len(question_ids)) * 100)
    }
    
    return render(request, 'take_quiz.html', context)

@login_required
def save_answer(request):
    """Save answer and move to next question"""
    if request.method == 'POST':
        quiz_data = request.session.get('quiz_data')
        
        if not quiz_data:
            return redirect('select_quiz')
        
        question_id = request.POST.get('question_id')
        answer = request.POST.get('answer')
        
        # Save answer
        quiz_data['answers'][question_id] = answer
        
        # Move to next question
        quiz_data['current_index'] += 1
        
        request.session['quiz_data'] = quiz_data
        request.session.modified = True
        
        return redirect('take_quiz')
    
    return redirect('select_quiz')

@login_required
def previous_question(request):
    """Go back to previous question"""
    quiz_data = request.session.get('quiz_data')
    
    if quiz_data and quiz_data['current_index'] > 0:
        quiz_data['current_index'] -= 1
        request.session['quiz_data'] = quiz_data
        request.session.modified = True
    
    return redirect('take_quiz')

@login_required
def submit_quiz(request):
    """Submit quiz and calculate results"""
    quiz_data = request.session.get('quiz_data')
    
    if not quiz_data:
        messages.error(request, 'No active quiz found')
        return redirect('select_quiz')
    
    # Calculate results
    question_ids = quiz_data['question_ids']
    answers = quiz_data['answers']
    
    correct_count = 0
    wrong_count = 0
    quiz_answers = []
    
    for q_id in question_ids:
        question = Question.objects.get(id=q_id)
        user_answer = answers.get(str(q_id), '')
        is_correct = user_answer == question.correct_answer
        
        if is_correct:
            correct_count += 1
        else:
            wrong_count += 1
        
        quiz_answers.append({
            'question': question,
            'user_answer': user_answer,
            'correct_answer': question.correct_answer,
            'is_correct': is_correct
        })
    
    # Calculate time taken
    from datetime import datetime
    start_time = datetime.fromisoformat(quiz_data['start_time'])
    time_taken = timezone.now() - start_time
    
    # Save quiz to database
    topic = Topic.objects.get(id=quiz_data['topic_id'])
    subtopic = Subtopic.objects.get(id=quiz_data['subtopic_id']) if quiz_data['subtopic_id'] else None
    
    quiz = Quiz.objects.create(
        user=request.user,
        topic=topic,
        subtopic=subtopic,
        difficulty=quiz_data['difficulty'],
        total_questions=len(question_ids),
        correct_answers=correct_count,
        wrong_answers=wrong_count,
        time_taken=time_taken
    )
    
    # Save individual answers
    for answer_data in quiz_answers:
        QuizAnswer.objects.create(
            quiz=quiz,
            question=answer_data['question'],
            user_answer=answer_data['user_answer'],
            is_correct=answer_data['is_correct']
        )
    
    # Clear session
    del request.session['quiz_data']
    
    # Redirect to results
    return redirect('quiz_result', quiz_id=quiz.id)

@login_required
def quiz_result(request, quiz_id):
    """Display quiz results"""
    quiz = get_object_or_404(Quiz, id=quiz_id, user=request.user)
    answers = QuizAnswer.objects.filter(quiz=quiz).select_related('question')
    
    context = {
        'quiz': quiz,
        'answers': answers,
    }
    
    return render(request, 'quiz_result.html', context)

@login_required
def user_dashboard(request):
    # Redirect admins to admin dashboard
    if request.user.is_superuser or request.user.is_staff:
        return redirect('admin_dashboard')
    
    user = request.user
    
    # Get user's quiz history
    recent_quizzes = Quiz.objects.filter(user=user).order_by('-date_taken')[:10]
    
    # Calculate statistics
    total_quizzes = Quiz.objects.filter(user=user).count()
    avg_score = Quiz.objects.filter(user=user).aggregate(Avg('score_percentage'))['score_percentage__avg'] or 0
    
    # Performance by topic
    topic_performance = Quiz.objects.filter(user=user).values(
        'topic__name'
    ).annotate(
        avg_score=Avg('score_percentage'),
        quiz_count=Count('id')
    ).order_by('-avg_score')
    
    # Performance by difficulty
    difficulty_stats = Quiz.objects.filter(user=user).values(
        'difficulty'
    ).annotate(
        avg_score=Avg('score_percentage'),
        total=Count('id')
    )
    
    # Recent activity (last 7 days)
    week_ago = timezone.now() - timedelta(days=7)
    recent_activity = Quiz.objects.filter(
        user=user, 
        date_taken__gte=week_ago
    ).count()
    
    context = {
        'user': user,
        'recent_quizzes': recent_quizzes,
        'total_quizzes': total_quizzes,
        'avg_score': round(avg_score, 2),
        'topic_performance': topic_performance,
        'difficulty_stats': difficulty_stats,
        'recent_activity': recent_activity,
    }
    
    return render(request, 'user_dashboard.html', context)

@login_required
def quiz_history(request):
    user = request.user
    quizzes = Quiz.objects.filter(user=user).order_by('-date_taken')
    
    # Filter options
    topic_filter = request.GET.get('topic')
    difficulty_filter = request.GET.get('difficulty')
    
    if topic_filter:
        quizzes = quizzes.filter(topic__id=topic_filter)
    if difficulty_filter:
        quizzes = quizzes.filter(difficulty=difficulty_filter)
    
    topics = Topic.objects.all()
    
    context = {
        'quizzes': quizzes,
        'topics': topics,
        'selected_topic': topic_filter,
        'selected_difficulty': difficulty_filter,
    }
    
    return render(request, 'quiz_history.html', context)

@login_required
def quiz_detail(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, user=request.user)
    answers = QuizAnswer.objects.filter(quiz=quiz).select_related('question')
    
    context = {
        'quiz': quiz,
        'answers': answers,
    }
    
    return render(request, 'quiz_detail.html', context)

# ==================== ADMIN DASHBOARD VIEWS ====================

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # Overall statistics
    total_users = User.objects.filter(is_superuser=False, is_staff=False).count()
    total_quizzes = Quiz.objects.count()
    total_questions = Question.objects.count()
    avg_score = Quiz.objects.aggregate(Avg('score_percentage'))['score_percentage__avg'] or 0
    
    # Recent quizzes
    recent_quizzes = Quiz.objects.select_related('user', 'topic').order_by('-date_taken')[:10]
    
    # Top performers
    top_performers = User.objects.filter(
        is_superuser=False,
        is_staff=False
    ).annotate(
        avg_score=Avg('quiz__score_percentage'),
        quiz_count=Count('quiz')
    ).filter(quiz_count__gt=0).order_by('-avg_score')[:5]
    
    # Topic statistics
    topic_stats = Topic.objects.annotate(
        question_count=Count('question'),
        quiz_count=Count('quiz'),
        avg_score=Avg('quiz__score_percentage')
    ).order_by('-quiz_count')
    
    # User activity (last 30 days)
    thirty_days_ago = timezone.now() - timedelta(days=30)
    active_users = Quiz.objects.filter(
        date_taken__gte=thirty_days_ago
    ).values('user').distinct().count()
    
    context = {
        'total_users': total_users,
        'total_quizzes': total_quizzes,
        'total_questions': total_questions,
        'avg_score': round(avg_score, 2),
        'recent_quizzes': recent_quizzes,
        'top_performers': top_performers,
        'topic_stats': topic_stats,
        'active_users': active_users,
    }
    
    return render(request, 'admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def manage_users(request):
    users = User.objects.filter(is_superuser=False, is_staff=False).annotate(
        quiz_count=Count('quiz'),
        avg_score=Avg('quiz__score_percentage')
    ).order_by('-quiz_count')
    
    context = {
        'users': users,
    }
    
    return render(request, 'manage_users.html', context)

@login_required
@user_passes_test(is_admin)
def user_performance(request, user_id):
    viewed_user = get_object_or_404(User, id=user_id)
    quizzes = Quiz.objects.filter(user=viewed_user).order_by('-date_taken')
    
    # User statistics
    total_quizzes = quizzes.count()
    avg_score = quizzes.aggregate(Avg('score_percentage'))['score_percentage__avg'] or 0
    
    topic_performance = quizzes.values('topic__name').annotate(
        avg_score=Avg('score_percentage'),
        count=Count('id')
    ).order_by('-avg_score')
    
    context = {
        'viewed_user': viewed_user,
        'quizzes': quizzes,
        'total_quizzes': total_quizzes,
        'avg_score': round(avg_score, 2),
        'topic_performance': topic_performance,
    }
    
    return render(request, 'user_performance.html', context)

@login_required
@user_passes_test(is_admin)
def manage_questions(request):
    questions = Question.objects.select_related('topic', 'subtopic').order_by('topic', 'difficulty')
    
    # Filter options
    topic_filter = request.GET.get('topic')
    difficulty_filter = request.GET.get('difficulty')
    
    if topic_filter:
        questions = questions.filter(topic__id=topic_filter)
    if difficulty_filter:
        questions = questions.filter(difficulty=difficulty_filter)
    
    topics = Topic.objects.all()
    
    context = {
        'questions': questions,
        'topics': topics,
        'selected_topic': topic_filter,
        'selected_difficulty': difficulty_filter,
    }
    
    return render(request, 'manage_questions.html', context)