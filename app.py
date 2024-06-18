from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# 初始化任务列表
current_task = {
    'title': 'XXX任务',
    'description': '这是一个任务描述，描述这个任务的具体内容和要求。',
    'context': ['Obsidian', 'http://baidu.com']
}

pending_tasks = [
    {'title': '任务1', 'description': '描述任务1的内容', 'context': []},
    {'title': '任务2', 'description': '描述任务2的内容', 'context': []}
]

# 编辑模式标志
edit_mode = False

@app.route('/')
def index():
    global edit_mode
    return render_template('index.html', current_task=current_task, pending_tasks=pending_tasks, edit_mode=edit_mode)

@app.route('/toggle_edit_mode', methods=['POST'])
def toggle_edit_mode():
    global edit_mode
    edit_mode = not edit_mode
    return redirect(url_for('index'))

@app.route('/save_description', methods=['POST'])
def save_description():
    global current_task, edit_mode
    new_description = request.form['new_description']
    current_task['description'] = new_description
    edit_mode = False
    return redirect(url_for('index'))

@app.route('/add_context', methods=['POST'])
def add_context():
    global current_task
    new_context = request.form['new_context']
    current_task['context'].append(new_context)
    return redirect(url_for('index'))

@app.route('/switch_task', methods=['POST'])
def switch_task():
    global current_task, pending_tasks
    task_title = request.form.get('task_title')
    task = next((task for task in pending_tasks if task['title'] == task_title), None)
    if task:
        pending_tasks = [t for t in pending_tasks if t['title'] != task_title]
        if current_task:
            pending_tasks.append(current_task)
        current_task = task
    return redirect(url_for('index'))

@app.route('/stop_task', methods=['POST'])
def stop_task():
    global current_task, pending_tasks
    if current_task:
        pending_tasks.append(current_task)
    current_task = None
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
