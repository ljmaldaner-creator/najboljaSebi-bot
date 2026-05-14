import json
import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = os.environ.get("TOKEN")

ZADACI = [
    "Dan 1 - Inventar umora\n\nZapisi tri stvari koje radis 'na misice' jer mislis da niko drugi nece.",
    "Dan 2 - Detektor 'Moras'\n\nKoliko puta si danas izgovorila 'moram', a koliko 'zelim'?",
    "Dan 3 - Tisina koja vristi\n\nSedi 5 minuta u tisini. Koja je prva neprijatna misao koja ispliva?",
    "Dan 4 - Fizicki odjek\n\nGde u telu osecas tezinu dok razmisljas o sutrasnjem radnom danu?",
    "Dan 5 - Kradljivci vremena\n\nKome si danas poklonila sat vremena svog zivota, a da to nije bila ti?",
    "Dan 6 - Ogledalo neiskrenosti\n\nGde si danas rekla 'da', a celo bice ti je govorilo 'ne'?",
    "Dan 7 - Cena stagnacije\n\nIzracunaj koliko te je (emotivno i energetski) kostalo to sto si i ove nedelje ostala na istom mestu.",
    "Dan 8 - Glas Dobro vaspitane devojcice\n\nCiju kritiku cujes u glavi kada pomislis da odmori?",
    "Dan 9 - Zabrana na uspeh\n\nSta je najgore sto bi se desilo da zaista postanem previse uspesna?",
    "Dan 10 - Nevidljivi lojaliteti\n\nKoga iz svoje porodice bi izdala ako bi postala istinski srecna i slobodna?",
    "Dan 11 - Iluzija kontrole\n\nSta se plasas da ce se raspasti ako ti prestanes da drzis sve konce?",
    "Dan 12 - Skriptna ponavljanja\n\nKoja se to neprijatna situacija u tvom zivotu stalno ponavlja sa razlicitim ljudima?",
    "Dan 13 - Strah od autenticnosti\n\nKoju masku najcesce noris da bi bila prihvacena u drustvu ili na poslu?",
    "Dan 14 - Saboter zadovoljstva\n\nZasto odmah nakon lepog trenutka trazis problem kojim ces se opteretiti?",
    "Dan 15 - Presek\n\nPogledaj zadatke od prethodnih 14 dana. Vidis li obrazac koji te drzi zarobljenom?",
    "Dan 16 - Autoritativna Ja\n\nZamisli sebe kako donosis tesku odluku bez ijednog grama krivice. Kakav je to osecaj?",
    "Dan 17 - Ekonomija energije\n\nKako bi trosila svoju snagu da ne moras nikome da se pravdas?",
    "Dan 18 - Kulturni kapital\n\nSta bi sve mogla da postignesh da tvoja unutrasnja vrednost nije vezana za to koliko si korisna drugima?",
    "Dan 19 - Miris slobode\n\nOpisi miris, ukus i osecaj jutra u kojem se budis kao zena koja je poslozena.",
    "Dan 20 - Intuicija kao kompas\n\nPrati jedan impuls danas koji nema veze sa logikom. Gde te vodi?",
    "Dan 21 - Arhetip pobednice\n\nKoja zena (iz istorije ili fikcije) otelovljuje tvoju potisnutu moc?",
    "Dan 22 - Granice kao ljubav\n\nZamisli da kazes 'ne' bez objasnjenja. Koliko prostora se time oslobadja?",
    "Dan 23 - Ostrvo je blizu\n\nShvatas li da zena sa ostrva nije druga osoba, vec ti bez tvojih kocnica?",
    "Dan 24 - Jaz\n\nKoliko je realno velika razdaljina izmedju tebe danas i tebe na ostrvu? Samo iskreno.",
    "Dan 25 - Analiza pokusaja\n\nNavedi sve sto si probala (knjige, podkasti, saveti) a sto nije dalo trajni rezultat jer je bilo spolja.",
    "Dan 26 - Duboki uzrok\n\nDa li si spremna da prestanes da lecis simptome i udjes u srz svog skripta?",
    "Dan 27 - Investicija u identitet\n\nSta je vrednije od tvoje buduce verzije koja vise ne trosi zivot na prezivljavanje?",
    "Dan 28 - Poslednji otpor\n\nKoji ti razlog tvoj mozak nudi da ne krenes sada? Prepoznaj ga kao poslednji trzaj starog sistema.",
    "Dan 29 - Svedocanstvo promene\n\nZamisli da za 6 meseci pises poruku o tome kako si se promenila. Sta u njoj pise?",
    "Dan 30 - Vrata su otvorena\n\nPut od 30 dana je bio samo uvid. Transformacija pocinje unutar NajboljaSEBI. Da li ulazis?",
]


def ucitaj_podatke():
    if os.path.exists("podaci.json"):
        with open("podaci.json") as f:
            return json.load(f)
    return {"korisnici": [], "dan": 1}


def sacuvaj_podatke(data):
    with open("podaci.json", "w") as f:
        json.dump(data, f)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = ucitaj_podatke()
    chat_id = update.effective_chat.id
    if chat_id not in data["korisnici"]:
        data["korisnici"].append(chat_id)
        sacuvaj_podatke(data)
        await update.message.reply_text(
            "Dobrodosla u 30-dnevni izazov!\n\nSvako jutro u 7:30 dobijas novi zadatak.\n\nPripremi se - pocinjemo sutra."
        )
    else:
        await update.message.reply_text("Vec si prijavljena! Zadaci stizu svako jutro u 7:30.")


async def danas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = ucitaj_podatke()
    dan = data["dan"]
    if dan < 1 or dan > 30:
        await update.message.reply_text("Izazov jos nije poceo ili je zavrsen.")
        return
    await update.message.reply_text(ZADACI[dan - 1])


async def slanje_zadatka(app):
    data = ucitaj_podatke()
    dan = data["dan"]
    if dan > 30:
        return
    zadatak = ZADACI[dan - 1]
    for chat_id in data["korisnici"]:
        try:
            await app.bot.send_message(chat_id=chat_id, text=zadatak)
        except Exception as e:
            print(f"Greska za {chat_id}: {e}")
    data["dan"] += 1
    sacuvaj_podatke(data)
    print(f"Poslat Dan {dan} za {len(data['korisnici'])} korisnica.")


async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("danas", danas))

    scheduler = AsyncIOScheduler(timezone="Europe/Belgrade")
    scheduler.add_job(slanje_zadatka, "cron", hour=7, minute=30, args=[app])
    scheduler.start()

    print("Bot je upaljen!")
    async with app:
        await app.start()
        await app.updater.start_polling()
        await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
