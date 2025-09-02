# Bot Seguridad Laboral — Corrección de comandos

## Pasos rápidos en Replit
1) Sube estos archivos y los dos .docx.
2) En **Secrets (🔑)** añade `TELEGRAM_BOT_TOKEN` = tu token.
3) En la Shell:
   ```bash
   pip install -r requirements.txt --force-reinstall
   ```
4) Run. Si falla, mira la consola: ahora hay *logging* y *error handler*.
5) Prueba:
   - /start, /menu, /help
   - /faq accidente   (búsqueda)
   - Botones del menú (FAQ, Reglamento, etc.)

### Notas
- Se usa `update.effective_message` en todas las respuestas (funciona en comandos y en botones).
- FAQ reconoce formato con `❓ / ✅` y también `Pregunta: / Respuesta:`.
- Incluye `/reglamento`, `/riesgos`, `/obligaciones`, `/psicosocial`, `/formatos`, `/denuncias` como comandos, además de botones.
