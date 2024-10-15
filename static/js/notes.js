
// Função para pegar o CSRF Token dos cookies
function getCSRFToken() {
  let cookieValue = null;
  const name = 'csrftoken';
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Variável para controlar se estamos editando ou criando
let currentEditingNoteId = null;

// Função para abrir o modal para criação de nova nota
function openCreateNoteModal() {
  document.getElementById('noteModal').classList.remove('hidden');
  document.getElementById('noteForm').reset();
  currentEditingNoteId = null; // Resetar o ID da nota para criar nova
  document.getElementById('submitButton').textContent = 'Create Note';
}

// Função para abrir o modal para edição de nota existente
function openEditNoteModal(noteId, title, content, categories) {
  document.getElementById('noteModal').classList.remove('hidden');
  document.getElementById('noteForm').reset();
  currentEditingNoteId = noteId; // Define o ID da nota que está sendo editada
  document.getElementById('noteTitle').value = title;
  document.getElementById('noteContent').value = content;

  // Preencher as categorias selecionadas
  const categorySelect = document.getElementById('categorySelect');
  Array.from(categorySelect.options).forEach(option => {
    option.selected = categories.includes(option.value);
  });

  document.getElementById('submitButton').textContent = 'Update Note';
}

// Função para fechar o modal
function closeModal() {
  document.getElementById('noteModal').classList.add('hidden');
}

// Função para enviar o formulário (criar ou editar nota)
function processNoteForm(event) {
  event.preventDefault();

  const title = document.getElementById('noteTitle').value;
  const content = document.getElementById('noteContent').value;
  const category_names = Array.from(document.getElementById('categorySelect').selectedOptions).map(option => option.value);

  const isEditing = currentEditingNoteId !== null;
  const url = isEditing ? `/api/notes/${currentEditingNoteId}/` : '/api/notes/';
  const method = isEditing ? 'PATCH' : 'POST';

  // Enviar os dados via fetch
  fetch(url, {
    method: method,
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken()
    },
    body: JSON.stringify({
      title: title,
      content: content,
      category_names: category_names
    })
  })
    .then(response => {
      if (!response.ok) {
        return response.text().then(text => { throw new Error(`Erro ao processar a nota: ${text}`); });
      }
      return response.json();
    })
    .then(data => {
      console.log(isEditing ? 'Nota atualizada com sucesso:' : 'Nota criada com sucesso:', data);
      closeModal(); // Fecha o modal após a ação
      window.location.reload(); // Recarrega a página para refletir as mudanças
    })
    .catch(error => {
      console.error('Erro ao processar a nota:', error);
    });
}

// Função para deletar uma nota
function deleteNote(id) {
  fetch(`/api/notes/${id}/`, {
    method: 'DELETE',
    headers: {
      'X-CSRFToken': getCSRFToken()
    }
  })
    .then(response => {
      if (response.ok) {
        console.log('Nota deletada com sucesso.');
        window.location.reload(); // Recarrega a página após a exclusão
      } else {
        console.error('Erro ao deletar a nota.');
      }
    })
    .catch(error => {
      console.error('Erro ao deletar a nota:', error);
    });
}

// Listagem das categorias no dropdown
document.addEventListener('DOMContentLoaded', function() {
  fetch('/api/categories/')
    .then(response => {
      if (!response.ok) {
        throw new Error('Erro ao carregar categorias');
      }
      return response.json();
    })
    .then(data => {
      const categorySelect = document.getElementById('categorySelect');
      data.forEach(category => {
        const option = document.createElement('option');
        option.value = category.name;
        option.textContent = category.name;
        categorySelect.appendChild(option);
      });
    })
    .catch(error => {
      console.error('Erro ao carregar categorias:', error);
    });
});

