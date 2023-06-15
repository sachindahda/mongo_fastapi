import json
from database.connection import *


# # Create a database for the courses
database = client[db_name]
print(f'database_names{client.list_database_names()}')
# print(f'database_{database.}')



# # Create a collection for the courses
courses_collection = database[courses_collection_name]
print(f'db_collection_{database.list_collection_names()}')
print(f'courses_collection_{courses_collection}')



with open('courses.json') as file:
    course_data = json.load(file)

# # Create indices for efficient retrieval
courses_collection.create_index('name')
courses_collection.create_index('date')


# # Insert the course data into the collection
inserted_courses_records=courses_collection.insert_many(course_data)

print(f'ids_inserted_{inserted_courses_records.inserted_ids}')


# # Close the MongoDB connection
client.close()
