from django.http import HttpResponse

shared_css = """
    <link href='https://fonts.googleapis.com/css?family=Lato' rel='stylesheet'>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">

    <style>
        body {
            font-family: 'Lato', sans-serif;
            background: linear-gradient(to right, #000000, #00213f, #000000);
            color: white;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            overflow-x: hidden;
        }

        .container {
            background-color: rgba(0, 33, 63, 0.5); 
            backdrop-filter: blur(6.5px);           
            border: 1.3px solid #008cff;            
            width: 90%;
            max-width: 900px;
            padding: 40px;
            border-radius: 13px;
            box-shadow: 0 5.2px 13px rgba(0, 0, 0, 0.3);
            margin-bottom: 30px;
            text-align: center;
            position: relative;
            z-index: 10;
        }

        h1 { font-size: 3rem; margin-bottom: 10px; font-weight: bold; }
        h2 { color: #008cff; margin-top: 0; font-size: 1.5rem; letter-spacing: 2px; }
        h3 { color: #008cff; border-bottom: 1px solid #008cff; display: inline-block; padding-bottom: 10px; margin-top: 40px; }
        p { font-size: 1.1rem; line-height: 1.6; }

        .profile-img {
            width: 180px;
            height: 180px;
            border-radius: 50%;
            border: 4px solid #008cff;
            object-fit: cover;
            box-shadow: 0 0 20px rgba(0, 140, 255, 0.4);
            margin-bottom: 20px;
            opacity: 0; 
            transform: scale(0.95);
            transition: opacity 0.6s ease-out, transform 0.6s ease-out;
        }
        .profile-img.in-view { opacity: 1; transform: scale(1); }

        button {
            padding: 12px 30px;
            margin: 10px;
            cursor: pointer;
            border-radius: 65px;
            font-size: 1rem;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .btn-primary {
            background-color: #008cff;
            color: white;
            border: none;
            box-shadow: 0 5px 15px rgba(0, 140, 255, 0.4);
        }
        .btn-primary:hover { transform: translateY(-3px); background-color: #007bbd; }
        
        .btn-secondary {
            background: transparent;
            border: 2px solid white;
            color: white;
        }
        .btn-secondary:hover { background-color: white; color: #00213f; transform: translateY(-3px); }

        .skills-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .skill-card {
            background-color: rgba(0, 33, 63, 0.6);
            border: 1px solid #008cff;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            transition: opacity 0.6s ease-out, transform 0.6s ease-out;
            opacity: 0;
            transform: translateY(26px);
        }
        .skill-card.in-view { opacity: 1; transform: translateY(0); }
        .skill-card:hover { background-color: rgba(0, 140, 255, 0.2); }
        .skill-icon { font-size: 40px; color: #008cff; margin-bottom: 10px; }

        .achievement-item {
            background-color: rgba(0, 33, 63, 0.4);
            border-left: 4px solid #008cff;
            padding: 20px;
            margin-bottom: 20px;
            text-align: left;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 20px;
            opacity: 0;
            transform: translateY(26px);
            transition: opacity 0.6s ease-out, transform 0.6s ease-out;
        }
        .achievement-item.in-view { opacity: 1; transform: translateY(0); }
        
        .achievement-img {
            width: 100px;
            height: 100px;
            object-fit: cover;
            border-radius: 8px;
            border: 1px solid #008cff;
            flex-shrink: 0; 
        }
        
        .achievement-content { flex-grow: 1; }
        .achievement-title { color: #008cff; font-weight: bold; font-size: 1.2rem; margin-bottom: 5px; }
        .achievement-desc { font-size: 0.95rem; color: #e0e0e0; }
        
        .question { color: #008cff; font-weight: bold; margin-top: 20px; text-align: left; }
        .ans { text-align: left; color: #ddd; margin-bottom: 15px; border-left: 2px solid #555; padding-left: 15px; }

        .footer {
            margin-top: 40px;
            padding: 20px;
            text-align: center;
            font-size: 0.9rem;
            color: rgba(255, 255, 255, 0.7);
            border-top: 1px solid rgba(0, 140, 255, 0.3);
            width: 100%;
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
    </style>
"""

