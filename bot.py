import os
import logging
import random
import sys
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
BOT_TOKEN = os.environ.get('BOT_TOKEN')

if not BOT_TOKEN:
    error_msg = """
❌ ERROR: BOT_TOKEN environment variable not set!

Please add it in Railway:
1. Go to your Railway project dashboard
2. Click on the "Variables" tab
3. Click "Add Variable"
4. Enter: BOT_TOKEN = your_token_from_botfather
5. Click "Deploy" to redeploy

For local testing:
Create a .env file with:
BOT_TOKEN=your_token_here
"""
    print(error_msg)
    logger.error("BOT_TOKEN environment variable not set!")
    sys.exit(1)

# Get optional environment variables
BOT_NAME = os.environ.get('BOT_NAME', 'Coffee Lover Bot')
BOT_OWNER = os.environ.get('BOT_OWNER', 'Unknown')

print(f"✅ Bot Token loaded successfully!")
print(f"🤖 Bot Name: {BOT_NAME}")
print(f"📱 Username: @coffee_lover298_bot")
print(f"👤 Owner: {BOT_OWNER}")

# Coffee data
COFFEE_QUOTES = [
    "☕ Life begins after coffee!",
    "☕ Coffee: because adulting is hard!",
    "☕ Rise and grind!",
    "☕ Coffee is my love language!",
    "☕ First coffee, then everything else!",
    "☕ Espresso yourself!",
    "☕ Coffee: the best part of waking up!",
    "☕ Keep calm and drink coffee!",
    "☕ I run on coffee and code!",
    "☕ Coffee: liquid motivation!",
    "☕ A yawn is just a silent scream for coffee!",
    "☕ Coffee is always a good idea!",
    "☕ But first, coffee!",
    "☕ Coffee: the official drink of productivity!",
    "☕ Life is too short for bad coffee!"
]

COFFEE_TYPES = [
    {"name": "Espresso", "emoji": "☕", "price": "$3.00", "description": "Strong and bold"},
    {"name": "Americano", "emoji": "☕", "price": "$3.50", "description": "Smooth and mellow"},
    {"name": "Cappuccino", "emoji": "☕", "price": "$4.00", "description": "Foamy and creamy"},
    {"name": "Latte", "emoji": "☕", "price": "$4.50", "description": "Milky and smooth"},
    {"name": "Mocha", "emoji": "☕", "price": "$4.75", "description": "Chocolatey delight"},
    {"name": "Macchiato", "emoji": "☕", "price": "$4.25", "description": "Bold with a hint of milk"},
    {"name": "Flat White", "emoji": "☕", "price": "$4.25", "description": "Silky and rich"},
    {"name": "Cold Brew", "emoji": "❄️", "price": "$4.50", "description": "Smooth and refreshing"},
    {"name": "Iced Coffee", "emoji": "🧊", "price": "$4.00", "description": "Cool and invigorating"},
    {"name": "Frappuccino", "emoji": "🍹", "price": "$5.00", "description": "Blended perfection"},
    {"name": "Turkish Coffee", "emoji": "🇹🇷", "price": "$4.00", "description": "Traditional and strong"},
    {"name": "Irish Coffee", "emoji": "🇮🇪", "price": "$6.00", "description": "Whiskey-infused warmth"}
]

