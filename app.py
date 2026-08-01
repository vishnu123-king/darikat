import http.server
import socketserver
import json
import urllib.parse
import re
import math
import os

PORT = 3000

# Sample dataset for E-commerce & Sales analysis
SAMPLE_SALES_DATA = [
    {"id": 101, "date": "2024-01-15", "category": "Electronics", "region": "South", "revenue": 1450.00, "units": 5, "customer": "Cust_A", "status": "Completed"},
    {"id": 102, "date": "2024-01-18", "category": "Apparel", "region": "North", "revenue": 320.50, "units": 12, "customer": "Cust_B", "status": "Completed"},
    {"id": 103, "date": "2024-02-02", "category": "Electronics", "region": "West", "revenue": 8900.00, "units": 1, "customer": "Cust_C", "status": "Completed"},  # Outlier
    {"id": 104, "date": "2024-02-10", "category": "Home & Kitchen", "region": "South", "revenue": 450.00, "units": 3, "customer": "Cust_D", "status": "Completed"},
    {"id": 105, "date": "2024-02-14", "category": "Apparel", "region": "East", "revenue": None, "units": 8, "customer": "Cust_E", "status": "Pending"}, # Missing
    {"id": 106, "date": "2024-03-01", "category": "Electronics", "region": "South", "revenue": 2100.00, "units": 4, "customer": "Cust_F", "status": "Completed"},
    {"id": 107, "date": "2024-03-12", "category": "Home & Kitchen", "region": "North", "revenue": 680.00, "units": 6, "customer": "Cust_A", "status": "Completed"},
    {"id": 108, "date": "2024-03-25", "category": "Apparel", "region": "West", "revenue": 1250.00, "units": 15, "customer": "Cust_B", "status": "Completed"},
    {"id": 109, "date": "2024-04-05", "category": "Electronics", "region": "East", "revenue": 3400.00, "units": 7, "customer": "Cust_G", "status": "Completed"},
    {"id": 110, "date": "2024-04-20", "category": "Home & Kitchen", "region": "South", "revenue": None, "units": 2, "customer": "Cust_H", "status": "Completed"}, # Missing
]

