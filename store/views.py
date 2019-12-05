#from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404
from .models import ALBUMS
from .models import Album, Artist, Contact, Booking
from .forms import ContactForm, ParagraphErrorlist
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction, IntegrityError

# Create your views here.
def index(request):
    #message = 'Salut tout le monde !!!'
    # request albums
    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
    # then format the request.
    # note that we don't use album['name'] anymore but album.name
    # because it's now an attribute.
    '''formatted_albums = ["<li>{}</li>".format(album.title) for album in albums]
    message = """<ul>{}</ul>""".format("\n".join(formatted_albums))
    template = loader.get_template('store/index.html')
    context = {'albums': albums}'''
    context = {'albums': albums}
    #return HttpResponse(template.render(context, request=request))
    return render(request, 'store/index.html', context)


def listing(request):
    #albums = ["<li>{}</li>".format(album['name']) for album in ALBUMS]
    albums_list = Album.objects.filter(available=True)
    paginator = Paginator(albums_list, 1)
    page = request.GET.get('page')
    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        albums = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        albums = paginator.page(paginator.num_pages)
    context = {'albums': albums, 'paginate': True}
    #return HttpResponse(message)
    return render(request, 'store/listing.html', context)

#@transaction.atomic
def detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    artists = [artist.name for artist in album.artists.all()]
    artists_name = " ".join(artists)
    context = {
        'album_title': album.title,
        'artists_name': artists_name,
        'album_id': album.id,
        'thumbnail': album.picture,
    }
    if request.method == 'POST':
        form = ContactForm(request.POST, error_class = ParagraphErrorlist)
        if form.is_valid():
            email = form.cleaned_data['email']
            name = form.cleaned_data['name']
            try:
                with transaction.atomic():
                    contact = Contact.objects.filter(email=email)
                    if not contact.exists():
                        contact = Contact.objects.create(
                            email = email,
                            name = name
                        )
                    else:
                        contact = contact.first()
                    album = get_object_or_404(Album, pk=album_id)
                    booking = Booking.objects.create(
                        contact = contact,
                        album = album
                    )
                    album.available = False
                    album.save()
                    context = {
                        'album_title' : album.title
                    }
                    return render(request, 'store/merci.html', context)
            except IntegrityError:
                form.errors['internal'] = "Une erreur interne est survenue. Merci de recommencer votre réservation"
    else:
        form = ContactForm()
    
    context['form'] = form
    context['errors'] = form.errors.items()
    return  render(request, 'store/detail.html', context)


def search(request):
    '''obj = str(request.GET)
    query = request.GET['query']
    message = "Propriété GET : {} est requête : {}". format(obj, query)
    return HttpResponse(message)
    query = request.GET.get('query')
    if not query:
        #message = "Aucun artistes demandé"
        albums = Album.objects.all()
    else:
        albums = [
            album for album in ALBUMS
            if query in " ".join(artist['name'] for artist in album['artists'])
        ]
        albums = Album.objects.filter(title__icontains=query)
        if not albums.exists():
             albums = Album.objects.filter(artists__name__icontains=query)

        if not albums.exists():
            message = "Misère de misère, nous n'avons trouvé aucun résultat !"
        else:
            albums = ["<li>{}</li>".format(album.title) for album in albums] 
            message = """Nous avons trouvé les albums correspondats à votre requête ! Les voici:
            <ul>
            {}
            </ul>
            """.format("<li><li>".join(albums))'''
    query = request.GET.get('query')
    if not query:
        #message = "Aucun artistes demandé"
        albums = Album.objects.all()
    else:
        albums = Album.objects.filter(title__icontains=query)
    if not albums.exists():
        albums = Album.objects.filter(artists__name__icontains=query)
    title = "Résultats pour la requêtes %s"%query
    context = {
         'albums': albums,
         'title': title,
     }
    return render(request, 'store/search.html', context)
