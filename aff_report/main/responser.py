import json

class Resp:
    def __init__(self, status, code, data):
        self.status = status
        self.code = code
        self.data = data

    def build(self):
        return json.dumps({"success": self.status, "code": self.code, "data": self.data})

def pull_response(status=False, code=0, data=None):
    result = Resp(status, code, data)
    return result.build()