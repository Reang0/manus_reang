"""
Manus API Web Client - Flask 后端
功能：
- API Key 配置
- 创建任务
- 多轮对话
- 文件上传
- 查看对话历史
- 实时轮询任务状态
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
import requests
import os
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

MANUS_BASE_URL = "https://api.manus.im"

# 确保上传目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


def get_headers(api_key):
    """获取请求头"""
    return {
        "accept": "application/json",
        "content-type": "application/json",
        "API_KEY": api_key
    }


# ==================== 页面路由 ====================

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


# ==================== API 路由 ====================

@app.route('/api/create-task', methods=['POST'])
def create_task():
    """创建任务"""
    try:
        data = request.json
        api_key = data.get('api_key')
        prompt = data.get('prompt')
        task_id = data.get('task_id')  # 可选，用于多轮对话
        agent_profile = data.get('agent_profile', 'manus-1.6')
        task_mode = data.get('task_mode', 'agent')
        attachments = data.get('attachments', [])
        
        if not api_key or not prompt:
            return jsonify({'error': '缺少 API Key 或 prompt'}), 400
        
        # 构建请求数据
        req_data = {
            "prompt": prompt,
            "agentProfile": agent_profile,
            "taskMode": task_mode
        }
        
        if task_id:
            req_data["taskId"] = task_id
        
        if attachments:
            req_data["attachments"] = attachments
        
        # 发送请求
        response = requests.post(
            f"{MANUS_BASE_URL}/v1/tasks",
            headers=get_headers(api_key),
            json=req_data
        )
        
        return jsonify(response.json()), response.status_code
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/get-task/<task_id>', methods=['POST'])
def get_task(task_id):
    """获取任务详情"""
    try:
        data = request.json
        api_key = data.get('api_key')
        
        if not api_key:
            return jsonify({'error': '缺少 API Key'}), 400
        
        response = requests.get(
            f"{MANUS_BASE_URL}/v1/tasks/{task_id}",
            headers=get_headers(api_key)
        )
        
        return jsonify(response.json()), response.status_code
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/upload-file', methods=['POST'])
def upload_file():
    """上传文件到 Manus"""
    try:
        api_key = request.form.get('api_key')
        
        if not api_key:
            return jsonify({'error': '缺少 API Key'}), 400
        
        if 'file' not in request.files:
            return jsonify({'error': '没有文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': '没有选择文件'}), 400
        
        filename = secure_filename(file.filename)
        
        # 步骤1: 创建文件记录
        create_resp = requests.post(
            f"{MANUS_BASE_URL}/v1/files",
            headers=get_headers(api_key),
            json={"filename": filename}
        )
        
        if create_resp.status_code != 200:
            return jsonify({'error': '创建文件记录失败', 'details': create_resp.text}), 400
        
        file_data = create_resp.json()
        file_id = file_data.get('id')
        upload_url = file_data.get('upload_url')
        
        # 步骤2: 上传文件内容
        file_content = file.read()
        upload_resp = requests.put(upload_url, data=file_content)
        
        if upload_resp.status_code not in [200, 201]:
            return jsonify({'error': '上传文件内容失败'}), 400
        
        return jsonify({
            'success': True,
            'file_id': file_id,
            'filename': filename,
            'size': len(file_content)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/list-files', methods=['POST'])
def list_files():
    """列出所有文件"""
    try:
        data = request.json
        api_key = data.get('api_key')
        
        if not api_key:
            return jsonify({'error': '缺少 API Key'}), 400
        
        response = requests.get(
            f"{MANUS_BASE_URL}/v1/files",
            headers=get_headers(api_key)
        )
        
        return jsonify(response.json()), response.status_code
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/get-file/<file_id>', methods=['POST'])
def get_file(file_id):
    """获取文件信息"""
    try:
        data = request.json
        api_key = data.get('api_key')
        
        if not api_key:
            return jsonify({'error': '缺少 API Key'}), 400
        
        response = requests.get(
            f"{MANUS_BASE_URL}/v1/files/{file_id}",
            headers=get_headers(api_key)
        )
        
        return jsonify(response.json()), response.status_code
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/list-tasks', methods=['POST'])
def list_tasks():
    """列出所有任务"""
    try:
        data = request.json
        api_key = data.get('api_key')
        
        if not api_key:
            return jsonify({'error': '缺少 API Key'}), 400
        
        response = requests.get(
            f"{MANUS_BASE_URL}/v1/tasks",
            headers=get_headers(api_key)
        )
        
        return jsonify(response.json()), response.status_code
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
