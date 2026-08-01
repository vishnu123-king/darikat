import { Skill, Project, Certification, Education } from './types';

export const PERSONAL_INFO = {
  name: "DARIKA T",
  title: "Data Analyst & Computer Science Professional",
  tagline: "Bridging Raw Data, Python Analytics, and Intelligent Web Applications",
  email: "tdarika3@gmail.com",
  phone: "+91 9342362394",
  github: "https://github.com/tdarika3-ui",
  linkedin: "https://www.linkedin.com/in/darika-t-883124320/",
  location: "Coimbatore, Tamil Nadu, India",
  defaultCareerObjective: "Dedicated B.Sc. Computer Science practitioner and Results-Driven Data Analyst with strong technical expertise in Python, SQL, Java, Excel, and Power BI. Proven track record in developing AI-assisted web applications, cleaning complex sales datasets, and translating transaction data into actionable business insights. Eager to leverage analytical rigor and collaborative problem-solving to contribute to high-impact technical initiatives."
};

export const SKILLS_DATA: Skill[] = [
  // Programming Languages
  {
    name: "Python",
    category: "programming",
    level: "Advanced",
    desc: "Data cleaning, statistical analysis, outlier detection, Pandas logic, and web automation",
    icon: "🐍",
    color: "emerald"
  },
  {
    name: "SQL",
    category: "programming",
    level: "Advanced",
    desc: "Filtering, aggregations, GROUP BY, subqueries, revenue trend extraction, and schema queries",
    icon: "🗄️",
    color: "sky"
  },
  {
    name: "Java",
    category: "programming",
    level: "Intermediate",
    desc: "Object-oriented programming, data structures, and core application logic",
    icon: "☕",
    color: "amber"
  },
  
  // Tools & Platforms
  {
    name: "Microsoft Excel",
    category: "tools",
    level: "Advanced",
    desc: "Pivot Tables, Charts, Slicers, Data Validation, VLOOKUP, and interactive sales dashboards",
    icon: "📊",
    color: "emerald"
  },
  {
    name: "Power BI",
    category: "tools",
    level: "Intermediate",
    desc: "Data modeling, interactive dashboards, visual storytelling, and business metrics tracking",
    icon: "📈",
    color: "yellow"
  },
  {
    name: "Google Colab",
    category: "tools",
    level: "Advanced",
    desc: "Jupyter environment, cloud Python execution, data visualization libraries, and notebook documentation",
    icon: "☁️",
    color: "orange"
  },

  // Soft Skills
  {
    name: "Time Management",
    category: "soft",
    level: "Core Competency",
    desc: "Prioritizing tasks and delivering project milestones promptly",
    icon: "⏱️",
    color: "purple"
  },
  {
    name: "Presentation Skills",
    category: "soft",
    level: "Core Competency",
    desc: "Communicating complex analytical findings clearly to non-technical stakeholders",
    icon: "🎙️",
    color: "indigo"
  },
  {
    name: "Leadership & Teamwork",
    category: "soft",
    level: "Core Competency",
    desc: "Fostering collaborative problem-solving, taking initiative, and driving shared goals",
    icon: "👥",
    color: "teal"
  }
];

export const PROJECTS_DATA: Project[] = [
  {
    id: "e-commerce-sales",
    title: "E-COMMERCE SALES DATA ANALYSIS",
    subtitle: "Microsoft Excel & SQL Analytics Project",
    tech: ["SQL", "Microsoft Excel", "Pivot Tables", "Slicers", "Data Validation"],
    category: "excel",
    badge: "Excel & SQL",
    description: [
      "Analyzed and transformed e-commerce transaction data using Microsoft Excel and SQL, executing data cleaning, validation, and performance diagnostics.",
      "Developed advanced SQL queries utilizing filtering, aggregation, and grouping techniques to extract key insights on customer purchasing behavior and product trends.",
      "Built interactive Excel dashboards featuring Pivot Tables, Charts, and Slicers to enable efficient executive visualization of key business metrics and sales volume."
    ]
  },
  {
    id: "ats-resumeiq",
    title: "ATS RESUMEIQ WEB APPLICATION",
    subtitle: "AI-Assisted Resume & ATS Scoring System",
    tech: ["Python", "AI Analysis", "Web Development", "Keyword Matching", "ATS Logic"],
    category: "ai",
    badge: "AI Web App",
    description: [
      "Built an AI-assisted web application designed to analyze candidate resumes and compute instant ATS compatibility scores.",
      "Evaluated resume structure, formatting hierarchy, key technical competencies, and target job description keyword resonance for modern Applicant Tracking Systems.",
      "Engineered automated feedback generation identifying missing keywords and formatting improvements to elevate interview callback rates."
    ]
  },
  {
    id: "python-sales-analysis",
    title: "SALES DATA ANALYSIS",
    subtitle: "Python Data Wrangling & Insights Pipeline",
    tech: ["Python", "Data Cleaning", "Outlier Detection", "Data Validation", "Statistical Analysis"],
    category: "python",
    badge: "Python Analytics",
    description: [
      "Analyzed and cleaned a comprehensive sales dataset using Python, executing missing value imputation, data validation, and outlier detection routines to ensure pristine data quality.",
      "Developed interactive visualizations and statistical analytical pipelines to identify seasonal sales trends, customer purchasing frequency, and revenue concentration.",
      "Extracted high-value business recommendations directly driving strategic inventory management and promotional campaign optimization."
    ]
  }
];

export const CERTIFICATIONS_DATA: Certification[] = [
  {
    title: "Basics of Data Visualization",
    issuer: "LinkedIn Learning",
    date: "Certified",
    skills: ["Data Visualization", "Visual Hierarchy", "Chart Selection", "Dashboard Design"],
    icon: "📜"
  },
  {
    title: "Learning Python",
    issuer: "Infosys SpringBoard",
    date: "Certified",
    skills: ["Python Programming", "Data Structures", "Control Flow", "Algorithmic Logic"],
    icon: "🐍"
  }
];

export const EDUCATION_DATA: Education[] = [
  {
    degree: "Bachelor of Science in Computer Science",
    period: "2024 – 2027",
    institution: "Rathinam Global Deemed To Be University"
  },
  {
    degree: "HSC (Higher Secondary Certificate)",
    period: "2024",
    institution: "Akshaya Academy Matric Hr.Sec School"
  }
];
