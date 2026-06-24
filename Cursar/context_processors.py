from datetime import datetime

def year_context(request):
    year = datetime.now().year
    return {'year': year}