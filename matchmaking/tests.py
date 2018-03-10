from django.test import TestCase

from .models import Location, Dog, PhysicalQualities, PersonalityQualities

# Create your tests here.

class SearchTestCase(TestCase):

    fixtures=['test_data']

    def setUp(self):
        #Location.objects.create(city="Corvallis", state="OR", zipcode=97333)
        pass

    def test_can_lookup_location(self):

        location = Location.objects.get(zipcode=97333)

        self.assertEqual(location.city, "Corvallis")
        self.assertEqual(location.state, "OR")

    def test_can_detect_bad_location(self):

        with self.assertRaises(Location.DoesNotExist) :
            location = Location.objects.get(zipcode=10000)

    def test_dog_by_location_lookup(self):

        location = Location.objects.get(zipcode=97333)
        self.assertIsNotNone(location)

        dogs = Dog.objects.filter(location=location)
        self.assertIsNotNone(dogs)

    def test_bad_dog_lookup(self):

        location = Location.objects.get(zipcode=77001)
        self.assertIsNotNone(location)

        dogs = Dog.objects.filter(location=location)
        # Use the fact that empty lists evaluate as False
        self.assertFalse(dogs)

    def test_different_dog_location_lookup(self):

        location_1 = Location.objects.get(zipcode=97333)
        self.assertIsNotNone(location_1)

        location_2 = Location.objects.get(zipcode=97331)
        self.assertIsNotNone(location_2)

        dogs_1 = Dog.objects.filter(location=location_1)
        self.assertIsNotNone(dogs_1)

        dogs_2 = Dog.objects.filter(location=location_2)
        self.assertIsNotNone(dogs_2)

        self.assertNotEqual(dogs_1, dogs_2)

    def test_sex_filter(self):
        # DB contains Rex as the only dog in 97333, and Rex is male
        location = Location.objects.get(zipcode=97333)
        self.assertIsNotNone(location)

        dogs_1 = Dog.objects.filter(location=location)
        self.assertIsNotNone(dogs_1)

        dogs_2 = dogs_1.filter(sex='f')
        self.assertNotEqual(list(dogs_1), list(dogs_2))

        dogs_3 = dogs_1.filter(sex='m')
        self.assertEqual(list(dogs_1), list(dogs_3))

    def test_color_filter(self):
        # DB contains Rex as the only dog in 97333, and Rex is male
        location = Location.objects.get(zipcode=97333)
        self.assertIsNotNone(location)

        all_physicals = PhysicalQualities.objects.all()
        d_color1 = all_physicals.filter(color="Yellow")
        self.assertTrue(list(d_color1))
        d_color2 = all_physicals.filter(color="Light Brown")
        self.assertTrue(list(d_color2))

        # Should return empty set since there are no yellow dogs in the zipcode
        dogs_1 = Dog.objects.filter(location=location).filter(physical__in=d_color1)
        self.assertFalse(list(dogs_1))

        # Should return at least 1 dog in the zipcode
        dogs_2 = Dog.objects.filter(location=location).filter(physical__in=d_color2)
        self.assertTrue(list(dogs_2))

    def test_kid_friendly_filter(self):
        # DB has two dogs in 97331, one is kid friendly and one is not

        location = Location.objects.get(zipcode=97331)
        self.assertIsNotNone(location)

        kf1 = PersonalityQualities.objects.filter(kid_friendly=1)
        self.assertTrue(list(kf1)) # True if a PersonalityQualities object was returned

        kf0 = PersonalityQualities.objects.filter(kid_friendly=0)
        self.assertTrue(list(kf0)) # True if a PersonalityQualities object was returned

        dogs_0 = Dog.objects.filter(location=location).filter(personality__in=kf0)
        self.assertTrue(list(dogs_0)) # True if a Dog object was returned

        dogs_1 = Dog.objects.filter(location=location).filter(personality__in=kf1)
        self.assertTrue(list(dogs_1)) # True if a Dog object was returned

        # Check that the two filtered results are not equal to one another
        self.assertNotEqual(list(dogs_0), list(dogs_1))
