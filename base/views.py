from django.shortcuts import render, redirect
from .models import ChatMessage, ChatSession
from .forms import MessageForm, FileForm, RegisterForm, LoginForm
import os
from google import genai
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
from base.utils.predictML import analyzeContent

# Create your views here.
def Register(request):
    userForm = RegisterForm(request.POST)
    if request.method == 'POST':
        if userForm.is_valid():
            user = userForm.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
        

    context = {'form': userForm}
    return render(request, 'base/register.html', context)

def LogoutUser(request):
    logout(request)
    return redirect('home')

def LoginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    loginUser = LoginForm(request.POST or None)

    if request.method == 'POST':
        if loginUser.is_valid():
            username = loginUser.cleaned_data.get('username')
            password = loginUser.cleaned_data.get('password')
            user = authenticate(request, username=username, password = password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Username or Password does not match in record")

    context = {'loginForm': loginUser}
    return render(request, 'base/login.html', context)


@login_required(login_url='login')
def Home(request):
    messageForm = MessageForm()
    fileForm = FileForm()

    chatSession, created = ChatSession.objects.get_or_create(
        user = request.user
    )

    if request.method == 'POST':
        fileForm = FileForm(request.POST, request.FILES)
        referenceMessage = request.POST.get('reference') or None
        regenerateChoice = True if (request.POST.get('regenerate') == 'true') else False
        saveFile = ""

        messageForm = MessageForm(request.POST)
        if messageForm.is_valid():
            saveMessage = messageForm.save(commit=False)
            saveMessage.role = 'User'
            saveMessage.session = chatSession
            saveMessage.save()
            
            if request.FILES.get('uploaded_file'):
                if fileForm.is_valid():
                    saveFile = fileForm.save(commit=False)
                    saveFile.associatedCont = saveMessage
                    saveFile.save()

                    #process_to_NLP(saveFile)
                else:
                    error_message = fileForm.errors.get('uploaded_file', ['Invalid file'])[0]

                    saveMessage.delete()
                    return JsonResponse({
                        'status': 'error',
                        'message': str(error_message)
                    })
            generate = False if (fileForm.data.get('context') == '') else True
            generatedMessage = process_summary(generate, chatSession, referenceMessage, regenerateChoice, saveFile)
            
            return JsonResponse({
                    'status': 'success',
                    'user_message': saveMessage.context,
                    'ai_message': generatedMessage,
                    'role': 'User'
                    })

    messages = chatSession.chatmessage_set.all()

    context = {'messages': messages, 'messageForm':messageForm, 'fileForm': fileForm}
    
    return render(request, 'base/home.html', context)

def process_to_NLP(file):
    result = analyzeContent(file)
    file_path = file.uploaded_file.path
    if os.path.exists(file_path):
        os.remove(file_path)
    
    file.delete()

    return result

def process_summary(textGenerate, chatSession, referenceMessage, regenerateChoice, file):
    currentSession = chatSession
    content = ""
    NLP_result = ""

    if file != '':
        NLP_result = process_to_NLP(file)

    if textGenerate:
        client = genai.Client( api_key=os.getenv("GEMINI_API_KEY"))

        
        nearestNum = (ChatMessage.objects.filter(session=currentSession).count() // 10) * 10 
        messages = ChatMessage.objects.filter(session = currentSession).order_by('id')[nearestNum:]
        messagesCombined = " ".join([message.context for message in messages])

        summary = currentSession.summary
        summary += messagesCombined

        if NLP_result != '':
            content += NLP_result
            content += "above is the analysis result of a network log, answer the last question referencing the result"

        if referenceMessage == None:
            content += ("I am providing you with a set of the previous questions asked" +
            "and the responses you generated, there can be only one message which in " +
            "case it is the question, Just give me the answer for the last question\n" + summary)
        
        else:
            content += ("I provided you with a list of the previous questions asked" + 
            "and the responses you generated\n this is the specific message that I'm referencing: " + 
            referenceMessage + " give me the answer for the reference question " + summary)
        
        if regenerateChoice:
            last_two_messages = ChatMessage.objects.filter(
                session = currentSession
            ).order_by('-id')[:2].values_list('id', flat=True)
            if last_two_messages:
                ChatMessage.objects.filter(id__in = last_two_messages).delete()

            content += "\n I was not satisfied with the last answer you gave. Give me a new response"

        

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview", 
            contents = content
        )
        content = response.text

    currentSession.refresh_from_db()

    messageForm = MessageForm()
    saveMessage = messageForm.save(commit = False)
    saveMessage.session = currentSession
    saveMessage.role = 'Model'
    saveMessage.context = content if textGenerate else NLP_result
    if currentSession.is_cancelled == True:
        currentSession.is_cancelled = False
        currentSession.save()
        return ""
    
    saveMessage.save()

    count = ChatMessage.objects.count()

    if count > 0 and count % 10 == 0:
        currentSummary = chatSession.summary
        summaryResp = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview", contents=(currentSummary + messagesCombined + "\n give me a summary for the above messages, don't make it too long")
        )
        currentSession.summary = summaryResp.text
        currentSession.save()
    
    return saveMessage.context

def cancelRequest(request):
    if request.method == 'POST':
        try:
            chatSession = ChatSession.objects.get(user = request.user)
            lastMessages = chatSession.chatmessage_set.order_by('-id')[:2]
            if lastMessages.exists():
                if lastMessages[0].role == 'Model':
                    lastMessages.delete()
                else:
                    lastMessages[0].delete()
                    chatSession.is_cancelled = True
                    chatSession.save()
                return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
        
    return JsonResponse({'status': 'Invalid method'}, status=400)







