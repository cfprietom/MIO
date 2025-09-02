import os
import datetime
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# ---------------- Logging ----------------
logging.basicConfig(
    format="%(asctime)s %(levelname)s %(name)s | %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ---------------- Token ------------------
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not TOKEN:
    raise RuntimeError("Falta la variable de entorno TELEGRAM_BOT_TOKEN")

# ---------------- Datos ------------------
DATOS_ESTADISTICOS = [
    "📊 ¿Sabías que… el **45%** de los accidentes laborales en Ecuador ocurren en el sector de la construcción?",
    "📊 ¿Sabías que… los **riesgos ergonómicos** generan el 30% de enfermedades profesionales reportadas?",
    "📊 ¿Sabías que… el **70% de empleadores** aún no cuenta con un plan anual de seguridad y salud?",
    "📊 ¿Sabías que… la mayoría de accidentes afectan a trabajadores entre 25 y 34 años?",
    "📊 ¿Sabías que… el **estrés laboral** es una de las 5 principales causas de ausentismo en Ecuador?",
]

# -------------- Helpers ------------------
def obtener_dato_rotado(context: ContextTypes.DEFAULT_TYPE) -> str:
    idx = context.user_data.get("sabiasque_idx", 0)
    dato = DATOS_ESTADISTICOS[idx % len(DATOS_ESTADISTICOS)]
    context.user_data["sabiasque_idx"] = (idx + 1) % len(DATOS_ESTADISTICOS)
    return dato

def menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("📘 Reglamento", callback_data="reglamento")],
        [InlineKeyboardButton("⚠️ Riesgos", callback_data="riesgos")],
        [InlineKeyboardButton("📑 Obligaciones", callback_data="obligaciones")],
        [InlineKeyboardButton("🧠 Psicosocial", callback_data="psicosocial")],
        [InlineKeyboardButton("📂 Formatos", callback_data="formatos")],
        [InlineKeyboardButton("❓ FAQ", callback_data="faq")],
        [InlineKeyboardButton("ℹ️ Sabías que…", callback_data="sabiasque")],
        [InlineKeyboardButton("📣 Denuncias", callback_data="denuncias")],
        ]
    return InlineKeyboardMarkup(keyboard)

# -------------- Comandos -----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dato = obtener_dato_rotado(context)
    await update.effective_message.reply_text(
        "👷‍♂️ ¡Bienvenido al Bot de Seguridad Laboral del Ecuador!\n"
        "Usa /menu para ver todas las funciones disponibles o /help para ayuda.\n\n"
        f"{dato}\n\n"
        "🔗 Fuente: Dashboard SST (Power BI): https://app.powerbi.com/view?r=eyJrIjoiNGMyNjdiZTctNDk5MC00MDBhLWJiZjctZTk3MDI3ODM4OGIwIiwidCI6IjZhNmNlOGVkLTBlMGYtNDY4YS05Yzg1LWU3Y2U0ZjIxZjRmMiJ9"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "🆘 *Comandos disponibles*\n\n"
        "/start — Mensaje de bienvenida\n"
        "/menu — Abre el menú interactivo\n"
        "/faq — Ver categorías de preguntas\n"
        "/faq <palabra> — Buscar preguntas por palabra clave\n"
        "/sabiasque — Mostrar un dato aleatorio\n"
        "/activar_diario — Enviar un dato cada día a las 9:00 AM\n"
        "/reglamento | /riesgos | /obligaciones | /psicosocial | /formatos | /denuncias — Accesos directos",
        parse_mode="Markdown"
    )

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Selecciona un tema:", reply_markup=menu_keyboard())

# ------ Secciones informativas (slash & botones) ------
async def reglamento(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "📘 *Reglamento de Higiene y Seguridad*\n\n"
        "Guía oficial para elaborar y registrar el reglamento obligatorio.\n"
        "🔗 https://www.trabajo.gob.ec/wp-content/uploads/2025/02/17022025_Estructura-RHS-v8.pdf",
        parse_mode="Markdown"
    )

async def riesgos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "⚠️ *Tipos de Riesgos Laborales (Ecuador):*\n"
        "- Físicos (ruido, calor, radiación)\n"
        "- Químicos (vapores, gases, líquidos tóxicos)\n"
        "- Biológicos (virus, bacterias)\n"
        "- Ergonómicos (posturas, esfuerzo repetitivo)\n"
        "- Psicosociales (estrés, violencia, acoso)\n"
        "- De seguridad (electricidad, caídas, atrapamientos)",
        parse_mode="Markdown"
    )

