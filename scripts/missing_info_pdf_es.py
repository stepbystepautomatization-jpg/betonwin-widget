#!/usr/bin/env python3
"""
BetonWin — Información Faltante para el Equipo de CS (PDF en Español)
55 preguntas nuevas NO incluidas en domande_senza_risposta.md
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, cm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)

# ── Colors ──
DARK   = colors.HexColor('#1a1a2e')
GREEN  = colors.HexColor('#16a34a')
RED    = colors.HexColor('#dc2626')
AMBER  = colors.HexColor('#d97706')
BLUE   = colors.HexColor('#2563eb')
GRAY   = colors.HexColor('#6b7280')
LGRAY  = colors.HexColor('#f3f4f6')
LGREEN = colors.HexColor('#dcfce7')
LBLUE  = colors.HexColor('#dbeafe')
WHITE  = colors.white

styles = getSampleStyleSheet()
styles.add(ParagraphStyle('Title2', parent=styles['Title'], fontSize=20, textColor=DARK, spaceAfter=4))
styles.add(ParagraphStyle('Sub', parent=styles['Normal'], fontSize=12, textColor=BLUE, spaceAfter=2))
styles.add(ParagraphStyle('H1X', parent=styles['Heading1'], fontSize=15, textColor=DARK, spaceBefore=12, spaceAfter=4))
styles.add(ParagraphStyle('H2X', parent=styles['Heading2'], fontSize=12, textColor=BLUE, spaceBefore=8, spaceAfter=3))
styles.add(ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, leading=12, textColor=DARK, alignment=TA_JUSTIFY))
styles.add(ParagraphStyle('Small', parent=styles['Normal'], fontSize=7.5, leading=9.5, textColor=GRAY))
styles.add(ParagraphStyle('SmallI', parent=styles['Normal'], fontSize=7.5, leading=9.5, textColor=GRAY, fontName='Helvetica-Oblique'))
styles.add(ParagraphStyle('BulletX', parent=styles['Normal'], fontSize=9, leading=12, leftIndent=14, bulletIndent=4))
styles.add(ParagraphStyle('CellBody', parent=styles['Normal'], fontSize=7.5, leading=9.5, textColor=DARK))
styles.add(ParagraphStyle('CellQ', parent=styles['Normal'], fontSize=7.5, leading=9.5, textColor=DARK, fontName='Helvetica-Bold'))
styles.add(ParagraphStyle('CellWhy', parent=styles['Normal'], fontSize=7, leading=8.5, textColor=GRAY, fontName='Helvetica-Oblique'))
styles.add(ParagraphStyle('CellAns', parent=styles['Normal'], fontSize=7.5, leading=9.5, textColor=RED))

def hr():
    return HRFlowable(width='100%', thickness=0.5, color=GRAY, spaceBefore=4, spaceAfter=4)

def spacer(h=3):
    return Spacer(1, h * mm)

def section_header(letter, title, impact, color=BLUE):
    data = [[Paragraph(f'<b>SECCION {letter} — {title}</b>',
             ParagraphStyle('sh', fontSize=10, textColor=WHITE, fontName='Helvetica-Bold')),
             Paragraph(f'<b>{impact}</b>',
             ParagraphStyle('sh2', fontSize=8, textColor=WHITE, alignment=TA_CENTER))]]
    t = Table(data, colWidths=['70%', '30%'])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    return t

def q_table(questions, W):
    header = [
        Paragraph('<b>#</b>', styles['CellBody']),
        Paragraph('<b>Pregunta para el equipo CS</b>', styles['CellBody']),
        Paragraph('<b>Por que lo necesitamos</b>', styles['CellBody']),
        Paragraph('<b>Respuesta<br/>(completar)</b>', styles['CellAns']),
    ]
    rows = [header]
    for qid, question, why in questions:
        rows.append([
            Paragraph(qid, styles['CellBody']),
            Paragraph(question, styles['CellQ']),
            Paragraph(why, styles['CellWhy']),
            Paragraph('', styles['CellBody']),
        ])
    t = Table(rows, colWidths=[W*0.05, W*0.38, W*0.32, W*0.25], repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTSIZE', (0,0), (-1,-1), 7.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#d1d5db')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LGRAY]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('BACKGROUND', (3,1), (3,-1), colors.HexColor('#fff7ed')),
    ]))
    return t

SECTIONS = [
    {
        'letter': 'A',
        'title': 'Saludos y Primer Contacto',
        'impact': '8.949 tickets (24,9%) — ~1.119/mes',
        'color': GREEN,
        'intro': 'Son usuarios que abren el chat con solo "hola" o "buenas" sin hacer ninguna pregunta. La IA ya maneja el 95% de estos, pero necesitamos mejorar el 5% restante y reducir los chats abandonados.',
        'note': None,
        'questions': [
            ('A.1', 'Cuando un usuario envia solo un saludo ("hola", "buenas"), cual es la respuesta ideal? El bot deberia listar las categorias principales de ayuda o hacer una pregunta abierta como "Como puedo ayudarte?"',
             'Actualmente el bot saluda y pregunta "como puedo ayudarte?" — pero el 15% de los usuarios no hace ninguna pregunta despues. Necesitamos una respuesta mas proactiva que los guie.'),
            ('A.2', 'El bot deberia enviar un menu de acciones rapidas con botones (ej: "Deposito", "Retiro", "Bono", "KYC", "Otro") despues de un saludo, o solo texto?',
             '8.949 tickets son solo saludos. Los botones de accion rapida podrian redirigir al 70%+ de estos al flujo correcto sin esperar que el usuario escriba un segundo mensaje.'),
            ('A.3', 'Si un usuario envia solo un saludo y luego queda en silencio (sin segundo mensaje por 2+ minutos), que deberia hacer el bot? Enviar un seguimiento? Cerrar el chat? Despues de cuantos minutos?',
             '~10% de los tickets de saludo terminan con el usuario abandonando el chat. Los agentes actualmente pierden tiempo esperando.'),
            ('A.4', 'Que idiomas debe soportar la respuesta de saludo? Actualmente tenemos ES/EN/IT/PT. Hay otros idiomas en los que los usuarios escriben? (ej: aleman, frances para mercados europeos)',
             'Algunos usuarios escriben saludos en idiomas inesperados. Necesitamos saber si debemos agregar mas.'),
        ]
    },
    {
        'letter': 'B',
        'title': 'Transferencia Bancaria: Detalles Operativos',
        'impact': '4.407 tickets (12,3%) — ~551/mes — SUBIENDO +271%',
        'color': RED,
        'intro': 'Los tickets de transferencia bancaria explotaron de 296/mes (Jul 2025) a 1.100/mes (Dic 2025). Estas preguntas cubren patrones operativos NO incluidos en "domande_senza_risposta.md" (que ya cubre datos bancarios, formato de comprobante y tiempos de procesamiento).',
        'note': 'Las preguntas sobre datos bancarios, requisitos del comprobante y tiempos de procesamiento ya estan en "domande_senza_risposta.md" Seccion 1 (P1.1–1.10). Estas preguntas son DIFERENTES.',
        'questions': [
            ('B.1', 'Los tickets de transferencia bancaria explotaron +271% en 6 meses. Hubo un cambio de proveedor de pagos, una promocion que impulsa las transferencias, o se lanzo un nuevo mercado? Necesitamos entender la causa raiz.',
             'Si sabemos POR QUE aumentaron las transferencias, podemos abordar proactivamente la causa (ej: si se agrego Directa24, necesitamos instrucciones especificas de Directa24 en el KB).'),
            ('B.2', 'Cuando un usuario envia una imagen del comprobante en el chat, cual es el flujo de trabajo EXACTO del agente? Revision manual? Sistema automatizado? Describa el proceso paso a paso despues de recibir un comprobante.',
             'Estamos construyendo un flujo automatizado de verificacion de comprobantes en el widget. Necesitamos conocer el proceso manual actual para replicarlo correctamente.'),
            ('B.3', 'Cuales son las 5 razones mas comunes por las que un deposito por transferencia bancaria NO se acredita incluso despues de enviar un comprobante valido?',
             'Ticket real: "Son 4 recargas de 5000 peso. Necesito una respuesta" — Multiples transferencias atoradas. Necesitamos explicar por que.'),
            ('B.4', 'Existe un numero maximo de transferencias bancarias pendientes por usuario? Un usuario puede tener 3-4 transferencias sin procesar al mismo tiempo?',
             'Los usuarios hacen multiples transferencias pequenas en vez de una grande, creando multiples tickets de soporte cada vez.'),
            ('B.5', 'Que pasa si un usuario hace una transferencia bancaria pero olvida incluir el codigo de referencia? El deposito puede ser emparejado? Como?',
             'Muchos tickets muestran transferencias sin referencia. El KB no explica que hacer en este caso.'),
            ('B.6', 'Chile especifico: La "Cuenta RUT" de Banco Estado funciona tanto para depositos COMO para retiros? Varios usuarios reportan que no aparece como opcion para retiros.',
             'Ticket real: "Consulta para retirar — no sale la opcion de banco estado, cuenta rut" — Problema recurrente sin respuesta en el KB.'),
        ]
    },
    {
        'letter': 'C',
        'title': 'Verificacion de Telefono y Correo',
        'impact': '2.096 tickets (67,5% de KYC) — ~262/mes',
        'color': RED,
        'intro': 'El 67,5% de los tickets de KYC son en realidad sobre verificacion de telefono/correo — un problema completamente diferente a la carga de documentos. Este es el problema #1 de KYC.',
        'note': '"domande_senza_risposta.md" Seccion 4 cubre KYC de documentos (carga de ID, calidad de foto, comprobante de domicilio). La verificacion de telefono/correo NO esta cubierta ahi.',
        'questions': [
            ('C.1', 'Paso a paso: como verifica un usuario su numero de telefono? Ruta exacta: Mi Cuenta > Configuracion > ...? Que pasa despues de hacer clic en "Verificar"? Codigo SMS? De cuantos digitos?',
             'Ticket real: "En las misiones me pide confirmar telefono y correo pero no se como hacerlo" — Los usuarios no conocen la ruta exacta.'),
            ('C.2', 'El codigo de verificacion SMS no llega. Cuales son las razones mas comunes? (Formato de numero incorrecto? Operador bloqueando? Falta codigo de pais?) Que debe intentar el usuario?',
             'Este es el problema #1 de KYC. Ticket real: "No puedo verificar mi numero de telefono. Cada vez que lo subo me arroja error"'),
            ('C.3', 'Si un usuario ingreso el numero de telefono EQUIVOCADO durante el registro, puede cambiarlo el mismo? O debe contactar soporte? Que verificacion requiere soporte?',
             'Ticket real: "Escribi mal mi numero de celular y no se como corregirlo" — Extremadamente comun. Los agentes dicen "dime tu numero y lo corrijo" pero el bot no puede hacer eso.'),
            ('C.4', 'Lo mismo para correo electronico: si el usuario ingreso el email equivocado (ej: ".com" en vez de ".cl"), puede cambiarlo el mismo? Cual es el proceso exacto?',
             'Ticket real: "Me equivoque y puse .com y termina en .cl, entonces no puedo verificarlo" — Error muy frecuente.'),
            ('C.5', 'Que formato de numero de telefono se requiere? Debe incluir codigo de pais (+56 Chile, +54 Argentina)? Con o sin cero inicial? Proporcione un ejemplo para cada pais.',
             'Los usuarios ingresan numeros en diferentes formatos y obtienen errores. Necesitamos el formato exacto para que el bot pueda validar antes del envio.'),
            ('C.6', 'Verificacion de email: que recibe el usuario? Un enlace? Un codigo? Cuanto tiempo es valido? Que pasa si va a spam? Se puede reenviar?',
             'Ticket real: "No puedo confirmar mi correo. Lo pongo y me dice que van a mandar un mensaje" — Los usuarios no saben que esperar.'),
            ('C.7', 'La verificacion de telefono + email es obligatoria para TODOS los usuarios, o solo para ciertas acciones? (Antes del primer retiro? Para el programa Hero/Fidelidad? Para depositos mayores a X monto?)',
             'Algunos usuarios estan bloqueados para jugar, otros juegan sin verificacion. Necesitamos aclarar exactamente cuando es obligatoria.'),
            ('C.8', 'La "pregunta secreta" — que es? Cuando se configura? Que pasa si el usuario no recuerda la respuesta? Como verifica soporte la identidad sin ella?',
             'Ticket real: "No recuerdo la respuesta a mi pregunta secreta" — Los agentes verifican con foto de documento. El bot necesita explicar este proceso.'),
        ]
    },
    {
        'letter': 'D',
        'title': '"Saldo 0.00" con Bono Activo (Analisis Profundo)',
        'impact': '~400/mes — Punto #1 de confusion',
        'color': AMBER,
        'intro': 'Este es el problema MAS CONFUSO para los usuarios. Aparece en tickets de Bonos, Casino y Saldo. Los usuarios depositan dinero, ven un saldo, pero cuando intentan jugar o retirar muestra "0.00". Piensan que fueron estafados.',
        'note': '"domande_senza_risposta.md" P5.1 pregunta esto brevemente. Necesitamos una explicacion MUCHO mas detallada con ejemplos numericos concretos.',
        'questions': [
            ('D.1', 'Explique en terminos simples: por que aparece "Saldo 0.00" cuando el usuario tiene un bono deportivo activo? Ejemplo paso a paso con numeros reales.',
             'Ticket real: "Cargue 50mil y me sale que no tengo saldo" — Usuario deposito $50.000 CLP, recibio un bono, pero no puede jugar. Causa frustracion extrema y acusaciones de fraude.'),
            ('D.2', 'Ejemplo concreto: Usuario deposita $10.000 CLP, recibe bono de bienvenida 150% ($15.000). Total muestra $25.000. Intenta apostar en deportes y aparece "Saldo 0.00". POR QUE? Que debe hacer?',
             'Necesitamos un ejemplo tan claro que cualquiera pueda entenderlo. La explicacion actual del KB es demasiado tecnica.'),
            ('D.3', '"Saldo 0.00" tambien pasa con bonos de casino, o solo con bonos deportivos? Si un usuario tiene un bono de casino, puede jugar slots normalmente?',
             'Vemos este problema tanto en deportes como en casino. Necesitamos aclarar la diferencia.'),
            ('D.4', 'Si el usuario NO quiere el bono, como lo elimina ANTES de usarlo? Paso a paso: Mi Cuenta > Promociones > Cancelar Bono? Perdera su deposito?',
             'Ticket real: "Hola quiero renunciar al bono de bienvenida. Ya deposite" — 248 tickets sobre cancelacion de bono.'),
            ('D.5', 'Despues de cancelar un bono, el dinero real (deposito original) queda disponible inmediatamente? O hay un periodo de espera?',
             'Los usuarios cancelan el bono esperando acceso instantaneo a su dinero. Funciona asi?'),
        ]
    },
    {
        'letter': 'E',
        'title': 'Ganancias de Casino No Acreditadas',
        'impact': '3.022 tickets (52,5% de Casino) — ~378/mes',
        'color': AMBER,
        'intro': 'Mas de la mitad de todos los tickets de Casino son sobre usuarios que ganaron pero el dinero no aparecio o no pueden retirar sus ganancias. Esto es diferente a la resolucion de problemas de juegos (cubierto en domande_senza_risposta.md Seccion 6).',
        'note': '"domande_senza_risposta.md" Seccion 6 cubre carga de juegos, disputas, desconexion. Estas preguntas son sobre GANANCIAS que no aparecen.',
        'questions': [
            ('E.1', 'Cuando un usuario gana en una slot o juego de casino, que tan rapido deben aparecer las ganancias en su saldo? Instantaneamente? Al terminar la ronda? Despues de un retraso de procesamiento?',
             'Ticket real: "Gane 74.000 y no lo puedo retirar" — El usuario dice que gano pero el saldo no lo refleja.'),
            ('E.2', 'Si un usuario gana pero no puede retirar por un bono activo, cual es el monto maximo que puede retirar? Explique el "Limite de Liberacion" (Release Limit) con un ejemplo real en moneda local.',
             'Ticket real: "No puedo retirar mi saldo. Gaste mi credito pero mi ganancia no la puedo retirar" — El Release Limit es extremadamente confuso.'),
            ('E.3', 'Si un juego se congela/crashea a mitad de giro o ronda, que pasa con la apuesta? El resultado se determina del lado del servidor? El usuario vera el resultado cuando vuelva a abrir el juego?',
             'Ticket real: "Compre un bono de giros y aun me sale recopilando datos. Hace horas" — Usuario atrapado en un juego sin resolver.'),
            ('E.4', 'Ganancias de jackpot — hay un proceso diferente para ganancias grandes? Requieren verificacion adicional? Hay un pago maximo?',
             'Los usuarios que ganan montos grandes enfrentan retrasos inesperados. Necesitamos explicar por que proactivamente.'),
            ('E.5', 'Si un usuario cree que el resultado de su juego fue injusto, cual es el proceso oficial de investigacion? Quien lo revisa? Cuanto tiempo toma? Que evidencia necesitan?',
             'Ticket real: "Me siento estafado" — Necesitamos una respuesta profesional y transparente con info de certificacion RNG.'),
        ]
    },
    {
        'letter': 'F',
        'title': 'Retiro Bloqueado por Bono',
        'impact': '401 tickets (46,5% de retiros) — ~50/mes',
        'color': AMBER,
        'intro': 'Este unico problema genera la MITAD de todas las quejas de retiro. Los usuarios intentan retirar, quedan bloqueados por un bono activo, y no entienden por que ni que hacer.',
        'note': '"domande_senza_risposta.md" P8.1 menciona esto brevemente. Necesitamos el flujo COMPLETO del usuario con descripciones exactas de pantalla.',
        'questions': [
            ('F.1', 'Cuando un usuario intenta retirar con un bono activo, que mensaje de error EXACTO ve? Proporcione el texto exacto que aparece en pantalla.',
             'Los usuarios envian capturas de pantalla de mensajes de error. Necesitamos reconocer y explicar cada uno.'),
            ('F.2', 'Paso a paso: como puede un usuario verificar su progreso actual de rollover/apuesta? Ruta exacta: Mi Cuenta > Promociones > ...? Que muestra la barra de progreso?',
             'Ticket real: "No entiendo que mas tengo que apostar en los bonos" — Los usuarios no saben donde mirar.'),
            ('F.3', 'Si el usuario decide cancelar el bono para retirar, cual es el proceso EXACTO? Pantalla por pantalla: donde hacer clic, que confirmacion aparece, que pasa con el saldo.',
             'Ticket real: "Quiero renunciar al bono y retirar el dinero" — Si el bot puede guiar esto, ahorramos ~200 tickets/mes.'),
            ('F.4', 'Despues de completar el requisito de apuesta (wagering), el retiro se desbloquea automaticamente? O el usuario necesita hacer algo adicional?',
             'Algunos usuarios completan el wagering pero aun no pueden retirar. Hay un paso adicional?'),
            ('F.5', '"Saldo disponible" vs "Saldo total" vs "Saldo de bono" — proporcione las definiciones exactas y donde aparece cada uno en la plataforma.',
             'Ticket real: "Deposite, aparece en pesos, pero al tratar de jugar aparece saldo 0 y al retirar lo mismo" — Tres conceptos de saldo confunden a los usuarios constantemente.'),
        ]
    },
    {
        'letter': 'G',
        'title': 'Cierre de Cuenta y Autoexclusion',
        'impact': '~62 tickets/mes — ALTA sensibilidad (compliance)',
        'color': BLUE,
        'intro': 'Las solicitudes de cierre de cuenta y autoexclusion son sensibles — involucran cumplimiento de juego responsable. El bot actualmente no puede manejar ninguna de estas.',
        'note': 'No cubierto en "domande_senza_risposta.md" en absoluto.',
        'questions': [
            ('G.1', 'Cual es el proceso exacto para cerrar una cuenta? El usuario debe tener saldo cero? Cuanto tiempo toma? Es reversible?',
             'Ticket real: "Quiero darme de baja. No pienso jugar mas" — Varios usuarios solicitan esto diariamente.'),
            ('G.2', 'Cual es la diferencia entre "cierre de cuenta" y "autoexclusion"? Diferentes duraciones? Diferente reversibilidad?',
             'Ticket real: "TENGO UNA QUEJA POR QUE NO CERRARON MI CUENTA" — El usuario pidio cierre pero la cuenta seguia activa. Problema critico de compliance.'),
            ('G.3', 'Opciones de autoexclusion: que periodos de tiempo estan disponibles? (24h, 1 semana, 1 mes, 6 meses, permanente?) El usuario puede elegir?',
             'Necesitamos opciones especificas para listar en la respuesta del bot.'),
            ('G.4', 'Si un usuario solicita cierre de cuenta, que pasa con su saldo restante? Debe retirar primero? Que pasa con los bonos pendientes?',
             'Los usuarios quieren irse pero tienen dinero en la cuenta.'),
            ('G.5', 'Despues de que expira la autoexclusion, la cuenta se reabre automaticamente? O el usuario debe contactar soporte para reactivar?',
             'Importante para usuarios que establecen autoexclusion temporal.'),
            ('G.6', 'Hay una linea de ayuda o organizacion de juego responsable que el bot deberia recomendar? (Organizaciones locales en Chile, Argentina)',
             'Por compliance, el bot deberia ofrecer proactivamente esta informacion cuando los usuarios mencionan problemas con el juego.'),
        ]
    },
    {
        'letter': 'H',
        'title': 'Programa de Fidelidad / Hero / Misiones',
        'impact': 'Creciendo — parte de tickets de Bono',
        'color': BLUE,
        'intro': 'El KB menciona el programa de fidelidad pero los usuarios tienen preguntas muy especificas sobre niveles, recompensas y misiones diarias que no podemos responder.',
        'note': 'No cubierto en "domande_senza_risposta.md".',
        'questions': [
            ('H.1', 'Cuantos niveles tiene el programa Hero/Fidelidad? Cuales son los nombres de los niveles? Cuanto debe apostar un usuario (en CLP/ARS) para alcanzar cada nivel?',
             'Los usuarios preguntan "como subo de nivel?" — necesitamos los umbrales especificos.'),
            ('H.2', 'Que recompensas desbloquea cada nivel? (% de cashback, cantidad de giros gratis, valor de apuesta gratis, % de bono de deposito). Idealmente una tabla por nivel.',
             'Los usuarios quieren saber que obtendran en el siguiente nivel.'),
            ('H.3', 'Misiones Diarias: que tipos de misiones existen? (ej: "hacer 5 apuestas", "depositar $X", "jugar juego Y") Son iguales para todos o personalizadas?',
             'Ticket real: "En las misiones me pide confirmar telefono" — Algunas misiones tienen prerrequisitos que los usuarios no entienden.'),
            ('H.4', '"Usuario activo" = 14 dias sin apostar = perdida de beneficios. El usuario pierde su NIVEL o solo los beneficios actuales? Cuando vuelve a apostar, reinicia desde nivel 1?',
             'Los usuarios que pausan el juego estan preocupados por perder todo su progreso.'),
            ('H.5', 'Bono de cumpleanos: es automatico o el usuario debe reclamarlo? Cuales son los requisitos? (Debe ser activo, haber depositado recientemente, etc.)',
             'Los usuarios esperan un bono en su cumpleanos y no reciben nada. Necesitamos explicar las condiciones claramente.'),
        ]
    },
    {
        'letter': 'I',
        'title': 'Apuestas Deportivas Especificas',
        'impact': '~200/mes — parte de Casino/Juegos',
        'color': BLUE,
        'intro': 'El KB tiene informacion basica de deportes pero los usuarios tienen preguntas operativas sobre liquidacion de apuestas, Cash Out y apuestas anuladas.',
        'note': 'No cubierto en "domande_senza_risposta.md".',
        'questions': [
            ('I.1', 'Que tan rapido se liquidan las apuestas deportivas despues de que termina un evento? (Minutos? Horas? Depende del deporte? De la liga?)',
             'Los usuarios ganan apuestas pero no ven el pago inmediatamente y piensan que algo esta mal.'),
            ('I.2', 'Un usuario puede cancelar o editar una apuesta colocada? Antes de que comience el evento? Despues de que comience?',
             'Los usuarios a veces colocan apuestas por error.'),
            ('I.3', 'Cash Out: esta disponible para todas las apuestas o solo para algunas? Que determina si se ofrece Cash Out? Puede ser parcial?',
             'Los usuarios ven Cash Out en algunas apuestas pero no en otras. No hay explicacion disponible.'),
            ('I.4', '"Mi apuesta ganadora fue anulada" — cuales son las razones por las que una apuesta ganadora puede ser cancelada? (Evento cancelado, error de cuota, actividad sospechosa?)',
             'Los usuarios se enojan mucho cuando esto pasa. Necesitamos una explicacion clara y justa.'),
            ('I.5', 'Para apuestas combinadas (parlay): si una seleccion se cancela, que pasa con el resto? Se recalcula o se anula toda?',
             'Los usuarios con apuestas de multiples selecciones frecuentemente enfrentan esta confusion sin respuesta disponible.'),
        ]
    },
    {
        'letter': 'J',
        'title': 'Problemas Especificos de la Plataforma (Nuevos patrones Ene-Feb 2026)',
        'impact': '~150/mes — Patrones NUEVOS',
        'color': GRAY,
        'intro': 'Estos son problemas nuevos que surgieron o crecieron significativamente en los datos de Ene-Feb 2026, particularmente relacionados con el registro y la visualizacion de moneda.',
        'note': 'No cubierto en "domande_senza_risposta.md".',
        'questions': [
            ('J.1', 'Chile: "Numero de contribuyente" / "RUT" — durante el registro, que deben ingresar los usuarios en el campo "numero de documento"? Su RUT? Con o sin digito verificador? Con puntos y guion? Ejemplo.',
             'Ticket real: "Cual es el numero de contribuyente para depositar?" y "Lo pongo y dice que no es valido" — Bloqueo de registro para usuarios chilenos.'),
            ('J.2', 'Argentina: "DNI" o "CUIL" — cual ingresan los usuarios argentinos? Que formato? Cuantos digitos?',
             'Mismo bloqueo de registro para usuarios argentinos.'),
            ('J.3', 'La plataforma muestra montos en EUR/USD pero el usuario deposito en CLP/ARS. Como se muestra la conversion? Donde pueden ver el tipo de cambio utilizado?',
             'Ticket real: "Dice que esta en ingles. Yo no te entiendo" — Usuarios confundidos por la visualizacion de moneda.'),
            ('J.4', 'Un usuario puede cambiar su idioma de visualizacion despues del registro? Donde en la configuracion? Cambia tanto la interfaz COMO el idioma de soporte?',
             'Algunos usuarios se registraron en el idioma equivocado y no pueden navegar el sitio.'),
            ('J.5', 'Error "Datos no validos" durante el registro — que significa EXACTAMENTE? Liste las causas mas comunes: formato de nombre? Caracteres especiales? Email duplicado? Edad?',
             'Ticket real: "Estoy escribiendo mis datos y sale que no son validos y son mis datos" — Bloqueo de registro. Muchos usuarios no pueden crear una cuenta.'),
            ('J.6', 'Hay una edad minima para registrarse? Como se verifica? Que pasa si un menor de edad logra registrarse?',
             'Pregunta de compliance — el bot necesita mencionar los requisitos de edad claramente.'),
        ]
    },
]

def build():
    path = '/Users/serhiykorenyev/Desktop/vs code/widget cs /BetonWin_Info_Faltante_Para_CS_ES.pdf'
    doc = SimpleDocTemplate(path, pagesize=A4,
        topMargin=1.4*cm, bottomMargin=1.4*cm, leftMargin=1.4*cm, rightMargin=1.4*cm)
    story = []
    W = A4[0] - 2.8*cm

    # ── COVER ──
    story.append(Spacer(1, 30*mm))
    story.append(Paragraph('BetonWin — Informacion Faltante', styles['Title2']))
    story.append(Paragraph('Solicitud para el Equipo de Soporte al Cliente', styles['Sub']))
    story.append(hr())
    story.append(spacer(4))
    story.append(Paragraph(
        'Este documento contiene <b>55 preguntas</b> que nuestro widget de IA <b>no puede responder hoy</b>. '
        'Necesitamos que el equipo de CS proporcione las respuestas correctas para agregarlas a la '
        'Knowledge Base y automatizar estas respuestas.',
        styles['Body']))
    story.append(spacer(4))
    story.append(Paragraph(
        '<b>IMPORTANTE:</b> Este documento NO repite las 64 preguntas ya enviadas en '
        '"domande_senza_risposta.md". Estas son brechas de informacion <b>ADICIONALES</b> descubiertas '
        'despues de expandir nuestro analisis de 26.963 a <b>35.963 tickets</b> (agregando datos Ene-Feb 2026).',
        styles['Body']))
    story.append(spacer(6))

    info = [
        ['Fuente de datos', '35.963 tickets de Zendesk (Jul 2025 – Feb 2026)'],
        ['Preguntas nuevas', '55 (ademas de las 64 ya enviadas)'],
        ['Total preguntas', '119 combinadas en ambos documentos'],
        ['Idioma', 'Espanol — responda en espanol o ingles'],
        ['Generado', 'Marzo 2026'],
    ]
    t = Table(info, colWidths=[W*0.25, W*0.75])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), LBLUE),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#d1d5db')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(spacer(8))

    story.append(Paragraph('<b>Como completar este documento:</b>', styles['Body']))
    instructions = [
        'Lea cada pregunta en la columna <b>"Pregunta para el equipo CS"</b>',
        'Lea <b>"Por que lo necesitamos"</b> para entender el problema real del cliente',
        'Escriba la respuesta correcta en la columna <b>"Respuesta"</b> (fondo naranja)',
        'Si la respuesta depende del pais, especifique: "Chile: X, Argentina: Y"',
        'Si no esta seguro, escriba <b>"POR VERIFICAR — preguntar a [persona/equipo]"</b>',
        'Si no aplica, escriba <b>"N/A"</b> y la razon',
    ]
    for i, inst in enumerate(instructions, 1):
        story.append(Paragraph(f'{i}. {inst}', styles['BulletX']))
    story.append(spacer(6))

    story.append(Paragraph('<b>Resumen de secciones:</b>', styles['Body']))
    summary = [['Seccion', 'Tema', 'Preguntas', 'Prioridad', 'Tickets/mes']]
    priorities = ['ALTA','CRITICA','CRITICA','ALTA','ALTA','ALTA','MEDIA','MEDIA','MEDIA','BAJA']
    tickets_mo = ['1.119','551','262','400','378','50','62','—','200','150']
    for i, s in enumerate(SECTIONS):
        summary.append([f'Seccion {s["letter"]}', s['title'], str(len(s['questions'])), priorities[i], tickets_mo[i]])
    summary.append(['', 'TOTAL', '55', '', '~3.172'])
    st = Table(summary, colWidths=[W*0.12, W*0.35, W*0.10, W*0.12, W*0.15], repeatRows=1)
    st.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#d1d5db')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LGRAY]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('BACKGROUND', (0,-1), (-1,-1), LGREEN),
    ]))
    story.append(st)
    story.append(PageBreak())

    # ── SECTIONS ──
    for sec in SECTIONS:
        story.append(section_header(sec['letter'], sec['title'], sec['impact'], sec['color']))
        story.append(spacer(3))
        story.append(Paragraph(sec['intro'], styles['Body']))
        if sec['note']:
            story.append(spacer(2))
            story.append(Paragraph(f'<b>Nota:</b> {sec["note"]}', styles['SmallI']))
        story.append(spacer(4))
        story.append(q_table(sec['questions'], W))
        story.append(spacer(6))
        story.append(hr())
        if sec['letter'] in ('B', 'D', 'F', 'H'):
            story.append(PageBreak())

    # ── CLOSING ──
    story.append(PageBreak())
    story.append(Paragraph('Resumen y Proximos Pasos', styles['H1X']))
    story.append(hr())
    story.append(Paragraph(
        'Una vez que se proporcionen las 55 respuestas, combinadas con las 64 respuestas de '
        '"domande_senza_risposta.md", tendremos <b>119 respuestas completas</b> que cubren '
        'virtualmente todos los problemas de clientes vistos en 35.963 tickets.',
        styles['Body']))
    story.append(spacer(4))
    story.append(Paragraph('<b>Impacto esperado despues de actualizar el KB:</b>', styles['Body']))
    impact_data = [
        ['Metrica', 'Actual', 'Despues de actualizar'],
        ['Cobertura de IA por ticket', '~47%', '~73%'],
        ['Tickets manejados por IA/mes', '~2.112', '~3.280'],
        ['Tickets adicionales automatizados', '—', '~1.168/mes'],
        ['Ahorro en costos ($3–5/ticket)', '—', '$3.504–$5.840/mes'],
        ['Tiempo de agente liberado', '—', '~584 horas/mes'],
    ]
    it = Table(impact_data, colWidths=[W*0.40, W*0.20, W*0.25], repeatRows=1)
    it.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.4, colors.HexColor('#d1d5db')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LGRAY]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('FONTNAME', (2,1), (2,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (2,1), (2,-1), GREEN),
    ]))
    story.append(it)
    story.append(spacer(8))

    story.append(Paragraph('<b>Orden de prioridad para responder:</b>', styles['Body']))
    story.append(Paragraph('1. <b>Secciones B + C</b> (Transferencia Bancaria + Verificacion Telefono) — CRITICA, mayor volumen', styles['BulletX']))
    story.append(Paragraph('2. <b>Secciones D + E + F</b> (Saldo 0.00 + Ganancias + Retiro) — ALTA, mayor frustracion', styles['BulletX']))
    story.append(Paragraph('3. <b>Secciones A + G</b> (Saludos + Cierre de Cuenta) — MEDIA, operativo + compliance', styles['BulletX']))
    story.append(Paragraph('4. <b>Secciones H + I + J</b> (Fidelidad + Deportes + Plataforma) — BAJA, pero creciendo', styles['BulletX']))

    story.append(spacer(10))
    story.append(hr())
    story.append(Paragraph(
        '<i>Generado: Marzo 2026 | Datos: 35.963 tickets de Zendesk (Jul 2025 – Feb 2026) | '
        'Complementa: domande_senza_risposta.md (64 preguntas)</i>',
        styles['Small']))

    doc.build(story)
    print(f'PDF generado: {path}')

if __name__ == '__main__':
    build()
