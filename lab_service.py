from app.extensions import db
from app.models import LabJob


def create_lab_job(job_no, customer_id, branch_id, sale_id=None, prescription_id=None, lens_description='', frame_description=''):
    job = LabJob(
        job_no=job_no, customer_id=customer_id, branch_id=branch_id, sale_id=sale_id,
        prescription_id=prescription_id, lens_description=lens_description, frame_description=frame_description
    )
    db.session.add(job)
    db.session.commit()
    return job
