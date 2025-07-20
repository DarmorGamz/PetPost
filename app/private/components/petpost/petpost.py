from fastapi import HTTPException
import json
import os
import string

class petpost:
    def __init__(self):
        self.filename = 'pets.json'

        # Ensure JSON file exists
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump([], f)

    def Gsad(self, cmd: string, varsIn: dict = None) -> dict | None:
        match cmd:
            case "Get":
                with open(self.filename, 'r') as f:
                    pets = json.load(f)
                return pets
            
            case "GetList":
                raise HTTPException(400, "Invalid Cmd")
            case "Set":
                raise HTTPException(400, "Invalid Cmd")
            case "Add":
                if varsIn is None or "name" not in varsIn or "age" not in varsIn or "breed" not in varsIn or "image" not in varsIn:
                    raise HTTPException(400, "Pet data required")
                
                # Add image to S3
                # Get S3 image url
                imageUrl = ""

                
                # Store JSON details on filesystem
                with open(self.filename, 'r+') as f:
                    pets = json.load(f)
                    pets.append({
                        'name': varsIn.get("name"),
                        'age': varsIn.get("age"),
                        'breed': varsIn.get("breed"),
                        'imageUrl': imageUrl
                    })
                    f.seek(0)
                    json.dump(pets, f)
                return '', 200
            
            case "Del":
                raise HTTPException(400, "Invalid Cmd")
            case _:
                raise HTTPException(400, "Invalid Cmd")
