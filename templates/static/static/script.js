async function sendMessage(){

let msg=
document
.getElementById(
"message"
).value

if(!msg)return

let r=
await fetch(
"/chat",
{

method:"POST",

headers:{
"Content-Type":
"application/json"
},

body:
JSON.stringify({
message:msg
})

}

)

let data=
await r.json()

document
.getElementById(
"messages"
)
.innerHTML+=
`
<div class="bubble">

${data.reply}

</div>
`

}

async function sendPhoto(){

let file=
document
.getElementById(
"photo"
)
.files[0]

if(!file)return

let form=
new FormData()

form.append(
"image",
file
)

await fetch(
"/upload",
{

method:"POST",

body:form

}

)

alert(
"Photo envoyée"
)

}
