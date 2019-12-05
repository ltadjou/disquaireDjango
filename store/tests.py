from django.test import TestCase
from django.urls import reverse
from .models import Album, Artist, Booking, Contact

# Create your tests here.

# Test de vue

#Index Page 
class IndexPageTestCase(TestCase):

    

    def test_index_page(self):
        response = self.client.get(reverse('index')
        )
        self.assertEqual(response.status_code, 200)
    # test that index page returns a 200

#detail Page 
class DetailPageTestCase(TestCase):

    def setUp(self):
        impossible = Album.objects.create(title="Transmission Impossible")
        self.album = Album.objects.get(title="Transmission Impossible")

    #test that detail page returns a 200 if item exists
    def test_detail_page_returns_200(self):
        
        albim_id = self.album.id 
        response = self.client.get(reverse('store:detail', args=(albim_id,)))
        self.assertEqual(response.status_code, 200)

    def test_detail_page_returns_404(self):
        albim_id = self.album.id +1
        response = self.client.get(reverse('store:detail', args=(albim_id,)))
        self.assertEqual(response.status_code, 404)

class BookingPageTestCase(TestCase):
    def setUp(self):
        Contact.objects.create(name='Tatal', email='tatali@test.fr')
        impossible = Album.objects.create(title="Transmission Impossible")
        journey = Artist.objects.create(name="Journey")
        impossible.artists.add(journey)

        self.album = Album.objects.get(title="Transmission Impossible")
        self.contact = Contact.objects.get(name="Tatal")


    def test_reservation(self):
        old_bookings = Booking.objects.count()
        albim_id = self.album.id 
        name = self.contact.name
        email = self.contact.email
        response = self.client.post(reverse('store:detail', args=(albim_id,)), {
            'name': name,
            'email': email
        })
        new_bookings = Booking.objects.count()
        self.assertEqual(old_bookings, new_bookings -1)