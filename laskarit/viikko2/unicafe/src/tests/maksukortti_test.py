import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_kortin_saldo_alussa_oikein(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")
    
    def test_saldo_kasvaa_oikein_rahaa_ladattaessa(self):
        self.maksukortti.lataa_rahaa(400)

        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 14.00 euroa")

    def test_saldo_vahenee_oikein_jos_rahaa_on_tarpeeksi(self):
        self.maksukortti.ota_rahaa(300)

        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 7.00 euroa")

    def test_saldo_ei_muutu_jos_rahaa_ei_ole_tarpeeksi(self):
        self.maksukortti.ota_rahaa(2000)

        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa")

    def test_metodi_palauttaa_true_jos_rahat_riittavat(self):
        self.maksukortti.ota_rahaa(500)

        self.assertNotEqual(self.maksukortti.ota_rahaa, True)

    def test_metodi_palauttaa_false_jos_rahat_ei_riita(self):
        self.maksukortti.ota_rahaa(1500)

        self.assertNotEqual(self.maksukortti.ota_rahaa, False)

    def test_saldo_euroina(self):
        self.assertEqual(str(self.maksukortti), "Kortilla on rahaa 10.00 euroa" )

    def test_kassaraha_euroina(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.0)