#!/usr/bin/env python3
"""Generate KB Gaps Report PDF in Spanish"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

OUTPUT = os.path.join(os.path.dirname(__file__), 'KB_Gaps_Report_BetonWin.pdf')

TEAL = HexColor('#03242D')
GREEN = HexColor('#45cd98')
GOLD = HexColor('#ffc572')
RED = HexColor('#f54943')
GRAY = HexColor('#666666')
LIGHT = HexColor('#f8f9fa')
DARK2 = HexColor('#0a3d4a')

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='DocTitle', fontName='Helvetica-Bold', fontSize=20, textColor=TEAL, spaceAfter=3*mm, alignment=TA_CENTER))
styles.add(ParagraphStyle(name='DocSub', fontName='Helvetica', fontSize=11, textColor=GRAY, spaceAfter=8*mm, alignment=TA_CENTER))
styles.add(ParagraphStyle(name='Sec', fontName='Helvetica-Bold', fontSize=14, textColor=TEAL, spaceBefore=8*mm, spaceAfter=4*mm))
styles.add(ParagraphStyle(name='Sub', fontName='Helvetica-Bold', fontSize=11, textColor=HexColor('#2c3e50'), spaceBefore=5*mm, spaceAfter=2*mm))
styles.add(ParagraphStyle(name='Body', fontName='Helvetica', fontSize=9.5, textColor=HexColor('#333333'), spaceAfter=2*mm, leading=13))
styles.add(ParagraphStyle(name='Quote', fontName='Helvetica-Oblique', fontSize=9, textColor=HexColor('#555555'), leftIndent=10*mm, spaceAfter=2*mm, leading=12, borderColor=GREEN, borderWidth=0, borderPadding=0))
styles.add(ParagraphStyle(name='BulletItem', fontName='Helvetica', fontSize=9.5, textColor=HexColor('#333333'), leftIndent=8*mm, bulletIndent=4*mm, spaceAfter=1.5*mm, leading=13))
styles.add(ParagraphStyle(name='Footer', fontName='Helvetica', fontSize=8, textColor=GRAY, alignment=TA_CENTER))
styles.add(ParagraphStyle(name='Rec', fontName='Helvetica', fontSize=9.5, textColor=HexColor('#333333'), spaceAfter=3*mm, leading=14, leftIndent=4*mm))

def section(t): return Paragraph(t, styles['Sec'])
def sub(t): return Paragraph(t, styles['Sub'])
def body(t): return Paragraph(t, styles['Body'])
def quote(t): return Paragraph(f'<i>"{t}"</i>', styles['Quote'])
def bullet(t): return Paragraph(f'•  {t}', styles['BulletItem'])
def rec(t): return Paragraph(t, styles['Rec'])
def hr(): return HRFlowable(width='100%', thickness=0.5, color=HexColor('#e0e0e0'), spaceAfter=3*mm, spaceBefore=3*mm)

def build():
    doc = SimpleDocTemplate(OUTPUT, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=18*mm, bottomMargin=18*mm)
    story = []

    # COVER
    story.append(Spacer(1, 25*mm))
    story.append(Paragraph('BetonWin AI Support', styles['DocTitle']))
    story.append(Paragraph('Informe de Brechas en la Base de Conocimiento (FAQ)', styles['DocSub']))
    story.append(Spacer(1, 3*mm))
    story.append(Paragraph('Periodo analizado: 28 Marzo — 1 Abril 2026', styles['Footer']))
    story.append(Paragraph('137 mensajes | 32 sesiones | 4 idiomas', styles['Footer']))
    story.append(Spacer(1, 8*mm))
    story.append(hr())

    # Summary
    story.append(section('1. Resumen Ejecutivo'))
    story.append(body('Durante el periodo de prueba, se analizaron <b>137 conversaciones</b> de usuarios reales con el agente AI. El análisis reveló que <b>solo el 18% de las consultas</b> recibieron contexto de la base de conocimiento (FAQ), mientras que el <b>82% fue respondido únicamente con datos de entrenamiento del modelo AI</b>.'))
    story.append(body('Se identificaron <b>13 temas frecuentes</b> que los usuarios preguntan pero que <b>no están cubiertos en la FAQ actual</b>. Agregar estas respuestas mejorará significativamente la calidad y precisión del soporte.'))

    # Stats
    stats = [
        ['Métrica', 'Valor', 'Estado'],
        ['Total de mensajes analizados', '137', 'OK'],
        ['Consultas CON contexto KB', '25 (18%)', 'BAJO'],
        ['Consultas SIN contexto KB', '112 (82%)', 'CRÍTICO'],
        ['Temas sin cobertura en FAQ', '13', 'ACCIÓN REQUERIDA'],
        ['Secciones existentes en FAQ', '14', 'OK'],
        ['Total líneas en FAQ actual', '338', 'MEJORABLE'],
    ]
    t = Table(stats, colWidths=[70*mm, 40*mm, 40*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TEXTCOLOR', (2, 3), (2, 3), RED),
        ('FONTNAME', (2, 3), (2, 4), 'Helvetica-Bold'),
        ('TEXTCOLOR', (2, 4), (2, 4), RED),
    ]))
    story.append(t)

    story.append(PageBreak())

    # ==================== GAPS LIST ====================
    story.append(section('2. Temas Faltantes — Detalle'))
    story.append(body('A continuación se detalla cada tema que los usuarios preguntaron y que <b>no tiene respuesta en la FAQ actual</b>. Para cada uno se incluye: la pregunta real del usuario, la prioridad sugerida, y la respuesta recomendada para agregar.'))

    # GAP 1
    story.append(sub('2.1  Proceso paso a paso para depositar'))
    story.append(Paragraph('<font color="#f54943"><b>PRIORIDAD ALTA</b></font> — Preguntado 2 veces', styles['Body']))
    story.append(quote('¿Me pueden explicar paso a paso cómo hacer un depósito en la plataforma?'))
    story.append(body('<b>Estado actual:</b> La FAQ tiene información sobre métodos y tiempos, pero NO un proceso paso a paso con instrucciones claras.'))
    story.append(body('<b>Respuesta sugerida para agregar:</b>'))
    story.append(rec('Para hacer un depósito en BetonWin, sigue estos pasos:<br/>1. Inicia sesión en tu cuenta<br/>2. Haz clic en "Caja" o el botón "Depositar" en la parte superior<br/>3. Selecciona tu método de pago preferido (tarjeta, cripto, billetera electrónica, etc.)<br/>4. Ingresa el monto que deseas depositar (mínimo: 10 EUR)<br/>5. Completa los datos del método de pago seleccionado<br/>6. Confirma la transacción<br/>7. Los fondos se acreditarán según el método: tarjeta/billetera = instantáneo, cripto = 10-30 min, banco = 1-3 días<br/><br/>Si tienes problemas, contacta soporte en ayuda@beton.win.'))

    # GAP 2
    story.append(sub('2.2  Dónde ver el saldo / balance'))
    story.append(Paragraph('<font color="#f54943"><b>PRIORIDAD ALTA</b></font> — Preguntado 3 veces', styles['Body']))
    story.append(quote('¿Dónde puedo ver mi saldo?'))
    story.append(quote('¿Podrías decirme cómo ver mi saldo?'))
    story.append(body('<b>Respuesta sugerida:</b>'))
    story.append(rec('Tu saldo se muestra en la esquina superior derecha de la pantalla, junto al botón "Depositar". Puedes ver:<br/>• <b>Saldo real</b>: dinero disponible para apostar o retirar<br/>• <b>Saldo de bono</b>: fondos de bonificación (sujetos a rollover)<br/><br/>Para ver el historial detallado, ve a Mi Cuenta → Historial de Transacciones.'))

    # GAP 3
    story.append(sub('2.3  Por qué no gano / juegos manipulados'))
    story.append(Paragraph('<font color="#f54943"><b>PRIORIDAD ALTA</b></font> — Preguntado 2 veces (incluye acusaciones de estafa)', styles['Body']))
    story.append(quote('No gano nada'))
    story.append(quote('Es una estafa, los juegos están manipulados'))
    story.append(body('<b>Respuesta sugerida:</b>'))
    story.append(rec('Todos los juegos de BetonWin son proporcionados por proveedores con licencia y certificados por organismos reguladores independientes. Los resultados se generan mediante un <b>Generador de Números Aleatorios (RNG)</b> certificado, lo que garantiza que cada resultado es completamente aleatorio e imparcial.<br/><br/>Cada juego tiene un <b>RTP (Return to Player)</b> publicado — por ejemplo, las tragamonedas suelen tener un RTP entre 94% y 97%, lo que significa que, a largo plazo, devuelven entre 94-97 centavos por cada euro apostado.<br/><br/>Es normal tener rachas perdedoras — esto es parte de la naturaleza aleatoria del juego. Si sientes que el juego se ha convertido en un problema, BetonWin ofrece herramientas de <b>juego responsable</b> como límites de depósito y autoexclusión.'))

    story.append(PageBreak())

    # GAP 4
    story.append(sub('2.4  Retiro cancelado'))
    story.append(Paragraph('<font color="#f54943"><b>PRIORIDAD ALTA</b></font> — Preguntado 1 vez', styles['Body']))
    story.append(quote('¿Por qué aparece cancelado el retiro?'))
    story.append(body('<b>Respuesta sugerida:</b>'))
    story.append(rec('Un retiro puede aparecer como "Cancelado" por las siguientes razones:<br/>• <b>Verificación KYC incompleta</b>: debes completar la verificación de identidad antes de retirar<br/>• <b>Bono activo con rollover pendiente</b>: si tienes un bono, debes cumplir los requisitos de apuesta antes de retirar<br/>• <b>Método de retiro diferente al de depósito</b>: por política anti-lavado, el retiro debe ir al mismo método usado para depositar<br/>• <b>Superaste el límite diario/mensual</b>: verifica los límites en Mi Cuenta<br/>• <b>Cancelación manual</b>: si tú mismo cancelaste el retiro desde Mi Cuenta → Mis Retiros<br/><br/>Los fondos de un retiro cancelado son devueltos automáticamente a tu saldo. Contacta soporte si necesitas más información.'))

    # GAP 5
    story.append(sub('2.5  Cuenta bloqueada y no puedo retirar'))
    story.append(Paragraph('<font color="#f54943"><b>PRIORIDAD ALTA</b></font> — Preguntado 1 vez', styles['Body']))
    story.append(quote('Quiero retirar pero me dice que mi cuenta está bloqueada'))
    story.append(body('<b>Respuesta sugerida:</b>'))
    story.append(rec('Si tu cuenta está bloqueada, puede deberse a:<br/>• <b>Verificación de seguridad</b>: actividad sospechosa detectada — contacta soporte para desbloquear<br/>• <b>Autoexclusión activa</b>: si activaste la autoexclusión, la cuenta permanecerá bloqueada durante el periodo seleccionado<br/>• <b>Múltiples cuentas</b>: si se detectaron cuentas duplicadas, una puede ser bloqueada<br/>• <b>KYC pendiente</b>: documentos de verificación requeridos<br/><br/>Contacta soporte en ayuda@beton.win con tu ID de jugador para resolver el bloqueo.'))

    # GAP 6
    story.append(sub('2.6  Verificar estado del depósito'))
    story.append(Paragraph('<font color="#ffc572"><b>PRIORIDAD MEDIA</b></font> — Preguntado 1 vez', styles['Body']))
    story.append(quote('¿Puedes ver si mi depósito ya fue aprobado?'))
    story.append(body('<b>Respuesta sugerida:</b>'))
    story.append(rec('Puedes verificar el estado de tu depósito en <b>Mi Cuenta → Historial de Transacciones</b>. Los estados posibles son:<br/>• <b>Completado</b>: fondos acreditados en tu saldo<br/>• <b>Pendiente</b>: en proceso (espera según el método de pago)<br/>• <b>Rechazado</b>: la transacción fue rechazada por el proveedor de pago<br/><br/>Si después de 30 minutos tu depósito no aparece, envía el comprobante de pago a ayuda@beton.win.'))

    # GAP 7
    story.append(sub('2.7  Reabrir una cuenta cerrada'))
    story.append(Paragraph('<font color="#ffc572"><b>PRIORIDAD MEDIA</b></font> — Preguntado 1 vez', styles['Body']))
    story.append(quote('Mi cuenta está cerrada y quiero reabrirla. ¿Me puedes ayudar?'))
    story.append(body('<b>Respuesta sugerida:</b>'))
    story.append(rec('Si tu cuenta fue cerrada y deseas reabrirla:<br/>• <b>Cierre voluntario (no por juego responsable)</b>: contacta soporte en ayuda@beton.win solicitando la reapertura. Se verificará tu identidad antes de proceder.<br/>• <b>Cierre por autoexclusión</b>: la cuenta NO puede reabrirse durante el periodo de exclusión seleccionado. Esto es por tu protección y cumplimiento normativo.<br/>• <b>Cierre por múltiples cuentas</b>: contacta soporte para evaluar tu caso.<br/><br/>Ten en cuenta que una cuenta reabierta puede requerir nueva verificación KYC.'))

    story.append(PageBreak())

    # GAP 8
    story.append(sub('2.8  Eliminar datos personales (GDPR)'))
    story.append(Paragraph('<font color="#ffc572"><b>PRIORIDAD MEDIA</b></font> — Preguntado 1 vez', styles['Body']))
    story.append(quote('No quiero cerrar mi cuenta, quiero eliminar la información de mi cuenta'))
    story.append(body('<b>Respuesta sugerida:</b>'))
    story.append(rec('Por regulaciones de anti-lavado de dinero y licencia de juego, estamos obligados a conservar ciertos datos de tu cuenta durante un periodo mínimo (generalmente 5-10 años tras el cierre).<br/><br/>Sin embargo, puedes solicitar:<br/>• <b>Eliminación de datos de marketing</b>: dejar de recibir comunicaciones promocionales<br/>• <b>Anonimización parcial</b>: ocultar datos no requeridos por regulación<br/><br/>Para solicitar la eliminación de datos, envía un email a ayuda@beton.win con el asunto "Solicitud de eliminación de datos" incluyendo tu ID de jugador.'))

    # GAP 9
    story.append(sub('2.9  Cambiar fecha de nacimiento'))
    story.append(Paragraph('<font color="#ffc572"><b>PRIORIDAD MEDIA</b></font> — Preguntado 1 vez', styles['Body']))
    story.append(quote('Quiero cambiar mi fecha de nacimiento'))
    story.append(body('<b>Respuesta sugerida:</b>'))
    story.append(rec('La fecha de nacimiento <b>no puede modificarse</b> una vez registrada, ya que se utiliza para verificar tu edad y cumplir con las regulaciones de juego.<br/><br/>Si cometiste un error al registrarte, contacta soporte en ayuda@beton.win con:<br/>• Tu ID de jugador<br/>• Una foto de tu documento de identidad que muestre la fecha de nacimiento correcta<br/><br/>El equipo verificará y corregirá la información si corresponde.'))

    # GAP 10-13
    story.append(sub('2.10  Otros temas (Prioridad Baja)'))

    gaps_low = [
        ['Tema', 'Pregunta del usuario', 'Respuesta sugerida'],
        ['Compartir dispositivo', '¿Puedo compartir dispositivo con otra persona?', 'Sí, puedes usar el mismo dispositivo, pero cada persona debe tener su propia cuenta. Compartir cuentas está prohibido por las políticas de seguridad.'],
        ['Partido no encontrado', 'Quiero apostar a un partido pero no lo encuentro', 'No todos los eventos están disponibles. Usa la barra de búsqueda o revisa las categorías por deporte. Algunos eventos se agregan poco antes del inicio.'],
        ['Colaborar con el casino', 'Quiero colaborar con el casino', 'Para consultas de afiliación o partnerships comerciales, contacta el equipo de negocios en partners@beton.win.'],
        ['País incorrecto (AR/CL)', 'Soy de Argentina pero mi perfil es de Chile', 'Para corregir el país de tu cuenta, contacta soporte en ayuda@beton.win con tu documento de identidad que acredite tu nacionalidad.'],
    ]
    t = Table(gaps_low, colWidths=[30*mm, 55*mm, 75*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t)

    story.append(PageBreak())

    # ==================== 3. SECCIONES EXISTENTES ====================
    story.append(section('3. Secciones Existentes en la FAQ'))
    story.append(body('La FAQ actual contiene <b>14 secciones</b> con 338 líneas de contenido:'))

    existing = [
        ['Sección', 'Estado', 'Notas'],
        ['Depósitos', '✅ Completa', 'Falta: proceso paso a paso'],
        ['Retiros', '⚠️ Parcial', 'Falta: razones de cancelación'],
        ['Bonos y Promociones', '✅ Completa', '—'],
        ['Programa de Fidelidad', '✅ Completa', '—'],
        ['Verificación KYC', '✅ Completa', '—'],
        ['Verificación de Teléfono', '✅ Completa', '—'],
        ['Cuenta y Acceso', '⚠️ Parcial', 'Falta: reapertura, GDPR, cambio fecha nacimiento'],
        ['Problemas Técnicos', '✅ Completa', '—'],
        ['Apuestas Deportivas', '⚠️ Parcial', 'Falta: partido no encontrado'],
        ['App Móvil', '✅ Completa', '—'],
        ['Casino', '✅ Completa', 'Falta: "juegos manipulados" (RNG/RTP)'],
        ['Saldo y Balance', '⚠️ Parcial', 'Falta: dónde ver el saldo'],
        ['Juego Responsable', '✅ Completa', '—'],
        ['Soporte', '✅ Completa', '—'],
    ]
    t = Table(existing, colWidths=[45*mm, 25*mm, 80*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#dee2e6')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t)

    # ==================== 4. PRÓXIMOS PASOS ====================
    story.append(section('4. Próximos Pasos'))
    story.append(bullet('<b>Paso 1:</b> Agregar las 9 respuestas de prioridad ALTA y MEDIA a la FAQ de Google Sheets'))
    story.append(bullet('<b>Paso 2:</b> Agregar las 4 respuestas de prioridad BAJA'))
    story.append(bullet('<b>Paso 3:</b> Verificar que el motor de búsqueda KB (Apps Script) encuentra las nuevas entradas'))
    story.append(bullet('<b>Paso 4:</b> Re-testear las mismas preguntas de los usuarios y verificar que ahora reciben contexto KB'))
    story.append(bullet('<b>Paso 5:</b> Monitorear el KB hit rate en la siguiente semana — objetivo: pasar de 18% a 60%+'))

    story.append(Spacer(1, 10*mm))
    story.append(hr())
    story.append(Paragraph('BetonWin AI Support — Informe de Brechas KB v1.0 — Abril 2026', styles['Footer']))

    doc.build(story)
    print(f'PDF generado: {OUTPUT}')

if __name__ == '__main__':
    build()
