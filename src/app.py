from flask import Flask, request, jsonify, render_template
from datetime import datetime
from models.ticket import Ticket
from config import Config
import os

# Get the directory where app.py is located
basedir = os.path.abspath(os.path.dirname(__file__))

# Determine frontend paths based on config
theme = Config.FRONTEND_THEME
if theme:
    frontend_base = os.path.join(basedir, 'frontends', theme)
    static_folder = os.path.join(frontend_base, 'static')
    template_folder = os.path.join(frontend_base, 'templates')
else:
    # No frontend - API only mode
    static_folder = None
    template_folder = None

app = Flask(__name__,
            static_folder=static_folder,
            template_folder=template_folder)

app.config.from_object(Config)

# In-memory storage
tickets: dict[int, Ticket] = {}
next_id = 1

@app.route('/')
def index():
    if theme:
        return render_template('index.html')
    else:
        return 'SimpleTask API - No frontend configured'

# Create ticket
@app.route('/tickets', methods=['POST'])
def create_ticket():
    global next_id
    data = request.get_json()
    ticket: Ticket = {
        'id': next_id,
        'title': data.get('title', ''),
        'description': data.get('description', ''),
        'status': data.get('status', 'todo'),
        'created_at': datetime.utcnow().isoformat()
    }
    tickets[next_id] = ticket
    next_id += 1
    return jsonify(ticket), 201

# Read all tickets
@app.route('/tickets', methods=['GET'])
def get_tickets():
    return jsonify(list(tickets.values()))

# Read single ticket
@app.route('/tickets/<int:ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    ticket = tickets.get(ticket_id)
    if not ticket:
        return jsonify({'error': 'Ticket not found'}), 404
    return jsonify(ticket)

# Update ticket
@app.route('/tickets/<int:ticket_id>', methods=['PUT'])
def update_ticket(ticket_id):
    ticket = tickets.get(ticket_id)
    if not ticket:
        return jsonify({'error': 'Ticket not found'}), 404
    data = request.get_json()
    ticket.update({
        'title': data.get('title', ticket['title']),
        'description': data.get('description', ticket['description']),
        'status': data.get('status', ticket['status'])
    })
    return jsonify(ticket)

# Delete ticket
@app.route('/tickets/<int:ticket_id>', methods=['DELETE'])
def delete_ticket(ticket_id):
    if ticket_id not in tickets:
        return jsonify({'error': 'Ticket not found'}), 404
    del tickets[ticket_id]
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)

