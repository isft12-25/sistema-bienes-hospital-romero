from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from core.models import BienPatrimonial, Expediente


class BienModelTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="tester", password="12345")

        self.expediente = Expediente.objects.create(
            numero_expediente="EXP-001",
            organismo_origen="Hospital Central",
            numero_compra="COMP-001",
        )

        self.base = {
            "numero_inventario": "INV-001",
            "nombre": "Computadora HP",
            "descripcion": "Equipo de oficina",
            "tipo": "INFORMATICA",
            "marca": "",
            "modelo": "",
            "numero_serie": "",
            "fecha_adquisicion": "2024-01-10",
            "valor_adquisicion": 1500.00,
            "proveedor": "",
            "cuenta_codigo": "",
            "origen": "COMPRA",
            "donante": "",
            "numero_identificacion": "NI-001",
            "ubicacion_actual": "Oficina 101",
            "responsable": "Juan Pérez",
            "expediente": self.expediente,
            "observaciones": "",
            "fecha_ultimo_mantenimiento": None,
            "proximo_mantenimiento": None,
            "usuario_creacion": self.user,
        }

    def test_creacion_valida_y_defaults(self):
        bien = BienPatrimonial(**self.base)
        bien.full_clean()
        bien.save()
        self.assertEqual(bien.estado, "ACTIVO")
        self.assertEqual(bien.origen, "COMPRA")
        self.assertEqual(str(bien), f"{bien.numero_inventario} - {bien.nombre}")

    def test_donacion_requiere_donante(self):
        data = self.base.copy()
        data.update({"origen": "DONACION", "donante": ""})
        bien = BienPatrimonial(**data)
        with self.assertRaises(ValidationError) as ctx:
            bien.full_clean()
        self.assertIn("donante", ctx.exception.error_dict)

        data_ok = self.base.copy()
        data_ok.update({"origen": "DONACION", "donante": "Fundación Amigos"})
        bien_ok = BienPatrimonial(**data_ok)
        bien_ok.full_clean()

    def test_valor_adquisicion_no_negativo(self):
        data = self.base.copy()
        data.update({"valor_adquisicion": -1})
        bien = BienPatrimonial(**data)
        with self.assertRaises(ValidationError) as ctx:
            bien.full_clean()
        self.assertIn("valor_adquisicion", ctx.exception.error_dict)

        for v in (0, 10, 1234.50):
            d = self.base.copy()
            d.update({"valor_adquisicion": v})
            b = BienPatrimonial(**d)
            b.full_clean()

    def test_unicidad_numero_inventario(self):
        primero = BienPatrimonial(**self.base)
        primero.full_clean()
        primero.save()

        dup = self.base.copy()
        dup.update({"nombre": "Otro bien"})
        segundo = BienPatrimonial(**dup)
        with self.assertRaises(ValidationError) as ctx:
            segundo.full_clean()
        self.assertIn("numero_inventario", ctx.exception.error_dict)

    def test_unicidad_numero_identificacion(self):
        a = BienPatrimonial(**self.base)
        a.full_clean()
        a.save()

        dup = self.base.copy()
        dup.update({
            "numero_inventario": "INV-002",
            "nombre": "Impresora",
        })
        b = BienPatrimonial(**dup)
        with self.assertRaises(ValidationError) as ctx:
            b.full_clean()
        self.assertIn("numero_identificacion", ctx.exception.error_dict)

    def test_numero_identificacion_puede_ser_null_o_blank(self):
        d1 = self.base.copy()
        d1.update({"numero_inventario": "INV-010", "numero_identificacion": None})
        b1 = BienPatrimonial(**d1)
        b1.full_clean()

        d2 = self.base.copy()
        d2.update({"numero_inventario": "INV-011", "numero_identificacion": ""})
        b2 = BienPatrimonial(**d2)
        b2.full_clean()
