# pyrefly: ignore [missing-import]
import ollama
prompt = """
You are an expert university question paper setter and academic evaluator.

Your task is to generate a well-structured university examination question paper strictly based on the provided syllabus and Course Outcomes (COs).

==================================================
GENERAL INSTRUCTIONS
==================================================

1. Generate questions ONLY from the given syllabus topics.
2. Maintain proper university examination standards.
3. Questions must be:
   - Clear
   - Grammatically correct
   - Academically meaningful
   - Non-repetitive
4. Ensure proper distribution across:
   - Conceptual questions
   - Application-oriented questions
   - Analytical questions
   - Problem-solving questions
5. Cover all units fairly.
6. Questions should progressively increase in difficulty.
7. Ensure Bloom’s Taxonomy coverage across all levels.
8. Map every question correctly to the relevant CO.
9. Avoid generating duplicate or nearly similar questions.
10. Include programming-oriented questions wherever relevant.

==================================================
QUESTION PAPER STRUCTURE
==================================================

PART A:
- Generate 10 short-answer questions.
- Questions should test:
  - Definitions
  - Basic concepts
  - Short explanations
  - Simple applications
- Each question must contain:
  - Question
  - CO Mapping
  - Bloom’s Taxonomy Level

PART B:
- Generate 10 long-answer questions.
- Questions should involve:
  - Explanation
  - Design
  - Coding
  - Comparison
  - Analysis
  - Real-world applications
  - Problem-solving
- Include internal choices whenever appropriate.
- Each question must contain:
  - Question
  - CO Mapping
  - Bloom’s Taxonomy Level

==================================================
OUTPUT FORMAT
==================================================

Return the response ONLY in valid JSON format.

Expected JSON Structure:

{
  "part_a": [
    {
      "question_number": 1,
      "question": "Define class and object.",
      "unit": "UNIT 1",
      "co": "CO1",
      "blooms_level": "Remember"
    }
  ],
  "part_b": [
    {
      "question_number": 11,
      "question": "Explain inheritance with a suitable Java program.",
      "unit": "UNIT 2",
      "co": "CO2",
      "blooms_level": "Apply"
    }
  ]
}

==================================================
BLOOM’S TAXONOMY LEVELS
==================================================

- Remember
- Understand
- Apply
- Analyze
- Evaluate
- Create

==================================================
COURSE OUTCOMES
==================================================

CO1: Understand basic Object-Oriented Programming concepts.
CO2: Apply inheritance and polymorphism in software development.
CO3: Analyze relationships between objects and classes.
CO4: Design applications using advanced OOP principles.
CO5: Develop problem-solving skills using Java programming concepts.

==================================================
SYLLABUS
==================================================

UNIT 1: Introduction to OOP
- Procedure-Oriented Programming
- Object-Oriented Programming
- Classes
- Objects
- Constructors
- Methods

UNIT 2: Inheritance and Polymorphism
- Inheritance
- Types of Inheritance
- Method Overloading
- Method Overriding
- Dynamic Binding
- Polymorphism

UNIT 3: Encapsulation and Abstraction
- Encapsulation
- Access Modifiers
- Abstract Classes
- Interfaces
- Data Hiding

UNIT 4: Exception Handling and File Handling
- Exception Handling
- try-catch-finally
- throw and throws
- File Handling
- Streams

UNIT 5: Advanced Java Concepts
- Collections Framework
- Generics
- Multithreading
- Lambda Expressions
- Stream API

==================================================
IMPORTANT REQUIREMENTS
==================================================

- Ensure every unit contributes questions.
- Maintain balanced difficulty distribution.
- Do not generate vague or incomplete questions.
- Use proper academic terminology.
- Questions should resemble autonomous university examination patterns.
- Ensure JSON is syntactically valid.
"""


print("==================================================")
print("GENERATING INITIAL QUESTION PAPER...")
print("==================================================")
print("Assistant is thinking (processing context)...", end="", flush=True)

messages = [
    {
        'role': 'user',
        'content': prompt
    }
]

try:
    stream = ollama.chat(
        model='llama3:latest',
        messages=messages,
        format='json',
        stream=True
    )

    # Clear the thinking line
    print("\r" + " " * 50 + "\r", end="", flush=True)

    response_content = ""
    for chunk in stream:
        content = chunk['message']['content']
        print(content, end='', flush=True)
        response_content += content
    print()
    
    messages.append({
        'role': 'assistant',
        'content': response_content
    })

except Exception as e:
    # Clear the thinking line in case of error
    print("\r" + " " * 50 + "\r", end="", flush=True)
    print(f"\nError during initial generation: {e}")
    # Initialize response_content to empty if it failed
    response_content = ""

print("\n==================================================")
print("CHAT SESSION ACTIVE")
print("==================================================")
print("You can now chat with the assistant to refine the question paper.")
print("Type 'exit' or 'quit' to end the conversation.\n")

while True:
    try:
        user_input = input("You: ")
        if user_input.strip().lower() in ['exit', 'quit']:
            print("\nExiting chat. Goodbye!")
            break
        if not user_input.strip():
            continue

        messages.append({
            'role': 'user',
            'content': user_input
        })

        print("\nAssistant is thinking (processing context)...", end="", flush=True)
        
        # We don't enforce format='json' in follow-up chat to allow the assistant 
        # to respond conversationally if the user asks questions, but it will
        # still output JSON if requested by the user.
        stream = ollama.chat(
            model='llama3:latest',
            messages=messages,
            stream=True
        )

        # Clear the thinking line and print header
        print("\r" + " " * 50 + "\rAssistant: ", end="", flush=True)

        response_content = ""
        for chunk in stream:
            content = chunk['message']['content']
            print(content, end='', flush=True)
            response_content += content
        print("\n")

        messages.append({
            'role': 'assistant',
            'content': response_content
        })

    except KeyboardInterrupt:
        print("\n\nExiting chat. Goodbye!")
        break
    except Exception as e:
        # Clear the thinking line in case of error
        print("\r" + " " * 50 + "\r", end="", flush=True)
        print(f"\nAn error occurred: {e}\n")