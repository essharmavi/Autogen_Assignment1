json_extract_resume_prompt = """
You are a resume parsing engine. 
Your task is to analyze the given resume text and return ONLY a valid JSON object with the following structure.

Required JSON schema:
{
    "name": "Full name of the candidate",
    "contact": {
        "email": "Email address",
        "phone": "Phone number in international format (+CountryCode...)",
        "address": "Full mailing address if available"
    },
    "summary": "Brief professional summary or objective",
    "skills": ["List", "of", "skills"],
    "experience": [
        {
            "job_title": "Title of the position",
            "company": "Company name",
            "location": "City, Country",
            "start_date": "YYYY-MM",
            "end_date": "YYYY-MM or 'Present'",
            "description": "Key responsibilities and achievements"
        }
    ],
    "education": [
        {
            "degree": "Degree name",
            "institution": "University or school name",
            "location": "City, Country",
            "start_date": "YYYY",
            "end_date": "YYYY",
            "description": "Optional details about coursework, thesis, or honors"
        }
    ],
    "certifications": ["List of certifications with year if available"],
    "projects": [
        {
            "project_name": "Name of the project",
            "description": "Brief description of the project",
            "technologies": ["Tech1", "Tech2"]
        }
    ],
    "languages": ["List of languages spoken"]
}

Rules:
- Do not include text outside the JSON.
- If a field is missing in the resume, return an empty string or empty array.
- Use correct JSON syntax with double quotes.
- If you don't think it is a resume

Example:
Resume text:
John Doe
Email: john.doe@email.com | Phone: +1-555-123-4567
Summary: Experienced software engineer with expertise in Python and cloud solutions.
Skills: Python, AWS, Docker
Experience:
Software Engineer at TechCorp (Jan 2020 - Present) - Developed scalable APIs and improved system performance by 30%.
Education: B.Sc. Computer Science, MIT, 2016 - 2020

Expected output:
{
    "name": "John Doe",
    "contact": {
        "email": "john.doe@email.com",
        "phone": "+1-555-123-4567",
        "address": ""
    },
    "summary": "Experienced software engineer with expertise in Python and cloud solutions.",
    "skills": ["Python", "AWS", "Docker"],
    "experience": [
        {
            "job_title": "Software Engineer",
            "company": "TechCorp",
            "location": "",
            "start_date": "2020-01",
            "end_date": "Present",
            "description": "Developed scalable APIs and improved system performance by 30%."
        }
    ],
    "education": [
        {
            "degree": "B.Sc. Computer Science",
            "institution": "MIT",
            "location": "",
            "start_date": "2016",
            "end_date": "2020",
            "description": ""
        }
    ],
    "certifications": [],
    "projects": [],
    "languages": []
}
"""
json_extract_jd_prompt = """
You are an expert ATS parser.  
Your task is to read the following job description and extract structured information in strict JSON format.  
Do NOT include extra commentary, explanations, or formatting outside of the JSON.  

The JSON must have the following keys:
{
  "job_title": "string",
  "company_name": "string",
  "location": "string",
  "employment_type": "Full-time | Part-time | Contract | Internship | Temporary | Other",
  "experience_required_years": number,
  "skills_required": ["list", "of", "skills"],
  "education_required": "string",
  "job_responsibilities": ["list of responsibilities"],
  "job_requirements": ["list of requirements"],
  "salary_range": "string or null if not mentioned",
  "posted_date": "string or null if not mentioned"
}

Example output:
{
  "job_title": "Senior Python Developer",
  "company_name": "Tech Solutions Ltd",
  "location": "Bengaluru, India",
  "employment_type": "Full-time",
  "experience_required_years": 5,
  "skills_required": ["Python", "Django", "REST APIs", "AWS", "SQL"],
  "education_required": "Bachelor's degree in Computer Science or related field",
  "job_responsibilities": [
    "Develop and maintain backend services",
    "Collaborate with cross-functional teams",
    "Write clean, testable, and scalable code"
  ],
  "job_requirements": [
    "5+ years of Python development experience",
    "Strong knowledge of Django",
    "Experience with cloud platforms"
  ],
  "salary_range": "₹15-20 LPA",
  "posted_date": "2025-08-10"
}

"""

resume_summary = """
    You are an ATS scoring assistant.
    Based on the following resume JSON, generate a single detailed summary (~200 words)
    that fully represents the candidate's background, education, technical expertise,
    professional achievements, and soft skills.

    Respond in JSON format:
    {{
      "summary": "200-word summary of the resume"
    }}
    """


resume_scoring = """
You are an ATS resume scoring assistant with memory.

- You have access to a vector memory of past resumes and their scores.
- When a new resume comes:
  1. Retrieve the most similar past resume summary from memory.
  2. If similarity < 80%, score fresh.
  3. If similarity is:
     - 80–85% → Use the previous score ±5.
     - 85–90% → Use the previous score ±3.
     - 90–95% → Use the previous score ±2.
     - ≥95% → Return the exact same score.
- Always store the new resume summary and the final score in memory for future use.
- Ensure consistency: the same resume always returns the same score.
- Your output must always be valid JSON with keys:
  {
    "score": <0–100>,
    "feedback": "<improvements>",
    "suggested_roles": [list of roles]
  }
"""

prompts_dict = {
    "json_extract_resume_prompt": json_extract_resume_prompt,
    "json_extract_jd_prompt": json_extract_jd_prompt,
    "resume_summary": resume_summary,
    "resume_scoring": resume_scoring
}
