from flask import jsonify

class ApiResponse:
    def __init__(self, data=None, message=None, status=None):
        self.data = data
        self.message = message
        self.status = status

    def toResponse(self):
        response_body = {
            "message": self.message,
            "data": self.data,
            "code": self.status
        }
        return jsonify(response_body), self.status

class SuccessResponse(ApiResponse):
    def __init__(self, data=None, message="Thành công"):
        super().__init__(data, message, status=200)

class InternalServerErrorResponse(ApiResponse):
    def __init__(self, error="Sever chúng tôi không phản hồi vui lòng thử lại sau", data=None):
        message = str(error)
        super().__init__(data, message, status=500)