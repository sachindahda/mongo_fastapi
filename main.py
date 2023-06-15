from fastapi import FastAPI,HTTPException, Query
from database.connection import *
from bson import json_util
from bson.objectid import ObjectId
from enum import Enum
from fastapi.responses import JSONResponse
import pydantic,json
# pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str

app = FastAPI()

# Specify the database and collection names
db = client[db_name]

course_collection = db[courses_collection_name]


@app.get('/courses')
def get_courses(sort_by: str = 'alphabetical', domain: str = None):
    '''
        API Endpoint To Fetch All of the courses stored in our database
        Parameters:
            sort_by (str): To Sort Courses by various parameters including alphabetical,date,rating etc
            domain (str): To Filter Courses by domains
        Returns:
            {} (dict): Courses in JSON Format
        Created By: Sachin Dahda
        Created On: 2023-06-15
    '''
    print(f'db_{db}')
    # Filter courses by domain if provided
    filter_query = {} if not domain else {'domain': domain}
    # Sort courses based on the specified mode
    if sort_by == 'alphabetical':
        sort_query = [('name', 1)]
    elif sort_by == 'date':
        sort_query = [('date', -1)]
    elif sort_by == 'rating':
        sort_query = [('total_rating', -1)]
    else:
        sort_query = [('name', 1)]
    print(f'sort_query_{sort_query}')
    # Retrieve the courses from the collection
    courses = course_collection.find(filter_query,{}).sort(sort_query)
    serialized_courses=json.loads(json_util.dumps(courses))
    return  JSONResponse(content=list(serialized_courses))


@app.get('/courses/{course_id}')
def get_course_overview(course_id: str):
    '''
        API Endpoint To Fetch Paricular course based on course_id
        Parameters:
            course_id (str): Course Id
        Returns:
            {} (dict): Course in JSON Format Based on course_id parameter
        Created By: Sachin Dahda
        Created On: 2023-06-15
    '''
    # Retrieve the course information by its ID
    print(f'course_id_to_fetch_{ObjectId(course_id)}')
    course = course_collection.find_one({'_id': ObjectId(course_id)})

    if not course:
        return JSONResponse(content={"error": "Course not found"}, status_code=404)
    # course = json.dumps(course,default=str)
    course=json.loads(json_util.dumps(course))
    return JSONResponse(content=course)


@app.get('/courses/{course_id}/chapters/{chapter_name}')
def get_chapter_info(course_id: str, chapter_name: str):
    '''
        API Endpoint To Retreive Paricular Chapter based on course_id and chapter_name
        Parameters:
            course_id (str): Course Id
            chapter_name (str): Name of Chapter

        Returns:
            {} (dict): Information of Chapter(if found) in  JSON Format Based on course_id and chapter_name parameter
        Created By: Sachin Dahda
        Created On: 2023-06-15
    '''
    # Retrieve chapter information by course ID and chapter name
    course = course_collection.find_one({"_id": ObjectId(course_id)})
    if not course:
        return JSONResponse(content={"error": "Course not found"}, status_code=404)

    chapters = course.get("chapters", [])
    print(f'chapters_{chapters}')
    chapter = next((chap for chap in chapters if chap["name"] == chapter_name), None)
    print(f'chapter_{chapter}')
    if not chapter:
        return JSONResponse(content={"error": "Chapter not found"}, status_code=404)
    return JSONResponse(content=chapter)




@app.post('/courses/{course_id}/chapters/{chapter_name}/rate/{rating}')
def rate_chapter(course_id: str, chapter_name: str, rating:int):
    '''
        API Endpoint To Save Rating Paricular Chapter(+ve/-ve) based on course_id and chapter_name
        Parameters:
            course_id (str): Course Id
            chapter_name (str): Name of Chapter
            rating (int): Rating Number ranging frm -5 to +5

        Returns:
            {} (dict): Success/Error Message depending on the record
        Created By: Sachin Dahda
        Created On: 2023-06-15
    '''
    # Update chapter rating and aggregate course ratings
    print(f'course_id_{course_id}')
    print(f'chapter_name_{chapter_name}')
    print(f'rating_{rating}')

    # Check if rating is valid (+1 or -1)
    if rating not in list(range(-5,6)):
        return JSONResponse(content={"error": "Invalid rating value, Please Enter rating b/w -5 to +5"}, status_code=400)

    course_id_obj=ObjectId(course_id)
    print(f'course_id_obj_{course_id_obj}')

    # Update chapter rating and aggregate course ratings
    course = course_collection.find_one({"_id": course_id_obj})
    chapters = course.get("chapters", [])
    chapter = next((single_chapter for single_chapter in chapters if single_chapter["name"] == chapter_name), None)
    
    if not course:
        return JSONResponse(content={"error": "Course not found"}, status_code=404)
    if not chapter:
        return JSONResponse(content={"error": "Chapter not found"}, status_code=404)
    
    # Initialize chapter rating as 0 if not set previously
    if "rating" not in chapter:
        chapter["rating"] = 0

    # Update chapter rating
    chapter["rating"] += rating
    course_collection.update_one(
       {"_id": course_id_obj, "chapters.name": chapter_name},
        {"$inc": {"chapters.$.rating": rating}}
    )

    # Recalculate and update course rating
    course_rating = sum(single_chapter["rating"] if 'rating' in single_chapter else 0 for single_chapter in chapters) / len(chapters)
    print(f'course_rating_{course_rating}')
    course_collection.update_one(
        {"_id": course_id_obj},
        {"$set": {"rating": course_rating}}
    )
    return JSONResponse(content={"message": "Rating submitted successfully"})

