async function send(){
    let msg = document.getElementById("msg").value

    let res = await fetch("/chat", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({message:msg})
    })

    let data = await res.json()

    document.getElementById("chat").innerHTML += `
        <div>👤 ${msg}</div>
        <div>🤖 ${data.reply}</div>
    `
}

async function register(){
    await fetch("/register",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            username:document.getElementById("u").value,
            password:document.getElementById("p").value
        })
    })
}

async function login(){
    await fetch("/login",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({
            username:document.getElementById("u").value,
            password:document.getElementById("p").value
        })
    })
}
