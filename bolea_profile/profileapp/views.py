from django.http import HttpResponse

def profile_view(request):
    
    my_name = "Christian Bolea" 
    my_course = "Bachelor of Science in Information Technology"
    
    q1_answer = "Using HttpResponse for large projects is messy. Mixing Python and HTML makes code difficult to read, debug, and maintain."
    q2_answer = "Django normally handles HTML using 'Templates' (separate .html files) and the render() function."
    q3_answer = "Templates allow us to separate design (HTML) from logic (Python), enabling code reuse and cleaner project structure."

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{my_name}'s Profile</title>
    </head>
    <body>

        <div class="container">
            <div class="profile-header">
                <img src="https://i.pinimg.com/736x/c2/2f/dd/c22fddb5fc540b0d525af870e00c39f9.jpg" alt="no image?" class="profile-img">
                
                <h1>{my_name}</h1>
                <p><strong>Course:</strong> {my_course}</p>
                
                <button onclick="toggleDarkMode()">Toggle Dark Mode</button>
                <button onclick="createEmojiRain()">🥳 Make it Rain!</button>
                
            </div>

            <div class="reflection-section">
                <h2>Reflection Section</h2>
                
                <p class="question">1. Why is using HttpResponse alone not ideal for large projects?</p>
                <p class="ans">{q1_answer}</p>
                
                <p class="question">2. How does Django normally handle HTML rendering?</p>
                <p class="ans">{q2_answer}</p>
                
                <p class="question">3. What advantages do templates provide?</p>
                <p class="ans">{q3_answer}</p>
            </div>
        </div>

        <script>
            function toggleDarkMode() {{
                var element = document.body;
                element.classList.toggle("dark-mode");
            }}

            function createEmojiRain() {{
                const emojis = ['🚀', '💻', '🐍', '🔥', '✨', '🎉', '😎', '👾', '💯', '🍕', '🤖'];
                const container = document.body;
                
                for (let i = 0; i < 30; i++) {{
                    const emoji = document.createElement('div');
                    emoji.innerText = emojis[Math.floor(Math.random() * emojis.length)];
                    emoji.classList.add('falling-emoji');
                    
                    emoji.style.left = Math.random() * 100 + "vw";
                    emoji.style.animationDuration = (Math.random() * 2 + 3) + "s"; 
                    emoji.style.fontSize = (Math.random() * 20 + 20) + "px";
                    
                    container.appendChild(emoji);
                    
                    setTimeout(() => {{
                        emoji.remove();
                    }}, 5000);
                }}
            }}
        </script>

        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #2c3e50;
                background-image: url("https://jooinn.com/images/sunny-1.jpg");
                background-repeat: no-repeat;
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
                color: #333;
                margin: 0;
                padding: 20px;
                display: flex;
                flex-direction: column;
                align-items: center;
                transition: background-color 0.5s, color 0.5s;
                overflow-x: hidden;
            }}
            .container {{
                background: white;
                width: 80%;
                max-width: 800px;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                margin-bottom: 20px;
                position: relative;
                z-index: 10;
            }}
            .profile-header {{
                text-align: center;
                border-bottom: 2px solid #f0f0f0;
                padding-bottom: 20px;
                margin-bottom: 20px;
            }}
            .profile-img {{
                width: 150px;
                height: 150px;
                border-radius: 50%;
                object-fit: cover;
                border: 4px solid #3498db;
                margin-bottom: 15px;
            }}
            h1 {{ color: #2c3e50; margin: 10px 0; }}
            h2 {{ color: #3498db; margin-top: 0; }}
            
            .reflection-section {{
                background-color: #f9f9f9;
                padding: 20px;
                border-left: 5px solid #3498db;
                margin-top: 30px;
            }}
            .question {{ font-weight: bold; color: #d35400; margin-top: 15px; }}
            
            button {{
                padding: 10px 20px;
                margin: 5px;
                cursor: pointer;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                position: relative;
                z-index: 20;
            }}
            button:hover {{ background-color: #2980b9; }}
            
            .falling-emoji {{
                position: fixed;
                top: -50px;
                user-select: none;
                pointer-events: none;
                z-index: 9999;
                animation-name: fall;
                animation-timing-function: linear;
            }}

            @keyframes fall {{
                0% {{
                    transform: translateY(0) rotate(0deg);
                    opacity: 1;
                }}
                100% {{
                    transform: translateY(110vh) rotate(360deg);
                    opacity: 0;
                }}
            }}

            .dark-mode {{
                background-color: #2c3e50;
                background-image: url("https://4kwallpapers.com/images/wallpapers/starry-sky-northern-lights-dark-night-landscape-cold-5k-1920x1200-1834.jpg");
                background-repeat: no-repeat;
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            .dark-mode .container {{
                background-color: #34495e;
                color: #ecf0f1;
            }}
            
            .dark-mode h1 {{ color: #ecf0f1; }}
            .dark-mode .ans {{ color: #000000; }}
        </style>
    </body>
    </html>
    """
    
    return HttpResponse(html_content)