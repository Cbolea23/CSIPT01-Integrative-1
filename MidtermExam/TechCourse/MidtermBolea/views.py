from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import Professor, Course, Assignment

def index(request):
    professors = Professor.objects.all()
    return render(request, 'index.html', {'professors': professors})

def details(request, prof_id):
    professor = get_object_or_404(Professor, ProfessorID=prof_id)
    
    courses = Course.objects.filter(professor=professor)
    assignments = Assignment.objects.filter(professor=professor)
    
    total = assignments.aggregate(Sum('Total_Amount'))['Total_Amount__sum'] or 0

    context = {
        'professor': professor,
        'courses': courses,
        'assignments': assignments,
        'total_amount': total
    }
    return render(request, 'details.html', context)