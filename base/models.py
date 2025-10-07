from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True, max_length=150)
    password = models.CharField(max_length=128)
    contact = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.email

# base/models.py
# KEEP YOUR EXISTING REGISTRATION MODEL CODE AT THE TOP
# Just ADD these new models below your existing code

from django.db import models
from django.contrib.auth.models import User

# === ADD THESE NEW MODELS BELOW YOUR EXISTING REGISTRATION CODE ===

class Topic(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Subtopic(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='subtopics')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.topic.name} - {self.name}"
    
    class Meta:
        ordering = ['topic', 'name']

class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    question_text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ])
    explanation = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.topic.name} - {self.question_text[:50]}"
    
    class Meta:
        ordering = ['topic', 'subtopic', 'difficulty']

class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE, null=True, blank=True)
    difficulty = models.CharField(max_length=10, choices=Question.DIFFICULTY_CHOICES)
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    score_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    date_taken = models.DateTimeField(auto_now_add=True)
    time_taken = models.DurationField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        # Auto-calculate score percentage
        if self.total_questions > 0:
            self.score_percentage = (self.correct_answers / self.total_questions) * 100
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} - {self.topic.name} ({self.date_taken.strftime('%Y-%m-%d')})"
    
    class Meta:
        ordering = ['-date_taken']
        verbose_name_plural = 'Quizzes'

class QuizAnswer(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=1)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Quiz {self.quiz.id} - Question {self.question.id}"
    
    class Meta:
        ordering = ['quiz', 'question']

class PDFDocument(models.Model):
    title = models.CharField(max_length=200)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE, null=True, blank=True)
    pdf_file = models.FileField(upload_to='quiz_pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_processed = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-uploaded_at']