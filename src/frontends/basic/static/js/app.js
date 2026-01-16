const API_BASE = '/tickets';

// Load tickets on page load
document.addEventListener('DOMContentLoaded', () => {
    loadTickets();
    setupEventListeners();
});

function setupEventListeners() {
    // Create ticket form
    document.getElementById('createTicketForm').addEventListener('submit', createTicket);
    
    // Edit ticket form
    document.getElementById('editTicketForm').addEventListener('submit', updateTicket);
    
    // Modal close button
    document.querySelector('.close').addEventListener('click', closeModal);
    
    // Close modal when clicking outside
    window.addEventListener('click', (e) => {
        const modal = document.getElementById('editModal');
        if (e.target === modal) {
            closeModal();
        }
    });
}

async function loadTickets() {
    try {
        const response = await fetch(API_BASE);
        const tickets = await response.json();
        displayTickets(tickets);
    } catch (error) {
        console.error('Error loading tickets:', error);
    }
}

function displayTickets(tickets) {
    const container = document.getElementById('ticketsList');
    
    if (tickets.length === 0) {
        container.innerHTML = '<p>No tickets yet. Create one to get started!</p>';
        return;
    }
    
    container.innerHTML = tickets.map(ticket => `
        <div class="ticket">
            <h3>${escapeHtml(ticket.title)}</h3>
            <p>${escapeHtml(ticket.description)}</p>
            <div class="ticket-meta">
                <span class="status-badge status-${ticket.status}">${formatStatus(ticket.status)}</span>
                <span> • Created: ${formatDate(ticket.created_at)}</span>
            </div>
            <div class="ticket-actions">
                <button class="btn-edit" onclick="editTicket(${ticket.id})">Edit</button>
                <button class="btn-delete" onclick="deleteTicket(${ticket.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

async function createTicket(e) {
    e.preventDefault();
    
    const formData = {
        title: document.getElementById('title').value,
        description: document.getElementById('description').value,
        status: document.getElementById('status').value
    };
    
    try {
        const response = await fetch(API_BASE, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            document.getElementById('createTicketForm').reset();
            loadTickets();
        }
    } catch (error) {
        console.error('Error creating ticket:', error);
    }
}

async function editTicket(id) {
    try {
        const response = await fetch(`${API_BASE}/${id}`);
        const ticket = await response.json();
        
        document.getElementById('editTicketId').value = ticket.id;
        document.getElementById('editTitle').value = ticket.title;
        document.getElementById('editDescription').value = ticket.description;
        document.getElementById('editStatus').value = ticket.status;
        
        document.getElementById('editModal').style.display = 'block';
    } catch (error) {
        console.error('Error loading ticket:', error);
    }
}

async function updateTicket(e) {
    e.preventDefault();
    
    const id = document.getElementById('editTicketId').value;
    const formData = {
        title: document.getElementById('editTitle').value,
        description: document.getElementById('editDescription').value,
        status: document.getElementById('editStatus').value
    };
    
    try {
        const response = await fetch(`${API_BASE}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            closeModal();
            loadTickets();
        }
    } catch (error) {
        console.error('Error updating ticket:', error);
    }
}

async function deleteTicket(id) {
    if (!confirm('Are you sure you want to delete this ticket?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/${id}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            loadTickets();
        }
    } catch (error) {
        console.error('Error deleting ticket:', error);
    }
}

function closeModal() {
    document.getElementById('editModal').style.display = 'none';
}

function formatStatus(status) {
    return status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleString();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