async def obligaciones(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "📑 *Obligaciones del empleador (MDT-2024-196):*\n"
        "• Elaborar y registrar el Reglamento de Higiene y Seguridad\n"
        "• Designar responsable(s) de SST\n"
        "• Implementar Plan Anual de SST\n"
        "• Formar brigadas internas\n"
        "• Reportar accidentes laborales\n"
        "🔗 https://www.trabajo.gob.ec/wp-content/uploads/2024/10/ACUERDO-MINISTERIAL-NRO.-MDT-2024-196-signed.pdf",
        parse_mode="Markdown"
    )

async def psicosocial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "🧠 *Prevención de Riesgos Psicosociales*\n"
        "Protocolos para acoso, estrés, violencia laboral, etc.\n"
        "🔗 https://www.trabajo.gob.ec/wp-content/uploads/2024/01/Guia-para-la-implementacion-del-programa-de-prevencion-de-riesgo-psicosocial.pdf",
        parse_mode="Markdown"
    )

async def formatos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "📂 *Formatos y guías oficiales:*\n"
        "https://www.trabajo.gob.ec/normativa-legal-programas-formatos-y-guias/",
        parse_mode="Markdown"
    )

async def denuncias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "📣 *Canales de denuncia:*\n"
        "• SUT: https://sut.trabajo.gob.ec/denuncias\n"
        "• Teléfono: 1800-266822",
        parse_mode="Markdown"
    )

# --------- FAQ (categorías y búsqueda simple) ----------
from docx import Document

def cargar_faqs_desde_archivos(*doc_paths):
    faqs = {}
    for doc_path in doc_paths:
        try:
            doc = Document(doc_path)
        except Exception as e:
            logger.warning("No se pudo abrir %s: %s", doc_path, e)
            continue

        current_category = None
        pregunta = None

        for p in doc.paragraphs:
            text = (p.text or "").strip()
            if not text:
                continue

            # Categorías por estilos de Heading
            if p.style and p.style.name and p.style.name.startswith("Heading"):
                current_category = text
                faqs.setdefault(current_category, [])
                continue

            # Formato con emojis
            if text.startswith("❓"):
                pregunta = text.replace("❓", "").strip()
                continue
            if text.startswith("✅") and pregunta:
                respuesta = text.replace("✅", "").strip()
                faqs.setdefault(current_category or "General", []).append(f"{pregunta}\n👉 {respuesta}")
                pregunta = None
                continue

            # Formato Pregunta:/Respuesta:
            low = text.lower()
            if low.startswith("pregunta:"):
                pregunta = text.split(":", 1)[1].strip()
                continue
            if low.startswith("respuesta:") and pregunta:
                respuesta = text.split(":", 1)[1].strip()
                faqs.setdefault(current_category or "General", []).append(f"{pregunta}\n👉 {respuesta}")
                pregunta = None
                continue

    return faqs

FAQS_CATEGORIAS = cargar_faqs_desde_archivos(
    "Banco_Preguntas_Decreto_255.docx",
    "Banco_Preguntas_Acuerdo_196.docx"
)

async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Si viene /faq con palabra -> búsqueda
    if getattr(context, "args", None):
        palabra = " ".join(context.args).lower()
        resultados = []
        for categoria, preguntas in FAQS_CATEGORIAS.items():
            for p in preguntas:
                if palabra in p.lower():
                    resultados.append(f"📌 {categoria}\n{p}")
        if resultados:
            texto = f"🔎 Resultados para *{palabra}*:\n\n" + "\n\n".join(resultados[:15])
        else:
            texto = f"❌ No se encontraron resultados para *{palabra}*."
        await update.effective_message.reply_text(texto, parse_mode="Markdown")
        return

    # Si no, mostrar categorías
    if not FAQS_CATEGORIAS:
        await update.effective_message.reply_text("Aún no hay preguntas cargadas.")
        return

    keyboard = [[InlineKeyboardButton(cat, callback_data=f"faqcat:{cat}")]
                for cat in FAQS_CATEGORIAS.keys()]
    await update.effective_message.reply_text("📂 Selecciona una categoría:", reply_markup=InlineKeyboardMarkup(keyboard))

