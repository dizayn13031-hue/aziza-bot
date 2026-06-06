import os
import logging
import requests
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
SELECTING_PROJECT, ENTERING_PHONE, ENTERING_SABAB = range(3)
APPS_SCRIPT_URL = os.environ.get("APPS_SCRIPT_URL", "https://script.google.com/macros/s/AKfycbycF4YeHSWFQoMuVagO2UBDFPpcEwjX50c_r8bheY702tYJFQTMdRCUvZQIQ_HyJovC_g/exec")
PROJECTS = ["Hofmann uz","Hofmann Jomiy","Hofmann Parkent","Hofmann Next","Hofmann Qo'yliq","Jomiy Outlet","Qo'yliq Outlet","SMEG","Joseph Joseph"]
SABAB_LIST = [["SOTUV","KOTARMADI"],["QAYTA ALOQA","VILOYAT"],["MALUMOT BERILDI","TELEGRAMDAN YOZILDI"],["SIFATSIZ","DOKONGA BORADI"],["BOSHQA FILIALGA BORADI","O'YLAB KO'RADI"],["Boshqa sabab"]]
MONTHS = {"January":"Yanvar","February":"Fevral","March":"Mart","April":"Aprel","May":"May","June":"Iyun","July":"Iyul","August":"Avgust","September":"Sentabr","October":"Oktabr","November":"Noyabr","December":"Dekabr"}

def save(l,s,n,t,sb):
    try:
            r=requests.post(APPS_SCRIPT_URL,json={"loyiha":l,"sana":s,"num":n,"telefon":t,"sabab":sb},timeout=15)
                    return r.json().get("status")=="ok"
                        except Exception as e:
                                logger.error(e);return False

                                def today():
                                    now=datetime.now();return f"{now.day}-{MONTHS[now.strftime('%B')]}"

                                    def mkb():return ReplyKeyboardMarkup([["Yangi yozuv"]],resize_keyboard=True)

                                    def pkb():
                                        rows=[[PROJECTS[i],PROJECTS[i+1]] if i+1<len(PROJECTS) else [PROJECTS[i]] for i in range(0,len(PROJECTS),2)]
                                            rows.append(["Bekor"]);return ReplyKeyboardMarkup(rows,resize_keyboard=True)

                                            async def start(u,c):await u.message.reply_text("Salom Aziza! Yangi malumot kiritish uchun tugmani bosing.",reply_markup=mkb())

                                            async def new_entry(u,c):
                                                await u.message.reply_text("Loyihani tanlang:",reply_markup=pkb());return SELECTING_PROJECT

                                                async def sel_proj(u,c):
                                                    t=u.message.text
                                                        if t=="Bekor":return await cancel(u,c)
                                                            if t not in PROJECTS:await u.message.reply_text("Tanlang:",reply_markup=pkb());return SELECTING_PROJECT
                                                                c.user_data["p"]=t;await u.message.reply_text(f"Loyiha:{t}\nTelefon:",reply_markup=ReplyKeyboardRemove());return ENTERING_PHONE

                                                                async def enter_phone(u,c):
                                                                    c.user_data["ph"]=u.message.text.strip()
                                                                        await u.message.reply_text("Sabab:",reply_markup=ReplyKeyboardMarkup(SABAB_LIST,resize_keyboard=True));return ENTERING_SABAB

                                                                        async def enter_sabab(u,c):
                                                                            sb=u.message.text.strip()
                                                                                if sb=="Boshqa sabab":await u.message.reply_text("Yozing:",reply_markup=ReplyKeyboardRemove());return ENTERING_SABAB
                                                                                    p,ph,d=c.user_data["p"],c.user_data["ph"],today()
                                                                                        cnt=c.user_data.get("cnt",{});key=f"{p}_{d}";num=cnt.get(key,0)+1;cnt[key]=num;c.user_data["cnt"]=cnt
                                                                                            ok=save(p,d,num,ph,sb)
                                                                                                await u.message.reply_text(f"Saqlandi!\n{p}\n{d}\n{ph}\n{sb}" if ok else "Xatolik.",reply_markup=mkb())
                                                                                                    return ConversationHandler.END
                                                                                                    
                                                                                                    async def cancel(u,c):await u.message.reply_text("Bekor.",reply_markup=mkb());return ConversationHandler.END
                                                                                                    
                                                                                                    def main():
                                                                                                        app=Application.builder().token(os.environ.get("BOT_TOKEN","8860968654:AAFvSnewn17ygVwdAviMOnX6I739yPo83PI")).build()
                                                                                                            conv=ConversationHandler(
                                                                                                                    entry_points=[CommandHandler("start",new_entry),MessageHandler(filters.Regex("^Yangi yozuv$"),new_entry)],
                                                                                                                            states={SELECTING_PROJECT:[MessageHandler(filters.TEXT&~filters.COMMAND,sel_proj)],ENTERING_PHONE:[MessageHandler(filters.TEXT&~filters.COMMAND,enter_phone)],ENTERING_SABAB:[MessageHandler(filters.TEXT&~filters.COMMAND,enter_sabab)]},
                                                                                                                                    fallbacks=[CommandHandler("cancel",cancel),MessageHandler(filters.Regex("^Bekor$"),cancel)])
                                                                                                                                        app.add_handler(CommandHandler("start",start));app.add_handler(conv)
                                                                                                                                            app.run_polling(drop_pending_updates=True)
                                                                                                                                            
                                                                                                                                            if __name__=="__main__":main()
