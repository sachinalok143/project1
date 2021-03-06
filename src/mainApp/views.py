from django.shortcuts import render
from .forms import *
from .models import *
from .backends import *
from django.contrib.auth import (
	authenticate,
	get_user_model,
	login,
	logout,
	)

from django.http import HttpResponseRedirect

Category_set=Category.objects.all().order_by("Name")
# for Category in Category_set:
	# print (Category.Name)


# Create your views here.
def home(request):
	return render(request, 'home.html',{"categories":Category_set})

def addAuthor(request):
	form=AddAuthorForm(request.POST or None)
	queryset=Author.objects.all().order_by('-Created_at')
	context={
	"query":queryset,
	"form": form,
	"categories":Category_set,
	}
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		if request.user.is_authenticated() and request.user.is_staff:
			queryset=Author.objects.all().order_by('-Created_at')
			context={
			"query":queryset,
			"form": form,
			"categories":Category_set,
			}

	return render(request,'addAuthor.html',context)

def deleteAuthor(request ,id=None):
	# queryset=signUp.objects.all().order_by('-Created_at')
	form=AddAuthorForm(request.POST or None)
	Author.objects.filter(id=id).delete()
	# print(Author.objects.filter(id=id).delete())
	queryset=Author.objects.all().order_by('-Created_at')
	context={
	"query":queryset,
	"form": form,
	"categories":Category_set,
	}
	return render(request,'authorTable.html',context)

# def editAuthor(request ,id=None):
# 	# queryset=signUp.objects.all().order_by('-Created_at')
# 	form=AddAuthorForm(request.POST or None)
# 	print(Author.objects.filter(id=id).delete())
# 	queryset=Author.objects.all().order_by('-Created_at')
# 	context={
# 	"query":queryset,
# 	"form": form
# 	}
# 	return render(request,'authorTable.html',context)



title="You are loged in as Customer!"
# Create your views here.
def customerLoginView(request):
	title="You are loged in as Customer!"
	form=LoginForm(request.POST or None)
	if form.is_valid():
		email=form.cleaned_data.get("email")
		password=form.cleaned_data.get("password")
		user=authenticate(username=email,password=password)
		logedInCustomerProfile=Customer.objects.filter(user_id=user.id)
		if not logedInCustomerProfile.count()>0:
			error="Email and Password does not matched."
			return render(request,"Authentication/customerLogin.html",{"form":form,"error":error,"categories":Category_set})
		else :
			login(request,user)
	if request.user.is_authenticated():		
		class orderObjectDetail(object):
			def __init__(self, orderObject=None, bookEdition=None):
				self.orderObject = orderObject
				self.bookEdition = bookEdition
		orderObjectList=[]
		totalPrice=0
		user=Customer.objects.get(user_id=request.user.id)
		customer=Customer.objects.get(user_id=request.user.id)
		orderObjects=Order.objects.filter(Customer_id=customer).order_by('-Created_at')[:5]
		for orderObject in orderObjects:
			bookEdition=BookEdition.objects.get(id=orderObject.Book_id)
			orderObjectList.append(orderObjectDetail(orderObject,bookEdition))
			# print (ordertObjectList.count)
			totalPrice+=(orderObject.Quantity*bookEdition.Price)
		totalPrice+=150

			# return render(request,"orderView.html",{"totalPrice":totalPrice,
			 # "Customer":customer,"orderObjectList":orderObjectList, "categories":Category_set})
		context={
		"totalPrice":totalPrice,
		 "Customer":customer,
		 "orderObjectList":orderObjectList,
		 "user":user,
		 # "form":form,
		 # "title":title,
		 "categories":Category_set,
		}
		# return render(request,"cartView.html",{"totalPrice":totalPrice,
		#  "Customer":customer,"cartObjectList":cartObjectList, "categories":Category_set})
		return render(request,"Authentication/customerProfileView.html",context)
	return render(request,"Authentication/customerLogin.html",{"form":form,"categories":Category_set})

