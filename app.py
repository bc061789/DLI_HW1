from flask import Flask, render_template, jsonify, request
import numpy as np

app = Flask(__name__)

GAMMA = 0.9
REWARD = -1

actions = {
    "↑": (-1, 0),
    "↓": (1, 0),
    "←": (0, -1),
    "→": (0, 1)
}

@app.route('/')
def index():
    return render_template('index.html')


def is_valid(r, c, n, obstacles):

    return (
        0 <= r < n and
        0 <= c < n and
        (r, c) not in obstacles
    )


def value_iteration(n, start, goal, obstacles):

    V = np.zeros((n, n))

    while True:

        delta = 0
        new_V = V.copy()

        for r in range(n):
            for c in range(n):

                if (r, c) in obstacles:
                    continue

                if (r, c) == goal:
                    new_V[r][c] = 10
                    continue

                values = []

                for act in actions:

                    dr, dc = actions[act]

                    nr = r + dr
                    nc = c + dc

                    if not is_valid(nr, nc, n, obstacles):
                        nr, nc = r, c

                    val = REWARD + GAMMA * V[nr][nc]

                    values.append(val)

                best = max(values)

                new_V[r][c] = round(best, 2)

                delta = max(
                    delta,
                    abs(new_V[r][c] - V[r][c])
                )

        V = new_V

        if delta < 0.001:
            break

    return V


def extract_policy(V, n, goal, obstacles):

    policy = []

    for r in range(n):

        row = []

        for c in range(n):

            if (r, c) in obstacles:
                row.append("X")
                continue

            if (r, c) == goal:
                row.append("G")
                continue

            best_action = ""
            best_value = -999999

            for act in actions:

                dr, dc = actions[act]

                nr = r + dr
                nc = c + dc

                if not is_valid(nr, nc, n, obstacles):
                    nr, nc = r, c

                val = REWARD + GAMMA * V[nr][nc]

                if val > best_value:

                    best_value = val
                    best_action = act

            row.append(best_action)

        policy.append(row)

    return policy


@app.route('/evaluate', methods=['POST'])
def evaluate():

    data = request.json

    n = int(data['n'])

    start = tuple(data['start'])
    goal = tuple(data['goal'])

    obstacles = [
        tuple(x)
        for x in data['obstacles']
    ]

    V = value_iteration(
        n,
        start,
        goal,
        obstacles
    )

    policy = extract_policy(
        V,
        n,
        goal,
        obstacles
    )

    return jsonify({
        'values': V.tolist(),
        'policy': policy
    })


if __name__ == '__main__':
    app.run(debug=True)
