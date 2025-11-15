from flask import Flask, jsonify
from utils.db import get_last_run

app = Flask(__name__)

@app.route('/health')
def health():
    lr = get_last_run()
    if not lr:
        return jsonify({'status':'no_runs'}), 500
    return jsonify({'status':'ok','last_run': lr}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
