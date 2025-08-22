from django.db import models


class Region(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Ciudad(models.Model):
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="ciudades")

    def __str__(self):
        return self.nombre


class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Terma(models.Model):
    ESTADOS = [
        ("activa", "Activa"),
        ("inactiva", "Inactiva"),
    ]
    nombre_terma = models.CharField(max_length=100)
    descripcion_terma = models.TextField(null=True, blank=True)
    direccion_terma = models.TextField(null=True, blank=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.SET_NULL, null=True, blank=True)
    telefono_terma = models.CharField(max_length=20, null=True, blank=True)
    email_terma = models.EmailField(max_length=100, null=True, blank=True)
    sitio_web = models.URLField(max_length=200, null=True, blank=True)
    estado_suscripcion = models.CharField(max_length=20, choices=ESTADOS)
    fecha_suscripcion = models.DateField(null=True, blank=True)
    calificacion_promedio = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.nombre_terma


class Calificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    terma = models.ForeignKey(Terma, on_delete=models.CASCADE)
    puntuacion = models.IntegerField()
    comentario = models.TextField(null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)


class MetodoPago(models.Model):
    nombre = models.CharField(max_length=50)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Compra(models.Model):
    ESTADO_PAGO = [
        ("pendiente", "Pendiente"),
        ("pagado", "Pagado"),
        ("cancelado", "Cancelado"),
    ]
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.SET_NULL, null=True, blank=True)
    fecha_compra = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado_pago = models.CharField(max_length=20, choices=ESTADO_PAGO)
    mercado_pago_id = models.CharField(max_length=100, null=True, blank=True)
    codigo_confirmacion = models.CharField(max_length=100, null=True, blank=True)


class CodigoQR(models.Model):
    compra = models.OneToOneField(Compra, on_delete=models.CASCADE)
    codigo = models.TextField()
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    fecha_uso = models.DateTimeField(null=True, blank=True)
    usado = models.BooleanField(default=False)


class CuponDescuento(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    descuento_porcentaje = models.IntegerField()
    fecha_vencimiento = models.DateField(null=True, blank=True)
    terma = models.ForeignKey(Terma, on_delete=models.SET_NULL, null=True, blank=True)


class CuponUsado(models.Model):
    cupon = models.ForeignKey(CuponDescuento, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    fecha_uso = models.DateTimeField(auto_now_add=True)


class EntradaTipo(models.Model):
    terma = models.ForeignKey(Terma, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_horas = models.IntegerField(null=True, blank=True)
    estado = models.BooleanField(default=True)


class HorarioDisponible(models.Model):
    terma = models.ForeignKey(Terma, on_delete=models.CASCADE)
    entrada_tipo = models.ForeignKey(EntradaTipo, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    cupos_totales = models.IntegerField()
    cupos_disponibles = models.IntegerField()


class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name="detalles")
    horario_disponible = models.ForeignKey(HorarioDisponible, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)


class ImagenTerma(models.Model):
    terma = models.ForeignKey(Terma, on_delete=models.CASCADE, related_name="imagenes")
    url_imagen = models.TextField()
    descripcion = models.TextField(null=True, blank=True)


class ServicioTerma(models.Model):
    terma = models.ForeignKey(Terma, on_delete=models.CASCADE, related_name="servicios")
    servicio = models.CharField(max_length=100)


class Carrito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    horario_disponible = models.ForeignKey(HorarioDisponible, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
