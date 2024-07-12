  // Aquí definir la variable de autenticación directamente en JavaScript
  const isAuthenticated = true; // Ajusta esto según sea necesario
        
  // Configurar Axios para incluir el token CSRF en las solicitudes
  axios.defaults.xsrfHeaderName = 'X-CSRFToken';
  axios.defaults.xsrfCookieName = 'csrftoken';
  axios.defaults.headers.common['X-CSRFToken'] = getCookie('csrftoken');

  // Función para obtener el valor de la cookie CSRF
  function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i = 0; i < cookies.length; i++) {
              const cookie = cookies[i].trim();
              if (cookie.startsWith(name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }

  // Script para manejar la interacción del usuario con el chatbot
  const chatContainer = document.getElementById('chat-container');
  const minimizeButton = document.getElementById('minimize-button');
  const chatMessages = document.getElementById('chat-messages');
  const chatForm = document.getElementById('chat-form');
  const userInput = document.getElementById('user-input');
  let isFirstMessageShown = false;

  // Evento submit para enviar mensaje
  chatForm.addEventListener('submit', (event) => {
      event.preventDefault();
      if (isAuthenticated) {
          sendMessage(userInput.value);
      } else {
          displayMessage('Error', 'Debes iniciar sesión para usar el chatbot.');
      }
  });

  // Evento para minimizar o maximizar el chat
  function toggleChat() {
      chatContainer.classList.toggle('minimized');
      if (chatContainer.classList.contains('minimized')) {
          minimizeButton.textContent = '+';
      } else {
          minimizeButton.textContent = '-';
      }
  }

  // Simular mensaje inicial del chatbot al cargar la página
  document.addEventListener('DOMContentLoaded', () => {
      if (!chatContainer.classList.contains('minimized') && !isFirstMessageShown) {
          displayMessage('ChatBot', '¡Hola! Soy un chatbot. ¿En qué puedo ayudarte?');
          isFirstMessageShown = true;
      }
  });

  // Inactividad del usuario
  let inactivityTime = function () {
      let time;
      window.onload = resetTimer;
      document.onmousemove = resetTimer;
      document.onkeypress = resetTimer;
      document.ontouchstart = resetTimer;
      document.onclick = resetTimer;

      function notifyUser() {
          if (isAuthenticated) {
              displayMessage('ChatBot', '¡Hola! Soy un chatbot. ¿En qué puedo ayudarte?');
          }
          resetTimer();
      }

      function resetTimer() {
          clearTimeout(time);
          time = setTimeout(notifyUser, 120000); // 10 segundos
      }
  };

  inactivityTime();

  // Función para enviar mensaje al servidor Django usando Axios
  function sendMessage(message) {
      // Mostrar mensaje del usuario en la ventana de chat
      displayMessage('Tú', message);

      // Enviar mensaje al servidor Django usando Axios
      axios.post('/sendmessage/', { message })
          .then(response => {
              if (response.data && response.data.message) {
                  // Mostrar respuesta del chatbot en la ventana de chat
                  displayMessage('ChatBot', response.data.message);
              } else {
                  console.error('Error: Respuesta inválida del servidor');
                  displayMessage('Error', 'Respuesta inválida del servidor');
              }
          })
          .catch(error => {
              console.error('Error:', error);
              // Mostrar mensaje de error en la ventana de chat
              displayMessage('Error', 'Se produjo un error al procesar tu solicitud.');
          });

      // Limpiar campo de entrada del usuario
      userInput.value = '';
  }

  // Función para mostrar mensajes en la ventana de chat
  function displayMessage(sender, message) {
      if (!chatContainer.classList.contains('minimized')) {
          const messageElement = document.createElement('div');
          messageElement.innerHTML = `<strong>${sender}: </strong> ${message}`;
          chatMessages.appendChild(messageElement);
          chatMessages.scrollTop = chatMessages.scrollHeight;
      }
  }