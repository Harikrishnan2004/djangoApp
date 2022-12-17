from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.http import HttpResponseRedirect
from django import forms
import random

ConnectionList = []
dict_names = {}
chats = []
            
class NewTaskForm(forms.Form):
    id = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Room Code','id':'formid'}))
    name = forms.CharField(widget=forms.TextInput(attrs = {"placeholder": "Name", 'id':'formname'}))
 
class Chat(forms.Form):
    chat = forms.CharField(widget=forms.TextInput(attrs = {"placeholder": 'Message', 'id': 'formchat'}))
    
def home(request):
    global dict_names
    if "ID" and "name" not in request.session:
        request.session["ID"] = random.randint(10000,99999)
        request.session["name"] = " "
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        
        if form.is_valid():
            id = form.cleaned_data["id"]
            request.session["name"] = form.cleaned_data["name"]
            
            if not ConnectionList and int(id) == request.session["ID"]:
                ConnectionList.append(int(id))
                dict_names[int(id)] = [request.session["name"]]
                return HttpResponseRedirect(reverse("twochat:room"))
            elif ConnectionList:
                for i in ConnectionList:
                    if i == int(id):
                        request.session["ID"] = id
                        dict_names[int(id)].append(request.session["name"])
                        return HttpResponseRedirect(reverse("twochat:room"))
            
    return render(request, 'twochat/home.html', {
        "form": NewTaskForm(),
        "id" : request.session["ID"]
    })
    
def room(request):
        
    x = list(dict_names[int(request.session["ID"])])
    x.append("Dummy")
    me = request.session["name"]
    x.remove(me)
    partner = x[0]
    
    if request.method == "POST":
        form = Chat(request.POST)
        if form.is_valid():
            chat = form.cleaned_data["chat"]
            chat = [request.session["name"], chat]
            chats.append(chat)
    
    return render(request, "twochat/room.html", {
            "id" : request.session["ID"],
            "me" : me,
            "part": partner,
            "chat_form": Chat(),
            "chats" : chats
        })


