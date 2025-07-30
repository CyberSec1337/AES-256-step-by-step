# app.py
from flask import Flask, render_template, request, jsonify, send_file
from aes_engine import AES256WithSteps
from xmind_exporter import export_to_xmind
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    try:
        action = request.form['action']
        plaintext = request.form['text']
        key = request.form['key']
        mode = request.form['mode']
        iv = request.form.get('iv')

        # Validate inputs
        if len(key) != 32:
            return jsonify({"error": "Key must be 32 characters (256-bit)."})
        
        if not plaintext.strip():
            return jsonify({"error": "Text input cannot be empty."})
        
        # Validate text length - must be at least 16 bytes
        plaintext_bytes = plaintext.encode('utf-8')
        if len(plaintext_bytes) < 16:
            # Simple Arabic error message
            error_en = f"Text must be at least 16 bytes long. Current length: {len(plaintext_bytes)} bytes. Please add more text to reach minimum 16 bytes."
            error_ar = f"يجب أن يكون النص 16 بايت على الأقل. الطول الحالي: {len(plaintext_bytes)} بايت. يرجى إضافة المزيد من النص للوصول إلى 16 بايت كحد أدنى."
            
            return jsonify({
                "error": error_en,
                "error_ar": error_ar
            })
        
        if mode in ['CBC', 'CFB', 'OFB', 'CTR'] and iv and len(iv) != 16:
            iv_label = "Nonce" if mode == 'CTR' else "IV"
            return jsonify({"error": f"{iv_label} must be 16 characters for {mode} mode."})

        # Create AES instance
        aes = AES256WithSteps(key.encode(), mode, iv.encode() if iv else None)

        # Perform encryption or decryption
        if action == 'encrypt':
            result = aes.encrypt(plaintext)
        else:
            result = aes.decrypt(plaintext)

        steps = aes.get_steps()

        # Save steps to Xmind
        xmind_path = 'static/aes_steps.xmind'
        export_to_xmind(steps, xmind_path)

        return jsonify({"result": result, "steps": steps})
        
    except ValueError as e:
        return jsonify({"error": str(e)})
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"})

@app.route('/download')
def download():
    return send_file('static/aes_steps.xmind', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
