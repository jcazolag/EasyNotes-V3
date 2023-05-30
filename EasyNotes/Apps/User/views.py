from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.http import JsonResponse

# Create your views here.
#@login_required
def userhome(request):
    if request.user.is_authenticated:
        groups = UserGroups.objects.filter(user_id=request.user.id)
        notes=[]
        for group in groups:
            if UserNotes.objects.filter(group_id=group.id):
                notes.append(UserNotes.objects.filter(group_id=group.id))
        data={
            'groups': groups,
            'notes': notes
        }
        return render(request, 'userhome.html', data)
    else:
        return redirect("home") 


#@login_required
def userconfig(request):
    if request.user.is_authenticated:
        return render(request, 'userconfig.html')
    else:
        return redirect("home")

#@login_required
def groups(request):
    if request.user.is_authenticated:
        try:
            grupos = UserGroups.objects.filter(user_id=request.user.id)
            return render(request, 'userGroups.html', {'groups': grupos})
        except Exception as e:
            print(e)
    else:
        return redirect("home")

#@login_required
#@csrf_exempt
def createGroups(request):
    if request.user.is_authenticated and request.method == 'POST' and 'title' in request.POST:
        try:
            title = request.POST['title']
            model = UserGroups(title=title,user_id=request.user.id)
            model.save()
            return redirect('/user/groups/')
        except Exception as e:
            print(e)
            return redirect('/user/groups/')
    else:
        return redirect("home")

def showGroup(request):
    if request.user.is_authenticated and request.method == 'POST' and 'group_id' in request.POST:
        try:
            group_id = request.POST['group_id']
            notes = UserNotes.objects.filter(group_id=group_id)
            group = get_object_or_404(UserGroups,pk=group_id)
            return render(request, 'userShowGroup.html', {'group': group,'notes': notes})
        except Exception as e:
            print(f"Error: {e}")
            return redirect('/user/groups/')
    else:
        return redirect("/user/groups/")

def newNote(request):
    if request.user.is_authenticated and request.method == "POST" and 'group_id' in request.POST and 'transcribe' in request.POST and not 'result' in request.POST:
        data={
            'option': 'create',
            'group_id': request.POST['group_id']
        }
        return render(request, 'transcribe.html', data )
    elif request.user.is_authenticated and request.method == "POST" and 'group_id' in request.POST and 'result' in request.POST and 'name' in request.POST:
        data={
            'option': 'create',
            'result': request.POST['result'],
            'group_id': request.POST['group_id'],
            'name': request.POST['name']
        }
        return render(request, 'transcribeResult.html', data)
    else:
        return redirect('home')

def createNote(request):
    if request.user.is_authenticated and request.method == 'POST' and 'title' in request.POST and 'group_id' in request.POST and 'result' in request.POST:
        try:
            title = request.POST['title']
            text = request.POST['result']
            group = request.POST['group_id']
            model = UserNotes(title=title,group_id=group,text=text)
            model.save()
            return redirect('/user/groups/')
        except Exception as e:
            print(e)
            return redirect('/user/groups/')
    else:
        return redirect("home")

def showNote(request):
    if request.user.is_authenticated and request.method == 'POST' and 'note_id' in request.POST:
        try:
            note_id = request.POST['note_id']
            note = get_object_or_404(UserNotes,pk=note_id)
            summary = noteSummary.objects.filter(note_id=note_id)
            date = noteDeadline.objects.filter(note_id=note_id)
            studyMaterial = noteStudyMaterial.objects.filter(note_id=note_id)
            group_id=note.group_id
            data={
                'note': note,
                'group_id':group_id,
                'summary': summary,
                'date': date,
                'study_material': studyMaterial
            }
            return render(request, 'Note.html', data )
        except Exception as e:
            print(f"Error: {e}")
            return redirect('/user/groups/')
    else:
        return redirect("/user/groups/")

#@csrf_exempt
def quickTranscribe(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            data={
                'option': 'quick',
            }
            return render(request, 'transcribe.html', data)
        elif request.method == "POST" and 'result' in request.POST and 'name' in request.POST:
            data={
                'option': 'quick',
                'result': request.POST['result'],
                'name' : request.POST['name']
            }
            return render(request, 'transcribeResult.html', data)
    else:
        return redirect('home')

def update(request):
    if request.user.is_authenticated and request.method == 'POST' and 'group_id' in request.POST and 'group_title' in request.POST:
        try:
            group = get_object_or_404(UserGroups,pk=request.POST['group_id'])
            title = request.POST["group_title"]
            group.title = title
            group.save()

            data={
                'message': 'Success',
            }
            return JsonResponse(data)
        except Exception as e:
            print(f"Error: {e}")
            data={
                'message': 'Error',
                'error': e,
            }
            return JsonResponse(data)
    elif request.user.is_authenticated and request.method == 'POST' and 'note_id' in request.POST and 'note_title' in request.POST and 'note_text' in request.POST:
        try:
            note = get_object_or_404(UserNotes,pk=request.POST['note_id'])
            title = request.POST["note_title"]
            text = request.POST["note_text"]
            note.title = title
            note.text = text
            note.save()

            data={
                'message': 'Success',
            }
            return JsonResponse(data)
        except Exception as e:
            print(f"Error: {e}")
            data={
                'message': 'Error',
                'error': e,
            }
            return JsonResponse(data)
    else:
        return redirect("/user/groups/")


def delete(request):
    if request.user.is_authenticated and request.method == 'POST' and 'group_id' in request.POST:
        group = get_object_or_404(UserGroups,pk=request.POST['group_id'])
        group.delete()
        return redirect('/user/groups/')
    if request.user.is_authenticated and request.method == 'POST' and 'note_id' in request.POST:
        note = get_object_or_404(UserNotes,pk=request.POST['note_id'])
        group_id = note.group_id
        note.delete()
        data={
                'message': 'Success',
                'group_id': group_id,
            }
        return JsonResponse(data)
    else:
        return redirect('/user/groups/')

def create(request):
    if request.user.is_authenticated and request.method == 'POST' and 'note_id' in request.POST and 'result' in request.POST and 'option' in request.POST:
        if request.POST['option'] == "summary":
            try:
                summary = noteSummary(text=request.POST['result'],note_id=request.POST['note_id'])
                summary.save()
                data={
                    'message': 'Success'
                }
            except Exception as e:
                print(e)
                data={
                'message': 'Error'
            }
        elif request.POST['option'] == "date":
            try:
                date = noteDeadline(description=request.POST['result'],note_id=request.POST['note_id'])
                date.save()
                data={
                    'message': 'Success'
                }
            except Exception as e:
                data={
                'message': 'Error'
            }
        elif request.POST['option'] == "study_material":
            try:
                date = noteStudyMaterial(text=request.POST['result'],note_id=request.POST['note_id'])
                date.save()
                data={
                    'message': 'Success'
                }
            except Exception as e:
                data={
                    'message': 'Error'
                }
        else:
            data={
                    'message': 'False'
                }

        return JsonResponse(data)
    else:
        return redirect('/user/groups/')