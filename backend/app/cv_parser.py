import re

def parse_resume(text):
    """
    Extracts skills and experience from a resume text.
    
    Args:
        text (str): Resume content as text.
    
    Returns:
        dict: Extracted skills and experience.
    """
    skills_keywords = ["Python", "JavaScript", "React", "SQL", "Machine Learning", "Django", "AWS"]
    experience_pattern = r"(\d+)\s*years?\s*experience"

    skills = [skill for skill in skills_keywords if skill.lower() in text.lower()]
    experience_match = re.search(experience_pattern, text)

    experience = experience_match.group(1) if experience_match else "Not specified"

    return {"skills": skills, "experience": experience}
