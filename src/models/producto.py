import uuid


class Producto:
    """clase base que representa un producto genérico de la tienda.

    todos los productos de el cowboy espacial (electrónicos, ropa, etc.) heredan
    de esta clase. aquí se guardan los datos comunes: id, nombre,
    precio y stock disponible.
    """

    def __init__(self, nombre: str, precio: float, stock: int) -> None:
        """crea un producto nuevo y le asigna un id único automáticamente."""
        self.id: str = str(uuid.uuid4())
        self.nombre: str = nombre
        self.precio: float = precio
        self.stock: int = stock

    def hay_stock(self, cantidad: int) -> bool:
        """comprueba si hay stock suficiente para la cantidad pedida."""
        if cantidad <= self.stock:
            return True
        else:
            return False

    def actualizar_stock(self, cantidad: int) -> None:
        """actualiza el stock del producto sumando o restando unidades."""
        self.stock = self.stock + cantidad

    def __str__(self) -> str:
        """devuelve un texto sencillo con la info principal del producto."""
        texto = f"[{self.id[:8]}] {self.nombre} - precio: {self.precio}€ - stock: {self.stock}"
        return texto


class ProductoElectronico(Producto):
    """producto electrónico de la tienda (por ejemplo, un reproductor de blu-ray).

    añade un campo extra respecto a producto: los meses de garantía.
    """

    def __init__(self, nombre: str, precio: float, stock: int, meses_garantia: int) -> None:
        """crea un producto electrónico llamando primero al constructor del padre."""
        super().__init__(nombre, precio, stock)
        self.meses_garantia: int = meses_garantia

    def __str__(self) -> str:
        """añade la información de la garantía al texto del padre."""
        texto_base = super().__str__()
        texto_final = f"{texto_base} - garantía: {self.meses_garantia} meses"
        return texto_final


class ProductoRopa(Producto):
    """producto de ropa de la tienda (camisetas, sudaderas, etc.).

    añade dos campos extra respecto a producto: la talla y el color.
    """

    def __init__(self, nombre: str, precio: float, stock: int, talla: str, color: str) -> None:
        """crea un producto de ropa llamando primero al constructor del padre."""
        super().__init__(nombre, precio, stock)
        self.talla: str = talla
        self.color: str = color

    def __str__(self) -> str:
        """añade la talla y el color al texto del padre."""
        texto_base = super().__str__()
        texto_final = f"{texto_base} - talla: {self.talla} - color: {self.color}"
        return texto_final