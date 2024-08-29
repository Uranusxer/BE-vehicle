from django.db import models
from utils.utils_require import MAX_CHAR_LENGTH,CheckRequire
from django.contrib.auth.hashers import make_password
from utils.constants import USER_STATUS,OFFLINE,ONLINE
from utils import utils_time
from django.http import HttpRequest
from utils.utils_jwt import check_jwt_token
from utils.utils_request import BAD_METHOD, request_failed

# Create your views here.
class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=MAX_CHAR_LENGTH, unique=True)
    password = models.CharField(max_length=MAX_CHAR_LENGTH)
    register_time = models.FloatField(default=utils_time.get_timestamp())
    login_time = models.FloatField(default=utils_time.get_timestamp())
    phone = models.BigIntegerField(default=0,null=True)
    status = models.CharField(max_length=20, choices=USER_STATUS, default=OFFLINE)
    manager = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)
    
    def set_login(self):
        self.login_time = utils_time.get_timestamp()
        self.status = ONLINE
        self.save()

    def serialize(self):
        data = {
            "id": self.id,
            "name": self.name,
            "phone":self.phone,
            "register_time":self.register_time,
            "login_time":self.login_time,
            "status":self.status
        }
        return data
    
@CheckRequire
def get_user_from_request(req: HttpRequest,type:str,type2:str=None):
    # Check if request method is POST
    if req.method != type and (type2 is None or req.method != type2):
        return BAD_METHOD, None
    jwt_token = req.headers.get("Authorization")
    user_data = check_jwt_token(token=jwt_token)
    # Check valid token  
    if not user_data:
        return request_failed(code=2, info="Invalid or expired JWT",status_code=401), None
    userID = user_data["userID"]
    # Check username in the token
    if not userID:
        return request_failed(code=-2,info="userID not contained in the jwt_token",status_code=400), None
    # Fetch the user from the database using user_id
    user = User.objects.filter(id=userID).first()
    if not user:    
        return request_failed(code=1,info="User does not exist",status_code=404), None
    return None, user