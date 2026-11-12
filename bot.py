import asyncio
import os
from telethon import TelegramClient, events

API_ID = 35503944
API_HASH = "d9388f0e7c540bf9b0f92d076f5f5a9e"

client = TelegramClient('my_tasteer_bot', API_ID, API_HASH)

# متغيرات التشغيل والتحكم بالسرعة
is_foshar_running = False
delay_time = 3 
FILE_NAME = "foshar_saved.txt"

# 1. أمر عرض قائمة الأوامر مع سرعة التسطير وسورس أبو الزوز
@client.on(events.NewMessage(outgoing=True, pattern=r'\.(الاوامر|الأوامر)'))
async def help_list(event):
    help_text = f"""
🦅 **قائمة أوامر اليوزر بوت المخزنة:** 🦅

⚙️ `\.حفظ` -> (بالرد على الملف النصي) لتخزين ملف الفشار.
⚙️ `\.فشار` -> لبدء إرسال الفشار من الملف المخزن.
⚙️ `\.سرعة <الرقم>` -> لضبط وقت التسطير (من 1 إلى 20 ثانية).
⚙️ `\.ايقاف` -> لإنهاء وإيقاف الفشار فوراً.
⚙️ `\.الاوامر` -> لعرض هذه القائمة.

⏱️ **السرعة الحالية:** {delay_time} ثواني بين الرسالة والأخرى (محمي ضد الفلود).
✨ **[ سورس أبو الزوز ]** ⚙️🔥
    """
    await event.edit(help_text)

# 2. أمر حفظ الملف المرسل من التليجرام
@client.on(events.NewMessage(outgoing=True, pattern=r'\.حفظ'))
async def save_foshar_file(event):
    if not event.is_reply:
        await event.edit("⚠️ يرجى الرد على ملف الفشار النصي (.txt) واكتب `\.حفظ` لتخزينه!")
        return
    
    reply = await event.get_reply_message()
    if reply.file:
        await client.download_media(reply.media, file_name=FILE_NAME)
        await event.edit("✅ **تم تخزين مستندات الفشار بنجاح وجاهزة للاستخدام!** 📋🔥\n✨ **سورس أبو الزوز**")
    else:
        await event.edit("⚠️ الرسالة التي ردرت عليها لا تحتوي على ملف!")

# 3. أمر التحكم بالسرعة (من 1 إلى 20 ثانية)
@client.on(events.NewMessage(outgoing=True, pattern=r'\.سرعة\s+(\d+)'))
async def set_speed(event):
    global delay_time
    args = event.pattern_match.group(1)
    speed = int(args)
    
    if 1 <= speed <= 20:
        delay_time = speed
        await event.edit(f"⚡ **تم تحديث سرعة التسطير بنجاح لتصبح كل {delay_time} ثواني!** ⚙️\n✨ **سورس أبو الزوز**")
    else:
        await event.edit("⚠️ عذراً يا وحش، اختر سرعة بين **1** إلى **20** ثانية فقط لضمان حماية الفلود!")

# 4. أمر بدء الفشار من الملف المخزن مع تطبيق السرعة وحماية الفلود
@client.on(events.NewMessage(outgoing=True, pattern=r'\.فشار'))
async def start_foshar(event):
    global is_foshar_running
    
    if not os.path.exists(FILE_NAME):
        await event.edit("⚠️ لا يوجد ملف فشار مخزن! أرسل ملفاً ورد عليه بـ `\.حفظ` أولاً.")
        return

    if is_foshar_running:
        await event.edit("⚠️ الفشار شغال أساساً يا وحش!")
        return

    is_foshar_running = True
    await event.edit(f"🔥 **تم بدء إرسال الفشار (السرعة: {delay_time} ثواني)!** 🔥\n✨ **سورس أبو الزوز**")

    with open(FILE_NAME, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    while is_foshar_running:
        for line in lines:
            if not is_foshar_running:
                break
            try:
                await event.respond(line)
                await asyncio.sleep(delay_time)
            except Exception as e:
                print(f"خطأ: {e}")
                break
        await asyncio.sleep(1)

# 5. أمر إيقاف الفشار
@client.on(events.NewMessage(outgoing=True, pattern=r'\.ايقاف'))
async def stop_foshar(event):
    global is_foshar_running
    is_foshar_running = False
    await event.edit("🛑 **تم إيقاف الفشار بنجاح!** 🛑\n✨ **سورس أبو الزوز**")

print("جاري تشغيل بوت الفشار بنظام خالي من الأخطاء والتحذيرات...")
client.start()
client.run_until_disconnected()

