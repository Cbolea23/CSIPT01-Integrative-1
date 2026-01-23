from django.http import HttpResponse

shared_css = """
    <style>
        body {
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
            min-height: 100vh;
            overflow-x: hidden;
        }

        .container {
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(10px);
            width: 80%;
            max-width: 800px;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
            margin-bottom: 20px;
            text-align: center;
            position: relative;
            z-index: 10;
        }

        h1 { color: #2c3e50; }
        h2 { color: #3498db; }
        
        button {
            padding: 10px 20px;
            margin: 10px;
            cursor: pointer;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            transition: transform 0.1s;
        }
        button:hover { background-color: #2980b9; transform: scale(1.05); }
        a { text-decoration: none; }

        .question { font-weight: bold; color: #d35400; margin-top: 15px; text-align: left;}
        .ans { text-align: left; margin-bottom: 20px;}
        
        .profile-img {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            border: 4px solid #3498db;
            object-fit: cover;
        }

        .falling-emoji {
            position: fixed;
            top: -50px;
            user-select: none;
            pointer-events: none;
            z-index: 9999;
            animation-name: fall;
            animation-timing-function: linear;
        }
        @keyframes fall {
            0% { transform: translateY(0) rotate(0deg); opacity: 1; }
            100% { transform: translateY(110vh) rotate(360deg); opacity: 0; }
        }

        .dark-mode {
            background-color: #2c3e50;
            background-image: url("https://4kwallpapers.com/images/wallpapers/starry-sky-northern-lights-dark-night-landscape-cold-5k-1920x1200-1834.jpg") !important;
            background-repeat: no-repeat !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
        }
        
        .dark-mode .container {
            background-color: #34495e;
            color: #ecf0f1;
            box-shadow: none;
        }
        
        .dark-mode h1 { color: #ecf0f1; }
        .dark-mode .ans { color: #ecf0f1; }
    </style>
"""

def profile_view(request):
    my_name = "Christian Louis Bolea" 
    my_course = "Bachelor of Science in Information Technology"
    my_desc = "Aspiring Web & Mobile Developer dedicated to building high-performance applications with a keen eye for design. Focused on transforming concepts into seamless, user-friendly digital solutions."

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><title>{my_name}'s Profile</title> {shared_css} </head>
    <body>
        <div class="container">
            <img src="https://i.pinimg.com/736x/c2/2f/dd/c22fddb5fc540b0d525af870e00c39f9.jpg" class="profile-img">
            <h1>{my_name}</h1>
            <p><strong>Course:</strong> {my_course}</p>
            <p>{my_desc}</p>
            
            <button onclick="nightmode()">Dark Mode</button>
            <button onclick="emojirain()">😊</button>
            
            <br>
            
            <a href="/reflection/">
                <button style="background-color: #e67e22;">Reflection Section</button>
            </a>
        </div>

        <script>
            function nightmode() {{
                var element = document.body;
                element.classList.toggle("dark-mode");
            }}

            function emojirain() {{
                const emojis = ['🚀', '💻', '🐍', '🔥', '✨', '🎉', '😎', '👾', '💯', '🍕', '🤖'];
                const container = document.body;
                
                for (let i = 0; i < 40; i++) {{
                    const emoji = document.createElement('div');
                    emoji.innerText = emojis[Math.floor(Math.random() * emojis.length)];
                    emoji.classList.add('falling-emoji');
                    
                    emoji.style.left = Math.random() * 100 + "vw";
                    emoji.style.animationDuration = (Math.random() * 1 + 1) + "s";
                    emoji.style.fontSize = (Math.random() * 20 + 20) + "px";
                    
                    container.appendChild(emoji);
                    setTimeout(() => {{ emoji.remove(); }}, 2000);
                }}
            }}
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_content)

def reflection(request):
    q1 = "Using HttpResponse alone is messy. It mixes Python logic with HTML design, making code hard to read and impossible to maintain for big projects."
    q2 = "Django normally uses 'Templates'. We write HTML in separate files and use render() to load them."
    q3 = "Templates allow us to separate design (HTML) from logic (Python) and provide cleaner project structure."

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><title>Reflection</title> {shared_css} </head>
    <body>
        <div class="container">
            <h1>Reflection Section</h1>
            
            <p class="question">1. Why is using HttpResponse alone not ideal?</p>
            <p class="ans">{q1}</p>
            
            <p class="question">2. How does Django normally handle HTML?</p>
            <p class="ans">{q2}</p>
            
            <p class="question">3. What advantages do templates provide?</p>
            <p class="ans">{q3}</p>
            
            <a href="/">
                <button>Profile</button>
            </a>
            
            <button onclick="nightmode()">Dark Mode</button>
        </div>
        
        <script>
            function nightmode() {{
                var element = document.body;
                element.classList.toggle("dark-mode");
            }}
        </script>
    </body>
    </html>
    """
    return HttpResponse(html_content)
