import os
import sys
from openai import OpenAI
from dotenv import load_dotenv


def cargar_api_key() -> str:
    """Carga la API key desde el archivo .env y valida que exista."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("ERROR: No se encontró OPENAI_API_KEY.")
        print("1. Copia '.env.example' a '.env'")
        print("2. Pega tu API key dentro de ese archivo")
        sys.exit(1)

    return api_key


def crear_cliente(api_key: str) -> OpenAI:
    """Crea y devuelve el cliente apuntando a la API de Groq (gratis, compatible con OpenAI)."""
    return OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")


def obtener_respuesta(client: OpenAI, historial: list) -> str:
    """Envía el historial de la conversación al modelo y devuelve la respuesta."""
    respuesta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=historial,
    )
    return respuesta.choices[0].message.content


def imprimir_bienvenida() -> None:
    """Muestra el mensaje inicial del chatbot."""
    print("=" * 50)
    print("  Lotus - Proyecto Semestral")
    print("  Escribe 'salir' para terminar la conversación")
    print("=" * 50)


def chat_loop(client: OpenAI) -> None:
    """Ciclo principal: recibe mensajes del usuario y responde usando la IA."""
    historial = [
        {
            "role": "system",
            "content": "Eres un asistente útil, breve y directo. Respondes en español.",
        }
    ]

    imprimir_bienvenida()

    while True:
        mensaje_usuario = input("\nTú: ").strip()

        if mensaje_usuario.lower() in ("salir", "exit", "quit"):
            print("Lotus: ¡Hasta luego!")
            break

        if not mensaje_usuario:
            continue

        historial.append({"role": "user", "content": mensaje_usuario})

        try:
            respuesta = obtener_respuesta(client, historial)
        except Exception as error:
            print(f"Ocurrió un error al contactar la API: {error}")
            continue

        historial.append({"role": "assistant", "content": respuesta})
        print(f"Lotus: {respuesta}")


def main() -> None:
    """Punto de entrada del programa."""
    api_key = cargar_api_key()
    client = crear_cliente(api_key)
    chat_loop(client)


if __name__ == "__main__":
    main()