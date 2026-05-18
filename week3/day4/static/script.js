async function startChat() {
    await fetch("http://127.0.0.1:8000/start", {
        method: "POST"
    });
}

async function sendMessage() {
    let input = document.getElementById("input").value;

    let res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: input})
    });

    let data = await res.json();
    
    let chat = document.getElementById("chat");
    chat.innerHTML += `<p><b>You:</b> ${input}</p>`;
    chat.innerHTML += `<p><b>AI:</b> ${data.response}</p>`;
}