BREWING_GUIDES = {
    'espresso': """
☕ **How to Brew Espresso:**

📋 **Ingredients:**
• Fresh coffee beans
• Filtered water

🔧 **Equipment:**
• Espresso machine or Moka pot
• Grinder

👨‍🍳 **Steps:**
1. Grind beans to fine consistency
2. Tamp 18-20g into portafilter
3. Extract for 25-30 seconds
4. Should yield 1-2 oz

💡 **Pro Tip:** 
Best served immediately with a glass of water!
""",
    'americano': """
☕ **How to Brew Americano:**

📋 **Ingredients:**
• Fresh espresso
• Hot water

👨‍🍳 **Steps:**
1. Pull a fresh espresso shot
2. Add hot water (1:2 ratio)
3. Adjust strength to taste

💡 **Pro Tip:**
Pour water first, then espresso to preserve the crema!
""",
    'cappuccino': """
☕ **How to Brew Cappuccino:**

📋 **Ingredients:**
• Fresh espresso
• Whole milk

👨‍🍳 **Steps:**
1. Pull a fresh espresso shot
2. Steam milk until foamy
3. Pour milk (1/3 espresso, 1/3 milk, 1/3 foam)
4. Dust with cocoa powder

💡 **Pro Tip:**
Use whole milk for the best foam!
""",
    'latte': """
☕ **How to Brew Latte:**

📋 **Ingredients:**
• Fresh espresso
• Milk

👨‍🍳 **Steps:**
1. Pull a fresh espresso shot
2. Steam milk until silky
3. Pour milk over espresso (1:3 ratio)
4. Top with a thin layer of foam

💡 **Pro Tip:**
Add flavored syrups for variety!
""",
    'cold_brew': """
❄️ **How to Brew Cold Brew:**

📋 **Ingredients:**
• Coarse ground coffee
• Cold water

👨‍🍳 **Steps:**
1. Mix coffee with water (1:4 ratio)
2. Steep for 12-24 hours
3. Filter using a fine mesh
4. Serve over ice

💡 **Pro Tip:**
Cold brew stays fresh for up to 2 weeks!
""",
    'mocha': """
☕ **How to Brew Mocha:**

📋 **Ingredients:**
• Fresh espresso
• Chocolate syrup
• Steamed milk
• Whipped cream

👨‍🍳 **Steps:**
1. Add chocolate syrup to cup
2. Pour espresso over chocolate
3. Add steamed milk
4. Top with whipped cream

💡 **Pro Tip:**
Use dark chocolate for richer flavor!
""",
    'turkish': """
🇹🇷 **How to Brew Turkish Coffee:**

📋 **Ingredients:**
• Finely ground coffee
• Water
• Sugar (optional)

👨‍🍳 **Steps:**
1. Add coffee and sugar to cezve
2. Add cold water
3. Heat slowly until foaming
4. Pour into small cups

💡 **Pro Tip:**
Let grounds settle before drinking!
"""
}

COFFEE_FACTS = [
    "🌍 Coffee is the second most traded commodity in the world, after oil!",
    "📜 The word 'coffee' comes from the Arabic word 'qahwah'!",
    "🍒 Coffee beans are actually seeds from a fruit called a coffee cherry!",
    "🇧🇷 Brazil produces about one-third of all coffee in the world!",
    "🇪🇹 Coffee was originally discovered in Ethiopia!",
    "🏛️ The first coffeehouse opened in Constantinople in 1475!",
    "🧠 Coffee can improve cognitive function and memory!",
    "⚡ Decaf coffee still contains small amounts of caffeine!",
    "💪 Coffee is a natural source of antioxidants!",
    "🇫🇮 Finland consumes more coffee per capita than any other country!",
    "🎵 Beethoven was a coffee lover and used exactly 60 beans per cup!",
    "💻 Coffee is the fuel of programmers worldwide!",
    "🌱 Coffee plants can live up to 100 years!",
    "☕ The world's most expensive coffee costs over $600 per pound!",
    "🧊 Cold brew coffee has 67% less acid than hot coffee!"
]

