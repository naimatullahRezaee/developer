from django.shortcuts import render,redirect
from .forms import ProjectForm, ReviewForm
from .models import Project, Tag
from .utils import searchProjects, paginateProjects
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def projects(request):

    search_query , projects = searchProjects(request)
    custom_page , projects = paginateProjects(request, projects, 2)

    context = {'projects':projects, 'search_query': search_query, 'custom_page': custom_page}
    return render(request, 'projects/projects.html' , context)

 

def single_project(request, pk):
    project = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()
        project.getVoteCount

        messages.success(request, 'your review was successfully submitted')
        return redirect('single-project', pk=project.id)

    context = {'project': project, 'form': form}
    return render(request, 'projects/single_project.html', context)



@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == 'POST':
        form= ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context = {'form': form}
    return render(request, "projects/project_form.html", context)


@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id =pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES ,instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form':form}
    return render(request, "projects/project_form.html", context)

    
@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile

    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')

    context = {'object':project}
    return render(request, 'delete_template.html', context)