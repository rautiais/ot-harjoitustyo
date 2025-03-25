import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.kortti = Maksukortti(1000)

    def test_kassan_saldo(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_kassan_saldo_euroina(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000)

    def test_kortin_lataus(self):
        self.maksukortti = Maksukortti(1000)
        self.assertEqual(self.kassapaate.lataa_rahaa_kortille(self.maksukortti, 2000), None)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 102000)

    def test_lataa_nega_rahaa_kortille(self):
        self.maksukortti = Maksukortti(1000)
        self.assertEqual(self.kassapaate.lataa_rahaa_kortille(self.maksukortti, -100), None)
   
   # Edulliset lounaat

    def test_edulliset_lounaat(self):
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_edullinen_kateisella_osto(self):
        self.kassapaate.syo_edullisesti_kateisella(400)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100240)
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(400), 160)
        self.assertEqual(self.kassapaate.edulliset, 2)

    def test_edullinen_kateisella_ei_riita_raha(self):
        self.kassapaate.syo_edullisesti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(200), 200)
        self.assertEqual(self.kassapaate.edulliset, 0)

    def test_edullinen_kortilla_osto(self):
        self.maksukortti = Maksukortti(1000)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti), True)
        self.assertEqual(self.kassapaate.edulliset, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_edullinen_kortilla_ei_riita_raha(self):
        self.maksukortti = Maksukortti(200)
        self.assertEqual(self.kassapaate.syo_edullisesti_kortilla(self.maksukortti),False)
        self.assertEqual(self.kassapaate.edulliset, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    # Maukkaat lounaat

    def test_maukkaat_lounaat(self):
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_maukas_kateisella_osto(self):
        self.kassapaate.syo_maukkaasti_kateisella(600)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100400)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(600), 200)
        self.assertEqual(self.kassapaate.maukkaat, 2)

    def test_maukas_kateisella_ei_riita_raha(self):
        self.kassapaate.syo_maukkaasti_kateisella(200)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(200), 200)
        self.assertEqual(self.kassapaate.maukkaat, 0)

    def test_maukas_kortilla_osto(self):
        self.maksukortti = Maksukortti(1000)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti), True)
        self.assertEqual(self.kassapaate.maukkaat, 1)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)

    def test_maukas_kortilla_ei_riita_raha(self):
        self.maksukortti = Maksukortti(50)
        self.assertEqual(self.kassapaate.syo_maukkaasti_kortilla(self.maksukortti),False)
        self.assertEqual(self.kassapaate.maukkaat, 0)
        self.assertEqual(self.kassapaate.kassassa_rahaa, 100000)
        