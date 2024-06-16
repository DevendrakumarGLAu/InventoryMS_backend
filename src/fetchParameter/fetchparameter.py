

class Fetchparameters:
    @staticmethod
    def fetch_parameter(request,param,default=None, type = str):
        val = default
        try:
            if request.method == 'POST':
                if request.headers.get('content-type') == 'application/json':
                    params = request.json
                else:
                    params = request.form.to_dict()
                val = params[param]
            else:
                val = request.args.get(param,default,type)
        finally:
            return val