# -------------------- COMMAND HANDLERS --------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message with coffee theme."""
    user = update.effective_user
    current_time = datetime.now().strftime("%I:%M %p")
    
    # Greeting based on time of day
    hour = datetime.now().hour
    if 5 <= hour < 12:
        time_greeting = "Good Morning! 🌅"
    elif 12 <= hour < 17:
        time_greeting = "Good Afternoon! ☀️"
    elif 17 <= hour < 21:
        time_greeting = "Good Evening! 🌅"
    else:
        time_greeting = "Late night coffee craving? 🌙"
    
    welcome_text = f"""
☕ **Welcome to Coffee Lover Bot!** ☕

{time_greeting}
Hello **{user.first_name}**! 👋

I'm your ultimate coffee companion! Here's what I can do:

**☕ Available Commands:**
/start - Show this welcome message
/help - Show all commands  
/coffee - Get a random coffee recommendation
/quote - Get a motivational coffee quote
/menu - See full coffee menu with prices
/brew <type> - Get brewing instructions
/facts - Interesting coffee facts
/fact - Random coffee trivia
/feedback <message> - Send feedback
/about - About this bot

**🎯 Quick Actions:**
Click the buttons below to explore!
"""
    
    keyboard = [
        [
            InlineKeyboardButton("☕ Random Coffee", callback_data='coffee'),
            InlineKeyboardButton("💬 Coffee Quote", callback_data='quote')
        ],
        [
            InlineKeyboardButton("📋 Full Menu", callback_data='menu'),
            InlineKeyboardButton("💡 Coffee Fact", callback_data='fact')
        ],
        [
            InlineKeyboardButton("📖 Brew Guide", callback_data='brew_guide'),
            InlineKeyboardButton("ℹ️ About", callback_data='about')
        ],
        [
            InlineKeyboardButton("🆘 Help", callback_data='help')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help menu with all commands."""
    help_text = """
☕ **Coffee Lover Bot Help**

Here's everything I can do for you:

**☕ Coffee Commands:**
• `/coffee` - Get a random coffee recommendation
• `/quote` - Get a motivational coffee quote  
• `/menu` - Browse full coffee menu with prices
• `/brew <type>` - Get brewing instructions
• `/facts` - List all coffee facts
• `/fact` - Random coffee fact

**ℹ️ General Commands:**
• `/start` - Show welcome message
• `/help` - Show this help menu
• `/about` - About this bot
• `/feedback <message>` - Send feedback

**💡 Quick Tips:**
• Click the buttons below messages for quick actions
• Coffee makes everything better! ☕
• Your data is private and secure

**🔄 Status:** 🟢 Online
**📱 Bot:** @coffee_lover298_bot

**☕ Brewing Guide Tips:**
Use `/brew espresso` for espresso instructions
Try: espresso, americano, cappuccino, latte, cold_brew, mocha, turkish
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """About information."""
    about_text = """
☕ **About @coffee_lover298_bot**

**☕ Project:** Coffee Lover Bot
**📌 Version:** 2.0.0
**👨‍💻 Created by:** Coffee Enthusiast

**🎯 Purpose:**
Your ultimate coffee companion! Whether you're a coffee connoisseur or just starting your coffee journey, I'm here to help!

**☕ Features:**
• Random coffee recommendations
• Coffee quotes & motivation
• Full coffee menu with prices
• Brewing instructions
• Coffee facts & trivia
• Interactive buttons
• 24/7 availability

**🛠️ Tech Stack:**
• Python 3.9+
• python-telegram-bot v20+
• Railway (Hosting)
• GitHub (Version Control)

**📊 Statistics:**
• Serving coffee lovers worldwide
• 12+ coffee types available
• 15+ coffee facts
• 10+ brewing guides

☕ **Keep calm and drink coffee!**
"""
    await update.message.reply_text(about_text, parse_mode='Markdown', disable_web_page_preview=True)

async def coffee_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recommend a random coffee."""
    coffee = random.choice(COFFEE_TYPES)
    quote = random.choice(COFFEE_QUOTES)
    
    coffee_text = f"""
☕ **Today's Coffee Recommendation:**

**{coffee['emoji']} {coffee['name']}**
💰 {coffee['price']}
📝 {coffee['description']}

{quote}

💡 **Did you know?**
Type `/brew {coffee['name'].lower()}` to learn how to make it!
"""
    await update.message.reply_text(coffee_text, parse_mode='Markdown')

async def quote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random coffee quote."""
    quote = random.choice(COFFEE_QUOTES)
    quote_text = f"""
💬 **Coffee Quote of the Day:**

*"{quote}"*

☕ Share this with someone who needs coffee!

#CoffeeLover #CoffeeQuotes ☕
"""
    await update.message.reply_text(quote_text, parse_mode='Markdown')

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show full coffee menu."""
    hot_coffees = [c for c in COFFEE_TYPES if c['emoji'] not in ['❄️', '🧊', '🍹']]
    cold_coffees = [c for c in COFFEE_TYPES if c['emoji'] in ['❄️', '🧊', '🍹']]
    specialty = [c for c in COFFEE_TYPES if c['name'] in ['Turkish Coffee', 'Irish Coffee']]
    
    menu_text = """
☕ **Coffee Lover's Full Menu** ☕

**☕ Hot Coffees:**
"""
    
    for coffee in hot_coffees:
        if coffee['name'] not in ['Turkish Coffee', 'Irish Coffee']:
            menu_text += f"• {coffee['emoji']} {coffee['name']:15} {coffee['price']:>8}\n"
    
    menu_text += "\n**❄️ Cold Coffees:**\n"
    for coffee in cold_coffees:
        menu_text += f"• {coffee['emoji']} {coffee['name']:15} {coffee['price']:>8}\n"
    
    menu_text += "\n**🌟 Specialty Coffees:**\n"
    for coffee in specialty:
        menu_text += f"• {coffee['emoji']} {coffee['name']:15} {coffee['price']:>8}\n"
    
    menu_text += """
**🍰 Food Items:**
• 🥐 Croissant ............ $3.00
• 🧁 Muffin .............. $3.50
• 🍰 Cake Slice ........... $4.00
• 🍪 Cookie .............. $2.50

**🍵 Other Drinks:**
• 🫖 Chai Latte ........... $4.00
• 🍵 Matcha Latte ......... $4.50
• 🍫 Hot Chocolate ........ $3.75
• 🍃 Green Tea ........... $2.50

💡 *Prices may vary by location*
☕ *Freshly brewed daily!*
"""
    await update.message.reply_text(menu_text, parse_mode='Markdown')

async def brew_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Provide brewing instructions."""
    if not context.args:
        brew_keyboard = [
            [
                InlineKeyboardButton("☕ Espresso", callback_data='brew_espresso'),
                InlineKeyboardButton("☕ Americano", callback_data='brew_americano')
            ],
            [
                InlineKeyboardButton("☕ Cappuccino", callback_data='brew_cappuccino'),
                InlineKeyboardButton("☕ Latte", callback_data='brew_latte')
            ],
            [
                InlineKeyboardButton("☕ Mocha", callback_data='brew_mocha'),
                InlineKeyboardButton("❄️ Cold Brew", callback_data='brew_cold_brew')
            ],
            [
                InlineKeyboardButton("🇹🇷 Turkish Coffee", callback_data='brew_turkish')
            ]
        ]
        reply_markup = InlineKeyboardMarkup(brew_keyboard)
        
        await update.message.reply_text(
            "☕ **Brewing Guide**\n\n"
            "Please select a coffee type below or type:\n"
            "`/brew <coffee_type>`\n\n"
            "Available types: espresso, americano, cappuccino, latte, cold_brew, mocha, turkish",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        return
    
    coffee_type = context.args[0].lower()
    instructions = BREWING_GUIDES.get(coffee_type)
    
    if instructions:
        await update.message.reply_text(instructions, parse_mode='Markdown')
    else:
        await update.message.reply_text(
            "❌ Coffee type not found!\n\n"
            "Try one of these:\n"
            "• espresso\n"
            "• americano\n"
            "• cappuccino\n"
            "• latte\n"
            "• cold_brew\n"
            "• mocha\n"
            "• turkish"
        )

async def facts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all coffee facts."""
    facts_text = "☕ **15 Coffee Facts You Need to Know!**\n\n"
    for i, fact in enumerate(COFFEE_FACTS, 1):
        facts_text += f"{i}. {fact}\n\n"
    
    # Split if too long
    if len(facts_text) > 4000:
        await update.message.reply_text(
            "☕ **Coffee Facts (Part 1)**\n\n" + 
            "\n".join(COFFEE_FACTS[:8])
        )
        await update.message.reply_text(
            "☕ **Coffee Facts (Part 2)**\n\n" + 
            "\n".join(COFFEE_FACTS[8:])
        )
    else:
        await update.message.reply_text(facts_text, parse_mode='Markdown')

async def fact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random coffee fact."""
    fact = random.choice(COFFEE_FACTS)
    await update.message.reply_text(f"☕ **Coffee Fact:**\n\n{fact}", parse_mode='Markdown')

async def feedback_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user feedback."""
    if not context.args:
        await update.message.reply_text(
            "📝 **Send Feedback**\n\n"
            "I'd love to hear from you!\n"
            "Usage: `/feedback Your message here`\n\n"
            "Examples:\n"
            "• `/feedback This bot is amazing!`\n"
            "• `/feedback Add more coffee types`"
        )
        return
    
    feedback = ' '.join(context.args)
    user = update.effective_user
    
    # Log feedback
    logger.info(f"Feedback from {user.username or user.first_name}: {feedback}")
    
    await update.message.reply_text(
        f"✅ **Thank you for your feedback!**\n\n"
        f"📝 Your message:\n*{feedback[:200]}*\n\n"
        "We appreciate your input! ☕\n"
        f"Here's a coffee quote: {random.choice(COFFEE_QUOTES)}",
        parse_mode='Markdown'
    )

async def handle_unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle unknown commands."""
    await update.message.reply_text(
        "❌ I don't understand that command.\n"
        "Type /help to see available commands.\n\n"
        "☕ Here's a coffee quote to cheer you up:\n"
        f"*{random.choice(COFFEE_QUOTES)}*",
        parse_mode='Markdown'
    )

# -------------------- CALLBACK QUERY HANDLERS --------------------

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses."""
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    
    # Coffee recommendation
    if callback_data == 'coffee':
        coffee = random.choice(COFFEE_TYPES)
        response = f"☕ **Coffee Recommendation:**\n\n**{coffee['emoji']} {coffee['name']}**\n💰 {coffee['price']}\n📝 {coffee['description']}\n\n{random.choice(COFFEE_QUOTES)}"
    
    # Quote
    elif callback_data == 'quote':
        response = f"💬 **Coffee Quote:**\n\n*{random.choice(COFFEE_QUOTES)}*"
    
    # Menu
    elif callback_data == 'menu':
        response = "☕ **Full Menu:**\n\nType /menu to see our complete menu with all items and prices! 📋"
    
    # Fact
    elif callback_data == 'fact':
        response = f"☕ **Coffee Fact:**\n\n{random.choice(COFFEE_FACTS)}"
    
    # Brew guide
    elif callback_data == 'brew_guide':
        response = "☕ **Brewing Guides:**\n\nType /brew to see all available brewing instructions!\n\nTry: `/brew espresso`, `/brew latte`, etc."
    
    # Specific brew guides
    elif callback_data.startswith('brew_'):
        coffee_type = callback_data.replace('brew_', '')
        instructions = BREWING_GUIDES.get(coffee_type)
        if instructions:
            response = instructions
        else:
            response = "❌ Brew guide not found!"
    
    # About
    elif callback_data == 'about':
        response = "ℹ️ **About:**\n\nType /about to learn more about me and my features!"
    
    # Help
    elif callback_data == 'help':
        response = "🆘 **Help:**\n\nType /help to see all available commands and features."
    
    else:
        response = "☕ Something went wrong! Try again."
    
    await query.edit_message_text(response, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular text messages."""
    text = update.message.text.lower()
    
    # Coffee-related keywords
    coffee_keywords = ['coffee', 'espresso', 'latte', 'cappuccino', 'mocha', 'brew', 'caffeine']
    
    if any(keyword in text for keyword in coffee_keywords):
        response = f"☕ {random.choice(COFFEE_QUOTES)}\n\nTry /coffee for a recommendation or /menu to see our menu!"
    elif text in ['hello', 'hi', 'hey', 'hola']:
        response = f"👋 Hello! Want some coffee? ☕\n{random.choice(COFFEE_QUOTES)}"
    elif 'thank' in text or 'thanks' in text:
        response = f"You're welcome! Enjoy your coffee! ☕\n\n{random.choice(COFFEE_QUOTES)}"
    elif 'love' in text or 'like' in text:
        response = f"☕ I love coffee too! Here's a quote for you:\n\n*{random.choice(COFFEE_QUOTES)}*"
    elif '?' in text:
        response = f"🤔 Good question! Try /help or ask me about coffee!\n\n{random.choice(COFFEE_QUOTES)}"
    else:
        response = f"☕ I'm a coffee bot! Try /coffee or /menu\n\n*{random.choice(COFFEE_QUOTES)}*"
    
    await update.message.reply_text(response, parse_mode='Markdown')

# -------------------- ERROR HANDLER --------------------

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors."""
    logger.error(f"Update {update} caused error {context.error}")
    
    # Send a message to the user
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ Oops! Something went wrong. Please try again later.\n"
            "☕ Have a coffee while I fix this!"
        )

# -------------------- MAIN FUNCTION --------------------

def main():
    """Start the bot."""
    print("=" * 50)
    print("☕ Coffee Lover Bot is starting...")
    print(f"🤖 Bot: @coffee_lover298_bot")
    print(f"🔄 Status: Online")
    print(f"📱 Check it out: https://t.me/coffee_lover298_bot")
    print("=" * 50)
    
    try:
        # Create the Application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("about", about_command))
        application.add_handler(CommandHandler("coffee", coffee_command))
        application.add_handler(CommandHandler("quote", quote_command))
        application.add_handler(CommandHandler("menu", menu_command))
        application.add_handler(CommandHandler("brew", brew_command))
        application.add_handler(CommandHandler("facts", facts_command))
        application.add_handler(CommandHandler("fact", fact_command))
        application.add_handler(CommandHandler("feedback", feedback_command))
        
        # Add callback query handler for buttons
        application.add_handler(CallbackQueryHandler(button_callback))
        
        # Add handler for messages
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Add handler for unknown commands
        application.add_handler(MessageHandler(filters.COMMAND, handle_unknown))
        
        # Add error handler
        application.add_error_handler(error_handler)
        
        # Start the Bot
        print("☕ Bot is now running and ready for commands!")
        print("=" * 50)
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        logger.error(f"Error starting bot: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
