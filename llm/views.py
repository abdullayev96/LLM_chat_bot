from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY
import os
from openai import OpenAI


def gym_chat_page(request):
    return render(request, "chat.html")


SYSTEM_PROMPT = """
👋 Assalamu alaykum! Men — Logical Team Group’ning virtual yordamchisiman.  

Biz — biznesingiz uchun zamonaviy texnologik va marketing yechimlar markazimiz.  
Sizga quyidagi yo‘nalishlarda yordam bera olaman:

- 🌐 Veb-sayt va landing page yaratish  
- 🤖 Telegram bot ishlab chiqish  
- 🎯 Target reklama va SMM xizmatlari  
- 🔰 CRM tizimi va avtomatlashtirish  
- 🎨 Grafik dizayn va brending  
- 📱 Mobil ilovalar ishlab chiqish  
- ⚛️ Sun’iy intellekt asosidagi yechimlar  
- 📢 DMM (Dublyaj Media Marketing)

❓ Menga istalgan paytda **veb-sayt**, **bot**, **reklama**, **CRM**, **dizayn**, **narx**, yoki **aloqa** kabi kalit so‘zlar bilan yozishingiz mumkin.  

Men sizga tez, aniq va foydali javob berishga harakat qilaman. 🚀
"""


# SYSTEM_PROMPT = """
# 👋 Assalamu alaykum! Men — Logical Team Group’ning virtual yordamchisiman.
# Sizga quyidagi savollarda yordam bera olaman:
# - 📋 Abonement narxlari va chegirmalar
# - 🏋️‍♂️ Xizmatlar va mavjud jihozlar
# - 👨‍🏫 Murabbiylar va mashg‘ulot jadvali
# - 🕒 Ish vaqti va band qilish
# - 📍 Manzil va kontakt ma’lumotlar
# - 🧒 Bolalar mashg‘ulotlari
# - 💳 To‘lov usullari
# - 🏊 Sauna, hovuz va VIP xizmatlar
#
# ❓ Siz menga istalgan payt **abonement**, **murabbiy**, **manzil**, **xizmat**, **chegirma** yoki boshqa kalit so‘zlar bilan so‘rashingiz mumkin.
#
# Men sizga tez va aniq javob berishga harakat qilaman. 🙂
# """


