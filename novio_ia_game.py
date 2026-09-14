import random
import gradio as gr
from groq import Groq

# Tu API Key colocada directamente para que funcione al instante
client = Groq(api_key="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")

# Definir las personalidades de los chicos
PERSONALITIES = {
    "Ren": "Eres Ren, un novio posesivo, oscuro, intenso y profundamente celoso. Te expresas con mucha pasión y siempre encierras tus acciones y movimientos físicos entre asteriscos (por ejemplo, *te agarra de la cintura con fuerza*).",
    "Liam": "Eres Liam, un novio flirtatious, juguetón, coqueto y divertido. Te encanta bromear y hacer sonrojar a tu pareja. Encierra siempre tus acciones físicas entre asteriscos (por ejemplo, *te guiña un ojo de forma traviesa*).",
    "Leo": "Eres Leo, un novio físico, directo, salvaje y protector. Te gusta el contacto cercano y demuestras tu afecto sin rodeos. Encierra siempre tus acciones físicas entre asteriscos (por ejemplo, *te acorrala contra la pared con una sonrisa de lado*)."
}

def generar_respuesta(mensaje_usuario, personaje_elegido, historial):
    if not mensaje_usuario:
        return historial, ""
    
    # Obtener el prompt del personaje
    system_prompt = PERSONALITIES.get(personaje_elegido, PERSONALITIES["Ren"])
    
    # Construir el historial para la API de Groq
    mensajes_chat = [{"role": "system", "content": system_prompt}]
    
    for humano, ia in historial:
        mensajes_chat.append({"role": "user", "content": humano})
        mensajes_chat.append({"role": "assistant", "content": ia})
        
    mensajes_chat.append({"role": "user", "content": mensaje_usuario})
    
    try:
        # Llamada a la API de Groq con Llama 3
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=mensajes_chat,
            temperature=0.8,
            max_tokens=500
        )
        respuesta_ia = completion.choices[0].message.content
    except Exception as e:
        respuesta_ia = f"*Frunce el ceño molesto* Ocurrió un error con la conexión... intenta de nuevo. (Error: {e})"
        
    historial.append((mensaje_usuario, respuesta_ia))
    return historial, ""

# Interfaz gráfica con Gradio
with gr.Blocks(theme=gr.themes.Soft(primary_hue="pink")) as demo:
    gr.Markdown("# 💖 My Perfect Boyfriend 💖")
    gr.Markdown("Elige a tu novio ideal y comienza a chatear. *(Recuerda que sus acciones van entre asteriscos)*")
    
    with gr.Row():
        personaje_selector = gr.Dropdown(
            choices=["Ren", "Liam", "Leo"], 
            value="Ren", 
            label="Elige a tu novio"
        )
        
    chatbot = gr.Chatbot(label="Chat", height=400)
    
    with gr.Row():
        txt_input = gr.Textbox(
            show_label=False, 
            placeholder="Escribe tu mensaje aquí...", 
            scale=4
        )
        btn_enviar = gr.Button("Enviar 💌", scale=1, variant="primary")
        
    # Enviar mensaje con Enter o botón
    txt_input.submit(generar_respuesta, [txt_input, personaje_selector, chatbot], [chatbot, txt_input])
    btn_enviar.click(generar_respuesta, [txt_input, personaje_selector, chatbot], [chatbot, txt_input])

if __name__ == "__main__":
    demo.launch()
