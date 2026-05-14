import json
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = os.environ.get("TOKEN")

ZADACI = [
    "🌀 Dan 1 — Inventar umora\n\nZapiši tri stvari koje radiš 'na mišiće' jer misliš da niko drugi neće.",
    "🌀 Dan 2 — Detektor 'Moraš'\n\nKoliko puta si danas izgovorila 'moram', a koliko 'želim'?",
    "🌀 Dan 3 — Tišina koja vrišti\n\nSedi 5 minuta u tišini. Koja je prva neprijatna misao koja ispliva?",
    "🌀 Dan 4 — Fizički odjek\n\nGde u telu osećaš težinu dok razmišljaš o sutrašnjem radnom danu?",
    "🌀 Dan 5 — Kradljivci vremena\n\nKome si danas poklonila sat vremena svog života, a da to nije bila ti?",
    "🌀 Dan 6 — Ogledalo neiskrenosti\n\nGde si danas rekla 'da', a celo biće ti je govorilo 'ne'?",
    "🌀 Dan 7 — Cena stagnacije\n\nIzračunaj koliko te je (emotivno i energetski) koštalo to što si i ove nedelje ostala na istom mestu.",
    "🌀 Dan 8 — Glas 'Dobro vaspitane devojčice'\n\nČiju kritiku čuješ u glavi kada pomisliš da odmoriš?",
    "🌀 Dan 9 — Zabrana na uspeh\n\nŠta je najgore što bi se desilo da zaista postaneš 'previše' uspešna?",
    "🌀 Dan 10 — Nevidljivi lojaliteti\n\nKoga iz svoje porodice bi 'izdala' ako bi postala istinski srećna i slobodna?",
    "🌀 Dan 11 — Iluzija kontrole\n\nŠta se plašiš da će se raspasti ako ti prestaneš da držiš sve konce?",
    "🌀 Dan 12 — Skriptna ponavljanja\n\nKoja se to neprijatna situacija u tvom životu stalno ponavlja sa različitim ljudima?",
    "🌀 Dan 13 — Strah od autentičnosti\n\nKoju masku najčešće nosiš da bi bila prihvaćena u društvu ili na poslu?",
    "🌀 Dan 14 — Saboter zadovoljstva\n\nZašto odmah nakon lepog trenutka tražiš problem kojim ćeš se opteretiti?",
    "🌀 Dan 15 — Presek\n\nPogledaj zadatke od prethodnih 14 dana. Vidiš li obrazac koji te drži zarobljenom?",
    "🌀 Dan 16 — Autoritativna Ja\n\nZamisli sebe kako donosiš tešku odluku bez ijednog grama krivice. Kakav je to osećaj?",
    "🌀 Dan 17 — Ekonomija energije\n\nKako bi trošila svoju snagu da ne moraš nikome da se pravdaš?",
    "🌀 Dan 18 — Kulturni kapital\n\nŠta bi sve mogla da postigneš da tvoja unutrašnja vrednost nije vezana za to koliko si korisna drugima?",
    "🌀 Dan 19 — Miris slobode\n\nOpiši miris, ukus i osećaj jutra u kojem se budiš kao žena koja je 'posložena'.",
    "🌀 Dan 20 — Intuicija kao kompas\n\nPrati jedan impuls danas koji nema veze sa logikom. Gde te vodi?",
    "🌀 Dan 21 — Arhetip pobednice\n\nKoja žena (iz istorije ili fikcije) otelovljuje tvoju potisnutu moć?",
    "🌀 Dan 22 — Granice kao ljubav\n\nZamisli da kažeš 'ne' bez objašnjenja. Koliko prostora se time oslobađa?",
    "🌀 Dan 23 — Ostrvo je blizu\n\nShvataš li da žena sa ostrva nije druga osoba, već ti bez tvojih kočnica?",
    "🌀 Dan 24 — Jaz\n\nKoliko je realno velika razdaljina između tebe danas i tebe na ostrvu? (Samo iskreno.)",
    "🌀 Dan 25 — Analiza pokušaja\n\nNavedi sve što si probala (knjige, podkasti, saveti) a što nije dalo trajni rezultat jer je bilo 'spolja'.",
    "🌀 Dan 26 — Duboki uzrok\n\nDa li si spremna da prestaneš da lečiš simptome i uđeš u srž svog skripta?",
    "🌀 Dan 27 — Investicija u identitet\n\nŠta je vrednije od tvoje buduće verzije koja više ne troši život na preživljavanje?",
    "🌀 Dan 28 — Poslednji otpor\n\nKoji ti razlog tvoj mozak nudi da ne kreneš sada? Prepoznaj ga kao poslednji trzaj starog sistema.",
    "🌀 Dan 29 — Svedočanstvo promene\n\nZamisli da za 6 meseci pišeš poruku o tome kako si se promenila. Šta u njoj piše?",
    "🌀 Dan 30 — Vrata su otvorena\n\nPut od 30 dana je bio samo uvid. Transformacija počinje unutar NajboljaSEBI. Da li ulaziš?",
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
            "Dobrodošla u 30-dnevni izazov! 🌿\n\n"
            "Svako jutro u 7:30 dobijaš novi zadatak koji te vodi dublje u sebe.\n\n"
            "Pripremi se — počinjemo sutra. 💛"
        )
    else:
        await update.message.reply_text(
            "Već si prijavljena! 💪\nZadaci stižu svako jutro u 7:30."
        )


async def danas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = ucitaj_podatke()
    dan = data["dan"]
    if dan < 1 or dan > 30:
        await update.message.reply_text("Izazov još nije počeo ili je završen.")
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
            print(f"Greška za {chat_id}: {e}")

    data["dan"] += 1
    sacuvaj_podatke(data)
    print(f"Poslat Dan {dan} za {len(data['korisnici'])} korisnica.")


def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("danas", danas))

    scheduler = AsyncIOScheduler(timezone="Europe/Belgrade")
    scheduler.add_job(
        slanje_zadatka,
        "cron",
        hour=7,
        minute=30,
        args=[app]
    )
    scheduler.start()

    print("Bot je upaljen! ✅")
    app.run_polling()


if __name__ == "__main__":
    main()
