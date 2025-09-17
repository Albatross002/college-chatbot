async function sendMessage() {
  const input = document.getElementById("userInput");
  const message = input.value.trim();
  if (!message) return;

  const chatbox = document.getElementById("chatbox");

  // show user message
  chatbox.innerHTML += `<div class="bot"><b>Bot:</b> ${data.response}</div>`;


  // show temporary bot typing indicator
  const typingId = "typing-" + Date.now();
  chatbox.innerHTML += `<div class="bot" id="${typingId}"><i>Bot is typing...</i></div>`;
  chatbox.scrollTop = chatbox.scrollHeight;

  // send to backend
  try {
    const response = await fetch("http://127.0.0.1:5000/get", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    const data = await response.json();

    // replace typing indicator with actual response
    const typingDiv = document.getElementById(typingId);
    if (typingDiv) {
      typingDiv.outerHTML = `<div class="bot"><b>Bot:</b> ${data.response}</div>`;
    }
  } catch (err) {
    // handle error
    const typingDiv = document.getElementById(typingId);
    if (typingDiv) {
      typingDiv.outerHTML = `<div class="bot"><b>Bot:</b> Sorry, something went wrong.</div>`;
    }
    console.error("Chat error:", err);
  }

  // auto scroll
  chatbox.scrollTop = chatbox.scrollHeight;

  // clear input
  input.value = "";
}
