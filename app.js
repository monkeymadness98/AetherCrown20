// Futuristic Todo 2030 - JavaScript with localStorage, filters, and drag & drop

class TodoApp {
    constructor() {
        this.todos = this.loadFromStorage();
        this.currentFilter = 'all';
        this.draggedElement = null;
        
        this.init();
    }

    init() {
        this.cacheDOMElements();
        this.attachEventListeners();
        this.render();
        this.updateCounts();
    }

    cacheDOMElements() {
        this.form = document.getElementById('todo-form');
        this.todoInput = document.getElementById('todo-input');
        this.dueDateInput = document.getElementById('due-date');
        this.tagsInput = document.getElementById('tags-input');
        this.todoList = document.getElementById('todo-list');
        this.filterBtns = document.querySelectorAll('.filter-btn');
        this.clearCompletedBtn = document.getElementById('clear-completed');
    }

    attachEventListeners() {
        // Form submission
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.addTodo();
        });

        // Filter buttons
        this.filterBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setFilter(e.target.dataset.filter);
            });
        });

        // Clear completed
        this.clearCompletedBtn.addEventListener('click', () => {
            this.clearCompleted();
        });
    }

    addTodo() {
        const text = this.todoInput.value.trim();
        if (!text) return;

        const todo = {
            id: Date.now().toString(),
            text: text,
            completed: false,
            createdAt: new Date().toISOString(),
            dueDate: this.dueDateInput.value || null,
            tags: this.parseTags(this.tagsInput.value)
        };

        this.todos.push(todo);
        this.saveToStorage();
        this.render();
        this.updateCounts();
        
        // Clear inputs
        this.todoInput.value = '';
        this.dueDateInput.value = '';
        this.tagsInput.value = '';
        
        // Focus back to input
        this.todoInput.focus();
    }

    parseTags(tagsString) {
        if (!tagsString.trim()) return [];
        return tagsString
            .split(',')
            .map(tag => tag.trim())
            .filter(tag => tag.length > 0);
    }

    toggleTodo(id) {
        const todo = this.todos.find(t => t.id === id);
        if (todo) {
            todo.completed = !todo.completed;
            this.saveToStorage();
            this.render();
            this.updateCounts();
        }
    }

    deleteTodo(id) {
        this.todos = this.todos.filter(t => t.id !== id);
        this.saveToStorage();
        this.render();
        this.updateCounts();
    }

    clearCompleted() {
        this.todos = this.todos.filter(t => !t.completed);
        this.saveToStorage();
        this.render();
        this.updateCounts();
    }

    setFilter(filter) {
        this.currentFilter = filter;
        
        // Update active button
        this.filterBtns.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.filter === filter);
        });
        
        this.render();
    }

    getFilteredTodos() {
        const now = new Date();
        now.setHours(0, 0, 0, 0);

        switch (this.currentFilter) {
            case 'active':
                return this.todos.filter(t => !t.completed);
            case 'completed':
                return this.todos.filter(t => t.completed);
            case 'overdue':
                return this.todos.filter(t => {
                    if (!t.dueDate || t.completed) return false;
                    const dueDate = new Date(t.dueDate);
                    dueDate.setHours(0, 0, 0, 0);
                    return dueDate < now;
                });
            default:
                return this.todos;
        }
    }

    isOverdue(dueDate, completed) {
        if (!dueDate || completed) return false;
        const now = new Date();
        now.setHours(0, 0, 0, 0);
        const due = new Date(dueDate);
        due.setHours(0, 0, 0, 0);
        return due < now;
    }

    formatDate(dateString) {
        if (!dateString) return '';
        const date = new Date(dateString);
        const options = { year: 'numeric', month: 'short', day: 'numeric' };
        return date.toLocaleDateString('en-US', options);
    }

    render() {
        const filteredTodos = this.getFilteredTodos();
        
        if (filteredTodos.length === 0) {
            this.todoList.innerHTML = `
                <div class="empty-state">
                    ${this.currentFilter === 'all' 
                        ? 'No tasks yet. Add one to get started!' 
                        : `No ${this.currentFilter} tasks.`}
                </div>
            `;
            return;
        }

        this.todoList.innerHTML = filteredTodos.map(todo => this.createTodoElement(todo)).join('');
        
        // Attach event listeners to new elements
        this.attachTodoEventListeners();
    }

    createTodoElement(todo) {
        const overdue = this.isOverdue(todo.dueDate, todo.completed);
        
        return `
            <div class="todo-item ${todo.completed ? 'completed' : ''} ${overdue ? 'overdue' : ''}" 
                 data-id="${todo.id}"
                 draggable="true">
                <div class="checkbox-wrapper">
                    <div class="checkbox ${todo.completed ? 'checked' : ''}" 
                         data-action="toggle" 
                         data-id="${todo.id}">
                    </div>
                </div>
                <div class="todo-details">
                    <div class="todo-content">${this.escapeHtml(todo.text)}</div>
                    ${this.createMetaSection(todo, overdue)}
                </div>
                <button class="delete-btn" data-action="delete" data-id="${todo.id}">
                    ×
                </button>
            </div>
        `;
    }

    createMetaSection(todo, overdue) {
        const parts = [];
        
        if (todo.dueDate) {
            parts.push(`
                <div class="meta-item ${overdue ? 'overdue-label' : 'due-date'}">
                    📅 ${this.formatDate(todo.dueDate)}
                    ${overdue ? '(Overdue)' : ''}
                </div>
            `);
        }
        
        if (todo.tags && todo.tags.length > 0) {
            const tagsHtml = todo.tags.map(tag => 
                `<span class="tag">${this.escapeHtml(tag)}</span>`
            ).join('');
            parts.push(`<div class="tags">${tagsHtml}</div>`);
        }
        
        if (parts.length === 0) return '';
        
        return `<div class="todo-meta">${parts.join('')}</div>`;
    }

    attachTodoEventListeners() {
        // Toggle and delete buttons
        this.todoList.addEventListener('click', (e) => {
            const action = e.target.dataset.action;
            const id = e.target.dataset.id;
            
            if (action === 'toggle') {
                this.toggleTodo(id);
            } else if (action === 'delete') {
                this.deleteTodo(id);
            }
        });

        // Drag and drop
        const todoItems = this.todoList.querySelectorAll('.todo-item');
        todoItems.forEach(item => {
            item.addEventListener('dragstart', (e) => this.handleDragStart(e));
            item.addEventListener('dragend', (e) => this.handleDragEnd(e));
            item.addEventListener('dragover', (e) => this.handleDragOver(e));
            item.addEventListener('drop', (e) => this.handleDrop(e));
        });
    }

    handleDragStart(e) {
        this.draggedElement = e.target;
        e.target.classList.add('dragging');
        e.dataTransfer.effectAllowed = 'move';
        e.dataTransfer.setData('text/html', e.target.innerHTML);
    }

    handleDragEnd(e) {
        e.target.classList.remove('dragging');
        
        // Remove all dragover classes
        const items = this.todoList.querySelectorAll('.todo-item');
        items.forEach(item => item.classList.remove('dragover'));
    }

    handleDragOver(e) {
        if (e.preventDefault) {
            e.preventDefault();
        }
        
        e.dataTransfer.dropEffect = 'move';
        
        const target = e.target.closest('.todo-item');
        if (target && target !== this.draggedElement) {
            target.classList.add('dragover');
        }
        
        return false;
    }

    handleDrop(e) {
        if (e.stopPropagation) {
            e.stopPropagation();
        }
        
        const target = e.target.closest('.todo-item');
        
        if (this.draggedElement !== target && target) {
            const draggedId = this.draggedElement.dataset.id;
            const targetId = target.dataset.id;
            
            // Reorder todos array
            const draggedIndex = this.todos.findIndex(t => t.id === draggedId);
            const targetIndex = this.todos.findIndex(t => t.id === targetId);
            
            if (draggedIndex !== -1 && targetIndex !== -1) {
                const [draggedTodo] = this.todos.splice(draggedIndex, 1);
                this.todos.splice(targetIndex, 0, draggedTodo);
                
                this.saveToStorage();
                this.render();
            }
        }
        
        return false;
    }

    updateCounts() {
        const now = new Date();
        now.setHours(0, 0, 0, 0);

        const counts = {
            all: this.todos.length,
            active: this.todos.filter(t => !t.completed).length,
            completed: this.todos.filter(t => t.completed).length,
            overdue: this.todos.filter(t => {
                if (!t.dueDate || t.completed) return false;
                const dueDate = new Date(t.dueDate);
                dueDate.setHours(0, 0, 0, 0);
                return dueDate < now;
            }).length
        };

        Object.keys(counts).forEach(key => {
            const countElement = document.getElementById(`count-${key}`);
            if (countElement) {
                countElement.textContent = counts[key];
            }
        });
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    saveToStorage() {
        localStorage.setItem('futuristic-todos-2030', JSON.stringify(this.todos));
    }

    loadFromStorage() {
        const data = localStorage.getItem('futuristic-todos-2030');
        return data ? JSON.parse(data) : [];
    }
}

// Initialize the app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new TodoApp();
});
