from django.urls import path
from .views import home_view, buy_view, checkout_view, remove_from_cart_view, complete_view, bought_view
from django.conf.urls.static import static
import bookstore.settings as settings


urlpatterns = [
    path('', home_view, name='home_page'),  # name keyword allow to call view by name instead of view function
    path('buy/<int:object_id>', buy_view, name='buy_page'),
    path('checkout/', checkout_view, name='checkout_page'),
    path('remove/<int:book_id>', remove_from_cart_view, name='remove_page'),
    path('complete/', complete_view, name='complete_page'),
    path('thank_for_buying', bought_view, name='bought_page')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) allows to route url
to specific image, so it can be actually displayed.
"""
"""
<int:object_id> argument before colon tells of what type the argument will be
object_id is a variable, it is designed to be ,,wildcard'' which means to catch
urls with buy/integer for ex. buy/1, buy/2, buy/20 etc. and pass object_id to view
"""