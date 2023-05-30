from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import openai
import whisper as wp
from decouple import config
from django.core.files.storage import FileSystemStorage
import os
from Apps.User.models import *

@csrf_exempt
def whisper(request):
    if request.user.is_authenticated and request.method == 'POST' and 'file' in request.FILES:
        try:
            #print("WHISPER")
            data = request.FILES
            audio = data['file']
            fs = FileSystemStorage()
            name = audio.name
            filename = fs.save(name, audio)
            model = wp.load_model("small")
            result = model.transcribe(f"media/{name}", fp16=False, verbose=None)  
            if os.path.exists(f'media/{name}'):
                        os.remove(f'media/{name}')
            if result:
                #print(result)
                data = {
                    'mesage': 'Success',
                    'result': result['text'],
                    'name': name,
                }
            else:
                data = {
                    'mesage': 'Error',
                }
            return JsonResponse(data)
        except Exception as e:
            #print(e)
            if os.path.exists(f'media/{name}'):
                        os.remove(f'media/{name}')
            data = {
                    'mesage': 'Error',
                }
            return JsonResponse(data)
    else:
        return redirect('home')


def chat(request):
    if request.user.is_authenticated and request.method == 'POST' and 'option' in request.POST and 'note_id' in request.POST:
        try:
            print("ChatGPT")
            note_id = request.POST['note_id']
            note = get_object_or_404(UserNotes,pk=note_id)
            option = request.POST['option']
            input_text =""
            if option == "summary":
                input_text = f"Resume el siguiente texto: \"{note.text}\" "
            elif option == "date":
                input_text = f"Del siguiente texto saca las fechas de examenes, tareas, actividades o eventos propuestos y dame una descripcion de dicho examen, tarea, actividad o evento: \"{note.text}\" \n\nEn caso de no haber, unicamente dime 'No se encontraron fechas' "
            elif option == "study_material":
                input_text = f"Dame o recomiendame material de estudio tales como libros, articulos o videos que esten relacionados con el tema o temas del siguiente texto: \"{note.text}\" \nCon el siguiente formato:'El material de estudio recomendado es: - Libros: \n- Articulos: \n- Videos: ' \n\nSi no es posible recomendar material de estudio, respondeme con: 'No se puede sugerir material de estudio para este texto' \n\nSi hay varios temas, dame los materiales de estudio para cada tema de forma individual, con el mismo formato. "
            else:
                input_text ="Buenos dias"
            
            #print("este es el input text: " + input_text)
            print("OpenAI")
            openai.api_key = config("OPENAI_API_KEY")
            completions = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo-0301",
            messages=[{"role": "user", "content": input_text}])
            output_text = completions.choices[0].message.content
            data={}
            if output_text:
                #print(result)
                data = {
                    'mesage': 'Success',
                    'result': output_text,
                }
            else:
                data = {
                    'mesage': 'Error',
                    'result': ""
                }
            return JsonResponse(data)
        except Exception as e:
            print(f"Chat error: {e}")
            data = {
                    'mesage': 'Error',
                }
            return JsonResponse(data)
    else:
        return redirect('home')
