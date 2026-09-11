from web.model.auth_model import SignUpRequest

class AuthMapper:
    @staticmethod
    def signup_request_to_user_data(request: SignUpRequest):
        return {
            "login": request.login,
            "password": request.password
        }