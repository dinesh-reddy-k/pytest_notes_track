// Função para pegar o CSRF Token dos cookies
function getCSRFToken() {
  let cookieValue = null;
  const name = 'csrftoken';
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Verifica se o cookie começa com o nome 'csrftoken'
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Abrir o modal
function openModal() {
  document.getElementById('noteModal').classList.remove('hidden');
}

// Fechar o modal
function closeModal() {
  document.getElementById('noteModal').classList.add('hidden');
}

// Enviar nova nota para a API
document.getElementById('noteForm').addEventListener('submit', function(event) {
  event.preventDefault();
  const title = document.getElementById('noteTitle').value;
  const content = document.getElementById('noteContent').value;

  fetch('/api/notes/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken() // Atualize esta linha
    },
    body: JSON.stringify({
      title: title,
      content: content,
      category_names: [] // Pode ser preenchido conforme necessário
    })
  })
    .then(response => response.json())
    .then(data => {
      window.location.reload(); // Recarrega a página após criar a nota
    });
});

// Função para editar uma nota existente
function editNote(id, title, content) {
  openModal();
  document.getElementById('noteTitle').value = title;
  document.getElementById('noteContent').value = content;

  document.getElementById('noteForm').onsubmit = function(event) {
    event.preventDefault();
    fetch(`/api/notes/${id}/`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken() // Atualize esta linha
      },
      body: JSON.stringify({
        title: document.getElementById('noteTitle').value,
        content: document.getElementById('noteContent').value,
      })
    })
      .then(response => response.json())
      .then(data => {
        window.location.reload();
      });
  };
}

// Função para deletar uma nota
function deleteNote(id) {
  fetch(`/api/notes/${id}/`, {
    method: 'DELETE',
    headers: {
      'X-CSRFToken': getCSRFToken() // Atualize esta linha
    }
  })
    .then(response => {
      if (response.ok) {
        window.location.reload();
      }
    });
}
