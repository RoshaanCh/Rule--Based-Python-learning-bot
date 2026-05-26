"""
My Python Buddy - ChatBot Backend API
Flask-based backend for the ChatGPT-style frontend
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import difflib

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# Chatbot Memory - Dictionary of responses
responses = {
    # Greetings
    "hello": "Hi! I'm your Python learning assistant. Ask me anything about Python.",
    "hi": "Hello! Welcome to My Python Buddy. What would you like to learn?",
    "hey": "Hey there! I'm here to help you master Python. What's on your mind?",
    "how are you": "I'm just code, but I'm ready to help you learn Python!",
    "who are you": "I am My Python Buddy - your AI-powered Python learning assistant!",
    "what is your name": "I'm My Python Buddy, your dedicated Python learning companion!",

    # Python Basics
    "what is python": "Python is a high-level, interpreted programming language used for web development, AI, data science, automation, and more.",
    "why learn python": "Python is beginner-friendly, versatile, and in high demand! It's perfect for automation, data science, web dev, and AI/ML.",
    "what are variables": "Variables are containers used to store data values in Python. Example: x = 10",
    "what is a variable": "A variable is a name that stores data in memory, like x = 5 or name = 'Ali'.",
    "how to create variables": "Simply assign a value: x = 10, name = 'Python', is_fun = True. Python infers the type automatically!",

    # Data Types
    "what are data types": "Data types define the type of data a variable holds. Main types: int, float, string, list, tuple, dict, bool.",
    "what is string": "A string is text enclosed in quotes. Example: 'Hello World' or \"Python Buddy\"",
    "what is integer": "An integer is a whole number like 1, 2, 100, -5. Example: age = 25",
    "what is float": "A float is a decimal number. Example: price = 19.99 or temperature = 36.5",
    "what is list": "A list is an ordered collection of items. Example: fruits = ['apple', 'banana', 'orange']",
    "what is dictionary": "A dictionary stores key-value pairs. Example: person = {'name': 'Ali', 'age': 25}",
    "what is tuple": "A tuple is an immutable sequence. Example: coordinates = (10, 20)",
    "what is boolean": "A boolean is either True or False. Example: is_student = True",

    # Conditions
    "what are if statements": "If statements are used for decision making. Example: if x > 5: print('x is greater than 5')",
    "what is if else": "If-else runs one block if a condition is true, another if false. Example: if age >= 18: print('Adult') else: print('Minor')",
    "what is elif": "Elif (else if) allows multiple conditions. Example: if x > 10: ... elif x > 5: ... else: ...",

    # Loops
    "what are loops": "Loops repeat a block of code. Python has for loops and while loops.",
    "what is for loop": "A for loop iterates over sequences. Example: for i in range(5): print(i)",
    "what is while loop": "A while loop repeats while a condition is true. Example: while x < 10: x += 1",
    "what is range": "range() generates a sequence of numbers. Example: range(5) produces 0, 1, 2, 3, 4",
    "what is break": "break exits a loop early. Example: for i in range(10): if i == 5: break",
    "what is continue": "continue skips the current iteration. Example: for i in range(5): if i == 2: continue",

    # Functions
    "what are functions": "Functions are reusable blocks of code. Example: def greet(name): return f'Hello {name}'",
    "how to define function": "Use def keyword: def function_name(parameters): body. Example: def add(a, b): return a + b",
    "what are parameters": "Parameters are variables in function definition. Arguments are values passed when calling.",
    "what is return": "return statement sends a value back from the function. Example: def get_sum(a, b): return a + b",
    "what is lambda": "Lambda is an anonymous function. Example: add = lambda x, y: x + y",
    "what is recursion": "Recursion is when a function calls itself. Used for problems like factorial or tree traversal.",

    # Lists and Strings
    "how to access list items": "Use index: my_list[0] for first item, my_list[-1] for last. Example: fruits[1] = 'banana'",
    "how to add to list": "Use append(): my_list.append(item) or extend(): my_list.extend([item1, item2])",
    "how to remove from list": "Use remove(): my_list.remove(item) or pop(): my_list.pop(index)",
    "what is list slicing": "Slicing extracts part of list: my_list[1:4] gets items at index 1,2,3. my_list[::2] gets every 2nd item.",
    "how to sort list": "Use sort(): my_list.sort() or sorted(my_list). Add reverse=True for descending.",
    "string methods": "Common methods: .upper(), .lower(), .strip(), .replace(), .split(), .join(), .startswith(), .endswith()",

    # File Operations
    "how to read file": "Use: with open('file.txt', 'r') as f: content = f.read()",
    "how to write file": "Use: with open('file.txt', 'w') as f: f.write('text')",
    "what are file modes": "Modes: 'r' (read), 'w' (write), 'a' (append), 'x' (create), 'b' (binary)",

    # Error Handling
    "what is try except": "Try-except catches errors. Example: try: x = 1/0 except ZeroDivisionError: print('Cannot divide by zero')",
    "what are exceptions": "Exceptions are errors that occur during execution. Examples: ValueError, TypeError, IndexError, KeyError",

    # Advanced
    "what is object oriented programming": "OOP organizes code using objects and classes. Key concepts: encapsulation, inheritance, polymorphism.",
    "what is a class": "A class is a blueprint for objects. Example: class Dog: def bark(self): print('Woof!')",
    "what is inheritance": "Inheritance allows a class to inherit from another. Example: class Puppy(Dog):",
    "what is self": "self refers to the instance of the class. It's used to access instance variables and methods.",

    # Modules and Packages
    "what are modules": "Modules are Python files with reusable code. Import with: import module_name",
    "what are common modules": "Common modules: math, random, datetime, os, sys, json, requests",
    "what is pip": "pip is the package manager for Python. Use: pip install package_name",

    # General
    "help": "I can help you with Python basics, data types, loops, functions, file operations, OOP, and more. Just ask!",
    "what can you teach": "I can teach you: variables, data types, loops, functions, lists, dictionaries, file I/O, error handling, OOP, and more!",
}


def find_best_response(user_input):
    """
    Find the best matching response using similarity matching
    """
    user_input = user_input.lower().strip()
    
    # Direct match
    if user_input in responses:
        return responses[user_input]
    
    # Find closest match using difflib
    closest_matches = difflib.get_close_matches(user_input, responses.keys(), n=1, cutoff=0.6)
    
    if closest_matches:
        return responses[closest_matches[0]]
    
    # Default response
    return "I'm still learning! Try asking me about Python basics, variables, loops, functions, or other Python concepts. Type 'help' for suggestions."


@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({
        'status': 'success',
        'message': 'My Python Buddy API is running!',
        'version': '1.0.0'
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint
    Accepts JSON with 'message' field
    Returns JSON with 'response' field
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Please provide a message'
            }), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({
                'status': 'error',
                'message': 'Message cannot be empty'
            }), 400
        
        # Get response from chatbot
        bot_response = find_best_response(user_message)
        
        return jsonify({
            'status': 'success',
            'user_message': user_message,
            'bot_response': bot_response,
            'timestamp': datetime.datetime.now().isoformat()
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'An error occurred: {str(e)}'
        }), 500


@app.route('/api/suggestions', methods=['GET'])
def get_suggestions():
    """Get list of popular questions"""
    suggestions = [
        "What is Python?",
        "How do variables work?",
        "Explain if statements",
        "What are loops?",
        "How to define functions?",
        "What are lists?",
        "Explain dictionaries",
        "How to handle errors?",
    ]
    return jsonify({
        'status': 'success',
        'suggestions': suggestions
    })


@app.route('/api/topics', methods=['GET'])
def get_topics():
    """Get list of available topics"""
    topics = {
        "Basics": ["what is python", "why learn python", "what are variables"],
        "Data Types": ["what is string", "what is list", "what is dictionary"],
        "Control Flow": ["what are if statements", "what are loops"],
        "Functions": ["what are functions", "what is return"],
        "Advanced": ["what is object oriented programming", "what are modules"]
    }
    return jsonify({
        'status': 'success',
        'topics': topics
    })


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
