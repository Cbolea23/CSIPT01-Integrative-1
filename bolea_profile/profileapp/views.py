from django.http import HttpResponse

def profile_view(request):
    
    my_name = "Christian Bolea" 
    my_course = "Bachelor of Science in Information Technology"
    
    q1_answer = "Using HttpResponse for large projects is messy and hard to maintain. Mixing Python and HTML makes code difficult to read, debug, and format."
    q2_answer = "Django normally handles HTML using 'Templates' (separate .html files) and the render() function."
    q3_answer = "Templates allow us to separate design (HTML) from logic (Python). They also allow code reusability (like headers/footers) and provide cleaner syntax."

   
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
                <button onclick="displayGreeting()">Show Greeting</button>
                
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
            // FUNCTION 1: Toggles Dark Mode styling
            function toggleDarkMode() {{
                var element = document.body;
                element.classList.toggle("dark-mode");
            }}

            // FUNCTION 2: Displays a dynamic greeting based on time
            function displayGreeting() {{
                const hour = new Date().getHours();
                let greeting;
                if (hour < 12) {{
                    greeting = "Good Morning, {my_name}!";
                }} else if (hour < 18) {{
                    greeting = "Good Afternoon, {my_name}!";
                }} else {{
                    greeting = "Good Evening, {my_name}!";
                }}
                document.getElementById("greeting-text").innerText = greeting;
                alert(greeting);
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
            }}
            .container {{
                background: white;
                width: 80%;
                max-width: 800px;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 10px 25px rgba(0,0,0,0.1);
                margin-bottom: 20px;
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
            }}
            button:hover {{ background-color: #2980b9; }}
            
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