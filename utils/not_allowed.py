def not_allowed(bot, event):
    bot.send_text(chat_id=event.from_chat,
                  text="❌ У вас нет доступа к этой функции.",
                  )