def customerRegisterView(request):
	# title="Register"
	title="You are loged In as Customer! For registering a new user you have to Logout."
	form1=RegistrationForm(request.POST or None)
	form2=CustomerForm(request.POST or None)
	if form1.is_valid():
		title='You are registered successfully!'
		user=form1.save(commit=False)
		password=form1.cleaned_data.get('password')
		username=form1.cleaned_data.get('username')
		user.set_password(password)
		user.save()
		new_user=authenticate(username=user.username,password=password)
		login(request,new_user)

		userprofile=form2.save(commit=False)
		# userprofile.User=username
		userprofile.user_id=request.user.id
		t=userprofile.save()
	if request.user.is_authenticated():		
		class orderObjectDetail(object):
			def __init__(self, orderObject=None, bookEdition=None):
				self.orderObject = orderObject
				self.bookEdition = bookEdition
		orderObjectList=[]
		totalPrice=0
		user=Customer.objects.get(user_id=request.user.id)
		customer=Customer.objects.get(user_id=request.user.id)
		orderObjects=Order.objects.filter(Customer_id=customer).order_by('-Created_at')[:5]
		for orderObject in orderObjects:
			bookEdition=BookEdition.objects.get(id=orderObject.Book_id)
			orderObjectList.append(orderObjectDetail(orderObject,bookEdition))
			# print (ordertObjectList.count)
			totalPrice+=(orderObject.Quantity*bookEdition.Price)
		totalPrice+=150
		context={
		"totalPrice":totalPrice,
		 "Customer":customer,
		 "orderObjectList":orderObjectList,
		 "user":user,
		 "categories":Category_set,
		}
		
		return render(request,"Authentication/customerProfileView.html",context)
	return render(request,"Authentication/customerRegister.html",{"form1":form1,"form2":form2,"title":title,"categories":Category_set})
	

title="You are loged in as Seller!"
# Create your views here.
def sellerLoginView(request):
	title="You are loged in as Seller!"
	form=LoginForm(request.POST or None)
	if form.is_valid():
		email=form.cleaned_data.get("email")
		password=form.cleaned_data.get("password")
		user=authenticate(username=email,password=password)
		# login(request,user)
		logedInCustomerProfile=Seller.objects.filter(User_id=user.id)
		if not logedInCustomerProfile.count()>0:
			error="Email and Password does not matched."
			return render(request,"Authentication/customerLogin.html",{"form":form,"error":error,"categories":Category_set})
		else :
			login(request,user)
	if request.user.is_authenticated():	
		seller=Seller.objects.get(User_id=request.user.id)
		
		# # title2="Add a Book"
		form2=BookForm(request.POST or None)
		if form2.is_valid():
			form2.save()
			return HttpResponseRedirect('')
		return render(request,"Authentication/sellerProfile.html",{"categories":Category_set,"seller":seller,
			"form2":form2})
	return render(request,"Authentication/customerLogin.html",{"form":form,"categories":Category_set})


def sellerRegisterView(request):
	# title="Register"
	title="You are loged In as Seller! For registering a new user you have to Logout."
	form1=RegistrationForm(request.POST or None)
	form2=SellerForm(request.POST or None)
	if form1.is_valid():
		title='You are registered successfully!'
		user=form1.save(commit=False)
		password=form1.cleaned_data.get('password')
		username=form1.cleaned_data.get('username')
		user.set_password(password)
		user.save()
		new_user=authenticate(username=user.username,password=password)
		login(request,new_user)

		userprofile=form2.save(commit=False)
		# userprofile.User=username
		userprofile.User_id=request.user.id
		t=userprofile.save()
		# print(t)
		
		# new_userProfile.save()
	# if request.user.is_authenticated():
	# 	logedInUserProfile=Customer.objects.get(user_id=request.user.id)
	return render(request,"Authentication/customerRegister.html",{"form1":form1,"form2":form2,"title":title,"categories":Category_set})
	
title="You are loged in as Admin!"
# Create your views here.
def adminLoginView(request):
	title="You are loged in as Admin!"
	form=LoginForm(request.POST or None)
	if form.is_valid():
		email=form.cleaned_data.get("email")
		password=form.cleaned_data.get("password")
		user=authenticate(username=email,password=password)
		# print ("ifin")
		logedInCustomerProfile=Admin.objects.filter(User_id=user.id)
		if not logedInCustomerProfile.count()>0:
			error="Email and Password does not matched."
			return render(request,"Authentication/customerLogin.html",{"form":form,"error":error,"categories":Category_set})
			# raise forms.ValidationError("You are not registered.")
		else :
			# print ("else")
			login(request,user)
		if request.user.is_authenticated():
			# print ("out")		
			return render(request,"Authentication/customerLogin.html",{"form":form,"title":title,"categories":Category_set})
	return render(request,"Authentication/customerLogin.html",{"form":form,"categories":Category_set})


