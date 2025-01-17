# Python UIC

Provides a simple, reusable way to implement optimistic concurrency control in MongoDB for Python. This package is inspired by Mongoose's update-if-current plugin, allowing you to safely update documents in a concurrent environment.

## Installation
To install the package, execute the command:
```
pip install python-uic
```

## Usage
1. Import the package:
```
from python-uic import versioned
from versioned import update_if_current, set_initial_version
```

```
# Define python struct eg product
# Explain how this is supposed to be used
# When creating a new product and updating a product 
# If version number matches
    # Update
# Else
    # Handle version conflict
```

2. Define your Document Struct. 
   
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

5. Handle Version Conflicts.

   If the version in the database does not match the version provided in the update, the update will not be applied, and the function will return a `VersionConflictError`. This allows you to handle concurrency issues safely.
```
    if updated_document is None:
        raise VersionConflictError("Version conflict occurred")
```

## API Reference
`update_if_current(collection, filter_dict, update_dict, version)`

Attempts to update a document if the current version matches the provided version. If successful, it increments the version field atomically.

`VersionConflictError`
An error returned when the version in the database does not match the expected version, indicating that the document has been modified by another process.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss changes.

## License
This project is licensed under the MIT License.