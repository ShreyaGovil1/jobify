def calculate_job_match_score(job_requirements, user_skills):
    """
    Calculate a match score between job requirements and user skills.
    
    Args:
        job_requirements (list): List of job skills.
        user_skills (list): User's extracted skills.
        
    Returns:
        float: Match score (0-100%).
    """
    if not job_requirements or not user_skills:
        return 0
    
    job_requirements = [req.lower() for req in job_requirements]
    user_skills = [skill.lower() for skill in user_skills]

    matches = sum(1 for skill in user_skills if any(req in skill or skill in req for req in job_requirements))
    
    match_percentage = (matches / len(job_requirements)) * 100
    return min(match_percentage, 100)
