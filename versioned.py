from pymongo import MongoClient, ReturnDocument
from pymongo.errors import PyMongoError
import os

# Custom exception to mimic Go's version conflict error
class VersionConflictError(Exception):
    """Raised when a version conflict is detected"""
    pass


# Function to update a document if the current version matches the provided version
# This mimics the behavior of the Go code where it checks the version and increments atomically
def update_if_current(collection, filter_dict, update_dict, version):
    """
    Updates a document if the current version matches the provided version, atomically incrementing the version.
    
    :param collection: The MongoDB collection.
    :param filter_dict: The filter to find the document (must contain _id or similar key).
    :param update_dict: The update operation (without version increment).
    :param version: The expected current version of the document.
    :return: The updated document or raises VersionConflictError if the version doesn't match.
    """
    try:
        # Filter by the version field in addition to the other filters
        filter_dict["version"] = version
        
        # Add atomic increment of version to the update
        update_dict["$inc"] = {"version": 1}

        # Use find_one_and_update to ensure atomicity and return the updated document
        updated_document = collection.find_one_and_update(
            filter_dict,
            update_dict,
            return_document=ReturnDocument.AFTER  # Return the updated document
        )

        if updated_document is None:
            # No document found means the version conflict occurred
            raise VersionConflictError("Version conflict occurred")

        return updated_document

    except PyMongoError as e:
        # Handle other pymongo exceptions
        raise e

# Example usage
if __name__ == "__main__":
    # Connect to the MongoDB instance
    client = MongoClient(os.environ['MONGO_URI'])
    db = client[os.environ['MYDB']]
    collection = db.mycollection

    # Example filter and update data
    filter_dict = {"_id": 1}  # Assuming your document has an _id field
    update_dict = {"$set": {"name": "new name"}}  # The update data
    version = 1  # The current version you're expecting

    # Ensure the initial version is set to 1
    version = 1

    try:
        # Try updating the document if the version matches
        updated_doc = update_if_current(collection, filter_dict, update_dict, version)
        print("Updated document:", updated_doc)
    except VersionConflictError:
        print("Version conflict detected")
    except Exception as e:
        print("An error occurred:", e)
