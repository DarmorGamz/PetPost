from fastapi import HTTPException
import json
import os
import boto3
import string
from dotenv import load_dotenv

load_dotenv()

class petpost:
    def __init__(self):
        self.filename = '/data/pets.json'

        self.s3 = boto3.client('s3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION')
        )
        self.bucket_name = os.getenv('AWS_BUCKET_NAME')

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
                image = varsIn['image']
                image_key = f"pets/{image.filename}"
                self.s3.upload_fileobj(image.file, self.bucket_name, image_key, ExtraArgs={'ContentType': image.content_type})
                
                # Get S3 image url (public)
                imageUrl = f"https://{self.bucket_name}.s3.amazonaws.com/{image_key}"
                
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
            case "DelAll":
                with open(self.filename, 'r') as f:
                    pets = json.load(f)
                for pet in pets:
                    if 'imageUrl' in pet:
                        try:
                            key = pet['imageUrl'].split(f"https://{self.bucket_name}.s3.amazonaws.com/")[1]
                            self.s3.delete_object(Bucket=self.bucket_name, Key=key)
                        except IndexError:
                            pass  # Skip invalid URL
                with open(self.filename, 'w') as f:
                    json.dump([], f)
                return '', 200
            case _:
                raise HTTPException(400, "Invalid Cmd")