class GymLLMView(APIView):
    def post(self, request):
        user_message = request.data.get("message", "").lower()

        if not user_message.strip():
            return Response(
                {"reply": "🙂 Savolingizni yozing, yordam berishga tayyorman!"},
                status=status.HTTP_200_OK,
            )

        if any(word in user_message for word in ["xizmat", "service", "nimalar", "nimani qilasiz", "nimalar qilasiz"]):
            reply = (
                "💼 Logical Team Group quyidagi xizmatlarni taklif etadi:\n"
                "- 🎯 Target reklama\n"
                "- 🌐 Veb-sayt va landing page yaratish\n"
                "- 🤖 Telegram bot ishlab chiqish\n"
                "- 🔰 CRM tizimi integratsiyasi\n"
                "- 🎨 Grafik va brending dizayn\n"
                "- 📱 Mobil ilovalar yaratish\n"
                "- 🗣 SMM xizmatlari\n"
                "- ⚛️ Sun’iy intellekt asosidagi yechimlar\n"
                "- 📢 DMM (Dublyaj Media Marketing)\n\n"
                "❓ Qaysi xizmat sizni qiziqtiryapti?"
            )


        elif any(word in user_message for word in [
            "loyiha", "loyihalar", "portfolio", "namuna", "ishlagan", "project", "examples", "botlar", "saytlar"
        ]):
            reply = (
                "🧩 Logical Team Group tomonidan amalga oshirilgan loyihalar:\n\n"
                "🌐 **Veb-saytlar va Crm Tizmlar:**\n"
                "- mockmaga.uz\n"
                "- al-tsuull.uz\n"
                "- venompro.de\n"
                "- tedboard.uz\n"
                "- ansorsafety.uz\n"
                "- breez.uz\n"
                "- alpertungatour.uz\n\n"
                "🤖 **Telegram botlar:**\n"
                "- [@Turonbank_Mahalla_bankiri_bot](https://t.me/Turonbank_Mahalla_bankiri_bot)\n"
                "- [@Bobo_Motors_Service_bot](https://t.me/Bobo_Motors_Service_bot)\n"
                "- [@turonbank_baholash_bot](https://t.me/turonbank_baholash_bot)\n\n"
                "💼 Bu loyihalar orqali bizning tajribamizni va sifat darajamizni ko‘rishingiz mumkin.\n"
                "Siz ham o‘zingizga o‘xshash loyiha xohlaysizmi? 😉"
            )

        elif any(word in user_message for word in ["narx", "price", "pul", "xizmat narxi", "qancha", "chegirma"]):
            reply = (
                "💰 Narxlar loyiha murakkabligiga qarab belgilanadi.\n\n"
                "Masalan:\n"
                "- Telegram bot: 800 000 so‘mdan\n"
                "- Veb-sayt: 3 000 000 so‘mdan\n"
                "- Target reklama: 1 000 000 so‘mdan\n"
                "- CRM tizimi: 8 000 000 so‘mdan\n\n"
                "🎯 Sizning loyihangizni qisqacha yozing — biz aniq narxni aytamiz."
            )

        elif any(word in user_message for word in ["kim", "siz kimsiz", "who are you", "sen kimsan"]):
            reply = (
                "👋 Men Logical Team Group virtual yordamchisiman.\n"
                "Biz sizning biznesingiz uchun zamonaviy texnologik yechimlar yaratamiz — "
                "veb-sayt, bot, SMM, reklama, dizayn va boshqa xizmatlar.\n\n"
                "Sizga qaysi yo‘nalish bo‘yicha yordam kerak?"
            )

        elif any(word in user_message for word in ["vaqt", "hours", "ish vaqti", "qachon ochiq", "ishlaysizmi"]):
            reply = (
                "🕒 Logical Team Group ish vaqti:\n"
                "Dushanba–Shanba: 09:00 – 19:00\n"
                "Yakshanba: dam kuni\n\n"
                "❓ Qaysi kuni siz bilan bog‘lanishimiz qulay bo‘ladi?"
            )

        elif any(word in user_message for word in
                 ["salom", "hi", "hello", "assalom", "qanday narsa bu", "vazifasi nima"]):
            reply = (
                "👋 Assalamu alaykum! Men — Logical Team Group’ning virtual yordamchisiman.\n\n"
                "Biznesingiz uchun quyidagi sohalarda yordam bera olamiz:\n"
                "- 🌐 Veb-sayt va Telegram bot yaratish\n"
                "- 🎯 Target reklama va SMM xizmatlari\n"
                "- 🔰 CRM tizimi va avtomatlashtirish\n"
                "- 🎨 Dizayn, brending va DMM xizmatlari\n\n"
                "❓ Siz qaysi xizmat haqida bilmoqchisiz? Masalan, yozing: *veb-sayt*, *bot*, *reklama* yoki *narx*"
            )

        elif any(word in user_message for word in ["manzil", "qayerda", "address", "location", "adres"]):
            reply = (
                "📍 Logical Team Group manzili:\n"
                "Toshkent shahri, Chilonzor tumani, PowerFit Plaza 2-qavat.\n\n"
                "💬 Shuningdek, biz bilan masofadan ham ishlash mumkin — butun O‘zbekiston bo‘ylab!"
            )

        elif any(word in user_message for word in
                 ["kontakt", "telefon", "raqam", "aloqa", "phone", "bog'lanish", "telegram", "instagram"]):
            reply = (
                "📞 Biz bilan bog‘lanish uchun:\n"
                "Telegram: @Baymax9663\n"
                "Telefon: +998 90 586 22 36\n"
                "Instagram: @logical_teams\n\n"
                "📬 Har qanday loyiha yoki savolingizni shu raqamlarga yuborishingiz mumkin."
            )

        elif any(word in user_message for word in ["dizayn", "grafik", "logo", "brend"]):
            reply = (
                "🎨 Grafik dizayn xizmati:\n"
                "- Logo va brending\n"
                "- Banner, post va reklama dizaynlari\n"
                "- UI/UX (sayt va ilova interfeyslari)\n\n"
                "Sizga kerakli dizayn turini yozing — biz namunalar bilan tanishtiramiz."
            )

        elif any(word in user_message for word in ["bot", "telegram", "avtomatlashtirish"]):
            reply = (
                "🤖 Telegram bot xizmati:\n"
                "- Savdo va buyurtma botlari\n"
                "- To‘lov tizimlari integratsiyasi (Payme, Click, Payze)\n"
                "- Statistika va CRM bilan bog‘lanish\n"
                "- Chatbotlar (AI asosida)\n\n"
                "Sizga qaysi turdagi bot kerak — savdo, xizmat yoki avtomatlashtirish uchunmi?"
            )

        elif any(word in user_message for word in ["crm", "tizim", "mijozlar", "baza"]):
            reply = (
                "🔰 CRM tizim xizmati:\n"
                "- Mijozlar bazasini yuritish\n"
                "- Avtomatik bildirishnomalar\n"
                "- Hisobot va statistika\n"
                "- Telegram yoki veb-sayt bilan integratsiya\n\n"
                "❓ Sizda hozirda qanday tizim mavjud yoki yangisini yaratmoqchimisiz?"
            )

        elif any(word in user_message for word in
                 ["smm", "target", "reklama", "instagram reklama", "facebook reklama"]):
            reply = (
                "📢 SMM va Target reklama xizmati:\n"
                "- Instagram, Facebook va TikTok reklamalari\n"
                "- Auditoriya tahlili va strategiya\n"
                "- Kontent reja va dizayn\n"
                "- Reklama kampaniyalarini boshqarish\n\n"
                "Sizda hozirda sahifa bormi yoki biz yarataylikmi?"
            )

        elif any(word in user_message for word in ["mobil", "ilova", "app", "android", "ios"]):
            reply = (
                "📱 Mobil ilova ishlab chiqish xizmati:\n"
                "- Android va iOS uchun ilovalar\n"
                "- Django REST yoki Node.js bilan backend\n"
                "- Dizayn va UX optimizatsiyasi\n\n"
                "❓ Sizga qaysi turdagi ilova kerak — biznes, savdo yoki xizmat uchun?"
            )

        elif any(word in user_message for word in ["vip", "premium", "maxsus", "exclusive"]):
            reply = (
                "🌟 VIP paketlar:\n"
                "- Shaxsiy loyiha menejeri\n"
                "- To‘liq dizayn, sayt va bot birlashtirilgan yechim\n"
                "- AI va CRM integratsiyasi\n"
                "- Reklama + SMM strategiyasi\n\n"
                "👉 VIP paketlar yirik bizneslar uchun mo‘ljallangan. Qiziqyapsizmi?"
            )

        else:
            reply = (
                "👋 Assalamu alaykum! Men — Logical Team Group’ning virtual yordamchisiman.\n\n"
                "Biz taqdim etamiz:\n"
                "🎯 Target reklama\n"
                "🌐 Veb-saytlar\n"
                "🤖 Telegram botlar\n"
                "🔰 CRM tizimlari\n"
                "🎨 Dizayn va brending\n"
                "📱 Mobil ilovalar\n"
                "🗣 SMM xizmatlari\n"
                "⚛️ AI yechimlari\n"
                "📢 DMM (Dublyaj Media Marketing)\n\n"
                "Nega aynan biz?\n"
                "✅ Tajribali va kreativ jamoa\n"
                "✅ Tezkor, sifatli va professional xizmat\n"
                "✅ Har bir loyiha — biz uchun alohida e’tibor!\n\n"
                "Bog‘lanish uchun:\n"
                "Telegram: @Baymax9663\n"
                "Telefon: +998 90 586 22 36\n\n"
                "Logical Team Group — G‘oya sizdan, texnik yechim bizdan! 🚀"
            )

        # --- Javoblar ---
        # if any(word in user_message for word in ["abonement", "narx", "price", "pul"]):
        #     reply = (
        #         "📋 Bizning abonement rejalari:\n"
        #         "- 1 oy: $50\n"
        #         "- 3 oy: $120\n"
        #         "- 6 oy: $200\n"
        #         "- 12 oy: $350\n\n"
        #         "👉 Qaysi reja sizga mos kelishini aytsangiz, resepsiyada band qilib beramiz."
        #     )
        #
        # elif any(word in user_message for word in ["xizmat", "service", "nimalar"]):
        #     reply = (
        #         "💪 Biz quyidagi xizmatlarni taklif qilamiz:\n"
        #         "- Trenajyor zali va jihozlardan foydalanish\n"
        #         "- Guruh mashg‘ulotlari (Yoga, Zumba, CrossFit)\n"
        #         "- Shaxsiy murabbiy bilan mashg‘ulotlar (qo‘shimcha to‘lov asosida)\n"
        #         "- Sauna va dam olish zonasi\n\n"
        #         "❓ Sizni qiziqtirgan xizmat qaysi?"
        #     )
        #
        # elif any(word in user_message for word in ["murabbiy", "trainer", "coach", "jadval"]):
        #     reply = (
        #         "👨‍🏫 Murabbiylarimiz va ularning jadvali:\n"
        #         "- John Smith (Kuch va Konditsionerlik) → Dush–Juma 08:00–14:00\n"
        #         "- Anna Lee (Yoga va Pilates) → Dush–Shanba 10:00–18:00\n"
        #         "- Mike Johnson (Boks va Kardio) → Ses–Yakshanba 12:00–20:00\n\n"
        #         "👉 Qaysi murabbiy bilan shug‘ullanishni xohlaysiz? Men siz uchun bron qilishga yordam bera olaman."
        #     )
        #
        #
        # elif any(word in user_message for word in [
        #     "sen kimsan", "kim siz", "siz kimsiz",
        #     "who are you", "who are u", "sen kimsan?"]):
        #
        #     reply = (
        #         "👋 Men Logical Team Group virtual yordamchisiman.\n"
        #         "Sizga abonementlar, xizmatlar, murabbiylar, ish vaqti, bron va to‘lovlar bo‘yicha yordam bera olaman.\n"
        #         "Nimani bilmoqchisiz — narxlar, jadval yoki murabbiy haqida so‘raysizmi?"
        #     )
        #
        # elif any(word in user_message for word in ["vaqt", "ochiq", "hours", "ish vaqti"]):
        #     reply = (
        #         "🕒 Logical Team Group ish vaqti:\n"
        #         "Dushanba–Yakshanba: 09:00 – 23:00.\n\n"
        #         "👉 Siz qaysi vaqtda kelishni rejalashtiryapsiz?"
        #     )
        #
        # elif any(word in user_message for word in ["salom", "hi", "hello", "assalom", "qanday narsa bu", "vazifasi nima buni"]):
        #     reply = ("""👋 Assalamu alaykum! Men — Logical Team Group’ning virtual yordamchisiman.
        #         Sizga quyidagi savollarda yordam bera olaman:
        #         - 📋 Abonement narxlari va chegirmalar
        #         - 🏋️‍♂️ Xizmatlar va mavjud jihozlar
        #         - 👨‍🏫 Murabbiylar va mashg‘ulot jadvali
        #         - 🕒 Ish vaqti va band qilish
        #         - 📍 Manzil va kontakt ma’lumotlar
        #         - 🧒 Bolalar mashg‘ulotlari
        #         - 💳 To‘lov usullari
        #         - 🏊 Sauna, hovuz va VIP xizmatlar
        #
        #         ❓ Siz menga istalgan paytda  abonement , ** murabbiy **, ** manzil **, ** xizmat **, ** chegirma ** yoki boshqa kalit so‘zlar bilan so‘rashingiz mumkin.
        #
        #         Men sizga tez va aniq javob berishga harakat qilaman.🙂"""
        #
        #
        #     )
        #
        #
        # elif any(word in user_message for word in ["manzil", "qayerda", "address", "location", "adress", "qayer"]):
        #     reply = (
        #         "📍 Bizning manzil:\n"
        #         "Toshkent shahri, Chilonzor 18-mavze, PowerFit Plaza 2-qavat.\n\n"
        #         "🚌 Eng yaqin metro: Chilonzor\n"
        #         "🚗 Avtomobillar uchun bepul to‘xtash joyi mavjud."
        #     )
        #
        # elif any(word in user_message for word in ["kontakt", "telefon", "raqam", "aloqa", "phone", "bog'lanish", "boglanish", "kontak"]):
        #     reply = (
        #         "📞 Biz bilan bog‘lanish uchun:\n"
        #         "Telefon: +998 90 586 22 36\n"
        #         "Telegram: @logical_teams\n"
        #         "Instagram: @logical_teams"
        #     )
        #
        # elif any(word in user_message for word in ["hovuz", "sauna", "pool", "spa", "bassen"]):
        #     reply = (
        #         "🏊‍♂️ Bizda sauna va kichik suzish hovuzi mavjud.\n"
        #         "Ular faqat VIP va Yillik abonement egalari uchun bepul.\n"
        #         "Qolgan abonementlarda qo‘shimcha to‘lov asosida foydalanish mumkin."
        #     )
        #
        # elif any(word in user_message for word in ["chegirma", "aksiya", "discount", "promo"]):
        #     reply = (
        #         "🔥 Hozirgi aksiyalar:\n"
        #         "- 6 oylik abonementga 10% chegirma\n"
        #         "- Do‘stingizni olib kelsangiz, ikkingizga ham 1 hafta BEPUL mashg‘ulot\n"
        #         "- Talabalar uchun maxsus chegirma mavjud.\n\n"
        #         "❓ Sizni qaysi aksiya qiziqtiradi?"
        #     )
        #
        # elif any(word in user_message for word in ["dush", "shower", "kiyim", "garderob"]):
        #     reply = (
        #         "🚿 Ha, sport zalimizda barcha uchun dush va kiyim almashtirish xonalari mavjud.\n"
        #         "Shaxsiy shkaf (locker) ham taqdim etiladi."
        #     )
        #
        #
        # elif any(word in user_message for word in ["jihoz", "asbob", "equipment", "trenajyor"]):
        #     reply = (
        #         "🏋️ Bizning zaldagi jihozlar:\n"
        #         "- Kardio trenajyorlar (yugurish yo‘lakchasi, velotrenajyor, ellips)\n"
        #         "- Og‘ir atletika asboblari (shtanga, gantel, press stantsiya)\n"
        #         "- Maxsus CrossFit maydonchasi\n"
        #         "- Functional mashg‘ulotlar uchun jihozlar\n\n"
        #         "👉 Sizni qiziqtirgan mashq turi qaysi?"
        #     )
        #
        # elif any(word in user_message for word in ["dieta", "ovqat", "nutrition", "dietolog", "parhez"]):
        #     reply = (
        #         "🍏 PowerFit Gym’da dietolog xizmatlari mavjud.\n"
        #         "Siz uchun shaxsiy ovqatlanish rejasi tuzib beramiz.\n"
        #         "Bu xizmat VIP va Yillik abonement egalari uchun bepul, boshqalar uchun qo‘shimcha to‘lov asosida."
        #     )
        #
        # elif any(word in user_message for word in ["musobaqa", "turnir", "competition", "chempionat"]):
        #     reply = (
        #         "🏆 Har oy ichki musobaqalar o‘tkaziladi:\n"
        #         "- Powerlifting\n"
        #         "- CrossFit Challenge\n"
        #         "- Zumba Dance Battle\n\n"
        #         "🥇 G‘oliblarga sovg‘alar va bepul abonementlar taqdim etiladi!"
        #     )
        #
        # elif any(word in user_message for word in ["bola", "kids", "children", "yoshlik", "bolalar"]):
        #     reply = (
        #         "🧒 Bolalar uchun maxsus mashg‘ulotlar mavjud:\n"
        #         "- 7–12 yosh uchun gimnastika\n"
        #         "- 10–16 yosh uchun boks va karate\n"
        #         "- Fitnes mashg‘ulotlari\n\n"
        #         "Darslar maxsus murabbiylar nazorati ostida o‘tkaziladi."
        #     )
        #
        # elif any(word in user_message for word in ["to'lov","tolov", "payment", "karta", "naqd", "pul o'tkazma"]):
        #     reply = (
        #         "💳 To‘lov usullari:\n"
        #         "- Naqd pul\n"
        #         "- Plastik karta (UZCARD / HUMO / VISA / MasterCard)\n"
        #         "- Payme, Click, Apelsin\n\n"
        #         "👉 Sizga qaysi usul qulay?"
        #     )
        #
        # elif any(word in user_message for word in ["trial", "birinchi dars", "bepul dars", "sinov"]):
        #     reply = (
        #         "🎁 Siz uchun BEPUL sinov mashg‘uloti mavjud!\n"
        #         "Birinchi kelganingizda zal, murabbiy va xizmatlarimizni sinab ko‘rishingiz mumkin.\n\n"
        #         "👉 Kelishingizdan oldin ro‘yxatdan o‘tish kifoya."
        #     )
        #
        # elif any(word in user_message for word in ["bron", "band qilish", "ro'yxat", "registratsiya"]):
        #     reply = (
        #         "📝 Bron qilish juda oddiy:\n"
        #         "1️⃣ Telefon orqali yoki Telegramdan yozasiz\n"
        #         "2️⃣ Sizga mos vaqt va murabbiy tanlaymiz\n"
        #         "3️⃣ To‘lov qilgach, mashg‘ulot jadvalingiz belgilanadi"
        #     )
        #
        # elif any(word in user_message for word in ["ayol", "xotin-qiz", "women", "qizlar"]):
        #     reply = (
        #         "👩‍🦰 Bizda ayollar uchun maxsus guruh mashg‘ulotlari bor:\n"
        #         "- Yoga, Zumba, Pilates\n"
        #         "- Ayollar uchun fitnes zalida mashg‘ulotlar\n\n"
        #         "Mashg‘ulotlarni faqat ayol murabbiylar olib boradi."
        #     )
        #
        # elif any(word in user_message for word in ["vip", "premium", "lux"]):
        #     reply = (
        #         "🌟 VIP paketlarimiz quyidagilarni o‘z ichiga oladi:\n"
        #         "- Shaxsiy murabbiy\n"
        #         "- Dietolog maslahatlari\n"
        #         "- Sauna va hovuzdan bepul foydalanish\n"
        #         "- Alohida mashg‘ulot xonasi\n\n"
        #         "👉 VIP abonement haqida batafsil bilishni xohlaysizmi?"
        #     )
        #
        # elif any(word in user_message for word in ["parking", "to'xtash", "avtomobil joy"]):
        #     reply = (
        #         "🚗 Bizning sport zal yonida bepul avtoturargoh mavjud.\n"
        #         "VIP mijozlar uchun alohida yopiq parking ham mavjud."
        #     )
        #
        #
        #
        # else:
        #     reply = (
        #         """👋 Assalamu alaykum! Men — PowerFit Gym’ning virtual yordamchisiman.
        #                         Sizga faqat quyidagi savollarda yordam bera olaman:
        #                         - 📋 Abonement narxlari va chegirmalar
        #                         - 🏋️‍♂️ Xizmatlar va mavjud jihozlar
        #                         - 👨‍🏫 Murabbiylar va mashg‘ulot jadvali
        #                         - 🕒 Ish vaqti va band qilish
        #                         - 📍 Manzil va kontakt ma’lumotlar
        #                         - 🧒 Bolalar mashg‘ulotlari
        #                         - 💳 To‘lov usullari
        #                         - 🏊 Sauna, hovuz va VIP xizmatlar
        #
        #                         ❓ Siz menga istalgan paytda  abonement , ** murabbiy **, ** manzil **, ** xizmat **, ** chegirma ** yoki boshqa kalit so‘zlar bilan so‘rashingiz mumkin.
        #
        #                         Men sizga tez va aniq javob berishga harakat qilaman.🙂"""
        #
        #     )


        return Response({"reply": reply}, status=status.HTTP_200_OK)




