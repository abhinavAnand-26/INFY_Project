# base/pdf_processor.py
# REPLACE your existing pdf_processor.py with this FIXED version

import re
import PyPDF2
from .models import Question, Topic, Subtopic, PDFDocument

class PDFQuestionExtractor:
    """
    Extracts MCQ questions from PDF files and saves them to database.
    
    Fixed to handle your specific PDF format with 50 questions
    """
    
    def __init__(self, pdf_document):
        self.pdf_document = pdf_document
        self.questions_extracted = []
        
    def extract_text_from_pdf(self):
        """Extract text from PDF file"""
        try:
            pdf_file = open(self.pdf_document.pdf_file.path, 'rb')
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                text += page_text + "\n"
            
            pdf_file.close()
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return None
    
    def parse_questions(self, text):
        """Parse questions from extracted text - FIXED VERSION"""
        print(f"Raw text length: {len(text)}")
        
        # Clean up the text - normalize whitespace but preserve line breaks
        text = re.sub(r'\r\n', '\n', text)  # Windows line endings
        text = re.sub(r'\r', '\n', text)    # Mac line endings
        
        # Find all question blocks using a more robust pattern
        # This pattern looks for: number + period + space/newline + question text
        question_pattern = r'(\d+)\.\s*([^0-9]+?)(?=\d+\.\s|\Z)'
        
        matches = re.findall(question_pattern, text, re.DOTALL)
        
        print(f"Found {len(matches)} potential question blocks")
        
        questions = []
        
        for match in matches:
            question_number = match[0]
            question_content = match[1].strip()
            
            try:
                question_data = self._parse_single_question(question_content, question_number)
                if question_data:
                    questions.append(question_data)
                    print(f"✓ Parsed question {question_number}: {question_data['question_text'][:50]}...")
                else:
                    print(f"✗ Failed to parse question {question_number}")
            except Exception as e:
                print(f"✗ Error parsing question {question_number}: {e}")
                continue
        
        return questions
    
    def _parse_single_question(self, content, question_num):
        """Parse a single question block - IMPROVED VERSION"""
        
        # Initialize question data
        question_data = {
            'question_text': '',
            'option_a': '',
            'option_b': '',
            'option_c': '',
            'option_d': '',
            'correct_answer': 'A',  # Default
            'explanation': '',
            'difficulty': 'easy'
        }
        
        # Clean up content
        content = content.strip()
        
        # Split into lines for processing
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        if not lines:
            return None
        
        # Find where options start
        option_start_idx = -1
        question_lines = []
        
        for i, line in enumerate(lines):
            # Check if this line is an option (A), B), C), D))
            if re.match(r'^[A-D]\)', line):
                option_start_idx = i
                break
            else:
                question_lines.append(line)
        
        # Extract question text
        if question_lines:
            question_data['question_text'] = ' '.join(question_lines)
        else:
            print(f"No question text found for question {question_num}")
            return None
        
        # Extract options
        if option_start_idx == -1:
            print(f"No options found for question {question_num}")
            return None
        
        # Process option lines
        current_option = None
        option_text = []
        
        for i in range(option_start_idx, len(lines)):
            line = lines[i]
            
            # Check if this line starts with an option marker
            option_match = re.match(r'^([A-D])\)\s*(.*)', line)
            
            if option_match:
                # Save previous option if exists
                if current_option and option_text:
                    text = ' '.join(option_text).strip()
                    if current_option == 'A':
                        question_data['option_a'] = text
                    elif current_option == 'B':
                        question_data['option_b'] = text
                    elif current_option == 'C':
                        question_data['option_c'] = text
                    elif current_option == 'D':
                        question_data['option_d'] = text
                
                # Start new option
                current_option = option_match.group(1)
                option_text = [option_match.group(2)] if option_match.group(2) else []
            else:
                # This line is continuation of current option
                if current_option:
                    option_text.append(line)
        
        # Save the last option
        if current_option and option_text:
            text = ' '.join(option_text).strip()
            if current_option == 'A':
                question_data['option_a'] = text
            elif current_option == 'B':
                question_data['option_b'] = text
            elif current_option == 'C':
                question_data['option_c'] = text
            elif current_option == 'D':
                question_data['option_d'] = text
        
        # Look for explicit answer in content
        answer_match = re.search(r'(?:Answer|Correct|Ans):\s*([A-D])', content, re.IGNORECASE)
        if answer_match:
            question_data['correct_answer'] = answer_match.group(1).upper()
        
        # Look for explanation
        explanation_match = re.search(r'Explanation:\s*(.+?)(?=Difficulty:|$)', content, re.IGNORECASE)
        if explanation_match:
            question_data['explanation'] = explanation_match.group(1).strip()
        
        # Set difficulty based on filename or explicit mention
        if 'easy' in self.pdf_document.title.lower():
            question_data['difficulty'] = 'easy'
        elif 'medium' in self.pdf_document.title.lower():
            question_data['difficulty'] = 'medium'
        elif 'hard' in self.pdf_document.title.lower():
            question_data['difficulty'] = 'hard'
        else:
            question_data['difficulty'] = 'easy'  # Default
        
        # Validate we have minimum required data
        if (question_data['question_text'] and 
            question_data['option_a'] and 
            question_data['option_b']):
            
            # Fill empty options with placeholder
            if not question_data['option_c']:
                question_data['option_c'] = 'N/A'
            if not question_data['option_d']:
                question_data['option_d'] = 'N/A'
            
            return question_data
        
        print(f"Question {question_num} validation failed:")
        print(f"  Question text: {bool(question_data['question_text'])}")
        print(f"  Option A: {bool(question_data['option_a'])}")
        print(f"  Option B: {bool(question_data['option_b'])}")
        
        return None
    
    def save_questions_to_database(self, questions):
        """Save extracted questions to database"""
        saved_count = 0
        
        for i, q_data in enumerate(questions, 1):
            try:
                # Handle subtopic
                subtopic = self.pdf_document.subtopic
                if not subtopic:
                    # Create or get default subtopic
                    subtopic, created = Subtopic.objects.get_or_create(
                        topic=self.pdf_document.topic,
                        name="General",
                        defaults={'description': 'Default subtopic'}
                    )
                
                question = Question.objects.create(
                    topic=self.pdf_document.topic,
                    subtopic=subtopic,
                    difficulty=q_data['difficulty'],
                    question_text=q_data['question_text'],
                    option_a=q_data['option_a'],
                    option_b=q_data['option_b'],
                    option_c=q_data['option_c'],
                    option_d=q_data['option_d'],
                    correct_answer=q_data['correct_answer'],
                    explanation=q_data.get('explanation', '')
                )
                saved_count += 1
                self.questions_extracted.append(question)
                print(f"✓ Saved question {i}: {question.question_text[:60]}...")
                
            except Exception as e:
                print(f"✗ Error saving question {i}: {e}")
                print(f"   Question data: {q_data.get('question_text', 'No question text')[:60]}")
                continue
        
        return saved_count
    
    def process(self):
        """Main process: extract, parse, and save questions"""
        print(f"\n{'='*80}")
        print(f"PROCESSING PDF: {self.pdf_document.title}")
        print(f"{'='*80}")
        
        # Extract text from PDF
        print("STEP 1: Extracting text from PDF...")
        text = self.extract_text_from_pdf()
        if not text:
            return False, "Failed to extract text from PDF"
        
        print(f"   ✓ Extracted {len(text)} characters")
        print(f"   ✓ Text preview: {text[:200]}...")
        
        # Parse questions
        print("\nSTEP 2: Parsing questions...")
        questions = self.parse_questions(text)
        
        if not questions:
            print("   ✗ No questions found!")
            return False, "No questions found in PDF. Check the PDF format."
        
        print(f"   ✓ Successfully parsed {len(questions)} questions")
        
        # Save to database
        print(f"\nSTEP 3: Saving {len(questions)} questions to database...")
        saved_count = self.save_questions_to_database(questions)
        
        if saved_count == 0:
            return False, "Failed to save any questions to database"
        
        # Mark PDF as processed
        self.pdf_document.is_processed = True
        self.pdf_document.save()
        
        print(f"\n{'='*80}")
        print(f"🎉 SUCCESS! Processed {saved_count}/{len(questions)} questions")
        print(f"{'='*80}\n")
        
        return True, f"Successfully extracted and saved {saved_count} out of {len(questions)} questions"


def process_pdf_document(pdf_document_id):
    """
    Process a PDF document and extract questions.
    Can be called from admin action or management command.
    """
    try:
        pdf_doc = PDFDocument.objects.get(id=pdf_document_id)
        
        if pdf_doc.is_processed:
            return False, "PDF already processed"
        
        extractor = PDFQuestionExtractor(pdf_doc)
        success, message = extractor.process()
        
        return success, message
    
    except PDFDocument.DoesNotExist:
        return False, "PDF document not found"
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        print(f"\nFULL ERROR TRACEBACK:")
        print(error_detail)
        return False, f"Error processing PDF: {str(e)}"