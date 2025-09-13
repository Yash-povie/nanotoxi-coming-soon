#!/usr/bin/env python3
"""
Simple Flask server to host the coming soon page on Railway
"""

from flask import Flask, render_template_string, request, jsonify
import os
import re
from datetime import datetime

app = Flask(__name__)

# Read the HTML content
with open('coming_soon.html', 'r', encoding='utf-8') as f:
    HTML_TEMPLATE = f.read()

@app.route('/')
def index():
    """Serve the coming soon page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/contact', methods=['POST'])
def contact_us():
    """Handle contact form submissions"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['name', 'email']
        for field in required_fields:
            if not data.get(field) or not data[field].strip():
                return jsonify({'success': False, 'message': f'{field.title()} is required'}), 400
        
        # Sanitize inputs
        name = sanitize_input(data['name'])
        email = sanitize_input(data['email'])
        organization = sanitize_input(data.get('organization', ''))
        interest = sanitize_input(data.get('interest', ''))
        
        # Validate email format
        if not is_valid_email(email):
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400
        
        # Log the submission (in production, you'd save to database)
        print(f"📧 New contact form submission:")
        print(f"   Name: {name}")
        print(f"   Email: {email}")
        print(f"   Organization: {organization}")
        print(f"   Interest: {interest}")
        print(f"   Timestamp: {datetime.now()}")
        
        return jsonify({
            'success': True, 
            'message': 'Thank you! We\'ll notify you when we launch.'
        })
        
    except Exception as e:
        print(f"Contact form error: {str(e)}")
        return jsonify({'success': False, 'message': 'Something went wrong. Please try again later.'}), 500

def sanitize_input(text):
    """Sanitize user input to prevent XSS and other attacks"""
    if not text:
        return ""
    
    # Remove potentially dangerous characters
    text = re.sub(r'[<>"\']', '', str(text))
    # Limit length
    text = text[:1000]
    return text.strip()

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

if __name__ == "__main__":
    print("🚀 NanoTox AI Coming Soon Page")
    print("=" * 50)
    print("🔬 Starting server...")
    
    # Get port from environment variable (Railway sets this)
    port = int(os.environ.get('PORT', 5000))
    print(f"📱 Server starting on port: {port}")
    
    # Start server
    app.run(host='0.0.0.0', port=port, debug=False)
