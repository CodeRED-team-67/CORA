from fastapi import APIRouter
import json
from pathlib import Path

router = APIRouter()

# Base path for all subject folders
SUBJECTS_DIR = Path(__file__).resolve().parent.parent / "data" / "subjects"

def load_json(path: Path):
    with open(path, "r") as f:
        return json.load(f)

# ------------------------------------------
# ROUTE 1 — List all subjects + course counts
# ------------------------------------------
@router.get("/")
def list_subjects_summary():
    subjects = []

    for subject_folder in SUBJECTS_DIR.iterdir():
        if subject_folder.is_dir():
            course_files = list(subject_folder.glob("*.json"))
            total_courses = len(course_files)

            subjects.append({
                "id": subject_folder.name,
                "name": subject_folder.name.replace("-", " ").title(),
                "total_courses": total_courses
            })

    return {"subjects": subjects}


# ------------------------------------------
# ROUTE 2 — List all courses for a subject
# ------------------------------------------
@router.get("/{subject_id}")
def list_courses_for_subject(subject_id: str):
    subject_path = SUBJECTS_DIR / subject_id
    if not subject_path.exists():
        return {"error": "Subject not found"}

    courses = []
    for file_path in subject_path.glob("*.json"):
        data = load_json(file_path)
        courses.append({
            "id": data["id"],
            "title": data["title"]
        })

    return {
        "subject": subject_id.replace("-", " ").title(),
        "total_courses": len(courses),
        "courses": courses
    }


# ------------------------------------------
# ROUTE 3 — Get full course info
# ------------------------------------------
@router.get("/{subject_id}/{course_id}")
def get_course_info(subject_id: str, course_id: str):
    file_path = SUBJECTS_DIR / subject_id / f"{course_id}.json"
    if not file_path.exists():
        return {"error": "Course not found"}
    return load_json(file_path)
