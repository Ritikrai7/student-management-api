from pydantic import BaseModel

class EnrollStudent(BaseModel):
    
    student_id:int
    course_id:int