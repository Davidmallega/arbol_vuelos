from vuelos_data import vuelos_disponibles

class Node:
    def __init__(self, vuelo_id, nombre_pasajero=None, fecha=None, pais_origen=None, pais_destino=None, asientos=None):
        self.vuelo_id = vuelo_id
        self.nombre_pasajero = nombre_pasajero
        self.fecha = fecha
        self.pais_origen = pais_origen
        self.pais_destino = pais_destino
        self.asientos = asientos
        self.left = None
        self.right = None
        self.height = 1

class FlightReservationSystem:
    def __init__(self):
        self.root = None
        self.vuelos_disponibles = vuelos_disponibles
        self.reservas = []

    def insert(self, vuelo_id, nombre_pasajero, fecha, pais_origen, pais_destino, asientos):
        self.root = self._insert(self.root, vuelo_id, nombre_pasajero, fecha, pais_origen, pais_destino, asientos)
        self.reservas.append({"vuelo_id": vuelo_id, "nombre_pasajero": nombre_pasajero, "fecha": fecha, "pais_origen": pais_origen, "pais_destino": pais_destino, "asientos": asientos})

    def _insert(self, node, vuelo_id, nombre_pasajero, fecha, pais_origen, pais_destino, asientos):
        if not node:
            return Node(vuelo_id, nombre_pasajero, fecha, pais_origen, pais_destino, asientos)
        
        if vuelo_id < node.vuelo_id:
            node.left = self._insert(node.left, vuelo_id, nombre_pasajero, fecha, pais_origen, pais_destino, asientos)
        else:
            node.right = self._insert(node.right, vuelo_id, nombre_pasajero, fecha, pais_origen, pais_destino, asientos)
        
        node.height = 1 + max(self._get_height(node.left), self._get_height(node.right))
        balance = self._get_balance(node)

        if balance > 1 and vuelo_id < node.left.vuelo_id:
            return self._right_rotate(node)
        if balance < -1 and vuelo_id > node.right.vuelo_id:
            return self._left_rotate(node)
        if balance > 1 and vuelo_id > node.left.vuelo_id:
            node.left = self._left_rotate(node.left)
            return self._right_rotate(node)
        if balance < -1 and vuelo_id < node.right.vuelo_id:
            node.right = self._right_rotate(node.right)
            return self._left_rotate(node)

        return node

    def search(self, vuelo_id):
        return self._search(self.root, vuelo_id)

    def _search(self, node, vuelo_id):
        if not node or node.vuelo_id == vuelo_id:
            return node
        if vuelo_id < node.vuelo_id:
            return self._search(node.left, vuelo_id)
        return self._search(node.right, vuelo_id)

    def delete(self, vuelo_id):
        self.root = self._delete_node(self.root, vuelo_id)

    def _delete_node(self, root, vuelo_id):
        if not root:
            return root

        if vuelo_id < root.vuelo_id:
            root.left = self._delete_node(root.left, vuelo_id)
        elif vuelo_id > root.vuelo_id:
            root.right = self._delete_node(root.right, vuelo_id)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            
            temp = self._get_min_value_node(root.right)
            root.vuelo_id = temp.vuelo_id
            root.right = self._delete_node(root.right, temp.vuelo_id)

        root.height = 1 + max(self._get_height(root.left), self._get_height(root.right))
        balance = self._get_balance(root)

        if balance > 1 and self._get_balance(root.left) >= 0:
            return self._right_rotate(root)
        if balance < -1 and self._get_balance(root.right) <= 0:
            return self._left_rotate(root)
        if balance > 1 and self._get_balance(root.left) < 0:
            root.left = self._left_rotate(root.left)
            return self._right_rotate(root)
        if balance < -1 and self._get_balance(root.right) > 0:
            root.right = self._right_rotate(root.right)
            return self._left_rotate(root)

        return root

    def _left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        return y

    def _get_height(self, node):
        if not node:
            return 0
        return node.height

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)

    def _get_min_value_node(self, node):
        if node is None or node.left is None:
            return node
        return self._get_min_value_node(node.left)

    def inorder_traversal(self, node):
        result = []
        if node:
            result = self.inorder_traversal(node.left)
            result.append(node)
            result = result + self.inorder_traversal(node.right)
        return result

    def get_vuelos_disponibles(self):
        return self.vuelos_disponibles

    def get_next_id(self):
        if not self.vuelos_disponibles and not self.reservas:
            return 1
        max_vuelo_id = max(vuelo["vuelo_id"] for vuelo in self.vuelos_disponibles)
        max_reserva_id = max(reserva["vuelo_id"] for reserva in self.reservas) if self.reservas else 0
        return max(max_vuelo_id, max_reserva_id) + 1

