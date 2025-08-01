const emotionSuggestions = {
    angry: "Take a deep breath 😊",
    sad: "It's okay, better days are ahead 💪",
    happy: "Keep smiling! 😄",
    neutral: "Stay calm and carry on 😌",
    surprise: "Whoa! Hope it's good news! 😲",
    fear: "Everything will be fine 🫂",
    disgust: "Take a break and refresh 🌿"
};

function updateSuggestion(emotion) {
    const text = emotionSuggestions[emotion] || "You’re doing great! 💖";
    const box = document.getElementById("suggestion-text");
    box.innerText = text;
}

function stopMusic() {
    fetch("/stop", {
        method: "POST"
    });
}

// Optional: Auto update suggestion box every few seconds with current emotion
setInterval(() => {
    fetch("/")
        .then(res => res.text())
        .then(html => {
            const match = html.match(/emotion="(.*?)"/);
            if (match && match[1]) {
                updateSuggestion(match[1]);
            }
        });
}, 4000);
