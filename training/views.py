from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Level, Section, Exercise, UserProgress
from .forms import SignUpForm

# Sign-up view
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')  # Redirect to the homepage after sign-up
    else:
        form = SignUpForm()
    return render(request, 'training/signup.html', {'form': form})  # Use correct template path

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')  # Redirect to homepage after login
    else:
        form = AuthenticationForm()
    return render(request, 'training/login.html', {'form': form})

# Homepage view
def homepage(request):
    return render(request, 'training/homepage.html')  # Render the homepage template

# List all available levels
def level_list(request):
    levels = Level.objects.all()  # Query all levels from the database
    return render(request, 'training/level_list.html', {'levels': levels})

# View for a section (either reading or listening) within a level
@login_required(login_url='login')  # Ensures user is logged in
def section_detail(request, level_number, section_type):
    level = get_object_or_404(Level, level_number=level_number)
    section = get_object_or_404(Section, level=level, section_type=section_type)
    exercises = section.exercises.all()

    # Prepare exercises with split answer choices
    for exercise in exercises:
        exercise.answer_choices = exercise.answer_choices.split(',')

    # Check if user is authenticated before querying user progress
    if request.user.is_authenticated:
        user_progress = UserProgress.objects.filter(user=request.user, exercise__section=section)
    else:
        user_progress = None

    return render(request, 'training/section_detail.html', {
        'section': section,
        'exercises': exercises,
        'user_progress': user_progress,
    })


# View for a specific exercise
def exercise_detail(request, section_id, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id, section_id=section_id)

    submitted = False
    is_correct = None

    if request.method == 'POST':
        user_answer = request.POST.get('answer')
        submitted = True
        # Check if the answer is correct
        if user_answer == exercise.correct_answer:
            is_correct = True
            # Record the user's progress (save that they answered correctly)
            UserProgress.objects.create(user=request.user, exercise=exercise, is_correct=True)
        else:
            is_correct = False
            UserProgress.objects.create(user=request.user, exercise=exercise, is_correct=False)

    return render(request, 'training/exercise_detail.html', {
        'exercise': exercise,
        'submitted': submitted,
        'is_correct': is_correct
    })