# SYSTEM_PROMPT = """
# Siz "PowerFit Gym" sport zalining menejerisiz.
# Doim quyidagi ma’lumotlardan foydalanib javob bering:
#
# 1. Abonement rejalari:
#    - 1 oy: $50
#    - 3 oy: $120
#    - 6 oy: $200
#    - 12 oy: $350
#
# 2. Xizmatlar:
#    - Trenajyor zali va jihozlardan foydalanish
#    - Guruh mashg‘ulotlari (Yoga, Zumba, CrossFit)
#    - Shaxsiy murabbiy (qo‘shimcha to‘lov asosida)
#    - Sauna va dam olish zonasi
#
# 3. Murabbiylar:
#    - John Smith → Dush–Juma 08:00–14:00
#    - Anna Lee → Dush–Shanba 10:00–18:00
#    - Mike Johnson → Ses–Yak 12:00–20:00
#
# 4. Ish vaqti: Dush–Yak 07:00–22:00
#
# 5. Qoidalar:
#    - Murabbiy bilan mashg‘ulot oldindan bron qilinadi
#    - Guruh mashg‘ulotlarida joy cheklangan
#    - Abonement oldindan to‘lanadi
# """
#
#
#
# class GymLLMView(APIView):
#     def post(self, request):
#         user_message = request.data.get("message", "")
#
#         client = OpenAI(api_key=settings.OPENAI_API_KEY)
#
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": SYSTEM_PROMPT},
#                 {"role": "user", "content": user_message},
#             ]
#         )
#
#         reply = response.choices[0].message.content
#         return Response({"reply": reply}, status=status.HTTP_200_OK)
