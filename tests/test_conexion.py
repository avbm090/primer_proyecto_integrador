from conexion.conexion_singleton import ConexionSingleton

def test_singleton_connection():
    conn1 = ConexionSingleton()
    conn2 = ConexionSingleton()
    print("¿Misma instancia?", conn1 is conn2)

    session1 = conn1.get_session()
    session2 = conn2.get_session()

    print("Misma engine:", session1.bind == session2.bind)

if __name__ == "__main__":
    test_singleton_connection()
