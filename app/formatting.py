from app import app

## format date ##
@app.template_filter()
def dateFormat(value):
    return value.strftime("%Y-%m-%d")

@app.template_filter()
def moneyFormat(value):
    value = float(value)
    return f"${value:,.2f}"