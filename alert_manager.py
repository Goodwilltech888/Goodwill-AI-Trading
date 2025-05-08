from bot.alert_manager import AlertManager

alert = AlertManager()
alert.send_telegram(f"🚨 {symbol} BUY signal at {price}")