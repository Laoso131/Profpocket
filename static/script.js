async function send() {

  let input = document.getElementById("msg")
  let msg = input.value
  if (!msg) return

  document.getElementById("chat").innerHTML += `
    <div class="msg user">👤 ${msg}</div>
  `

  input.value = ""

  let res = await fetch("/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message: msg})
  })

  let data = await res.json()

  document.getElementById("chat").innerHTML += `
    <div class="msg bot">🤖 ${data.reply}</div>
  `
}

function newChat(){
  document.getElementById("chat").innerHTML = ""
}
