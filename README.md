# python-mongo-uic

Provides a simple, reusable way to implement optimistic concurrency control in MongoDB for Python. This package is inspired by Mongoose's update-if-current plugin, allowing you to safely update documents in a concurrent environment.

## Installation
To install the package, execute the command:
```
pip install git+https://github.com/agumbe-ai/python-mongo-uic.git
```

## Usage
1. Import the package:
```
from versioned import update_if_current
```

2. Define your Document Structure. 
   
   The MongoDB document should include a `version` field to manage versioning:
```
    model_doc = ModelDocument(
        name="meddle",
        primary_contact="david@pink-floyd.ai",
        model_weight="",
        model_arch="",
        training_logs="",
        owner_id="12345",
        tenant_id="54321",
        version=1
    )
```
3. Insert the Document into MongoDB.
```
    client = MongoClient(os.environ['MONGO_URI'])
    db = client[os.environ['MYDB']]
    model_doc = ModelDocument.from_dict(body)
    result = model_doc.save_to_db(db.models)
    model_dict = model_doc.to_dict()
    model_dict["_id"] = str(result.inserted_id)
```
4. Update the Document with Version Control.
   
When updating a document, ensure that the Version field matches the current version in the database. Use the `update_if_current` function to perform an atomic update:
```
    filter_dict["version"] = version
        
    # Add atomic increment of version to the update
    update_dict["$inc"] = {"version": 1}

    # Use find_one_and_update to ensure atomicity and return the updated document
    updated_document = collection.find_one_and_update(
        filter_dict,
        update_dict,
        return_document=ReturnDocument.AFTER  # Return the updated document
    )
```


## API Reference
### Class: `VersionConflictError`
* Custom exception class which mimics Go's version conflict error

* Description: This class is used to raise an exception when the version provided in the request does not match the current version of the document.

* Inheritance: Inherits from the built-in Exception class.


### Function: `update_if_current(collection, filter_dict, update_dict, version)`
Looks for a document where the current version matches the provided version. If found, the `version` field is incremented atomically. 

* Parameters:
    * `collection`: The MongoDB collection.
    * `filter_dict`: The filter to find the document (must contain _id or similar key).  
    * `update_dict`: The update operation (without version increment).
    * `version`: The expected current version of the document.

* Returns: 
    The updated document, or raises a `VersionConflictError` if the version doesn't match.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss changes.

## License
This project is licensed under the MIT License.