from django.shortcuts import render ,redirect, get_object_or_404
from .models import *  # It's better to import specific models rather than using *
from .forms import BookForm, CategoryForm  # Assuming you've defined these forms

def index(request):
    if request.method == 'POST':
        add_book = BookForm(request.POST, request.FILES)
        add_category = CategoryForm(request.POST)

        if add_book.is_valid():
            add_book.save()
            return redirect('index')  # Redirect to the same page or another page

        if add_category.is_valid():
            add_category.save()
            return redirect('index')  # Redirect to avoid re-post on refresh

    context = {
        'category': Category.objects.all(),
        'books': Book.objects.all(),
        'form': BookForm(),  
        'formcat': CategoryForm(),  
        'all_books': Book.objects.filter(active=True).count(),
        'bookssold': Book.objects.filter(status='sold').count(),
        'booksavailable': Book.objects.filter(status='available').count(),
        'rentedbooks': Book.objects.filter(status='rented').count(),
    }
    return render(request, 'pages/index.html', context)

def books(request):
    search = Book.objects.all()
    title = request.GET.get('search_name', '')
    if title:
        search = search.filter(title__icontains=title)

    context = {
        'category': Category.objects.all(),
        'books': search,  # Use the QuerySet directly, without calling it as a function
        
        'formcat': CategoryForm(),  

    
    }
    return render(request, 'pages/books.html', context)
def update(request, id):
    book_id =  Book.objects.get(id=id)
    if request.method == 'POST':
        book_save =BookForm(request.POST, request.FILES ,instance=book_id)
        if book_save.is_valid():
            book_save.save()
            return redirect('index')
    else:
        book_save=BookForm(instance=book_id)
    context={
        'form':book_save,

    }
    return render(request, 'pages/update.html', context)


def delete(request, id):
    book_delete= get_object_or_404(Book, id=id)
    if request.method == 'POST':
        book_delete.delete()
        return redirect('index')
    return render(request, 'pages/delete.html')