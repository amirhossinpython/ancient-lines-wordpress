from flask import Flask, request, jsonify
from flask_cors import CORS
from ancient import AncientScripts

app = Flask(__name__)
CORS(app)

converter = AncientScripts()


@app.route('/convert', methods=['POST'])
def convert_text():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'داده JSON معتبر نیست', 'success': False}), 400
        
        text = data.get('text', '')
        script = data.get('script', 'cuneiform')
        
        if not text:
            return jsonify({'error': 'متن وارد نشده است', 'success': False}), 400
        
        func = getattr(converter, script.lower(), None)
        
        if not func:
            return jsonify({'error': f'خط "{script}" پشتیبانی نمی‌شود', 'success': False}), 400
        
        result = func(text)
        
        return jsonify({'success': True, 'result': result})
        
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'وب سرویس فعال است'})


if __name__ == '__main__':
   
   
    app.run(debug=False, host='0.0.0.0', port=5001)
