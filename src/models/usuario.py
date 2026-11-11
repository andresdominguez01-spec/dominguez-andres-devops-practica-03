import uuid


class Usuario:
    """clase base que representa a cualquier persona que usa la tienda.

    tanto los clientes como los administradores heredan de esta clase.
    """

    def __init__(self, nombre: str, email: str) -> None:
        """crea un usuario nuevo y le asigna un id único automáticamente."""
        self.id: str = str(uuid.uuid4())
        self.nombre: str = nombre
        self.email: str = email

    def is_admin(self) -> bool:
        """por defecto, un usuario normal no es administrador."""
        return False

    def __str__(self) -> str:
        """devuelve un texto sencillo con la info principal del usuario."""
        texto = f"[{self.id[:8]}] {self.nombre} ({self.email})"
        return texto


class Cliente(Usuario):
    """representa a un cliente de la tienda el cowboy espacial.

    añade un campo extra respecto a usuario: la dirección postal,
    que se usará para poder enviarle los pedidos.
    """

    def __init__(self, nombre: str, email: str, direccion: str) -> None:
        """crea un cliente llamando primero al constructor del padre."""
        super().__init__(nombre, email)
        self.direccion: str = direccion

    def __str__(self) -> str:
        """añade la dirección al texto del padre."""
        texto_base = super().__str__()
        texto_final = f"{texto_base} - dirección: {self.direccion}"
        return texto_final


class Administrador(Usuario):
    """representa a un gestor de la tienda el cowboy espacial.

    sobrescribe is_admin() para dejar claro que tiene permisos de
    administrador dentro del sistema.
    """

    def is_admin(self) -> bool:
        """un administrador siempre devuelve true."""
        return True