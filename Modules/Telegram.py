import os

from dotenv import load_dotenv
from telegram import InputFile, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import Google
import ip
import number
import preview
import protonmail
import Social_media_analyzer as sma

load_dotenv()
Token = os.getenv("tele_token")
bot_username = os.getenv("b_name")

file_path = ""

url = ""


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """Welcome to OXINT Bot! 🌐🔍

Your ultimate tool for automated OSINT and investigations. From cybersecurity to corporate security, we’ve got you covered.

🛠️ Key Features:

    Automated Data Collection
    Advanced Data Analysis
    User-Friendly Interface
    Scalable Integration

Empower your intelligence gathering with OXINT! 🚀"""
    )


async def name_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """Kindly provide name in the format 'name:firstname lastname' \nCan also provide identifying keywords with it as 'name:firstname lastname keyword: identification' \nReturn: Social media profiles, online presence, images, etc"""
    )


async def number_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Kindly provide number in the format 'number:XXXXXXXXXX'\nReturn:Carrier lookup, Location"
    )


async def ip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Kindly provide ip in the format 'ip:XXX.XXX.XX.XX'\nReturn: Reverse DNS, ISP, organization, location"
    )


async def pm_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kindly provide protonmail in the format 'protonmail: mail@proton.com'\nReturn: Date of creation, encryption standard")  # type: ignore[attr-defined]


async def handle_response(
    text: str, update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    keyword = ""
    text = text.lower()
    if "hello" in text:
        return "How are you"

    if "name:" in text:
        name = text.strip().replace("name:", "").strip()
        print(name)
        if "keyword:" in text:
            phrases = name.strip().split("keyword:")
            print(phrases)
            keyword = phrases[1].strip()
            name = phrases[0].strip()
            print(name, keyword)
        print("successfully captured")
        # Await ox_name correctly here
        return await ox_name(name, keyword, update, context)  # Pass update and context

    if "number" in text:
        num = int(text.strip().replace("number:", "").strip())
        print("number found", num, type(num))
        return await ox_number(num, update, context)
    if "ip:" in text:
        ipaddr = text.strip().replace("ip:", "").strip()
        return await ox_ip(ipaddr, update, context)

    if "protonmail" in text:
        mail = text.strip().replace("protonmail:", "").strip()
        return await ox_pm(update, context, mail)
    return "I don’t understand"


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type
    text = update.message.text

    print(f'User {update.message.chat.id} in {message_type}: "{text}"')

    if message_type == "supergroup":
        if context.bot.username.lower() in text.lower():
            new_text = text.replace(context.bot.username, "").strip()
            print(new_text)
            print("hello")
            # Await handle_response correctly here
            response = await handle_response(new_text, update, context)
            print("Bot: ", response)
            await update.message.reply_text(response)
        else:
            return
    else:
        # Await handle_response correctly here
        response = await handle_response(text, update, context)
        print("Bot: ", response)
        await update.message.reply_text(response)


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Assuming you want to handle images received from users
    photo_file = await update.message.photo[
        -1
    ].get_file()  # Get the highest resolution photo
    file_path = f"../{photo_file.file_id}.jpg"  # Adjust path as needed
    await photo_file.download_to_drive(file_path)

    print(f"Downloaded image to {file_path}")

    await update.message.reply_text("Image received!")
    await send_local_image(
        update, context, file_path, url_var=False
    )  # Send the received image


async def send_local_image(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    file_path: str,
    url_var: bool,
    capt="",
):
    chat_id = update.message.chat.id
    try:
        if url_var:
            await context.bot.send_photo(chat_id=chat_id, photo=file_path, caption=capt)
        else:
            await context.bot.send_photo(
                chat_id=chat_id, photo=open(file_path, "rb"), caption=capt
            )
        print("Image sent successfully!")
    except Exception as e:
        print(f"Error sending image: {e}")


async def ox_name(
    name: str, keyword: str, update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    print("Function called")
    dorks = Google.Dork(
        name, keyword, False
    )  # Assuming Google and sma are defined elsewhere
    print("Dork done")
    # print(dorks)
    sm_profiles, sm_posts = sma.classify(dorks[0])
    content = {}
    # print(sm_profiles)
    ##    for j in sm_profiles:
    ##      if j == "facebook":
    ##    for i in sm_profiles[j]:
    ##    print(i)
    ## path = preview.facebook_crawl(i)
    ## content = sma.facebook_extractor(i)
    ##sm_profiles.update(content)
    activity = dorks[2]
    documents = dorks[3]
    images = dorks[4]
    for i in images:
        try:
            await send_message(update, context, img=True, file_path=i, url_var=True)
        except:
            pass

    await send_message(
        update, context, message="Personal Profiles profiles:", img=False
    )
    for j in sm_profiles:
        for i in sm_profiles[j]:
            if j == "facebook":
                pass
                ##   await send_local_image(update, context, path, False, f"{j}: {i}")
            else:
                await send_message(update, context, message=f"{j}: {i}")
    await send_message(update, context, message="Social media activity:", img=False)
    for i in sm_posts:
        await send_message(update, context, message=i)
    await send_message(update, context, message="Online Presence:")
    for i in activity:
        await send_message(update, context, message=i)
    await send_message(update, context, message="Important Documents:")
    for i in documents:
        await send_message(update, context, message=i)
    for j in sm_profiles:
        if j == "phonenum":
            for i in sm_profiles[j]:
                await send_message(
                    update, context, "Phone Number Found, Starting Analysis"
                )
            if i[0] == "0":
                i = i[1:]
            await ox_number(eval(i.replace(" ", "")), update, context)
    sma.search_results = []
    sma.instagram = []
    sma.facebook = []
    sma.linkedin = []
    sma.twitter = []
    sma.email = []
    sma.phonenum = []
    sma.external_link = []
    sma.bio = []
    sma.content = []
    return "OSINT DONE"


async def send_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    message="",
    img=False,
    file_path="",
    url_var=False,
):
    chat_id = update.message.chat.id

    if not (img):
        await update.message.reply_text(message)
    else:
        print("image function called")
        await send_local_image(
            update, context, file_path, url_var, capt=f"Source: {file_path}"
        )


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")


async def ox_number(num, update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("function called")
    result_dict = number.find_trace(num)
    print(result_dict)
    if result_dict:
        print("found")
        for key, value in result_dict.items():
            await send_message(update, context, f"{key}: {value}")
        return "Number Osint Done"
    return "No details found"


async def ox_ip(ipaddr, update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = ip.ipinfo(ipaddr)
    for i in result[0]:
        if i == "data":
            pass
        else:
            await send_message(update, context, f"{i}:{result[0][i]}")
    for i in result[1]:
        await send_message(update, context, f"{i}:{result[1][i]}")
    return "IP OSINT DONE"


async def ox_pm(update: Update, context: ContextTypes.DEFAULT_TYPE, mail):
    result = protonmail.check_email(mail)

    for i in result:
        await send_message(update, context, i)
    return "Proton mail osint done"


if __name__ == "__main__":
    print("starting")
    app = Application.builder().token(Token).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("name", name_command))
    app.add_handler(CommandHandler("number", number_command))
    app.add_handler(CommandHandler("ip", ip_command))
    app.add_handler(CommandHandler("protonmail", pm_command))
    # app.add_handler(CommandHandler('sendimage', send_local_image))  # Command to send local image
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    print("polling")
    app.run_polling(poll_interval=3)