def adminRegisterView(request):
	# title="Register"
	title="You are loged In as Admin! For registering a new user you have to Logout."
	form1=RegistrationForm(request.POST or None)
	form2=AdminForm(request.POST or None)
	if form1.is_valid():
		title='You are registered successfully!'
		user=form1.save(commit=False)
		password=form1.cleaned_data.get('password')
		username=form1.cleaned_data.get('username')
		user.set_password(password)
		user.save()
		new_user=authenticate(username=user.username,password=password)
		login(request,new_user)

		userprofile=form2.save(commit=False)
		# userprofile.User=username
		userprofile.User_id=request.user.id
		t=userprofile.save()
		# print(t)
		
		# new_userProfile.save()
	# if request.user.is_authenticated():
	# 	logedInUserProfile=Customer.objects.get(user_id=request.user.id)
	return render(request,"Authentication/customerRegister.html",{"form1":form1,"form2":form2,"title":title,"categories":Category_set})

# def getBookDeatail()

def getBooksByCategory(request,id=None):
	if id!="0":	
		bookCategories=BookCategory.objects.filter(Category_id=id)
		Cs=Category.objects.get(id=id)
		C=Cs.Name
	else :
		bookCategories=BookCategory.objects.all()
		C="All"

	class completeBookDetail(object):
		def __init__(self, book=None, bookEdition=None,discountedPrice=None):
			self.book = book
			self.bookEdition = bookEdition
			self.discountedPrice=discountedPrice
	bookDetailList=[]
	for bookCategory in bookCategories:
		books=Book.objects.filter(id=bookCategory.Book_id)
		# print (books)
		for book in books:
			# print (book.Title)
			bookEditions=BookEdition.objects.filter(Book_id=book.id)
			for bookEdition in bookEditions :
				d=bookEdition.Price*bookEdition.Discount/100
				d=bookEdition.Price-d
				# print (d)
				bookDetailList.append(completeBookDetail(book,bookEdition,d))
		# print (bookDetailList)
	return render(request,"categoryView.html",{"bookDetailList":bookDetailList,"categories":Category_set,"CategoryName":C})

def getSingleBook(request,id=None):
	form=ReviewForm(request.POST or None)
	bookEdition=BookEdition.objects.get(id=id)
	book=Book.objects.get(id=bookEdition.Book_id)
	class completeBookDetail(object):
		def __init__(self, book=None, bookEdition=None,discountedPrice=None,categories=None):
			self.book = book
			self.bookEdition = bookEdition
			self.discountedPrice=discountedPrice
			self.categories=categories
	d=bookEdition.Price*bookEdition.Discount/100
	d=bookEdition.Price-d
	Cs=BookCategory.objects.filter(Book_id=book.id)
	C=[]
	for x in Cs:
		y=Category.objects.get(id=x.Category_id)
		C.append(str(y.Name))
	bookDetail=completeBookDetail(book,bookEdition,d,C)
		# print (bookDetailList)\

	allReviews=Review.objects.filter(Book_id=book.id).order_by("-Created_at")
	class reviewDetail:
		def __init__(self, review=None, customer=None,user=None):
			self.review = review
			self.customer = customer
			self.user=user
	
	reviewList=[]

	for aReview in allReviews:
		customer=Customer.objects.get(id=aReview.Customer_id)
		user=User.objects.get(id=customer.user_id)
		reviewList.append(reviewDetail( aReview,customer,user))
	
	return render(request,"singleView.html",{"bookDetail":bookDetail,"categories":Category_set,"form":form,"reviewList":reviewList})

def addPublisher(request):
	form=PublisherForm(request.POST or None )
	seller=Seller.objects.get(User_id=request.user.id)

	if form.is_valid():
		form.save()
		return HttpResponseRedirect("../seller-login")
	return render(request,"Authentication/addPublisher.html",{"categories":Category_set,"seller":seller,
			"form":form})