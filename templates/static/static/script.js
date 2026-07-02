async function send() {

    let input = document.getElementById("msg")
    let msg = input.value

    if (!msg) return

    document.getElementById("chat-box").innerHTML += `
        <div class="msg">👤 ${msg}</div>
    `

    let res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: msg })
    })

    let data = await res.json()

    document.getElementById("chat-box").innerHTML += `
        <div class="msg">🤖 ${data.reply}</div>
    `

    input.value = ""
}
