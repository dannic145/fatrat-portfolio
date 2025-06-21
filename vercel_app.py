from app import vercel_handler

# Vercel requires a handler named "app"
def app(request):
    return vercel_handler(request)
