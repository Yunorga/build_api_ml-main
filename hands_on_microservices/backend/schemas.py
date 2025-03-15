from pydantic import BaseModel

class PredictRequest(BaseModel):
    image_base64: str

class PredictResponse(BaseModel):
    predicted_shape: str

class UpdateShapeRequest(BaseModel):
    image_id: int
    new_shape: str

class UserAuth(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
