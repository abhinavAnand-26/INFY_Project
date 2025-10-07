# base/admin.py
# REPLACE ENTIRE FILE with this code

from django.contrib import admin
from .models import Topic, Subtopic, Question, Quiz, QuizAnswer, PDFDocument

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Subtopic)
class SubtopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'topic', 'description')
    list_filter = ('topic',)
    search_fields = ('name', 'topic__name')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text_short', 'topic', 'subtopic', 'difficulty', 'correct_answer')
    list_filter = ('topic', 'subtopic', 'difficulty')
    search_fields = ('question_text',)
    actions = ['set_difficulty_easy', 'set_difficulty_medium', 'set_difficulty_hard']
    
    def question_text_short(self, obj):
        return obj.question_text[:50] + "..." if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Question'
    
    def set_difficulty_easy(self, request, queryset):
        updated = queryset.update(difficulty='easy')
        self.message_user(request, f'{updated} questions set to Easy difficulty')
    set_difficulty_easy.short_description = "Set difficulty to Easy"
    
    def set_difficulty_medium(self, request, queryset):
        updated = queryset.update(difficulty='medium')
        self.message_user(request, f'{updated} questions set to Medium difficulty')
    set_difficulty_medium.short_description = "Set difficulty to Medium"
    
    def set_difficulty_hard(self, request, queryset):
        updated = queryset.update(difficulty='hard')
        self.message_user(request, f'{updated} questions set to Hard difficulty')
    set_difficulty_hard.short_description = "Set difficulty to Hard"

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'subtopic', 'difficulty', 'score_percentage', 'total_questions', 'date_taken')
    list_filter = ('topic', 'difficulty', 'date_taken')
    search_fields = ('user__username', 'topic__name')
    readonly_fields = ('date_taken', 'score_percentage')
    
    def has_add_permission(self, request):
        # Users create quizzes from the app, not admin panel
        return False

@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'question_short', 'user_answer', 'is_correct')
    list_filter = ('is_correct', 'quiz__topic')
    search_fields = ('quiz__user__username',)
    
    def question_short(self, obj):
        return obj.question.question_text[:40] + "..."
    question_short.short_description = 'Question'
    
    def has_add_permission(self, request):
        return False

@admin.register(PDFDocument)
class PDFDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'subtopic', 'uploaded_at', 'uploaded_by', 'is_processed', 'process_button')
    list_filter = ('topic', 'is_processed', 'uploaded_at')
    search_fields = ('title', 'topic__name')
    readonly_fields = ('uploaded_at', 'is_processed')
    actions = ['process_selected_pdfs']
    
    def process_button(self, obj):
        if obj.is_processed:
            return "✅ Processed"
        else:
            return "⏳ Pending"
    process_button.short_description = 'Status'
    
    def process_selected_pdfs(self, request, queryset):
        """Admin action to process selected PDFs"""
        from .pdf_processor import process_pdf_document
        
        processed = 0
        failed = 0
        
        for pdf_doc in queryset:
            if not pdf_doc.is_processed:
                success, message = process_pdf_document(pdf_doc.id)
                if success:
                    processed += 1
                    self.message_user(request, f"{pdf_doc.title}: {message}")
                else:
                    failed += 1
                    self.message_user(request, f"{pdf_doc.title}: {message}", level='ERROR')
        
        if processed > 0:
            self.message_user(request, f"Successfully processed {processed} PDF(s)")
        if failed > 0:
            self.message_user(request, f"Failed to process {failed} PDF(s)", level='ERROR')
    
    process_selected_pdfs.short_description = "Process selected PDF documents"