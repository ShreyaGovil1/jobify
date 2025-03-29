import logging
from app.models import Job, db

def initialize_jobs():
    """Initialize the database with some job data for testing"""
    jobs_data = [
        {
            "title": "Frontend Developer",
            "company": "TechCorp",
            "location": "San Francisco, CA",
            "description": "We're looking for a passionate Frontend Developer.",
            "requirements": "JavaScript, React, HTML, CSS, Git",
        },
        {
            "title": "Backend Engineer",
            "company": "DataSystems",
            "location": "New York, NY",
            "description": "Work on scalable backend solutions.",
            "requirements": "Python, Django, PostgreSQL, RESTful APIs",
        }
    ]
    
    if Job.query.count() == 0:
        try:
            for job_data in jobs_data:
                job = Job(**job_data)
                db.session.add(job)
            db.session.commit()
            logging.info("Initialized jobs database")
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error initializing jobs: {str(e)}")
    else:
        logging.info("Jobs already exist, skipping initialization")
