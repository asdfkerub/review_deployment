from django.shortcuts import render , redirect
from .models import User,Book,Rating
from django.contrib import messages
from django.db.models import Avg , Count , Sum
# Create your views here.
def index(request):
    return render(request,'login_reg/index.html')
def fuckit(request):
    Book.objects.all().delete()
    Rating.objects.all().delete()
    print 'Fucked Everything'
    return redirect('/')
def register(request):
    if request.method == 'POST':
        validated_user = User.objects.register(request.POST)
        if 'error' in validated_user:
            for validation_error in validated_user['error']:
                messages.error(request,validation_error)
        if 'the_user' in validated_user:
            messages.success(request,'Added user with an email ' + validated_user['the_user'].email)
        return redirect('/')
def login(request):
    if request.method == 'POST':
        validated_user = User.objects.login(request.POST)
        if 'error' in validated_user:
            for validation_error in validated_user['error']:
                messages.error(request,validation_error)
            return redirect('/')
        if 'the_user' in validated_user:
            if 'logged_in' not in request.session:
                request.session['logged_in'] = validated_user['the_user'].id
            request.session['logged_in'] = validated_user['the_user'].id
            print request.session['logged_in']
            return redirect('/books')
def logout(request):
    request.session['logged_in'] = "null"
    print request.session['logged_in']
    messages.success(request,'Loged Out')
    return redirect('/')
def all_books(request):
    context = {
        'logged_in_id' : request.session['logged_in'],
        'book' : Book.objects.all(),
        'user' : User.objects.get(id=request.session['logged_in']),
        'the_reviews' : Rating.objects.order_by('-created_at')[:3],
        'reviewed_books' : Book.objects.annotate(the_count=Count('reviews')).filter(the_count__gt=0).order_by('-created_at')
    }
    return render(request,'login_reg/all_book.html', context)
def account(request,id):
    the_books = Rating.objects.filter(user=id)
    the_user = User.objects.get(id=id)
    context = {
        'user' : User.objects.get(id=id),
        'reviews' : Rating.objects.filter(user=id).aggregate(Count('book')),
        # 'all_reviews' : Rating.objects.filter(user=id)
        'all_reviews': Book.objects.filter(reviews__user=the_user).distinct()
    }
    return render(request,'login_reg/account.html', context)

def add(request):
    return render(request,'login_reg/add.html')

def add_process(request):
    the_author = ""
    if len(request.POST['add_author']) <= 0:
        the_author = request.POST['choosen_author']
    else:
        the_author = request.POST['add_author']
    exist_book = Book.objects.filter(title = request.POST['title'])
    if Book.objects.filter(title=request.POST['title']).exists():
        the_book = Book.objects.get(title = request.POST['title'])
        the_user = User.objects.get(id=request.session['logged_in'])
        Rating.objects.create(review = request.POST['review'],rating = request.POST['rating'],book = the_book,user = the_user)
        return redirect('/books/'+str(the_book.id))
    else:
        Book.objects.create(title = request.POST['title'],author = the_author)
        the_book = Book.objects.get(title = request.POST['title'],author = the_author)
        the_user = User.objects.get(id=request.session['logged_in'])
        Rating.objects.create(review = request.POST['review'],rating = request.POST['rating'],book = the_book,user = the_user)
        return redirect('/books/'+str(the_book.id))

def book(request,book_id):
    context = {
        # 'logged_in_id' : request.session['logged_in'],
        'logged_in_id' : request.session['logged_in'],
        'the_book' : Book.objects.get(id=book_id),
        'books' : Book.objects.get(id=book_id),
        'user' : User.objects.get(id=request.session['logged_in'])
    }
    return render(request,'login_reg/book.html' , context)

def add_review(request,book_id):
    the_book = Book.objects.get(id=book_id)
    the_user = User.objects.get(id=request.session['logged_in'])
    Rating.objects.create(review=request.POST['review'],rating=request.POST['rating'],book=the_book,user=the_user)
    return redirect('/books/' + str(the_book.id))

def delete_review(request,review_id):
    Rating.objects.get(id=review_id).delete()
    return redirect('/books')
