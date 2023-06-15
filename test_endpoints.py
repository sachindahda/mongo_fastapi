import pytest
import requests

# Set the base URL for making requests to the API
BASE_URL = "http://localhost:8000"

def test_get_all_courses():
    response = requests.get(f"{BASE_URL}/courses")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_get_course_overview():
    course_id = "6489fb29afcae5d974735ae9"  
    response = requests.get(f"{BASE_URL}/courses/{course_id}")
    assert response.status_code == 200
    assert "name" in response.json()
    assert "description" in response.json()
    assert "domain" in response.json()
    assert "chapters" in response.json()

def test_get_chapter_info():
    course_id = "6489fb29afcae5d974735ae9"  # Replace with a valid course ID
    chapter_name = "CNN Architectures"  # Replace with a valid chapter name
    response = requests.get(f"{BASE_URL}/courses/{course_id}/chapters/{chapter_name}")
    assert response.status_code == 200
    assert "name" in response.json()
    assert "text" in response.json()

def test_rate_chapter():
    course_id = "6489fb29afcae5d974735ae9"  # Replace with a valid course ID
    chapter_name = "CNN Architectures"  # Replace with a valid chapter name
    rating = 1  # Replace with a valid rating value (+1 or -1)
    response = requests.post(
        f"{BASE_URL}/courses/{course_id}/chapters/{chapter_name}/rate/{rating}",
        json={"rating": rating}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Rating submitted successfully"

# Run the tests
if __name__ == "__main__":
    pytest.main(["-v"])