async def faq_categoria(update: Update, context: ContextTypes.DEFAULT_TYPE, categoria: str, page: int = 0):
    preguntas = FAQS_CATEGORIAS.get(categoria, [])
    if not preguntas:
        await update.callback_query.edit_message_text("No hay preguntas en esta categoría.")
        return

    por_pagina = 5
    inicio = page * por_pagina
    fin = min(inicio + por_pagina, len(preguntas))
    bloque = preguntas[inicio:fin]

    texto = f"❓ *Preguntas Frecuentes - {categoria}:*\n\n"
    for i, pregunta in enumerate(bloque, start=inicio + 1):
        texto += f"{i}. {pregunta}\n\n"

    botones = []
    if page > 0:
        botones.append(InlineKeyboardButton("⬅️ Anterior", callback_data=f"faqnav:{categoria}:{page-1}"))
    if fin < len(preguntas):
        botones.append(InlineKeyboardButton("➡️ Siguiente", callback_data=f"faqnav:{categoria}:{page+1}"))

    await update.callback_query.edit_message_text(texto, parse_mode="Markdown",
                                                  reply_markup=InlineKeyboardMarkup([botones]) if botones else None)

# ---------- Sabías que & difusión diaria ----------
async def sabiasque(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dato = obtener_dato_rotado(context)
    await update.effective_message.reply_text(
        f"{dato}\n\n🔗 Power BI: https://app.powerbi.com/view?r=eyJrIjoiNGMyNjdiZTctNDk5MC00MDBhLWJiZjctZTk3MDI3ODM4OGIwIiwidCI6IjZhNmNlOGVkLTBlMGYtNDY4YS05Yzg1LWU3Y2U0ZjIxZjRmMiJ9"
    )

async def enviar_sabiasque_diario(context: ContextTypes.DEFAULT_TYPE):
    dato = obtener_dato_rotado(context)
    await context.bot.send_message(chat_id=context.job.chat_id, text=dato)

async def activar_diario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_message.chat_id
    context.job_queue.run_daily(enviar_sabiasque_diario, time=datetime.time(hour=9, minute=0), chat_id=chat_id)
    await update.effective_message.reply_text("✅ Difusión automática activada: todos los días a las 9:00 AM.")

# ---------------- Handlers ----------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    try:
        if data == "reglamento":
            await reglamento(update, context)
        elif data == "riesgos":
            await riesgos(update, context)
        elif data == "obligaciones":
            await obligaciones(update, context)
        elif data == "psicosocial":
            await psicosocial(update, context)
        elif data == "formatos":
            await formatos(update, context)
        elif data == "denuncias":
            await denuncias(update, context)
        elif data == "sabiasque":
            await sabiasque(update, context)
        elif data == "faq":
            await faq(update, context)
        elif data.startswith("faqcat:"):
            _, cat = data.split(":", 1)
            await faq_categoria(update, context, cat, 0)
        elif data.startswith("faqnav:"):
            _, cat, page = data.split(":")
            await faq_categoria(update, context, cat, int(page))
        else:
            await update.effective_message.reply_text("Opción no reconocida.")
    except Exception as e:
        logger.exception("Error en button_handler: %s", e)
        await update.effective_message.reply_text("Ocurrió un error al procesar tu solicitud.")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.exception("Excepción no manejada: %s", context.error)

# ----------------- Main ------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Slash commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("menu", menu))
    app.add_handler(CommandHandler("faq", faq))
    app.add_handler(CommandHandler("sabiasque", sabiasque))
    app.add_handler(CommandHandler("activar_diario", activar_diario))
    # accesos directos también como slash
    app.add_handler(CommandHandler("reglamento", reglamento))
    app.add_handler(CommandHandler("riesgos", riesgos))
    app.add_handler(CommandHandler("obligaciones", obligaciones))
    app.add_handler(CommandHandler("psicosocial", psicosocial))
    app.add_handler(CommandHandler("formatos", formatos))
    app.add_handler(CommandHandler("denuncias", denuncias))

    # Inline buttons
    app.add_handler(CallbackQueryHandler(button_handler))

    # Errors
    app.add_error_handler(error_handler)

    logger.info("✅ Bot de Seguridad Laboral activo...")
    app.run_polling()

if __name__ == "__main__":
    main()
