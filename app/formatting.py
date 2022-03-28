from app import app

## format date ##
@app.template_filter()
def dateFormat(value):
    return value.strftime("%Y-%m-%d")