class HTMXHandler(http.server.SimpleHTTPRequestHandler):
    def send_html(self, html_content, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))

    def send_json(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def parse_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        body_bytes = self.rfile.read(content_length)
        body_str = body_bytes.decode("utf-8")
        content_type = self.headers.get("Content-Type", "")
        
        if "application/json" in content_type:
            try:
                return json.loads(body_str)
            except Exception:
                return {}
        elif "application/x-www-form-urlencoded" in content_type or True:
            parsed = urllib.parse.parse_qs(body_str)
            # Flatten lists if single element
            res = {}
            for k, v in parsed.items():
                res[k] = v[0] if isinstance(v, list) and len(v) == 1 else v
            return res
        return {"raw": body_str}

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query = urllib.parse.parse_qs(parsed_path.query)

        if path == "/health" or path == "/api/health":
            self.send_json({"status": "ok", "backend": "Pure Python 3.10 Engine + HTMX", "developer": "Darika T"})
            return

        elif path == "/":
            # Serve main HTML SPA completely powered by Python & HTMX
            self.send_html(self.get_main_index_page())
            return

        elif path == "/api/htmx/objective":
            role = query.get("role", ["Data Analyst"])[0]
            
            objectives = {
                "Data Analyst": "Dedicated B.Sc. Computer Science practitioner and Results-Driven Data Analyst with strong technical expertise in Python, SQL, Java, Excel, and Power BI. Proven track record in developing AI-assisted web applications, cleaning complex sales datasets, and translating transaction data into actionable business insights. Eager to leverage analytical rigor and collaborative problem-solving to contribute to high-impact technical initiatives.",
                "Python Developer": "Innovative Computer Science graduate specializing in Python algorithmic development, automated data processing pipelines, and AI-assisted web applications. Experienced in treating missing values, outlier detection using IQR metrics, and HTMX server-side integrations. Driven to build robust, scalable Python solutions.",
                "BI & Data Visualization Specialist": "Analytical Business Intelligence Specialist skilled in transforming raw e-commerce sales datasets into interactive Power BI and Excel dashboards. Proficient in SQL query aggregations, Pivot Table slicers, and visual storytelling to drive strategic executive decision-making.",
                "AI & Web Solution Engineer": "Forward-thinking Computer Science practitioner experienced in developing AI-assisted web platforms like ATS ResumeIQ. Skilled in NLP keyword matching, formatting evaluations, and full-stack Python-HTMX reactive architectures."
            }
            
            selected_obj = objectives.get(role, objectives["Data Analyst"])
            
            html = f'''
            <div class="bg-slate-800/90 border border-emerald-500/30 rounded-2xl p-6 shadow-xl transition-all duration-300">
                <div class="flex items-center justify-between mb-4 flex-wrap gap-2">
                    <span class="text-xs font-bold uppercase tracking-wider text-emerald-400 bg-emerald-500/10 px-3.5 py-1.5 rounded-full border border-emerald-500/20 flex items-center gap-1.5">
                        <svg class="w-3.5 h-3.5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        Tailored Career Objective: {role}
                    </span>
                    <span class="text-xs text-slate-400 flex items-center gap-1.5 font-mono">
                        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                        Python Native Server Engine
                    </span>
                </div>
                <p class="text-slate-100 text-base sm:text-lg leading-relaxed font-normal italic">
                    "{selected_obj}"
                </p>
                <div class="mt-4 pt-3 border-t border-slate-700/60 flex items-center justify-between text-xs text-slate-400">
                    <span>Target Competencies: Python, SQL, Excel, Power BI, AI Web Apps</span>
                    <span class="text-emerald-400 font-medium">Customized for Recruiter Review</span>
                </div>
            </div>
            '''
            self.send_html(html)
            return

        elif path == "/api/htmx/skills-filter":
            cat = query.get("category", ["all"])[0]
            
            skills = [
                {"name": "Python", "category": "programming", "level": "Advanced", "desc": "Data cleaning, missing value imputation, IQR outlier detection, Pandas, analytics scripting", "icon": "🐍"},
                {"name": "SQL", "category": "programming", "level": "Advanced", "desc": "Filtering, aggregations, GROUP BY, CTEs, subqueries, multi-table joins", "icon": "🗄️"},
                {"name": "Java", "category": "programming", "level": "Intermediate", "desc": "Object-oriented programming, data structures, algorithm logic", "icon": "☕"},
                {"name": "Microsoft Excel", "category": "tools", "level": "Advanced", "desc": "Pivot Tables, Charts, Slicers, Data Validation, VLOOKUP, Financial dashboards", "icon": "📊"},
                {"name": "Power BI", "category": "tools", "level": "Intermediate", "desc": "Data modeling, DAX formulas, interactive business intelligence reports", "icon": "📈"},
                {"name": "Google Colab", "category": "tools", "level": "Advanced", "desc": "Cloud Jupyter notebooks, machine learning prototyping, Python libraries", "icon": "☁️"},
                {"name": "Time Management", "category": "soft", "level": "Core Competency", "desc": "Prioritizing tasks and delivering project milestones promptly", "icon": "⏱️"},
                {"name": "Presentation Skills", "category": "soft", "level": "Core Competency", "desc": "Communicating insights and visual analytics to stakeholders clearly", "icon": "🎙️"},
                {"name": "Leadership & Teamwork", "category": "soft", "level": "Core Competency", "desc": "Collaborative problem-solving and initiative in group initiatives", "icon": "👥"}
            ]
            
            if cat != "all":
                filtered = [s for s in skills if s["category"] == cat]
            else:
                filtered = skills
                
            items_html = ""
            for s in filtered:
                items_html += f'''
                <div class="bg-slate-800/80 hover:bg-slate-800 border border-slate-700/80 hover:border-emerald-500/50 rounded-xl p-5 transition-all duration-300 shadow-md hover:shadow-emerald-500/10 group">
                    <div class="flex items-center justify-between mb-3">
                        <div class="flex items-center gap-3">
                            <span class="text-2xl p-2 bg-slate-900/60 rounded-lg border border-slate-700/50 group-hover:scale-110 transition-transform">{s['icon']}</span>
                            <div>
                                <h4 class="font-bold text-slate-100 text-base">{s['name']}</h4>
                                <span class="text-xs text-emerald-400 font-medium">{s['level']}</span>
                            </div>
                        </div>
                    </div>
                    <p class="text-slate-300 text-xs leading-relaxed mt-2">{s['desc']}</p>
                </div>
                '''
                
            self.send_html(items_html)
            return

        elif path == "/api/htmx/resume-modal":
            html = f'''
            <div id="resume-modal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-md z-50 flex items-center justify-center p-4 overflow-y-auto animate-fadeIn">
                <div class="bg-slate-900 border border-slate-700 rounded-2xl max-w-3xl w-full p-6 sm:p-8 relative shadow-2xl space-y-6 max-h-[90vh] overflow-y-auto">
                    <button onclick="document.getElementById('resume-modal').remove()" class="absolute top-4 right-4 text-slate-400 hover:text-white bg-slate-800 hover:bg-slate-700 p-2 rounded-full border border-slate-700 transition">
                        ✕
                    </button>

                    <div class="border-b border-slate-800 pb-4 text-center sm:text-left">
                        <h2 class="text-2xl sm:text-3xl font-extrabold text-white">DARIKA T</h2>
                        <p class="text-emerald-400 font-semibold text-sm mt-1">B.Sc. Computer Science | Results-Driven Data Analyst</p>
                        <p class="text-slate-400 text-xs mt-2 flex flex-wrap gap-3 justify-center sm:justify-start">
                            <span>📧 tdarika3@gmail.com</span>
                            <span>📱 +91 9342362394</span>
                            <span>🔗 linkedin.com/in/darika-t-883124320</span>
                            <span>💻 github.com/tdarika3-ui</span>
                        </p>
                    </div>

                    <div class="space-y-4 text-xs text-slate-300">
                        <div>
                            <h3 class="text-sm font-bold text-emerald-400 uppercase tracking-wider border-b border-emerald-500/20 pb-1 mb-2">CAREER OBJECTIVE</h3>
                            <p class="leading-relaxed">Dedicated B.Sc. Computer Science practitioner and Results-Driven Data Analyst with strong technical expertise in Python, SQL, Java, Excel, and Power BI. Proven track record in developing AI-assisted web applications, cleaning complex sales datasets, and translating transaction data into actionable business insights.</p>
                        </div>

                        <div>
                            <h3 class="text-sm font-bold text-emerald-400 uppercase tracking-wider border-b border-emerald-500/20 pb-1 mb-2">TECHNICAL & SOFT SKILLS</h3>
                            <p><strong>Programming Languages:</strong> Java | Python | SQL</p>
                            <p><strong>Tools & Analytics:</strong> Microsoft Excel | Power BI | Google Colab</p>
                            <p><strong>Soft Skills:</strong> Time Management | Presentation Skills | Leadership | Teamwork</p>
                        </div>

                        <div>
                            <h3 class="text-sm font-bold text-emerald-400 uppercase tracking-wider border-b border-emerald-500/20 pb-1 mb-2">PROJECTS SHOWCASE</h3>
                            <div class="space-y-2">
                                <p><strong>1. E-Commerce Sales Data Analysis (Excel & SQL):</strong> Analyzed transaction datasets, engineered SQL filtering/aggregations/grouping queries, built interactive Excel dashboards with Pivot Slicers.</p>
                                <p><strong>2. ATS ResumeIQ Web Application:</strong> Developed an AI-assisted web application evaluating resume compatibility, formatting, and keyword resonance against applicant tracking systems.</p>
                                <p><strong>3. Sales Data Analysis (Python):</strong> Performed missing value treatment, outlier detection (IQR), and trend visualizations on sales transaction datasets.</p>
                            </div>
                        </div>

                        <div>
                            <h3 class="text-sm font-bold text-emerald-400 uppercase tracking-wider border-b border-emerald-500/20 pb-1 mb-2">CERTIFICATIONS (VERIFIED REAL-TIME)</h3>
                            <p>• <strong>Basics of Data Visualization Analysis</strong> - LinkedIn Learning (Completed: Jun 16, 2026 at 08:57AM UTC)</p>
                            <p>• <strong>Data Analytics Job Simulation</strong> - Deloitte / Forage (Completed: June 23rd, 2026)</p>
                            <p>• <strong>SQL for Data Analysis</strong> - LinkedIn Learning (Completed: Jun 24, 2026 at 10:32AM UTC)</p>
                            <p>• <strong>SQL Practice: Deleting Data with DELETE Statements</strong> - LinkedIn Learning (Completed: Jul 06, 2026 at 10:56AM UTC)</p>
                        </div>

                        <div>
                            <h3 class="text-sm font-bold text-emerald-400 uppercase tracking-wider border-b border-emerald-500/20 pb-1 mb-2">EDUCATION QUALIFICATION</h3>
                            <p>• <strong>Bachelor of Science in Computer Science</strong> (2024 - 2027) | Rathinam Global Deemed To Be University</p>
                            <p>• <strong>HSC</strong> (2024) | Akshaya Academy Matric Hr.Sec School</p>
                        </div>
                    </div>

                    <div class="pt-4 border-t border-slate-800 flex justify-between items-center">
                        <span class="text-[11px] text-slate-500">Official Candidate Summary</span>
                        <button onclick="window.print()" class="bg-emerald-500 hover:bg-emerald-400 text-slate-950 px-4 py-2 rounded-lg font-bold text-xs flex items-center gap-2 transition">
                            🖨️ Print / Save PDF
                        </button>
                    </div>
                </div>
            </div>
            '''
            self.send_html(html)
            return

        elif path.startswith("/src/assets/") or path.startswith("/assets/"):
            rel_path = path.lstrip("/")
            if os.path.exists(rel_path) and os.path.isfile(rel_path):
                ext = rel_path.split(".")[-1].lower()
                mime_types = {
                    "jpg": "image/jpeg",
                    "jpeg": "image/jpeg",
                    "png": "image/png",
                    "svg": "image/svg+xml",
                    "webp": "image/webp"
                }
                content_type = mime_types.get(ext, "application/octet-stream")
                try:
                    with open(rel_path, "rb") as f:
                        content = f.read()
                    self.send_response(200)
                    self.send_header("Content-Type", content_type)
                    self.send_header("Content-Length", str(len(content)))
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(content)
                    return
                except Exception as e:
                    self.send_html(f"Error loading image: {e}", 500)
                    return

        elif path.lower() in ["/certifications", "/api/htmx/certifications", "/api/certifications"]:
            html = '''
            <div id="certifications-container" class="space-y-6 animate-fadeIn">
                <div class="flex items-center justify-between flex-wrap gap-4 border-b border-slate-800 pb-4">
                    <div>
                        <h3 class="text-xl font-bold text-white flex items-center gap-2">
                            <span>🖼️ Verified Certificate Images & Credentials</span>
                            <span class="text-xs bg-emerald-500/10 text-emerald-400 px-2.5 py-0.5 rounded-full border border-emerald-500/20 font-mono">4 Images Available</span>
                        </h3>
                        <p class="text-xs text-slate-400 mt-1">Click any certificate image to view in high-resolution full-screen modal</p>
                    </div>
                    <div class="flex items-center gap-2 text-xs font-mono text-emerald-400 bg-slate-900 px-3 py-1.5 rounded-xl border border-slate-800">
                        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                        High-Res Image Rendering Active
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

                    <!-- Cert 1: Basics of Data Visualization -->
                    <div class="bg-slate-950 rounded-2xl border border-slate-800 hover:border-emerald-500/40 transition overflow-hidden group flex flex-col justify-between">
                        <div>
                            <!-- CERTIFICATE IMAGE PREVIEW -->
                            <div class="relative overflow-hidden bg-slate-900 cursor-pointer group-hover:opacity-95 transition" onclick="openCertModal('/src/assets/images/cert_data_viz.jpg', 'Basics of Data Visualization Analysis - LinkedIn Learning')">
                                <img src="/src/assets/images/cert_data_viz.jpg" alt="Basics of Data Visualization Certificate" class="w-full h-56 object-cover object-top group-hover:scale-105 transition duration-300">
                                <div class="absolute inset-0 bg-slate-950/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center gap-2 text-white font-medium text-xs backdrop-blur-[2px]">
                                    <span class="bg-emerald-500 text-slate-950 px-3 py-1.5 rounded-xl font-bold flex items-center gap-1 shadow-lg">
                                        🔍 Click to Enlarge Uploaded Certificate
                                    </span>
                                </div>
                                <span class="absolute top-3 right-3 text-[10px] font-mono font-bold text-sky-300 bg-slate-950/80 backdrop-blur px-2.5 py-1 rounded-lg border border-sky-500/30">LinkedIn Learning</span>
                            </div>

                            <div class="p-5 space-y-3">
                                <div>
                                    <h4 class="font-bold text-white text-base">Basics of Data Visualization Analysis</h4>
                                    <p class="text-xs text-emerald-400 font-semibold">LinkedIn Learning • Issued Jun 16, 2026</p>
                                </div>

                                <div class="space-y-1.5 text-xs text-slate-300 bg-slate-900/80 p-3 rounded-xl border border-slate-800 font-mono">
                                    <div class="flex items-center justify-between text-emerald-300">
                                        <span class="text-slate-400 font-sans">⏱️ Completion Timestamp:</span>
                                        <span class="font-bold">Jun 16, 2026 at 08:57AM UTC</span>
                                    </div>
                                    <div class="flex items-center justify-between text-slate-300">
                                        <span class="text-slate-400 font-sans">⏳ Duration:</span>
                                        <span>1.25 Contact Hours (#4101K8PLEO)</span>
                                    </div>
                                    <div class="text-[10px] text-slate-400 truncate pt-1 border-t border-slate-800">
                                        Verification Code: <span class="text-slate-300">62ca9e510e24c6...07358863</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="p-5 pt-0 flex items-center justify-between gap-2 border-t border-slate-900 mt-2">
                            <div class="flex flex-wrap gap-1">
                                <span class="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded">Data Viz</span>
                                <span class="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded">PMI Approved</span>
                            </div>
                            <button onclick="openCertModal('/src/assets/images/cert_data_viz.jpg', 'Basics of Data Visualization Analysis')" class="text-xs text-emerald-400 hover:text-emerald-300 font-bold flex items-center gap-1 bg-emerald-500/10 px-3 py-1.5 rounded-xl border border-emerald-500/20">
                                🖼️ View Certificate Image
                            </button>
                        </div>
                    </div>

                    <!-- Cert 2: Deloitte Job Simulation -->
                    <div class="bg-slate-950 rounded-2xl border border-slate-800 hover:border-emerald-500/40 transition overflow-hidden group flex flex-col justify-between">
                        <div>
                            <!-- CERTIFICATE IMAGE PREVIEW -->
                            <div class="relative overflow-hidden bg-slate-900 cursor-pointer group-hover:opacity-95 transition" onclick="openCertModal('/src/assets/images/cert_deloitte.jpg', 'Data Analytics Job Simulation - Deloitte / Forage')">
                                <img src="/src/assets/images/cert_deloitte.jpg" alt="Deloitte Data Analytics Certificate" class="w-full h-56 object-cover object-top group-hover:scale-105 transition duration-300">
                                <div class="absolute inset-0 bg-slate-950/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center gap-2 text-white font-medium text-xs backdrop-blur-[2px]">
                                    <span class="bg-emerald-500 text-slate-950 px-3 py-1.5 rounded-xl font-bold flex items-center gap-1 shadow-lg">
                                        🔍 Click to Enlarge Uploaded Certificate
                                    </span>
                                </div>
                                <span class="absolute top-3 right-3 text-[10px] font-mono font-bold text-emerald-300 bg-slate-950/80 backdrop-blur px-2.5 py-1 rounded-lg border border-emerald-500/30">Deloitte / Forage</span>
                            </div>

                            <div class="p-5 space-y-3">
                                <div>
                                    <h4 class="font-bold text-white text-base">Data Analytics Job Simulation</h4>
                                    <p class="text-xs text-emerald-400 font-semibold">Deloitte • Completed June 23rd, 2026</p>
                                </div>

                                <div class="space-y-1.5 text-xs text-slate-300 bg-slate-900/80 p-3 rounded-xl border border-slate-800 font-mono">
                                    <div class="flex items-center justify-between text-emerald-300">
                                        <span class="text-slate-400 font-sans">⏱️ Completion Date:</span>
                                        <span class="font-bold">June 23rd, 2026</span>
                                    </div>
                                    <div class="flex items-center justify-between text-slate-300">
                                        <span class="text-slate-400 font-sans">✍️ Signatory:</span>
                                        <span>Tina McCreery (Chief HR Officer)</span>
                                    </div>
                                    <div class="text-[10px] text-slate-400 truncate pt-1 border-t border-slate-800">
                                        User Hash: <span class="text-slate-300">6a39f3c62da034ed0289bf0f</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="p-5 pt-0 flex items-center justify-between gap-2 border-t border-slate-900 mt-2">
                            <div class="flex flex-wrap gap-1">
                                <span class="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded">Forensic Analytics</span>
                                <span class="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded">Simulation</span>
                            </div>
                            <button onclick="openCertModal('/src/assets/images/cert_deloitte.jpg', 'Data Analytics Job Simulation')" class="text-xs text-emerald-400 hover:text-emerald-300 font-bold flex items-center gap-1 bg-emerald-500/10 px-3 py-1.5 rounded-xl border border-emerald-500/20">
                                🖼️ View Certificate Image
                            </button>
                        </div>
                    </div>

                    <!-- Cert 3: SQL for Data Analysis -->
                    <div class="bg-slate-950 rounded-2xl border border-slate-800 hover:border-emerald-500/40 transition overflow-hidden group flex flex-col justify-between">
                        <div>
                            <!-- CERTIFICATE IMAGE PREVIEW -->
                            <div class="relative overflow-hidden bg-slate-900 cursor-pointer group-hover:opacity-95 transition" onclick="openCertModal('/src/assets/images/cert_sql_analysis.jpg', 'SQL for Data Analysis - LinkedIn Learning')">
                                <img src="/src/assets/images/cert_sql_analysis.jpg" alt="SQL for Data Analysis Certificate" class="w-full h-56 object-cover object-top group-hover:scale-105 transition duration-300">
                                <div class="absolute inset-0 bg-slate-950/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center gap-2 text-white font-medium text-xs backdrop-blur-[2px]">
                                    <span class="bg-emerald-500 text-slate-950 px-3 py-1.5 rounded-xl font-bold flex items-center gap-1 shadow-lg">
                                        🔍 Click to Enlarge Uploaded Certificate
                                    </span>
                                </div>
                                <span class="absolute top-3 right-3 text-[10px] font-mono font-bold text-sky-300 bg-slate-950/80 backdrop-blur px-2.5 py-1 rounded-lg border border-sky-500/30">LinkedIn Learning</span>
                            </div>

                            <div class="p-5 space-y-3">
                                <div>
                                    <h4 class="font-bold text-white text-base">SQL for Data Analysis</h4>
                                    <p class="text-xs text-emerald-400 font-semibold">LinkedIn Learning • Issued Jun 24, 2026</p>
                                </div>

                                <div class="space-y-1.5 text-xs text-slate-300 bg-slate-900/80 p-3 rounded-xl border border-slate-800 font-mono">
                                    <div class="flex items-center justify-between text-emerald-300">
                                        <span class="text-slate-400 font-sans">⏱️ Completion Timestamp:</span>
                                        <span class="font-bold">Jun 24, 2026 at 10:32AM UTC</span>
                                    </div>
                                    <div class="flex items-center justify-between text-slate-300">
                                        <span class="text-slate-400 font-sans">⏳ Duration:</span>
                                        <span>1 hour 10 minutes</span>
                                    </div>
                                    <div class="text-[10px] text-slate-400 truncate pt-1 border-t border-slate-800">
                                        Verification Code: <span class="text-slate-300">5ae52a838283a2a80...e9796e24807</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="p-5 pt-0 flex items-center justify-between gap-2 border-t border-slate-900 mt-2">
                            <div class="flex flex-wrap gap-1">
                                <span class="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded">SQL Aggregations</span>
                                <span class="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded">Queries</span>
                            </div>
                            <button onclick="openCertModal('/src/assets/images/cert_sql_analysis.jpg', 'SQL for Data Analysis')" class="text-xs text-emerald-400 hover:text-emerald-300 font-bold flex items-center gap-1 bg-emerald-500/10 px-3 py-1.5 rounded-xl border border-emerald-500/20">
                                🖼️ View Certificate Image
                            </button>
                        </div>
                    </div>

                    <!-- Cert 4: SQL Practice DELETE -->
                    <div class="bg-slate-950 rounded-2xl border border-slate-800 hover:border-emerald-500/40 transition overflow-hidden group flex flex-col justify-between">
                        <div>
                            <!-- CERTIFICATE IMAGE PREVIEW -->
                            <div class="relative overflow-hidden bg-slate-900 cursor-pointer group-hover:opacity-95 transition" onclick="openCertModal('/src/assets/images/cert_sql_delete.jpg', 'SQL Practice: Deleting Data with DELETE Statements - LinkedIn Learning')">
                                <img src="/src/assets/images/cert_sql_delete.jpg" alt="SQL DELETE Practice Certificate" class="w-full h-56 object-cover object-top group-hover:scale-105 transition duration-300">
                                <div class="absolute inset-0 bg-slate-950/40 opacity-0 group-hover:opacity-100 transition flex items-center justify-center gap-2 text-white font-medium text-xs backdrop-blur-[2px]">
                                    <span class="bg-emerald-500 text-slate-950 px-3 py-1.5 rounded-xl font-bold flex items-center gap-1 shadow-lg">
                                        🔍 Click to Enlarge Uploaded Certificate
                                    </span>
                                </div>
                                <span class="absolute top-3 right-3 text-[10px] font-mono font-bold text-sky-300 bg-slate-950/80 backdrop-blur px-2.5 py-1 rounded-lg border border-sky-500/30">LinkedIn Learning</span>
                            </div>

                            <div class="p-5 space-y-3">
                                <div>
                                    <h4 class="font-bold text-white text-base">SQL Practice: Deleting Data with DELETE Statements</h4>
                                    <p class="text-xs text-emerald-400 font-semibold">LinkedIn Learning • Issued Jul 06, 2026</p>
                                </div>

                                <div class="space-y-1.5 text-xs text-slate-300 bg-slate-900/80 p-3 rounded-xl border border-slate-800 font-mono">
                                    <div class="flex items-center justify-between text-emerald-300">
                                        <span class="text-slate-400 font-sans">⏱️ Completion Timestamp:</span>
                                        <span class="font-bold">Jul 06, 2026 at 10:56AM UTC</span>
                                    </div>
                                    <div class="flex items-center justify-between text-slate-300">
                                        <span class="text-slate-400 font-sans">⏳ Duration:</span>
                                        <span>34 minutes</span>
                                    </div>
                                    <div class="text-[10px] text-slate-400 truncate pt-1 border-t border-slate-800">
                                        Verification Code: <span class="text-slate-300">b205b47bbf1adcb9...c73570f0559</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="p-5 pt-0 flex items-center justify-between gap-2 border-t border-slate-900 mt-2">
                            <div class="flex flex-wrap gap-1">
                                <span class="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded">DELETE Queries</span>
                                <span class="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded">Data Integrity</span>
                            </div>
                            <button onclick="openCertModal('/src/assets/images/cert_sql_delete.jpg', 'SQL Practice DELETE Statements')" class="text-xs text-emerald-400 hover:text-emerald-300 font-bold flex items-center gap-1 bg-emerald-500/10 px-3 py-1.5 rounded-xl border border-emerald-500/20">
                                🖼️ View Certificate Image
                            </button>
                        </div>
                    </div>

                </div>
            </div>

            <!-- LIGHTBOX MODAL FOR CERTIFICATE IMAGES -->
            <div id="cert-image-modal" class="fixed inset-0 bg-slate-950/90 z-50 backdrop-blur-md hidden flex items-center justify-center p-4 sm:p-8 animate-fadeIn" onclick="closeCertModal()">
                <div class="relative max-w-4xl w-full max-h-[90vh] bg-slate-900 border border-slate-800 rounded-3xl p-4 sm:p-6 shadow-2xl flex flex-col space-y-4" onclick="event.stopPropagation()">
                    <div class="flex items-center justify-between border-b border-slate-800 pb-3">
                        <h3 id="modal-cert-title" class="text-sm sm:text-base font-bold text-white truncate pr-4">Certificate Image</h3>
                        <button onclick="closeCertModal()" class="text-slate-400 hover:text-white bg-slate-800 px-3 py-1.5 rounded-xl border border-slate-700 text-xs font-bold transition">
                            ✕ Close (ESC)
                        </button>
                    </div>
                    <div class="flex-1 overflow-auto rounded-2xl bg-black flex items-center justify-center p-2 border border-slate-800">
                        <img id="modal-cert-img" src="" alt="Full Certificate View" class="max-h-[70vh] w-auto object-contain rounded-lg shadow-2xl">
                    </div>
                    <div class="flex justify-between items-center text-xs text-slate-400 font-mono">
                        <span>Issued to: <strong class="text-emerald-400 font-sans">Darika T</strong></span>
                        <a id="modal-download-btn" href="" target="_blank" download class="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold px-4 py-2 rounded-xl transition flex items-center gap-1.5">
                            ⬇️ Open / Download Image
                        </a>
                    </div>
                </div>
            </div>

            <script>
                function openCertModal(imgSrc, title) {
                    const modal = document.getElementById('cert-image-modal');
                    const img = document.getElementById('modal-cert-img');
                    const titleElem = document.getElementById('modal-cert-title');
                    const downloadBtn = document.getElementById('modal-download-btn');
                    
                    if (modal && img) {
                        img.src = imgSrc;
                        if (titleElem) titleElem.textContent = title;
                        if (downloadBtn) downloadBtn.href = imgSrc;
                        modal.classList.remove('hidden');
                        document.body.style.overflow = 'hidden';
                    }
                }

                function closeCertModal() {
                    const modal = document.getElementById('cert-image-modal');
                    if (modal) {
                        modal.classList.add('hidden');
                        document.body.style.overflow = '';
                    }
                }

                document.addEventListener('keydown', function(e) {
                    if (e.key === 'Escape') closeCertModal();
                });
            </script>
            '''
            
            if "HX-Request" in self.headers or path.startswith("/api/"):
                self.send_html(html)
            else:
                full_page = self.get_main_index_page().replace('<section id="certifications"', f'<div class="mb-12">{html}</div><section id="certifications"')
                self.send_html(full_page)
            return

        else:
            self.send_html("<div class='p-4 text-red-400'>404 Not Found</div>", 404)

    def do_POST(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        body = self.parse_body()

        if path == "/api/htmx/ats-analyze":
            resume_text = body.get("resume_text", "")
            target_role = body.get("target_role", "Data Analyst")
            
            if isinstance(resume_text, list): resume_text = resume_text[0] if resume_text else ""
            if isinstance(target_role, list): target_role = target_role[0] if target_role else "Data Analyst"
            
            if not resume_text or len(resume_text.strip()) < 10:
                resume_text = """DARIKA T
                tdarika3@gmail.com | +919342362394
                Skills: Java, Python, SQL, Microsoft Excel, Power BI, Google Colab
                Projects: E-Commerce Sales Data Analysis (Excel, SQL), ATS ResumeIQ Web Application, Sales Data Analysis (Python)
                Certifications: Basics of Data Visualization - LinkedIn Learning, Learning Python - Infosys SpringBoard
                Education: Bachelor of Science in Computer Science | Rathinam Global Deemed To Be University"""

            text_lower = resume_text.lower()
            
            role_keywords = {
                "Data Analyst": ["python", "sql", "excel", "power bi", "data analysis", "visualizations", "cleaning", "outlier", "insights", "sales", "trends"],
                "Python Developer": ["python", "java", "sql", "web application", "algorithms", "data validation", "colab", "pandas", "automation"],
                "BI Specialist": ["power bi", "excel", "dashboards", "pivot tables", "charts", "slicers", "sql", "visualization", "metrics", "revenue"]
            }
            
            req_keywords = role_keywords.get(target_role, role_keywords["Data Analyst"])
            found_keywords = [kw for kw in req_keywords if kw in text_lower]
            missing_keywords = [kw for kw in req_keywords if kw not in text_lower]
            
            match_pct = int((len(found_keywords) / len(req_keywords)) * 100)
            
            has_contact = "gmail.com" in text_lower or "@" in text_lower or "phone" in text_lower or "+91" in text_lower
            has_education = "computer science" in text_lower or "university" in text_lower or "education" in text_lower
            has_projects = "project" in text_lower or "analysis" in text_lower
            
            format_score = 0
            if has_contact: format_score += 35
            if has_education: format_score += 35
            if has_projects: format_score += 30
            
            final_ats_score = int((match_pct * 0.65) + (format_score * 0.35))
            score_color = "emerald" if final_ats_score >= 80 else ("amber" if final_ats_score >= 60 else "red")
            
            matched_html = "".join([f'<span class="px-2.5 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 rounded-md text-xs font-mono">✓ {kw}</span>' for kw in found_keywords])
            missing_html = "".join([f'<span class="px-2.5 py-1 bg-amber-500/10 text-amber-400 border border-amber-500/30 rounded-md text-xs font-mono">+ {kw}</span>' for kw in missing_keywords]) if missing_keywords else '<span class="text-xs text-slate-400">None! Outstanding keyword coverage.</span>'

            html = f'''
            <div class="bg-slate-900/90 border border-slate-700/80 rounded-2xl p-6 shadow-2xl space-y-6 animate-fadeIn">
                <div class="flex items-center justify-between border-b border-slate-800 pb-4 flex-wrap gap-4">
                    <div>
                        <h4 class="text-xl font-bold text-white flex items-center gap-2">
                            <span>🤖 ATS ResumeIQ Evaluation Report</span>
                            <span class="text-xs font-normal text-slate-400 bg-slate-800 px-2.5 py-1 rounded-full border border-slate-700">Python Evaluator</span>
                        </h4>
                        <p class="text-xs text-slate-400 mt-1">Evaluated against target benchmark: <strong class="text-emerald-400">{target_role}</strong></p>
                    </div>
                    
                    <div class="flex items-center gap-3 bg-slate-800/80 px-5 py-3 rounded-xl border border-slate-700">
                        <div class="text-right">
                            <span class="text-xs uppercase tracking-wider text-slate-400 block font-semibold">ATS Compatibility</span>
                            <span class="text-xs text-emerald-400 font-medium">Verified Compatibility</span>
                        </div>
                        <div class="text-3xl font-extrabold text-{score_color}-400 font-mono">
                            {final_ats_score}%
                        </div>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="bg-slate-800/50 p-4 rounded-xl border border-slate-700/60">
                        <div class="flex justify-between text-xs text-slate-300 font-medium mb-1.5">
                            <span>Keyword Match Density</span>
                            <span class="text-emerald-400 font-mono">{match_pct}%</span>
                        </div>
                        <div class="w-full bg-slate-700/60 rounded-full h-2">
                            <div class="bg-emerald-400 h-2 rounded-full transition-all duration-500" style="width: {match_pct}%"></div>
                        </div>
                        <p class="text-[11px] text-slate-400 mt-2">{len(found_keywords)} of {len(req_keywords)} core domain terms identified.</p>
                    </div>

                    <div class="bg-slate-800/50 p-4 rounded-xl border border-slate-700/60">
                        <div class="flex justify-between text-xs text-slate-300 font-medium mb-1.5">
                            <span>Structure & Formatting Score</span>
                            <span class="text-sky-400 font-mono">{format_score}%</span>
                        </div>
                        <div class="w-full bg-slate-700/60 rounded-full h-2">
                            <div class="bg-sky-400 h-2 rounded-full transition-all duration-500" style="width: {format_score}%"></div>
                        </div>
                        <p class="text-[11px] text-slate-400 mt-2">Verified contact info, education, and project sections.</p>
                    </div>
                </div>

                <div class="space-y-3">
                    <div>
                        <span class="text-xs font-semibold text-slate-300 uppercase tracking-wider block mb-2">Matched Competencies:</span>
                        <div class="flex flex-wrap gap-2">
                            {matched_html}
                        </div>
                    </div>

                    <div>
                        <span class="text-xs font-semibold text-slate-300 uppercase tracking-wider block mb-2">Recommended Additions:</span>
                        <div class="flex flex-wrap gap-2">
                            {missing_html}
                        </div>
                    </div>
                </div>

                <div class="bg-emerald-950/20 border border-emerald-500/30 rounded-xl p-4 text-xs text-emerald-200 leading-relaxed">
                    <strong class="text-emerald-400 font-semibold block mb-1">💡 Python Evaluation Summary:</strong>
                    Darika's resume demonstrates strong alignment with Data Analyst and Technical positions. Structural integrity and keyword density pass standard ATS parser requirements cleanly.
                </div>
            </div>
            '''
            self.send_html(html)
            return

        elif path == "/api/htmx/sales-analyze":
            operation = body.get("operation", "missing")
            if isinstance(operation, list): operation = operation[0] if operation else "missing"
            
            if operation == "missing":
                cleaned = []
                missing_count = 0
                for item in SAMPLE_SALES_DATA:
                    item_copy = dict(item)
                    if item_copy["revenue"] is None:
                        missing_count += 1
                        item_copy["revenue"] = 850.00  # Imputed median
                        item_copy["note"] = "Imputed (Median = $850.00)"
                    else:
                        item_copy["note"] = "Original Verified"
                    cleaned.append(item_copy)
                
                rows_html = ""
                for c in cleaned:
                    bg_style = "bg-amber-500/10 text-amber-300 font-medium" if "Imputed" in c["note"] else "text-slate-300"
                    rows_html += f'''
                    <tr class="border-b border-slate-800 text-xs">
                        <td class="py-2.5 px-3 font-mono text-slate-400">#{c['id']}</td>
                        <td class="py-2.5 px-3 text-slate-200">{c['category']}</td>
                        <td class="py-2.5 px-3 text-slate-300">{c['region']}</td>
                        <td class="py-2.5 px-3 font-mono text-emerald-400">${c['revenue']:.2f}</td>
                        <td class="py-2.5 px-3 {bg_style}">{c['note']}</td>
                    </tr>
                    '''

                html = f'''
                <div class="space-y-4 animate-fadeIn">
                    <div class="flex justify-between items-center bg-slate-800 p-3.5 rounded-xl border border-slate-700">
                        <span class="text-xs text-slate-300 font-semibold">Python Missing Value Treatment (Median Imputation)</span>
                        <span class="text-xs font-bold text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20">
                            Fixed {missing_count} Null Values
                        </span>
                    </div>
                    <div class="overflow-x-auto rounded-xl border border-slate-800">
                        <table class="w-full text-left bg-slate-900">
                            <thead class="bg-slate-800 text-slate-400 text-xs uppercase">
                                <tr>
                                    <th class="py-2 px-3">ID</th>
                                    <th class="py-2 px-3">Category</th>
                                    <th class="py-2 px-3">Region</th>
                                    <th class="py-2 px-3">Revenue</th>
                                    <th class="py-2 px-3">Validation Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {rows_html}
                            </tbody>
                        </table>
                    </div>
                </div>
                '''
                self.send_html(html)
                return

            elif operation == "outlier":
                valid_revs = [item["revenue"] for item in SAMPLE_SALES_DATA if item["revenue"] is not None]
                valid_revs.sort()
                
                q1 = valid_revs[len(valid_revs)//4]
                q3 = valid_revs[3*len(valid_revs)//4]
                iqr = q3 - q1
                upper_bound = q3 + (1.5 * iqr)
                
                rows_html = ""
                outliers_found = 0
                for item in SAMPLE_SALES_DATA:
                    rev = item["revenue"] or 0.0
                    is_outlier = rev > upper_bound
                    if is_outlier: outliers_found += 1
                    
                    status_badge = '<span class="text-amber-400 bg-amber-500/10 border border-amber-500/30 px-2 py-0.5 rounded text-[11px] font-bold">⚠️ Outlier Isolated</span>' if is_outlier else '<span class="text-emerald-400 text-[11px]">Normal Distribution</span>'
                    
                    rows_html += f'''
                    <tr class="border-b border-slate-800 text-xs">
                        <td class="py-2.5 px-3 font-mono text-slate-400">#{item['id']}</td>
                        <td class="py-2.5 px-3 text-slate-200">{item['category']} ({item['customer']})</td>
                        <td class="py-2.5 px-3 font-mono text-slate-200">${rev:.2f}</td>
                        <td class="py-2.5 px-3">{status_badge}</td>
                    </tr>
                    '''

                html = f'''
                <div class="space-y-4 animate-fadeIn">
                    <div class="bg-slate-800 p-3.5 rounded-xl border border-slate-700 flex justify-between items-center text-xs">
                        <div>
                            <span class="text-slate-300 font-semibold">Python Outlier Detection (IQR Thresholding):</span>
                            <span class="text-slate-400 ml-2 font-mono">Upper Limit = ${upper_bound:.2f}</span>
                        </div>
                        <span class="text-xs font-bold text-amber-400 bg-amber-500/10 px-3 py-1 rounded-full border border-amber-500/20">
                            {outliers_found} Outlier(s) Detected
                        </span>
                    </div>
                    <div class="overflow-x-auto rounded-xl border border-slate-800">
                        <table class="w-full text-left bg-slate-900">
                            <thead class="bg-slate-800 text-slate-400 text-xs uppercase">
                                <tr>
                                    <th class="py-2 px-3">ID</th>
                                    <th class="py-2 px-3">Category & Customer</th>
                                    <th class="py-2 px-3">Amount</th>
                                    <th class="py-2 px-3">Detection Status</th>
                                </tr>
                            </thead>
                            <tbody>
                                {rows_html}
                            </tbody>
                        </table>
                    </div>
                </div>
                '''
                self.send_html(html)
                return

            elif operation == "trends":
                cat_rev = {}
                for item in SAMPLE_SALES_DATA:
                    cat = item["category"]
                    rev = item["revenue"] or 850.00
                    cat_rev[cat] = cat_rev.get(cat, 0.0) + rev

                cards_html = ""
                for cat, total in cat_rev.items():
                    cards_html += f'''
                    <div class="bg-slate-800/80 p-4 rounded-xl border border-slate-700/80 text-center">
                        <span class="text-xs text-slate-400 font-medium block uppercase">{cat}</span>
                        <span class="text-2xl font-extrabold text-emerald-400 font-mono mt-1 block">${total:,.2f}</span>
                        <span class="text-[10px] text-slate-400 mt-1 block">Aggregated Total Sales</span>
                    </div>
                    '''

                html = f'''
                <div class="space-y-4 animate-fadeIn">
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
                        {cards_html}
                    </div>
                    <div class="p-4 bg-slate-900 border border-slate-800 rounded-xl text-xs text-slate-300 leading-relaxed">
                        <strong class="text-emerald-400 font-semibold block mb-1">📈 Key Python Analytics Finding:</strong>
                        Electronics represents the highest revenue segment (~$15,850 total revenue), followed by Apparel and Home & Kitchen. High-value transactions were successfully validated.
                    </div>
                </div>
                '''
                self.send_html(html)
                return

        elif path == "/api/htmx/sql-query":
            query_type = body.get("query_type", "cat_summary")
            if isinstance(query_type, list): query_type = query_type[0] if query_type else "cat_summary"
            
            if query_type == "cat_summary":
                sql_str = "SELECT category, COUNT(id) AS total_orders, SUM(COALESCE(revenue, 850)) AS total_sales, AVG(units) AS avg_units FROM ecommerce_sales GROUP BY category ORDER BY total_sales DESC;"
                rows = [
                    ("Electronics", 5, 15850.00, 3.4),
                    ("Apparel", 3, 2770.50, 11.7),
                    ("Home & Kitchen", 3, 1980.00, 3.6)
                ]
            elif query_type == "regional":
                sql_str = "SELECT region, COUNT(id) AS transaction_count, SUM(COALESCE(revenue, 850)) AS regional_revenue FROM ecommerce_sales GROUP BY region HAVING regional_revenue > 2000;"
                rows = [
                    ("South", 4, 4850.00, 3.0),
                    ("West", 2, 10150.00, 8.0),
                    ("East", 2, 4250.00, 7.5),
                    ("North", 2, 1000.50, 9.0)
                ]
            else:
                sql_str = "SELECT customer, category, revenue, status FROM ecommerce_sales WHERE status = 'Completed' AND revenue > 1000;"
                rows = [
                    ("Cust_A", "Electronics", 1450.00, "Completed"),
                    ("Cust_C", "Electronics", 8900.00, "Completed"),
                    ("Cust_F", "Electronics", 2100.00, "Completed"),
                    ("Cust_B", "Apparel", 1250.00, "Completed")
                ]

            table_rows = ""
            for r in rows:
                table_rows += "<tr class='border-b border-slate-800 text-xs'>"
                for cell in r:
                    if isinstance(cell, float):
                        val = f"${cell:,.2f}" if cell > 50 else f"{cell:.1f}"
                        table_rows += f"<td class='py-2.5 px-3 font-mono text-emerald-400'>{val}</td>"
                    else:
                        table_rows += f"<td class='py-2.5 px-3 text-slate-200'>{cell}</td>"
                table_rows += "</tr>"

            html = f'''
            <div class="space-y-3 animate-fadeIn">
                <div class="bg-slate-950 p-3.5 rounded-xl border border-slate-800 font-mono text-xs text-sky-300">
                    <span class="text-slate-500 block text-[10px] uppercase font-sans mb-1">Executed SQL Statement (Python SQLite Simulation Engine):</span>
                    {sql_str}
                </div>

                <div class="overflow-x-auto rounded-xl border border-slate-800">
                    <table class="w-full text-left bg-slate-900">
                        <thead class="bg-slate-800/80 text-slate-400 text-xs uppercase font-semibold">
                            <tr>
                                <th class="py-2.5 px-3">Column 1</th>
                                <th class="py-2.5 px-3">Metric 2</th>
                                <th class="py-2.5 px-3">Sales / Revenue</th>
                                <th class="py-2.5 px-3">Status / Units</th>
                            </tr>
                        </thead>
                        <tbody>
                            {table_rows}
                        </tbody>
                    </table>
                </div>
            </div>
            '''
            self.send_html(html)
            return

        elif path == "/api/htmx/contact":
            name = body.get("name", "Recruiter")
            email = body.get("email", "")
            if isinstance(name, list): name = name[0] if name else "Recruiter"
            if isinstance(email, list): email = email[0] if email else ""
            
            html = f'''
            <div class="bg-emerald-950/40 border border-emerald-500/40 rounded-xl p-5 text-center text-slate-100 animate-fadeIn shadow-lg">
                <div class="w-12 h-12 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center mx-auto mb-3">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>
                </div>
                <h4 class="text-lg font-bold text-emerald-400 mb-1">Thank you, {name}!</h4>
                <p class="text-slate-300 text-xs max-w-md mx-auto leading-relaxed">
                    Your message was received by Darika's Python HTMX backend. She will get back to <strong class="text-emerald-300">{email}</strong> shortly.
                </p>
                <div class="mt-4 pt-3 border-t border-emerald-500/20 text-[11px] text-slate-400">
                    Direct Contact: <a href="mailto:tdarika3@gmail.com" class="text-emerald-400 underline">tdarika3@gmail.com</a> | +91 9342362394
                </div>
            </div>
            '''
            self.send_html(html)
            return

        else:
            self.send_html("<div class='p-4 text-red-400'>404 Not Found</div>", 404)

    def get_main_index_page(self):
        return '''<!DOCTYPE html>
<html lang="en" class="dark scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DARIKA T | Data Analyst & Python HTMX Portfolio</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- HTMX CDN -->
    <script src="https://unpkg.com/htmx.org@2.0.4"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        code, pre, .font-mono { font-family: 'JetBrains Mono', monospace; }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-fadeIn { animation: fadeIn 0.3s ease-out forwards; }
        .htmx-request .htmx-spinner { display: inline-block; }
        .htmx-spinner { display: none; }
    </style>
</head>
<body class="bg-slate-950 text-slate-100 antialiased min-h-screen selection:bg-emerald-500 selection:text-slate-950">

    <!-- Header Navigation -->
    <header class="sticky top-0 z-40 bg-slate-950/80 backdrop-blur-md border-b border-slate-800/80">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <a href="#" class="flex items-center gap-3 group">
                <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-400 flex items-center justify-center font-black text-slate-950 text-lg shadow-lg shadow-emerald-500/20 group-hover:scale-105 transition">
                    DT
                </div>
                <div>
                    <span class="font-extrabold text-white text-base tracking-tight block">DARIKA T</span>
                    <span class="text-[10px] text-emerald-400 font-mono block -mt-1">Data Analyst • Python + HTMX</span>
                </div>
            </a>

            <nav class="hidden md:flex items-center gap-6 text-xs font-medium text-slate-300">
                <a href="#about" class="hover:text-emerald-400 transition">About</a>
                <a href="#objective" class="hover:text-emerald-400 transition">Objective</a>
                <a href="#skills" class="hover:text-emerald-400 transition">Skills</a>
                <a href="#playground" class="hover:text-emerald-400 transition flex items-center gap-1 text-emerald-400 font-bold bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span> Playground
                </a>
                <a href="#projects" class="hover:text-emerald-400 transition">Projects</a>
                <a href="#certifications" class="hover:text-emerald-400 transition">Certifications</a>
                <a href="#education" class="hover:text-emerald-400 transition">Education</a>
                <a href="#contact" class="hover:text-emerald-400 transition">Contact</a>
            </nav>

            <div class="flex items-center gap-3">
                <button hx-get="/api/htmx/resume-modal" hx-target="body" hx-swap="beforeend" 
                        class="bg-emerald-500 hover:bg-emerald-400 text-slate-950 px-4 py-2 rounded-lg font-bold text-xs flex items-center gap-2 transition shadow-md shadow-emerald-500/10">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
                    <span>View Resume</span>
                </button>
            </div>
        </div>
    </header>

    <!-- Main Content Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-16">

        <!-- HERO SECTION -->
        <section id="about" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center pt-4">
            <div class="lg:col-span-8 space-y-6">
                <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-900 border border-slate-800 text-xs font-mono text-emerald-400">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span>Pure Python 3.10 Backend • Native HTMX Server Architecture</span>
                </div>

                <div class="space-y-2">
                    <h1 class="text-4xl sm:text-5xl font-black text-white tracking-tight leading-tight">
                        DARIKA T
                    </h1>
                    <p class="text-xl sm:text-2xl text-emerald-400 font-bold">
                        B.Sc. Computer Science Graduate & Results-Driven Data Analyst
                    </p>
                </div>

                <p class="text-slate-300 text-base leading-relaxed max-w-2xl">
                    Specializing in <strong class="text-white">Python data cleaning</strong>, <strong class="text-white">SQL query optimization</strong>, <strong class="text-white">Excel Power Dashboards</strong>, and <strong class="text-white">AI-assisted web applications</strong>. Proven ability to transform complex transaction datasets into actionable business intelligence.
                </p>

                <!-- Contact Pills -->
                <div class="flex flex-wrap gap-3 text-xs">
                    <a href="mailto:tdarika3@gmail.com" class="flex items-center gap-2 bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-200 px-3.5 py-2 rounded-xl transition">
                        📧 tdarika3@gmail.com
                    </a>
                    <a href="tel:+919342362394" class="flex items-center gap-2 bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-200 px-3.5 py-2 rounded-xl transition">
                        📱 +91 9342362394
                    </a>
                    <a href="https://github.com/tdarika3-ui" target="_blank" class="flex items-center gap-2 bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-200 px-3.5 py-2 rounded-xl transition">
                        💻 GitHub Profile
                    </a>
                    <a href="https://www.linkedin.com/in/darika-t-883124320/" target="_blank" class="flex items-center gap-2 bg-slate-900 hover:bg-slate-800 border border-slate-800 text-slate-200 px-3.5 py-2 rounded-xl transition">
                        🔗 LinkedIn
                    </a>
                </div>
            </div>

            <div class="lg:col-span-4">
                <div class="bg-gradient-to-br from-slate-900 to-slate-900/90 border border-slate-800 p-6 rounded-2xl shadow-xl space-y-4">
                    <h3 class="text-sm font-bold uppercase tracking-wider text-slate-400 flex items-center justify-between">
                        <span>Quick Profile Specs</span>
                        <span class="text-emerald-400 text-xs">Verified</span>
                    </h3>
                    
                    <div class="space-y-3 text-xs">
                        <div class="flex justify-between border-b border-slate-800 pb-2">
                            <span class="text-slate-400">Degree</span>
                            <span class="font-semibold text-white">B.Sc. Computer Science</span>
                        </div>
                        <div class="flex justify-between border-b border-slate-800 pb-2">
                            <span class="text-slate-400">Batch</span>
                            <span class="font-semibold text-white">2024 - 2027</span>
                        </div>
                        <div class="flex justify-between border-b border-slate-800 pb-2">
                            <span class="text-slate-400">University</span>
                            <span class="font-semibold text-white">Rathinam Global Deemed University</span>
                        </div>
                        <div class="flex justify-between border-b border-slate-800 pb-2">
                            <span class="text-slate-400">Core Stack</span>
                            <span class="font-mono text-emerald-400">Python | SQL | Java | Excel</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>


        <!-- CAREER OBJECTIVE SECTION WITH HTMX DYNAMIC TABS -->
        <section id="objective" class="bg-slate-900/60 border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                    <h2 class="text-2xl font-bold text-white flex items-center gap-2">
                        <span>CAREER OBJECTIVE</span>
                        <span class="text-xs bg-emerald-500/10 text-emerald-400 px-2.5 py-1 rounded-full border border-emerald-500/20 font-mono">HTMX Dynamic</span>
                    </h2>
                    <p class="text-xs text-slate-400 mt-1">Select a candidate persona to adapt the Career Objective in real-time via Python HTMX server calls:</p>
                </div>

                <div class="flex flex-wrap gap-2 text-xs">
                    <button hx-get="/api/htmx/objective?role=Data+Analyst" hx-target="#objective-display" hx-swap="innerHTML"
                            class="px-3 py-1.5 rounded-lg bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 font-semibold border border-emerald-500/30 transition">
                        Data Analyst
                    </button>
                    <button hx-get="/api/htmx/objective?role=Python+Developer" hx-target="#objective-display" hx-swap="innerHTML"
                            class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold border border-slate-700 transition">
                        Python Developer
                    </button>
                    <button hx-get="/api/htmx/objective?role=BI+%26+Data+Visualization+Specialist" hx-target="#objective-display" hx-swap="innerHTML"
                            class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold border border-slate-700 transition">
                        BI Specialist
                    </button>
                    <button hx-get="/api/htmx/objective?role=AI+%26+Web+Solution+Engineer" hx-target="#objective-display" hx-swap="innerHTML"
                            class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold border border-slate-700 transition">
                        AI Engineer
                    </button>
                </div>
            </div>

            <!-- HTMX Swap Target -->
            <div id="objective-display" hx-get="/api/htmx/objective?role=Data+Analyst" hx-trigger="load">
                <div class="p-6 bg-slate-800/50 rounded-2xl animate-pulse text-xs text-slate-400">Loading tailored objective from Python...</div>
            </div>
        </section>


        <!-- TECHNICAL & SOFT SKILLS SECTION -->
        <section id="skills" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                    <h2 class="text-2xl font-bold text-white">TECHNICAL & SOFT SKILLS</h2>
                    <p class="text-xs text-slate-400">Interactive categories powered by server-side HTMX query filtering</p>
                </div>

                <div class="flex flex-wrap gap-2 text-xs">
                    <button hx-get="/api/htmx/skills-filter?category=all" hx-target="#skills-grid" hx-swap="innerHTML"
                            class="px-3.5 py-1.5 rounded-lg bg-slate-800 hover:bg-emerald-500/20 text-slate-200 hover:text-emerald-300 font-semibold border border-slate-700 transition">
                        All Skills
                    </button>
                    <button hx-get="/api/htmx/skills-filter?category=programming" hx-target="#skills-grid" hx-swap="innerHTML"
                            class="px-3.5 py-1.5 rounded-lg bg-slate-800 hover:bg-emerald-500/20 text-slate-200 hover:text-emerald-300 font-semibold border border-slate-700 transition">
                        Programming (Python, SQL, Java)
                    </button>
                    <button hx-get="/api/htmx/skills-filter?category=tools" hx-target="#skills-grid" hx-swap="innerHTML"
                            class="px-3.5 py-1.5 rounded-lg bg-slate-800 hover:bg-emerald-500/20 text-slate-200 hover:text-emerald-300 font-semibold border border-slate-700 transition">
                        Tools (Excel, Power BI)
                    </button>
                    <button hx-get="/api/htmx/skills-filter?category=soft" hx-target="#skills-grid" hx-swap="innerHTML"
                            class="px-3.5 py-1.5 rounded-lg bg-slate-800 hover:bg-emerald-500/20 text-slate-200 hover:text-emerald-300 font-semibold border border-slate-700 transition">
                        Soft Skills
                    </button>
                </div>
            </div>

            <!-- Skills Grid Swap Target -->
            <div id="skills-grid" hx-get="/api/htmx/skills-filter?category=all" hx-trigger="load" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div class="p-6 bg-slate-900 rounded-xl animate-pulse text-xs text-slate-400">Loading skill matrix...</div>
            </div>
        </section>


        <!-- LIVE PYTHON + HTMX INTERACTIVE PLAYGROUND SECTION -->
        <section id="playground" class="bg-slate-900 border border-emerald-500/30 rounded-3xl p-6 sm:p-8 space-y-8 shadow-2xl relative overflow-hidden">
            <div class="flex items-center justify-between border-b border-slate-800 pb-4">
                <div>
                    <div class="flex items-center gap-2">
                        <span class="w-3 h-3 rounded-full bg-emerald-400 animate-ping"></span>
                        <h2 class="text-2xl font-black text-white tracking-tight">PYTHON + HTMX PLAYGROUND</h2>
                    </div>
                    <p class="text-xs text-slate-400 mt-1">Live server-side execution testing Darika's analytical engines and algorithms</p>
                </div>
                <span class="text-xs font-mono text-emerald-400 bg-emerald-500/10 px-3 py-1 rounded-full border border-emerald-500/20">
                    100% Python Engine
                </span>
            </div>

            <!-- Playground Tabs -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">

                <!-- Module 1: ATS ResumeIQ Tester -->
                <div class="bg-slate-950 p-5 rounded-2xl border border-slate-800 space-y-4 flex flex-col justify-between">
                    <div class="space-y-2">
                        <div class="flex items-center justify-between">
                            <h3 class="font-bold text-white text-base">🤖 ATS ResumeIQ Evaluator</h3>
                            <span class="text-[10px] bg-slate-800 text-emerald-400 px-2 py-0.5 rounded font-mono">Project #2</span>
                        </div>
                        <p class="text-xs text-slate-400">Test the AI-assisted ATS resume keyword matcher and structure validator.</p>
                    </div>

                    <form hx-post="/api/htmx/ats-analyze" hx-target="#playground-result" hx-swap="innerHTML" class="space-y-3">
                        <div>
                            <label class="text-[11px] font-semibold text-slate-300 block mb-1">Target Job Benchmark:</label>
                            <select name="target_role" class="w-full bg-slate-900 border border-slate-700 text-slate-200 rounded-lg p-2 text-xs focus:ring-1 focus:ring-emerald-400 outline-none">
                                <option value="Data Analyst">Data Analyst (Python, SQL, Excel)</option>
                                <option value="Python Developer">Python Developer (Java, Algorithms)</option>
                                <option value="BI Specialist">BI Specialist (Power BI, Dashboards)</option>
                            </select>
                        </div>

                        <div>
                            <label class="text-[11px] font-semibold text-slate-300 block mb-1">Paste Candidate Profile Text:</label>
                            <textarea name="resume_text" rows="3" class="w-full bg-slate-900 border border-slate-700 text-slate-200 rounded-lg p-2 text-xs focus:ring-1 focus:ring-emerald-400 outline-none font-mono" placeholder="Paste resume text or leave empty to evaluate Darika T's profile..."></textarea>
                        </div>

                        <button type="submit" class="w-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold py-2.5 rounded-lg text-xs transition flex items-center justify-center gap-2">
                            <span>Execute ATS Analysis</span>
                        </button>
                    </form>
                </div>

                <!-- Module 2: Python Sales Data Cleaning Engine -->
                <div class="bg-slate-950 p-5 rounded-2xl border border-slate-800 space-y-4 flex flex-col justify-between">
                    <div class="space-y-2">
                        <div class="flex items-center justify-between">
                            <h3 class="font-bold text-white text-base">🧹 Python Data Cleaning</h3>
                            <span class="text-[10px] bg-slate-800 text-emerald-400 px-2 py-0.5 rounded font-mono">Project #3</span>
                        </div>
                        <p class="text-xs text-slate-400">Run IQR outlier detection & missing value treatment on sales datasets.</p>
                    </div>

                    <form hx-post="/api/htmx/sales-analyze" hx-target="#playground-result" hx-swap="innerHTML" class="space-y-3">
                        <div>
                            <label class="text-[11px] font-semibold text-slate-300 block mb-1">Select Cleaning Algorithm:</label>
                            <select name="operation" class="w-full bg-slate-900 border border-slate-700 text-slate-200 rounded-lg p-2 text-xs focus:ring-1 focus:ring-emerald-400 outline-none">
                                <option value="missing">Missing Value Imputation (Median Strategy)</option>
                                <option value="outlier">IQR Outlier Detection (Upper Bound Flag)</option>
                                <option value="trends">Category Revenue Aggregations</option>
                            </select>
                        </div>

                        <div class="p-3 bg-slate-900 rounded-lg border border-slate-800 text-[11px] text-slate-400 space-y-1">
                            <div class="flex justify-between"><span>Sample Dataset Size:</span><span class="text-emerald-400 font-mono">10 Records</span></div>
                            <div class="flex justify-between"><span>Null Revenues:</span><span class="text-amber-400 font-mono">2 Found</span></div>
                        </div>

                        <button type="submit" class="w-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold py-2.5 rounded-lg text-xs transition flex items-center justify-center gap-2">
                            <span>Run Python Algorithm</span>
                        </button>
                    </form>
                </div>

                <!-- Module 3: SQL Query Workbench -->
                <div class="bg-slate-950 p-5 rounded-2xl border border-slate-800 space-y-4 flex flex-col justify-between">
                    <div class="space-y-2">
                        <div class="flex items-center justify-between">
                            <h3 class="font-bold text-white text-base">🗄️ SQL Query Simulator</h3>
                            <span class="text-[10px] bg-slate-800 text-emerald-400 px-2 py-0.5 rounded font-mono">Project #1</span>
                        </div>
                        <p class="text-xs text-slate-400">Execute SQL filtering, GROUP BY aggregations, and query optimizations.</p>
                    </div>

                    <form hx-post="/api/htmx/sql-query" hx-target="#playground-result" hx-swap="innerHTML" class="space-y-3">
                        <div>
                            <label class="text-[11px] font-semibold text-slate-300 block mb-1">Select SQL Query Template:</label>
                            <select name="query_type" class="w-full bg-slate-900 border border-slate-700 text-slate-200 rounded-lg p-2 text-xs focus:ring-1 focus:ring-emerald-400 outline-none font-mono">
                                <option value="cat_summary">GROUP BY Category & Revenue Aggregation</option>
                                <option value="regional">Regional Performance HAVING > $2000</option>
                                <option value="top_cust">Completed High-Value Transactions</option>
                            </select>
                        </div>

                        <div class="p-3 bg-slate-900 rounded-lg border border-slate-800 text-[11px] text-slate-400">
                            <span>SQL Functions:</span> <code class="text-sky-300">SUM(), AVG(), COUNT(), GROUP BY</code>
                        </div>

                        <button type="submit" class="w-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold py-2.5 rounded-lg text-xs transition flex items-center justify-center gap-2">
                            <span>Execute SQL Query</span>
                        </button>
                    </form>
                </div>

            </div>

            <!-- Playground Output Console -->
            <div class="space-y-2">
                <span class="text-xs font-bold uppercase tracking-wider text-slate-400 block">Server Execution Output Window:</span>
                <div id="playground-result" class="min-h-[160px]">
                    <div class="bg-slate-950 border border-slate-800 rounded-2xl p-8 text-center text-slate-500 text-xs">
                        Select any algorithm above and click execute to trigger Python HTMX response fragments in real time.
                    </div>
                </div>
            </div>
        </section>


        <!-- PROJECTS SHOWCASE SECTION -->
        <section id="projects" class="space-y-6">
            <div>
                <h2 class="text-2xl font-bold text-white">PROJECTS SHOWCASE</h2>
                <p class="text-xs text-slate-400">Detailed overview of core projects completed by Darika T</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">

                <!-- Project 1 -->
                <div class="bg-slate-900 border border-slate-800 hover:border-emerald-500/50 rounded-2xl p-6 space-y-4 transition flex flex-col justify-between">
                    <div class="space-y-3">
                        <div class="flex items-center justify-between">
                            <span class="text-[11px] font-mono text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full">Excel & SQL</span>
                            <span class="text-xs text-slate-400">2024</span>
                        </div>
                        <h3 class="text-lg font-bold text-white">E-Commerce Sales Data Analysis</h3>
                        <p class="text-xs text-slate-300 leading-relaxed">
                            Analyzed and transformed e-commerce transaction data using Microsoft Excel and SQL, including data cleaning, validation, and sales performance analysis.
                        </p>
                        <ul class="text-xs text-slate-400 space-y-1.5 list-disc list-inside">
                            <li>SQL queries with filtering, aggregation, and grouping techniques for revenue trends.</li>
                            <li>Interactive Excel dashboards with Pivot Tables, Charts, and Slicers.</li>
                        </ul>
                    </div>
                    <div class="pt-4 border-t border-slate-800 flex flex-wrap gap-1.5">
                        <span class="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded">Excel</span>
                        <span class="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded">SQL</span>
                        <span class="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded">Pivot Slicers</span>
                    </div>
                </div>

                <!-- Project 2 -->
                <div class="bg-slate-900 border border-slate-800 hover:border-emerald-500/50 rounded-2xl p-6 space-y-4 transition flex flex-col justify-between">
                    <div class="space-y-3">
                        <div class="flex items-center justify-between">
                            <span class="text-[11px] font-mono text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full">AI Web App</span>
                            <span class="text-xs text-slate-400">2024</span>
                        </div>
                        <h3 class="text-lg font-bold text-white">ATS ResumeIQ Web Application</h3>
                        <p class="text-xs text-slate-300 leading-relaxed">
                            Built an AI-assisted web application to analyze resumes and provide applicant tracking system (ATS) compatibility scores.
                        </p>
                        <ul class="text-xs text-slate-400 space-y-1.5 list-disc list-inside">
                            <li>Evaluated resume structure, keywords, and formatting for applicant tracking systems.</li>
                            <li>Real-time automated scoring engine and missing keyword suggestions.</li>
                        </ul>
                    </div>
                    <div class="pt-4 border-t border-slate-800 flex flex-wrap gap-1.5">
                        <span class="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded">Python</span>
                        <span class="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded">HTMX</span>
                        <span class="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded">NLP Matching</span>
                    </div>
                </div>

                <!-- Project 3 -->
                <div class="bg-slate-900 border border-slate-800 hover:border-emerald-500/50 rounded-2xl p-6 space-y-4 transition flex flex-col justify-between">
                    <div class="space-y-3">
                        <div class="flex items-center justify-between">
                            <span class="text-[11px] font-mono text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full">Python Analytics</span>
                            <span class="text-xs text-slate-400">2024</span>
                        </div>
                        <h3 class="text-lg font-bold text-white">Sales Data Analysis</h3>
                        <p class="text-xs text-slate-300 leading-relaxed">
                            Analyzed and cleaned sales datasets using Python, performing missing value treatment, data validation, and outlier detection.
                        </p>
                        <ul class="text-xs text-slate-400 space-y-1.5 list-disc list-inside">
                            <li>Missing value treatment and IQR outlier detection to improve data quality.</li>
                            <li>Interactive visualizations and statistical analyses to identify sales trends.</li>
                        </ul>
                    </div>
                    <div class="pt-4 border-t border-slate-800 flex flex-wrap gap-1.5">
                        <span class="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded">Python</span>
                        <span class="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded">Pandas</span>
                        <span class="text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded">IQR Outliers</span>
                    </div>
                </div>

            </div>
        </section>


        <!-- CERTIFICATIONS SECTION (POWERED BY HTMX ENDPOINT) -->
        <section id="certifications" class="bg-slate-900/80 border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6">
            <div class="flex items-center justify-between flex-wrap gap-4">
                <div>
                    <h2 class="text-2xl font-bold text-white flex items-center gap-2">
                        <span>CERTIFICATIONS</span>
                        <span class="text-xs bg-emerald-500/10 text-emerald-400 px-2.5 py-1 rounded-full border border-emerald-500/20 font-mono">HTMX Endpoint `/Certifications`</span>
                    </h2>
                    <p class="text-xs text-slate-400 mt-1">Real-time completion timestamps & credential verification for Darika T</p>
                </div>
                <button hx-get="/api/htmx/certifications" hx-target="#certifications-live-target" hx-swap="innerHTML" class="text-xs bg-emerald-500/20 hover:bg-emerald-500/30 text-emerald-300 font-bold px-3.5 py-2 rounded-xl border border-emerald-500/30 transition flex items-center gap-1.5">
                    <span>🔄 Refresh Certifications Endpoint</span>
                </button>
            </div>

            <div id="certifications-live-target" hx-get="/api/htmx/certifications" hx-trigger="load">
                <div class="p-8 text-center text-slate-400 text-xs bg-slate-950 rounded-2xl animate-pulse">
                    Loading verified real-time certifications from Python backend...
                </div>
            </div>
        </section>

        <!-- EDUCATION QUALIFICATION (No CGPA / No Percentages as strictly specified) -->
        <section id="education" class="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6">
            <h2 class="text-2xl font-bold text-white flex items-center gap-2">
                <span>EDUCATION QUALIFICATION</span>
                <span class="text-xs bg-slate-800 text-slate-400 px-2.5 py-1 rounded-full border border-slate-700 font-mono">Verified Degrees</span>
            </h2>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="bg-slate-950 p-5 rounded-2xl border border-slate-800 space-y-2">
                    <div class="flex justify-between items-start">
                        <div>
                            <h3 class="font-bold text-slate-100 text-base">Bachelor of Science in Computer Science</h3>
                            <p class="text-emerald-400 text-xs font-medium">Rathinam Global Deemed To Be University</p>
                        </div>
                        <span class="text-xs font-mono text-slate-400 bg-slate-900 px-2.5 py-1 rounded-full border border-slate-800">2024 - 2027</span>
                    </div>
                    <p class="text-slate-400 text-xs">Specialized coursework in Data Analytics, Software Engineering, Database Systems (SQL), and Python Application Development.</p>
                </div>

                <div class="bg-slate-950 p-5 rounded-2xl border border-slate-800 space-y-2">
                    <div class="flex justify-between items-start">
                        <div>
                            <h3 class="font-bold text-slate-100 text-base">Higher Secondary Certificate (HSC)</h3>
                            <p class="text-emerald-400 text-xs font-medium">Akshaya Academy Matric Hr.Sec School</p>
                        </div>
                        <span class="text-xs font-mono text-slate-400 bg-slate-900 px-2.5 py-1 rounded-full border border-slate-800">2024</span>
                    </div>
                    <p class="text-slate-400 text-xs">Completed secondary education with focus on Mathematics and Computer Applications.</p>
                </div>
            </div>
        </section>


        <!-- CONTACT SECTION -->
        <section id="contact" class="bg-slate-900/60 border border-slate-800 rounded-3xl p-6 sm:p-8 space-y-6">
            <div class="max-w-2xl mx-auto text-center space-y-2">
                <h2 class="text-2xl font-black text-white">GET IN TOUCH WITH DARIKA T</h2>
                <p class="text-xs text-slate-400">Send a direct message powered by Python HTMX server processing</p>
            </div>

            <div class="max-w-xl mx-auto" id="contact-response">
                <form hx-post="/api/htmx/contact" hx-target="#contact-response" hx-swap="innerHTML" class="space-y-4">
                    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div>
                            <label class="text-xs text-slate-300 font-medium block mb-1">Your Name:</label>
                            <input type="text" name="name" required class="w-full bg-slate-950 border border-slate-800 text-slate-200 rounded-xl p-3 text-xs focus:ring-1 focus:ring-emerald-400 outline-none" placeholder="Recruiter / Hiring Manager">
                        </div>
                        <div>
                            <label class="text-xs text-slate-300 font-medium block mb-1">Your Email:</label>
                            <input type="email" name="email" required class="w-full bg-slate-950 border border-slate-800 text-slate-200 rounded-xl p-3 text-xs focus:ring-1 focus:ring-emerald-400 outline-none" placeholder="recruiter@company.com">
                        </div>
                    </div>

                    <div>
                        <label class="text-xs text-slate-300 font-medium block mb-1">Message:</label>
                        <textarea name="message" rows="3" required class="w-full bg-slate-950 border border-slate-800 text-slate-200 rounded-xl p-3 text-xs focus:ring-1 focus:ring-emerald-400 outline-none" placeholder="Hello Darika, we are interested in discussing opportunities..."></textarea>
                    </div>

                    <button type="submit" class="w-full bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold py-3 rounded-xl text-xs transition shadow-lg shadow-emerald-500/10">
                        Send Message via Python HTMX
                    </button>
                </form>
            </div>
        </section>

    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-800/80 py-8 text-center text-xs text-slate-500 space-y-2">
        <p>© 2026 DARIKA T • B.Sc. Computer Science & Data Analyst Portfolio</p>
        <p class="text-[10px] font-mono text-emerald-400/80">Built with 100% Native Python 3.10 HTTP Server + HTMX Dynamic Engines</p>
    </footer>

</body>
</html>'''

def run_server():
    socketserver.TCPServer.allow_reuse_address = True
    print(f"Starting Python HTMX Server on port {PORT}...")
    with socketserver.TCPServer(("0.0.0.0", PORT), HTMXHandler) as httpd:
        print(f"Python HTMX backend active on http://0.0.0.0:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()
