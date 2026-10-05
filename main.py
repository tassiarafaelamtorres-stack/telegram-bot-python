import os
import re
import telebot

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Contas ficam separadas por grupo
contas = {}

def dinheiro(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "💰 Bot de Contas da Casa funcionando!\n\n"
        "Para adicionar uma conta, mande assim:\n"
        "Luz 250\n"
        "Internet 119,90\n"
        "Escola 800\n\n"
        "Comandos:\n"
        "/total - mostra o total\n"
        "/lista - mostra todas as contas\n"
        "/limpar - apaga a lista"
    )

@bot.message_handler(commands=["total"])
def total(message):
    chat_id = message.chat.id
    lista = contas.get(chat_id, [])
    soma = sum(valor for _, valor in lista)

    bot.reply_to(
        message,
        f"💰 Total das contas: {dinheiro(soma)}"
    )

@bot.message_handler(commands=["lista"])
def lista(message):
    chat_id = message.chat.id
    itens = contas.get(chat_id, [])

    if not itens:
        bot.reply_to(message, "📭 Nenhuma conta cadastrada.")
        return

    texto = "📋 CONTAS DA CASA\n\n"

    for i, (nome, valor) in enumerate(itens, 1):
        texto += f"{i}. {nome}: {dinheiro(valor)}\n"

    soma = sum(valor for _, valor in itens)
    texto += f"\n💰 TOTAL: {dinheiro(soma)}"

    bot.reply_to(message, texto)

@bot.message_handler(commands=["limpar"])
def limpar(message):
    contas[message.chat.id] = []
    bot.reply_to(message, "🗑️ Lista de contas apagada.")

@bot.message_handler(func=lambda message: True, content_types=["text"])
def adicionar(message):
    texto = message.text.strip()

    resultado = re.match(r"^(.+?)\s+R?\$?\s*(\d+(?:[.,]\d{1,2})?)$", texto)

    if not resultado:
        bot.reply_to(
            message,
            "Não consegui entender. 😅\n"
            "Envie assim:\n\n"
            "Luz 250\n"
            "ou\n"
            "Internet 119,90"
        )
        return

    nome = resultado.group(1).strip()
    valor = float(resultado.group(2).replace(",", "."))

    chat_id = message.chat.id

    if chat_id not in contas:
        contas[chat_id] = []

    contas[chat_id].append((nome, valor))

    soma = sum(v for _, v in contas[chat_id])

    bot.reply_to(
        message,
        f"✅ {nome}: {dinheiro(valor)} adicionada.\n"
        f"💰 Total acumulado: {dinheiro(soma)}"
    )

print("Bot iniciado!")
bot.infinity_polling(skip_pending=True)
