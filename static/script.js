let chatBox = document.getElementById("chat");

// ======================
// ADD MESSAGE
// ======================
function addMessage(text, type) {
    let div = document.createElement("div");
    div.classList.add("msg");
    div.classList.add(type);

    div.innerText = text;

    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// ======================
// TYPING EFFECT (AI)
// ======================
function typingEffect(text, callback) {

    let i = 0;
    let temp = "";

    let interval = setInterval(() => {

        if (i < text.length) {
            temp += text[i];
            chatBox.lastChild.innerText = temp;
            i++;
        } else {
            clearInterval(interval);
            if (callback) callback();
        }

    }, 20);
}

// ======================
// SEND MESSAGE
// ======================
async function send() {

    let input = document.getElementById("msg");
    let text = input.value;

    if (!text) return;

    // user message
    addMessage(text, "user");

    input.value = "";

    // placeholder AI message
    addMessage("...", "ai");

    try {

        let res = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text })
        });

        let data = await res.json();

        // replace last message (AI)
        chatBox.lastChild.innerText = "";

        let reply = data.reply || "Erreur IA";

        typingEffect(reply);

    } catch (err) {
        chatBox.lastChild.innerText = "Erreur serveur";
    }
}

// ======================
// ENTER TO SEND
// ======================
document.addEventListener("keydown", function(e) {
    if (e.key === "Enter") {
        send();
    }
});
async function search() {
    const input = document.querySelector(".search-input").value;

    const res = await fetch("/search", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ query: input })
    });

    const data = await res.json();
    console.log(data);
}
