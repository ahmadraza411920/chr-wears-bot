from flask import Flask, request, jsonify, render_template_string
from google import genai
from google.genai import types

app = Flask(__name__)

# API Key
GEMINI_API_KEY = "AQ.Ab8RN6Jnyad3lsR_R-Myx5OJnU3Uxg5Rs3Y6VV2UtreIW3j0Qg"
client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_INSTRUCTION = """
Aap CHR Wears ke AI Customer Support Assistant hain. 
Aap ka kaam clients ko hamare kapron ke baray mein polite aur helpful tariqay se jawab dena hai.

Business Details & Pricing:
1. Products & Prices:
   - Premium Khaddar Suit: Rs. 2,600
   - Aura Cotton Suit: Rs. 2,650
   - Wash and Wear Suit: Rs. 2,750
   - Karandi (Light Yellow/Off-white tone) & other unstitched fabrics available.
2. Delivery & Shipping: Delivery time 3-5 working days hai. Shipping FREE hai (Har order par Delivery charges Zero hain). Kisi bhi courier service ka naam nahi lena.
3. Payment Methods: Cash on Delivery (COD), JazzCash, EasyPaisa, Bank Transfer.
4. Return Policy: 7 days return/exchange policy agar fabric damaged ho.

Rules:
- Shipping charges ka poocha jaye toh hamesha kahein ke "Delivery bilkul FREE hai".
- Kisi courier service (jaise M&P wagerah) ka naam bilkul nahi lena.
- Hamesha Roman Urdu ya Urdu mein baat karein. Jawab chota, to-the-point aur khush-akhlaqi se dein.
"""

HTML_CODE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CHR Wears - AI Support</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .chat-container { width: 380px; height: 500px; background: white; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); display: flex; flex-direction: column; overflow: hidden; }
        .chat-header { background: #111827; color: white; padding: 15px; text-align: center; font-weight: bold; }
        .chat-box { flex: 1; padding: 15px; overflow-y: auto; display: flex; flex-direction: column; gap: 10px; }
        .message { padding: 10px 14px; border-radius: 8px; max-width: 75%; word-wrap: break-word; font-size: 14px; }
        .user-msg { background: #007bff; color: white; align-self: flex-end; }
        .bot-msg { background: #e5e7eb; color: #1f2937; align-self: flex-start; }
        .input-area { display: flex; border-top: 1px solid #ddd; }
        input { flex: 1; padding: 12px; border: none; outline: none; }
        button { background: #007bff; color: white; border: none; padding: 12px 18px; cursor: pointer; }
    </style>
</head>
<body>

<div class="chat-container">
    <div class="chat-header">CHR Wears Assistant</div>
    <div class="chat-box" id="chatBox">
        <div class="message bot-msg">Assalam-o-Alaikum! Main CHR Wears se hun. Main aap ki kya madad kar sakta hun?</div>
    </div>
    <div class="input-area">
        <input type="text" id="userInput" placeholder="Sawal pūchein...">
        <button onclick="sendMessage()">Send</button>
    </div>
</div>

<script>
    async function sendMessage() {
        let inputField = document.getElementById("userInput");
        let chatBox = document.getElementById("chatBox");
        let message = inputField.value.trim();

        if (message === "") return;

        chatBox.innerHTML += `<div class="message user-msg">${message}</div>`;
        inputField.value = "";
        chatBox.scrollTop = chatBox.scrollHeight;

        let response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        });

        let data = await response.json();
        chatBox.innerHTML += `<div class="message bot-msg">${data.response}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    }
</script>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_CODE)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    
    if not user_message:
        return jsonify({"response": "Mehrbani karke koi sawal pūchein."})

    try:
        response = client.models.generate_content(
            model='gemini-3.6-flash',
            contents=user_message,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.3,
            )
        )
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)