async function send() {

  let input = document.getElementById("msg")
  let msg = input.value
  if (!msg) return

  addMsg("user", msg)
  input.value = ""

  let res = await fetch("/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message: msg})
  })

  let data = await res.json()

  addMsg("bot", data.reply)
}

function addMsg(type, text) {
  document.getElementById("chat").innerHTML += `
    <div class="msg ${type}">
      ${text}
    </div>
  `
}

function newChat() {
  document.getElementById("chat").innerHTML = ""
}

async function loadHistory() {
  let res = await fetch("/history")
  let data = await res.json()

  document.getElementById("chat").innerHTML = ""

  data.reverse().forEach(m => {
    addMsg("user", m[1])
    addMsg("bot", m[2])
  })
}
