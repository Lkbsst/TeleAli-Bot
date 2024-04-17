from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram import Update
import pandas as pd
import emoji
import time

TOKEN = 'TOKEN AQUI'        # Adicionar Seu Token do BOT Aqui
GRUPO_ID = -IDGROUP         # Adicionar o ID do grupo Aqui
XLS_PATH = 'PATH'           # Adicionar o Caminho do Arquivo .xls baixado no ALI
DELAY_BETWEEN_SHARES = 300  # Delay de 60 segundos (1 minuto)

emoji_hand = '👉'    # Alteravel
emoji_money = '💰'   # Alteravel
emoji_eye = '👁️'     # Alteravel

def start(update: Update, context: CallbackContext) -> None:
    if update.message:
        update.message.reply_text('Olá! Eu sou um bot para compartilhar links do AliExpress. Envie-me o comando /share para compartilhar os produtos.')

def load_products_from_xls():
    try:
        df = pd.read_excel(XLS_PATH)
        products = df.to_dict(orient='records')
        return products
    except Exception as e:
        print(f"Erro ao obter a lista de produtos do XLS: {e}")
        return []

def share_products(update: Update, context: CallbackContext) -> None:
    products = load_products_from_xls()

    if not products:
        mensagem = "Não há produtos para compartilhar."
        context.bot.send_message(chat_id=update.message.chat_id, text=mensagem)
        print(f'Mensagem enviada para o grupo: {mensagem}')
        return

    for product in products:
        print(product)  # Verifique se os dados estão sendo lidos corretamente

        # Construa a mensagem com emojis
        mensagem = f'👉 Produto: {product.get("Product Desc", "N/A")}\n\n' \
                   f'💰 Preço Original: {product.get("Origin Price", "N/A")}\n' \
                   f'📉 Preço Desconto: {product.get("Discount Price", "N/A")}\n' \
                   f'🔗 Link do Produto: {product.get("Promotion Url", "N/A")}\n\n' \
                   f'Telegram de Ofertas:\n' \
                   f'https://t.me/LinkdoGrupo\n' #mudar o LinkdoGrupo para o seu grupo

        # Adiciona a imagem ao envio
        if product.get("Image Url"):
            context.bot.send_photo(chat_id=GRUPO_ID, photo=product.get("Image Url"), caption=emoji.emojize(mensagem))
        else:
            context.bot.send_message(chat_id=GRUPO_ID, text=emoji.emojize(mensagem))

        print(f'Mensagem enviada para o grupo: {mensagem}')
        
        # Aguarde o intervalo definido antes de compartilhar o próximo produto
        time.sleep(DELAY_BETWEEN_SHARES)

def main() -> None:
    if TOKEN is None:
        raise ValueError("O token do bot não foi fornecido. Certifique-se de substituir 'SEU_TOKEN' pelo token real do seu bot.")

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Adicione os manipuladores de comandos
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("share", share_products))

    # Inicie o bot
    updater.start_polling()

    # Mantenha o bot em execução
    updater.idle()

if __name__ == '__main__':
    main()
