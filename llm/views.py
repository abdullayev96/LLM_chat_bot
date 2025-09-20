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
👋 Salom! Men — PowerFit Gym’ning virtual yordamchisiman. 
Sizga quyidagi savollarda yordam bera olaman:
- 📋 Abonement narxlari va chegirmalar
- 🏋️‍♂️ Xizmatlar va mavjud jihozlar
- 👨‍🏫 Murabbiylar va mashg‘ulot jadvali
- 🕒 Ish vaqti va band qilish
- 📍 Manzil va kontakt ma’lumotlar
- 🧒 Bolalar mashg‘ulotlari
- 💳 To‘lov usullari
- 🏊 Sauna, hovuz va VIP xizmatlar

❓ Siz meni istalgan payt **abonement**, **murabbiy**, **manzil**, **xizmat**, **chegirma** yoki boshqa kalit so‘zlar bilan so‘rashingiz mumkin. 

Men sizga tez va aniq javob berishga harakat qilaman. 🙂
"""


class GymLLMView(APIView):
    def post(self, request):
        user_message = request.data.get("message", "").lower()

        if not user_message.strip():
            return Response(
                {"reply": "🙂 Savolingizni yozing, yordam berishga tayyorman!"},
                status=status.HTTP_200_OK,
            )

        # --- Javoblar ---
        if any(word in user_message for word in ["abonement", "narx", "price", "pul"]):
            reply = (
                "📋 Bizning abonement rejalari:\n"
                "- 1 oy: $50\n"
                "- 3 oy: $120\n"
                "- 6 oy: $200\n"
                "- 12 oy: $350\n\n"
                "👉 Qaysi reja sizga mos kelishini aytsangiz, resepsiyada band qilib beramiz."
            )

        elif any(word in user_message for word in ["xizmat", "service", "nimalar"]):
            reply = (
                "💪 Biz quyidagi xizmatlarni taklif qilamiz:\n"
                "- Trenajyor zali va jihozlardan foydalanish\n"
                "- Guruh mashg‘ulotlari (Yoga, Zumba, CrossFit)\n"
                "- Shaxsiy murabbiy bilan mashg‘ulotlar (qo‘shimcha to‘lov asosida)\n"
                "- Sauna va dam olish zonasi\n\n"
                "❓ Sizni qiziqtirgan xizmat qaysi?"
            )

        elif any(word in user_message for word in ["murabbiy", "trainer", "coach", "jadval"]):
            reply = (
                "👨‍🏫 Murabbiylarimiz va ularning jadvali:\n"
                "- John Smith (Kuch va Konditsionerlik) → Dush–Juma 08:00–14:00\n"
                "- Anna Lee (Yoga va Pilates) → Dush–Shanba 10:00–18:00\n"
                "- Mike Johnson (Boks va Kardio) → Ses–Yakshanba 12:00–20:00\n\n"
                "👉 Qaysi murabbiy bilan shug‘ullanishni xohlaysiz? Men siz uchun bron qilishga yordam bera olaman."
            )


        elif any(word in user_message for word in [
            "sen kimsan", "kim siz", "siz kimsiz",
            "who are you", "who are u", "sen kimsan?"]):

            reply = (
                "👋 Men PowerFit Gym’ning virtual yordamchisiman.\n"
                "Sizga abonementlar, xizmatlar, murabbiylar, ish vaqti, bron va to‘lovlar bo‘yicha yordam bera olaman.\n"
                "Nimani bilmoqchisiz — narxlar, jadval yoki murabbiy haqida so‘raysizmi?"
            )

        elif any(word in user_message for word in ["vaqt", "ochiq", "hours", "ish vaqti"]):
            reply = (
                "🕒 PowerFit Gym ish vaqti:\n"
                "Dushanba–Yakshanba: 07:00 – 22:00.\n\n"
                "👉 Siz qaysi vaqtda kelishni rejalashtiryapsiz?"
            )

        elif any(word in user_message for word in ["salom", "hi", "hello", "assalom"]):
            reply = (
                "👋 Assalamu alaykum! PowerFit Gym’ga xush kelibsiz.\n"
                "Siz abonement narxlari, xizmatlar, murabbiylar yoki ish vaqti haqida so‘rashingiz mumkin."
            )


        elif any(word in user_message for word in ["manzil", "qayerda", "address", "location"]):
            reply = (
                "📍 Bizning manzil:\n"
                "Toshkent shahri, Chilonzor 10-mavze, PowerFit Plaza 2-qavat.\n\n"
                "🚌 Eng yaqin metro: Chilonzor\n"
                "🚗 Avtomobillar uchun bepul to‘xtash joyi mavjud."
            )

        elif any(word in user_message for word in ["kontakt", "telefon", "raqam", "aloqa", "phone", "bog'lanish", "boglanish"]):
            reply = (
                "📞 Biz bilan bog‘lanish uchun:\n"
                "Telefon: +998 90 123 45 67\n"
                "Telegram: @PowerFitGym\n"
                "Instagram: @powerfit_gym"
            )

        elif any(word in user_message for word in ["hovuz", "sauna", "pool", "spa", "bassen"]):
            reply = (
                "🏊‍♂️ Bizda sauna va kichik suzish hovuzi mavjud.\n"
                "Ular faqat VIP va Yillik abonement egalari uchun bepul.\n"
                "Qolgan abonementlarda qo‘shimcha to‘lov asosida foydalanish mumkin."
            )

        elif any(word in user_message for word in ["chegirma", "aksiya", "discount", "promo"]):
            reply = (
                "🔥 Hozirgi aksiyalar:\n"
                "- 6 oylik abonementga 10% chegirma\n"
                "- Do‘stingizni olib kelsangiz, ikkingizga ham 1 hafta BEPUL mashg‘ulot\n"
                "- Talabalar uchun maxsus chegirma mavjud.\n\n"
                "❓ Sizni qaysi aksiya qiziqtiradi?"
            )

        elif any(word in user_message for word in ["dush", "shower", "kiyim", "garderob"]):
            reply = (
                "🚿 Ha, sport zalimizda barcha uchun dush va kiyim almashtirish xonalari mavjud.\n"
                "Shaxsiy shkaf (locker) ham taqdim etiladi."
            )


        elif any(word in user_message for word in ["jihoz", "asbob", "equipment", "trenajyor"]):
            reply = (
                "🏋️ Bizning zaldagi jihozlar:\n"
                "- Kardio trenajyorlar (yugurish yo‘lakchasi, velotrenajyor, ellips)\n"
                "- Og‘ir atletika asboblari (shtanga, gantel, press stantsiya)\n"
                "- Maxsus CrossFit maydonchasi\n"
                "- Functional mashg‘ulotlar uchun jihozlar\n\n"
                "👉 Sizni qiziqtirgan mashq turi qaysi?"
            )

        elif any(word in user_message for word in ["dieta", "ovqat", "nutrition", "dietolog", "parhez"]):
            reply = (
                "🍏 PowerFit Gym’da dietolog xizmatlari mavjud.\n"
                "Siz uchun shaxsiy ovqatlanish rejasi tuzib beramiz.\n"
                "Bu xizmat VIP va Yillik abonement egalari uchun bepul, boshqalar uchun qo‘shimcha to‘lov asosida."
            )

        elif any(word in user_message for word in ["musobaqa", "turnir", "competition", "chempionat"]):
            reply = (
                "🏆 Har oy ichki musobaqalar o‘tkaziladi:\n"
                "- Powerlifting\n"
                "- CrossFit Challenge\n"
                "- Zumba Dance Battle\n\n"
                "🥇 G‘oliblarga sovg‘alar va bepul abonementlar taqdim etiladi!"
            )

        elif any(word in user_message for word in ["bola", "kids", "children", "yoshlik", "bolalar"]):
            reply = (
                "🧒 Bolalar uchun maxsus mashg‘ulotlar mavjud:\n"
                "- 7–12 yosh uchun gimnastika\n"
                "- 10–16 yosh uchun boks va karate\n"
                "- Fitnes mashg‘ulotlari\n\n"
                "Darslar maxsus murabbiylar nazorati ostida o‘tkaziladi."
            )

        elif any(word in user_message for word in ["to'lov", "payment", "karta", "naqd", "pul o'tkazma"]):
            reply = (
                "💳 To‘lov usullari:\n"
                "- Naqd pul\n"
                "- Plastik karta (UZCARD / HUMO / VISA / MasterCard)\n"
                "- Payme, Click, Apelsin\n\n"
                "👉 Sizga qaysi usul qulay?"
            )

        elif any(word in user_message for word in ["trial", "birinchi dars", "bepul dars", "sinov"]):
            reply = (
                "🎁 Siz uchun BEPUL sinov mashg‘uloti mavjud!\n"
                "Birinchi kelganingizda zal, murabbiy va xizmatlarimizni sinab ko‘rishingiz mumkin.\n\n"
                "👉 Kelishingizdan oldin ro‘yxatdan o‘tish kifoya."
            )

        elif any(word in user_message for word in ["bron", "band qilish", "ro'yxat", "registratsiya"]):
            reply = (
                "📝 Bron qilish juda oddiy:\n"
                "1️⃣ Telefon orqali yoki Telegramdan yozasiz\n"
                "2️⃣ Sizga mos vaqt va murabbiy tanlaymiz\n"
                "3️⃣ To‘lov qilgach, mashg‘ulot jadvalingiz belgilanadi"
            )

        elif any(word in user_message for word in ["ayol", "xotin-qiz", "women", "qizlar"]):
            reply = (
                "👩‍🦰 Bizda ayollar uchun maxsus guruh mashg‘ulotlari bor:\n"
                "- Yoga, Zumba, Pilates\n"
                "- Ayollar uchun fitnes zalida mashg‘ulotlar\n\n"
                "Mashg‘ulotlarni faqat ayol murabbiylar olib boradi."
            )

        elif any(word in user_message for word in ["vip", "premium", "lux"]):
            reply = (
                "🌟 VIP paketlarimiz quyidagilarni o‘z ichiga oladi:\n"
                "- Shaxsiy murabbiy\n"
                "- Dietolog maslahatlari\n"
                "- Sauna va hovuzdan bepul foydalanish\n"
                "- Alohida mashg‘ulot xonasi\n\n"
                "👉 VIP abonement haqida batafsil bilishni xohlaysizmi?"
            )

        elif any(word in user_message for word in ["parking", "to'xtash", "avtomobil joy"]):
            reply = (
                "🚗 Bizning sport zal yonida bepul avtoturargoh mavjud.\n"
                "VIP mijozlar uchun alohida yopiq parking ham mavjud."
            )



        else:
            reply = (
                "😊 Men sizga yordam bera olaman.\n"
                "Abonement narxlari, xizmatlar, murabbiylar yoki ish vaqti haqida bilishni xohlaysizmi?"
            )

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
