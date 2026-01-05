# Manus API Web Client

一个功能完整的 Manus API 网页客户端，支持对话、文件上传、多轮对话等功能。

## 功能特性

- ✅ **API Key 配置** - 本地保存，安全便捷
- ✅ **多模型支持** - manus-1.6 / manus-1.6-max / manus-1.6-lite
- ✅ **多轮对话** - 支持连续对话，上下文保持
- ✅ **文件上传** - 拖拽上传，支持多种格式
- ✅ **附件管理** - 上传后可在对话中使用
- ✅ **实时状态** - 轮询任务状态，实时显示进度
- ✅ **历史查询** - 查看任意任务的完整对话历史
- ✅ **响应式设计** - 支持桌面和移动设备

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
python app.py
```

### 3. 访问网页

打开浏览器访问：http://localhost:5000

## 部署方式

### 方式一：本地运行

```bash
# 克隆或下载项目
cd manus-web-client

# 安装依赖
pip install -r requirements.txt

# 运行
python app.py
```

### 方式二：使用 Gunicorn（生产环境）

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### 方式三：Docker 部署

创建 `Dockerfile`：

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "app.py"]
```

构建并运行：

```bash
docker build -t manus-web-client .
docker run -p 5000:5000 manus-web-client
```

### 方式四：云平台部署

支持部署到：
- Vercel
- Railway
- Render
- Heroku
- 阿里云/腾讯云服务器

## 项目结构

```
manus-web-client/
├── app.py              # Flask 后端应用
├── requirements.txt    # Python 依赖
├── README.md          # 说明文档
├── templates/
│   └── index.html     # 前端页面
└── uploads/           # 临时上传目录
```

## API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 主页 |
| `/api/create-task` | POST | 创建任务 |
| `/api/get-task/<task_id>` | POST | 获取任务详情 |
| `/api/upload-file` | POST | 上传文件 |
| `/api/list-files` | POST | 列出文件 |
| `/api/get-file/<file_id>` | POST | 获取文件信息 |
| `/api/list-tasks` | POST | 列出任务 |

## 使用说明

### 1. 配置 API Key

1. 在页面顶部输入您的 Manus API Key（以 `sk-` 开头）
2. 点击"保存"按钮，API Key 会保存在浏览器本地

### 2. 发送消息

1. 选择模型（推荐 manus-1.6-max）
2. 在输入框中输入消息
3. 点击"发送消息"或按 Enter 键
4. 等待任务完成，查看回复

### 3. 多轮对话

- 发送第一条消息后，任务 ID 会自动填充
- 后续消息会自动关联到同一对话
- 清空对话会重置任务 ID

### 4. 上传文件

1. 切换到"文件管理"标签
2. 拖拽文件或点击上传区域
3. 上传成功后，点击"使用"按钮添加到附件
4. 回到"对话"标签，发送消息时会自动带上附件

### 5. 查看历史

1. 切换到"任务历史"标签
2. 输入任务 ID
3. 点击"查询"查看完整对话记录

## 注意事项

- API Key 仅保存在浏览器本地，不会上传到服务器
- 文件上传大小限制为 50MB
- 建议使用 HTTPS 部署以保护 API Key 安全

## License

MIT License
