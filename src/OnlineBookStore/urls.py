from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    # Examples:
    url(r'^$', 'mainApp.views.home', name='home'),
    url(r'^add-author$', 'mainApp.views.addAuthor', name='add-author'),
    # url(r'^add-item/$', 'newsletter.views.addItem', name='add-item'),
    url(r'^delete-author/(?P<id>\w{1,50})$', 'mainApp.views.deleteAuthor', name='delete-author/id'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^customer-login/','mainApp.views.customerLoginView',name='customer-login'), 
    url(r'^customer-register/','mainApp.views.customerRegisterView',name='customer-register'), 
    url(r'^seller-login/','mainApp.views.sellerLoginView',name='seller-login'), 
    url(r'^seller-register/','mainApp.views.sellerRegisterView',name='seller-register'), 
    url(r'^admin-login/','mainApp.views.adminLoginView',name='admin-login'), 
    url(r'^admin-register/','mainApp.views.adminRegisterView',name='admin-register'),
    url(r'^get-books-by-category/(?P<id>\d+)$', 'mainApp.views.getBooksByCategory', name='get_books_by_category'), 
    url(r'^get-single-book/(?P<id>\d+)$', 'mainApp.views.getSingleBook', name='get_single_book'), 
    url(r'^post-review/','mainApp.moreViews.postReview',name='post-review'), 
    url(r'^delete-review/(?P<id>\d+)/(?P<Book_id>\d+)$', 'mainApp.moreViews.deleteReview', name='delete_review'), 
    url(r'^add-to-cart/(?P<Book_id>\d+)','mainApp.moreViews.addToCart',name='add-to-cart'), 
    url(r'^cart-view/','mainApp.moreViews.cartView',name='cart-view'),
    url(r'^dec-quantity-in-cart/(?P<id>\d+)','mainApp.moreViews.decQuantityInCart',name='dec-quantity-in-cart'), 
    url(r'^inc-quantity-in-cart/(?P<id>\d+)','mainApp.moreViews.incQuantityInCart',name='inc-quantity-in-cart'), 
    url(r'^delete-book-from-cart/(?P<id>\d+)','mainApp.moreViews.deleteBookFromCart',name='delete-book-from-cart'), 
   
    url(r'^admin/', include(admin.site.urls)),
]


if settings.DEBUG:
	urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
	urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
