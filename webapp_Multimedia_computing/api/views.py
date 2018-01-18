from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.views import APIView

from api.models import Document
from .Huffman.HuffmanCompress import huffman_compress_main_process
from .forms import DocumentForm


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def home(request):
    documents = Document.objects.all()
    return render(request, 'home.html', {'documents': documents})


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        saving_based_dir = 'media/compress/'
        saving_dir = saving_based_dir + 'compressed_' + uploaded_file_url.split('/')[2]
        # huffman_compress_main_process(uploaded_file_url, saving_dir)
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url,
            'path': saving_dir
        })
    return render(request, 'simple_upload.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'model_form_upload.html', {
        'form': form
    })


class Multimedia_engine(APIView):
    def get(self, request):
        return model_form_upload(request)
