from django.shortcuts import render

# python manage.py makemigrations --dry-run --verbosity 3

def blog(request):
    ctx = {

    }
    
    return render(request,"blogs/blogs.html", ctx)