shared_script = """
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const observerOptions = {
                root: null,
                rootMargin: '0px',
                threshold: 0.1
            };

            const observerCallback = (entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        // Element enters screen: Add class to animate IN
                        entry.target.classList.add('in-view');
                    } else {
                        // Element leaves screen: Remove class to reset animation
                        entry.target.classList.remove('in-view');
                    }
                });
            };

            const observer = new IntersectionObserver(observerCallback, observerOptions);

            const animatedElements = document.querySelectorAll('.profile-img, .skill-card, .achievement-item');
            animatedElements.forEach(element => {
                observer.observe(element);
            });
        });

        function emojirain() {
            const emojis = ['🚀', '💻', '🐍', '🔥', '✨', '🎉', '😎', '👾', '💯', '🍕', '🤖'];
            const container = document.body;
            
            for (let i = 0; i < 40; i++) {
                const emoji = document.createElement('div');
                emoji.innerText = emojis[Math.floor(Math.random() * emojis.length)];
                emoji.classList.add('falling-emoji');
                
                emoji.style.left = Math.random() * 100 + "vw";
                emoji.style.animationDuration = (Math.random() * 1 + 1) + "s";
                emoji.style.fontSize = (Math.random() * 20 + 20) + "px";
                
                container.appendChild(emoji);
                setTimeout(() => { emoji.remove(); }, 2000);
            }
        }
    </script>
"""

