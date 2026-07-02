async function send() {

  let msg = document.getElementById("msg").value;
  if (!msg) return;

  document.getElementById("chat").innerHTML += `<div class="msg"><b>You:</b> ${msg}</div>`;

  const eventSource = new EventSourcePolyfill("/stream", {
    method: "POST",
    body: JSON.stringify({message: msg}),
    headers: {"Content-Type": "application/json"}
  });

  let aiBox = document.createElement("div");
  aiBox.className = "msg";
  aiBox.innerHTML = "<b>AI:</b> ";
  document.getElementById("chat").appendChild(aiBox);

  eventSource.onmessage = function(event) {
    aiBox.innerHTML += event.data.replaceAll('"','');
  };
}

function addMsg(type, text) {
  document.getElementById("chat").innerHTML += `
    <div class="msg ${type}">${text}</div>
  `
}

async function loadHistory() {
  let res = await fetch("/history")
  let data = await res.json()

  document.getElementById("chat").innerHTML = ""

  data.forEach(m => {
    addMsg("user", m[0])
    addMsg("bot", m[1])
  })
}

function newChat() {
  document.getElementById("chat").innerHTML = ""
}
