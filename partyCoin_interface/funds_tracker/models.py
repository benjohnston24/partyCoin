from django.db import models

# Create your models here.


class Donation(models.Model):
    year = models.CharField(max_length=20)
    party = models.CharField(max_length=200)
    donor = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    party_state = models.CharField(max_length=4)
    state = models.CharField(max_length=3)
    postcode = models.CharField(max_length=4)
    donor_type = models.CharField(max_length=40)
    amount = models.FloatField()

    def get_year(self):
        return self.year.__str__()

    def get_party(self):
        return self.party.__str__()

    def get_donor(self):
        return self.donor.__str__()

    def get_address(self):
        return self.address.__str__()

    def get_state(self):
        return self.state.__str__()

    def get_postcode(self):
        return self.postcode.__str__()

    def get_donor_type(self):
        return self.donor_type.__str__()

    def __str__(self):
        return '%s:%s:$%0.2f' % (self.get_party(),
                                 self.get_donor(),
                                 self.amount)
