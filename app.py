from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json or {}
    n = int(data.get('n', 5))
    
    # 定義四個邊的方向
    dirs = ['up', 'down', 'left', 'right']
    
    # HW1-2: 生成包含轉彎資訊的隨機策略
    policy = []
    for r in range(n):
        row = []
        for c in range(n):
            # 隨機決定從哪邊進入，從哪邊離開
            entry = random.choice(dirs)
            exit = random.choice(dirs)
            # 確保入口和出口不同（必須移動）
            while entry == exit:
                exit = random.choice(dirs)
            
            row.append({
                'entry': entry,  # 入口邊
                'exit': exit     # 出口邊（箭頭所在位置）
            })
        policy.append(row)
    
    # HW1-2: 生成隨機價值小數 (比照範例圖格式)
    values = [[round(random.uniform(-5.0, 2.0), 2) for _ in range(n)] for _ in range(n)]
    
    return jsonify({
        'policy': policy,
        'values': values
    })

if __name__ == '__main__':
    app.run(debug=True)