def profile_view(request):
    my_name = "Christian Louis Bolea" 
    my_course = "3RD YEAR - BSIT"
    my_bio = "Aspiring Web & Mobile Developer dedicated to building high-performance applications with a keen eye for design. Focused on transforming concepts into seamless, user-friendly digital solutions."

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{my_name}'s Profile</title> 
        {shared_css} 
    </head>
    <body>
        <div class="container">
            <img src="https://i.pinimg.com/736x/c2/2f/dd/c22fddb5fc540b0d525af870e00c39f9.jpg" class="profile-img">
            <h1>{my_name}</h1>
            <h2>{my_course}</h2>
            <p>{my_bio}</p>
            
            <button class="btn-primary" onclick="emojirain()">🥳 Make it Rain!</button>
            <a href="/reflection/"><button class="btn-secondary">View Reflection ➡️</button></a>

            <h3>MY SKILLS</h3>
            <div class="skills-grid">
                <div class="skill-card"><i class="fab fa-html5 skill-icon"></i><br>HTML5</div>
                <div class="skill-card"><i class="fab fa-css3-alt skill-icon"></i><br>CSS</div>
                <div class="skill-card"><i class="fab fa-js-square skill-icon"></i><br>JavaScript</div>
                <div class="skill-card"><i class="fab fa-python skill-icon"></i><br>Python</div>
                <div class="skill-card"><i class="fab fa-java skill-icon"></i><br>Java</div>
                <div class="skill-card"><i class="fab fa-git-alt skill-icon"></i><br>Git</div>
                <div class="skill-card"><i class="fas fa-mobile-alt skill-icon"></i><br>Flutter</div>
            </div>

            <h3>MY ACHIEVEMENTS</h3>
            <div style="margin-top: 20px;">
                <div class="achievement-item">
                    <img src="https://s3.amazonaws.com/coursera_assets/meta_images/generated/CERTIFICATE_LANDING_PAGE/CERTIFICATE_LANDING_PAGE~RU6NWZOOYURW/CERTIFICATE_LANDING_PAGE~RU6NWZOOYURW.jpeg" class="achievement-img">
                    <div class="achievement-content">
                        <div class="achievement-title">Flutter and Dart Certification</div>
                        <div class="achievement-desc">Developing iOS, Android, and Mobile Apps</div>
                    </div>
                </div>
                <div class="achievement-item">
                    <img src="https://placehold.co/100x100/00213f/008cff?text=CCNA" class="achievement-img">
                    <div class="achievement-content">
                        <div class="achievement-title">CCNAv7: Introduction to Networks</div>
                        <div class="achievement-desc">Cisco Networking Academy Certification</div>
                    </div>
                </div>
                <div class="achievement-item">
                    <img src="https://s3.amazonaws.com/coursera_assets/meta_images/generated/CERTIFICATE_LANDING_PAGE/CERTIFICATE_LANDING_PAGE~0TK79ZXOQLGX/CERTIFICATE_LANDING_PAGE~0TK79ZXOQLGX.jpeg" class="achievement-img">
                    <div class="achievement-content">
                        <div class="achievement-title">Generative AI for Students</div>
                        <div class="achievement-desc">Ethics & Academic Integrity Certification</div>
                    </div>
                </div>
                <div class="achievement-item">
                    <img src="https://s3.amazonaws.com/coursera_assets/meta_images/generated/CERTIFICATE_LANDING_PAGE/CERTIFICATE_LANDING_PAGE~3IUYK1X5KD8B/CERTIFICATE_LANDING_PAGE~3IUYK1X5KD8B.jpeg"class="achievement-img">
                    <div class="achievement-content">
                        <div class="achievement-title">Operating System Virtualization - Bachelor's</div>
                        <div class="achievement-desc">For operating virtual machines</div>
                    </div>
                </div>
                <div class="achievement-item">
                    <img src="https://s3.amazonaws.com/coursera_assets/meta_images/generated/CERTIFICATE_LANDING_PAGE/CERTIFICATE_LANDING_PAGE~HR9975CURUKN/CERTIFICATE_LANDING_PAGE~HR9975CURUKN.jpeg"class="achievement-img">
                    <div class="achievement-content">
                        <div class="achievement-title">Introduction to Object-Oriented Programming with Java</div>
                        <div class="achievement-desc">Proper understing on OOP with java</div>
                    </div>
                </div>
                <div class="achievement-item">
                    <img src="https://s3.amazonaws.com/coursera_assets/meta_images/generated/CERTIFICATE_LANDING_PAGE/CERTIFICATE_LANDING_PAGE~XKDZ8Z1QMUMY/CERTIFICATE_LANDING_PAGE~XKDZ8Z1QMUMY.jpeg"class="achievement-img">
                    <div class="achievement-content">
                        <div class="achievement-title">Advanced MySQL Topics</div>
                        <div class="achievement-desc">Building and designing databases</div>
                    </div>
                </div>
                <div class="achievement-item">
                    <img src="https://s3.amazonaws.com/coursera_assets/meta_images/generated/CERTIFICATE_LANDING_PAGE/CERTIFICATE_LANDING_PAGE~Z434HWP2AB1K/CERTIFICATE_LANDING_PAGE~Z434HWP2AB1K.jpeg"class="achievement-img">
                    <div class="achievement-content">
                        <div class="achievement-title">Single Page Web Applications with AngularJS</div>
                        <div class="achievement-desc">Building and designing web applications with AngularJS</div>
                    </div>
                </div>
            </div>
        </div>

        <footer class="footer">
            &copy; profileapp | {my_name}
        </footer>

        {shared_script}
    </body>
    </html>
    """
    return HttpResponse(html_content)

def reflection(request):
    q1 = "Writing HTML directly inside HttpResponse forces you to mix your website's design with your Python programming logic, which creates a messy and confusing file. This makes it very difficult to read or fix errors later on, especially in larger projects where keeping your code organized is essential."
    q2 = "Instead of writing raw HTML code inside Python functions, Django uses a system called 'Templates,' which are just standard HTML files stored in a separate folder. When a user requests a page, we use Django's built-in render() function to load these specific HTML files and display them to the browser."
    q3 = "Templates allow us to keep the 'front-end' design completely separate from the 'back-end' Python logic, ensuring that changes to the look of the site don't accidentally break the code. This separation makes the project structure much cleaner and allows us to reuse common layout elements, like headers and footers, across multiple pages."

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Reflection</title> 
        {shared_css} 
    </head>
    <body>
        <div class="container">
            <h1>Reflection Section</h1>
            
            <p class="question">1. Why is using HttpResponse alone not ideal?</p>
            <p class="ans">{q1}</p>
            
            <p class="question">2. How does Django normally handle HTML?</p>
            <p class="ans">{q2}</p>
            
            <p class="question">3. What advantages do templates provide?</p>
            <p class="ans">{q3}</p>
            
            <br>
            <a href="/"><button class="btn-primary">⬅️ Back to Profile</button></a>
        </div>

        <footer class="footer">
            &copy; profileapp | Christian Louis Bolea
        </footer>
        
        {shared_script}
    </body>
    </html>
    """
    return HttpResponse(html_content)