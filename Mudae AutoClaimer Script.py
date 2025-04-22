from nighty import on_message, sleep, react, send, on_ready
from datetime import datetime, timedelta
import asyncio
import json
import random
import os
import matplotlib.pyplot as plt
from collections import defaultdict
import re

# ---------- CONFIGURATION ----------
CONFIG = {
    "MUDAE_NAME": "Mudae",
    "PREFIX": "$",
    "CLAIM_EMOJI": "❤️",           # Heart emoji
    "ROLL_COMMANDS": ["$wa", "$wg", "$mx", "$p"], # Multiple roll types including Pokemon
    "ROLL_INTERVAL": 120,           # Seconds between auto-rolls
    "ROLL_WINDOW": 30,              # Seconds to evaluate batch
    "WAIT_TIME": 5,                 # Delay before reacting
    "MIN_KAKERA": 400,              # Minimum kakera to consider claiming
    "AUTO_DK": True,                # Toggle DK auto-claim
    "DK_INTERVAL": 86400,           # 24 hours
    "ENABLE_RANDOM_DELAY": True,    # Adds humanlike delay before claiming
    "ENABLE_AUTO_ROLL": True,       # Toggles auto roller
    "ROLL_AMOUNT": 10,              # Number of rolls to perform before evaluation
    "LOG_FILE": "claimed_characters.json",
    "WISHED_CHARACTERS": [],        # Characters to prioritize for claims
    "WISHED_BONUS": 300,            # Extra "value" to add to wished characters
    "ENABLE_ANTI_SNIPE": True,      # Enable anti-snipe measures
    "ANTI_SNIPE_PATTERNS": [        # Patterns that might indicate someone trying to snipe
        r"\$claim",
        r"\$c\s",
        r"claim.*character", 
    ],
    "ENABLE_SMART_ROTATION": True,  # Smart command rotation
    "DISABLE_DURING_HOURS": [],     # Hours to disable autorolling (e.g. [3, 4, 5] for 3-5 AM)
    "ENABLE_DAILY_COMMANDS": True,  # Use daily commands automatically
    "DAILY_COMMANDS": ["$daily", "$dk", "$vote"],
    "NOTIFICATIONS": {
        "DK_READY": True,
        "CLAIM_SUCCESS": True,
        "ROLLS_COMPLETE": False
    },
    "ENABLE_POKEMON_MODE": True,    # Enables dedicated Pokemon rolling
    "POKEMON_INTERVAL": 3600,       # Special interval for Pokemon rolls (hourly)
    "POKEMON_MIN_KAKERA": 350,      # Minimum kakera threshold for Pokemon
    "POKEMON_ROLL_COMMAND": "$p",   # Pokemon roll command
    "POKEMON_ROLLS": 10,            # Number of Pokemon rolls per session
    "RARE_POKEMON": [               # List of rare/valuable Pokemon to prioritize
        "Mewtwo", "Mew", "Rayquaza", "Arceus", "Giratina", "Dialga", "Palkia",
        "Lugia", "Ho-Oh", "Groudon", "Kyogre", "Zekrom", "Reshiram", "Kyurem"
    ],
    "RARE_POKEMON_BONUS": 250,      # Bonus value for rare Pokemon
    "ENABLE_BATCH_COMMANDS": True,  # Enable batch command execution
    "AVOID_PATTERNS": [             # Patterns in usernames to avoid interacting with
        r"mod", r"admin", r"owner", r"bot"
    ],
    "ADVANCED_TIMING": True,        # Enable advanced timing algorithms 
    "MAX_DAILY_ROLLS": 200,         # Maximum rolls per day (to avoid detection)
    "ACTIVITY_SIMULATION": True     # Simulate human-like activity patterns
}
# ----------------------------------

embed_buffer = []
last_dk_time = None
auto_roll_channel = None
snipe_detection_timer = None
current_roll_command_index = 0
active_sessions = {}
last_rolls = {}
roll_counts = defaultdict(int)
wish_pattern = None

# Initialize log
def init_log():
    if not os.path.exists(CONFIG["LOG_FILE"]):
        with open(CONFIG["LOG_FILE"], "w") as f:
            json.dump({
                "claims": [], 
                "total": 0, 
                "by_name": {}, 
                "by_day": {},
                "kakera_total": 0,
                "wish_claims": 0
            }, f, indent=2)
    
    # Create backup file
    backup_file = CONFIG["LOG_FILE"].replace(".json", "_backup.json")
    try:
        if os.path.exists(CONFIG["LOG_FILE"]):
            with open(CONFIG["LOG_FILE"], "r") as src:
                with open(backup_file, "w") as dst:
                    dst.write(src.read())
            print(f"✅ Backup created: {backup_file}")
    except Exception as e:
        print(f"❌ Failed to create backup: {e}")

# Print startup banner
@on_ready()
async def startup():
    print("""
    ╔══════════════════════════════════════════════╗
    ║  MUDAE AUTO-CLAIMER v2.0 - NIGHTY.ONE READY  ║
    ╚══════════════════════════════════════════════╝
    """)
    print(f"🔄 Roll interval: {CONFIG['ROLL_INTERVAL']}s | Min kakera: {CONFIG['MIN_KAKERA']}")
    print(f"🎮 Auto-roll: {'✅' if CONFIG['ENABLE_AUTO_ROLL'] else '❌'} | Auto-DK: {'✅' if CONFIG['AUTO_DK'] else '❌'}")
    init_log()
    await load_wishlist()
    await load_rare_pokemon()

# Load wishlist from file if exists
async def load_wishlist():
    global wish_pattern
    try:
        if os.path.exists("wishlist.txt"):
            with open("wishlist.txt", "r") as f:
                CONFIG["WISHED_CHARACTERS"] = [line.strip() for line in f if line.strip()]
                print(f"📋 Loaded {len(CONFIG['WISHED_CHARACTERS'])} characters from wishlist")
                
                # Create regex pattern for faster matching
                if CONFIG["WISHED_CHARACTERS"]:
                    wish_pattern = re.compile('|'.join(re.escape(name) for name in CONFIG["WISHED_CHARACTERS"]), re.IGNORECASE)
    except Exception as e:
        print(f"❌ Failed to load wishlist: {e}")

# -------------------------------
# SMART CHARACTER EVALUATION
# -------------------------------
def evaluate_character(embed, message):
    character_name = embed.author.name if embed.author else "Unknown Character"
    series = None
    value = 0
    claimed_by = None
    is_wished = False
    is_claimed = False
    is_pokemon = False
    rarity = None
    is_rare_pokemon = False
    
    # Extract series from description if available
    if embed.description:
        series_match = re.search(r'\*\*(.*?)\*\*', embed.description)
        if series_match:
            series = series_match.group(1)
            
        # Check if this is a Pokemon
        if series and "pokemon" in series.lower():
            is_pokemon = True
            
            # Check for rarity indicators in Pokemon descriptions
            if "legendary" in embed.description.lower():
                rarity = "Legendary"
            elif "mythical" in embed.description.lower():
                rarity = "Mythical"
    
    # Check if character is from footer text
    if embed.footer and embed.footer.text:
        footer = embed.footer.text.lower()
        
        # Check if already claimed
        if "claimed" in footer or "belongs to" in footer:
            is_claimed = True
            claimed_match = re.search(r'(claimed by|belongs to) (.*?)( \||\.|\n|$)', footer, re.IGNORECASE)
            if claimed_match:
                claimed_by = claimed_match.group(2).strip()
        
        # Extract kakera value
        if '🔠' in footer or '💎' in footer:
            try:
                kakera_symbol = '🔠' if '🔠' in footer else '💎'
                parts = footer.split(kakera_symbol)[0].strip().split()
                value = int(parts[-1])
            except:
                value = 0
                
        # Further Pokemon detection from footer
        if "pokemon" in footer or is_pokemon:
            is_pokemon = True
    
    # Apply bonuses based on character type
    
    # Check if character is on wishlist
    if wish_pattern and character_name:
        is_wished = bool(wish_pattern.search(character_name))
        if is_wished:
            # Add bonus value to wished characters
            value += CONFIG["WISHED_BONUS"]
    
    # Check if it's a rare Pokemon
    if is_pokemon and character_name in CONFIG["RARE_POKEMON"]:
        is_rare_pokemon = True
        value += CONFIG["RARE_POKEMON_BONUS"]
        
    # Final character evaluation data
    character_data = {
        'message': message,
        'value': value,
        'name': character_name,
        'series': series,
        'timestamp': datetime.now(),
        'is_wished': is_wished,
        'is_claimed': is_claimed,
        'claimed_by': claimed_by,
        'is_pokemon': is_pokemon,
        'rarity': rarity,
        'is_rare_pokemon': is_rare_pokemon
    }
    
    # Debug log for rare finds
    if is_rare_pokemon or (is_pokemon and rarity in ["Legendary", "Mythical"]):
        print(f"🌟 RARE POKEMON DETECTED: {character_name} ({value} kakera)")
    
    return character_data

# -------------------------------
# AUTO CLAIM BEST OF BATCH ROLLS
# -------------------------------
@on_message()
async def handle_roll(message):
    global embed_buffer, snipe_detection_timer

    # Skip non-Mudae messages or messages without embeds
    if message.author.name != CONFIG["MUDAE_NAME"] or not message.embeds:
        # Check for potential sniping
        if CONFIG["ENABLE_ANTI_SNIPE"] and auto_roll_channel:
            for pattern in CONFIG["ANTI_SNIPE_PATTERNS"]:
                if re.search(pattern, message.content, re.IGNORECASE):
                    if snipe_detection_timer:
                        snipe_detection_timer.cancel()
                    
                    # Anti-snipe - quickly claim the best character
                    await anti_snipe_protocol()
                    break
        return

    embed = message.embeds[0]
    if not (embed.footer and embed.footer.text):
        return

    # Evaluate the character
    character_data = evaluate_character(embed, message)
    
    # Skip already claimed characters
    if character_data['is_claimed']:
        return
        
    embed_buffer.append(character_data)
    
    # Log for debugging
    if character_data['is_wished']:
        print(f"⭐ Wished character appeared: {character_data['name']} ({character_data['value']} kakera)")
    
    # Clean old entries from buffer
    now = datetime.now()
    embed_buffer = [e for e in embed_buffer if (now - e['timestamp']).seconds < CONFIG["ROLL_WINDOW"]]
    
    # If we've accumulated enough characters in our buffer, evaluate and claim
    if len(embed_buffer) >= CONFIG["ROLL_AMOUNT"]:
        # Cancel any existing timers
        if snipe_detection_timer:
            snipe_detection_timer.cancel()
            
        # Set a timer to claim after waiting
        snipe_detection_timer = asyncio.create_task(claim_best_character())

async def claim_best_character():
    global embed_buffer
    
    # Wait before claiming to avoid suspicion
    await sleep(CONFIG["WAIT_TIME"])
    
    eligible = [e for e in embed_buffer if e['value'] >= CONFIG["MIN_KAKERA"]]
    if not eligible:
        print("🔍 No claim-worthy characters this batch.")
        embed_buffer.clear()
        return
    
    # Sort by value and prioritize wished characters
    eligible.sort(key=lambda x: (x['value'], x['is_wished']), reverse=True)
    best = eligible[0]
    
    # Add random delay to seem more human-like
    if CONFIG["ENABLE_RANDOM_DELAY"]:
        await sleep(random.uniform(1.0, 2.5))
    
    try:
        await react(best['message'], CONFIG["CLAIM_EMOJI"])
        print(f"✅ Claimed: {best['name']} ({best['value']} kakera)" + 
              (f" - WISHED!" if best['is_wished'] else ""))
        
        log_claim(best['name'], best['value'], best['is_wished'], best.get('series'))
        
        # Notify if enabled
        if CONFIG["NOTIFICATIONS"]["CLAIM_SUCCESS"] and auto_roll_channel:
            await send(auto_roll_channel, f"💎 Claimed **{best['name']}** for {best['value']} kakera!")
    except Exception as e:
        print(f"❌ Failed to react: {e}")
    
    embed_buffer.clear()

# Emergency claim protocol when potential sniping detected
async def anti_snipe_protocol():
    global embed_buffer
    
    if not embed_buffer:
        return
        
    # Sort all characters by value regardless of kakera threshold
    embed_buffer.sort(key=lambda x: (x['is_wished'], x['value']), reverse=True)
    
    # Claim the best character immediately
    best = embed_buffer[0]
    try:
        print(f"⚠️ ANTI-SNIPE PROTOCOL: Claiming {best['name']} immediately!")
        await react(best['message'], CONFIG["CLAIM_EMOJI"])
        log_claim(best['name'], best['value'], best['is_wished'], best.get('series'))
    except Exception as e:
        print(f"❌ Anti-snipe failed: {e}")
    
    embed_buffer.clear()

# -------------------------------
# LOG CLAIMED CHARACTER
# -------------------------------
def log_claim(name, value, is_wished=False, series=None):
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")

    try:
        with open(CONFIG["LOG_FILE"], "r") as f:
            data = json.load(f)

        data["total"] += 1
        data["kakera_total"] = data.get("kakera_total", 0) + value
        
        if is_wished:
            data["wish_claims"] = data.get("wish_claims", 0) + 1
            
        claim_entry = {
            "name": name, 
            "value": value, 
            "timestamp": now.isoformat(),
            "is_wished": is_wished
        }
        
        if series:
            claim_entry["series"] = series
            
        data["claims"].append(claim_entry)
        data["by_name"][name] = data["by_name"].get(name, 0) + 1
        
        if today not in data["by_day"]:
            data["by_day"][today] = {"count": 0, "kakera": 0, "wish_count": 0}
            
        data["by_day"][today]["count"] += 1
        data["by_day"][today]["kakera"] += value
        
        if is_wished:
            data["by_day"][today]["wish_count"] = data["by_day"][today].get("wish_count", 0) + 1

        with open(CONFIG["LOG_FILE"], "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"❌ Failed to log claim: {e}")

# -------------------------------
# ENHANCED STATS WITH VISUALIZATION
# -------------------------------
@on_message()
async def handle_stats_commands(message):
    if message.author.name != "You":
        return

    if message.content.lower() == "!stats":
        await show_stats(message.channel)
    elif message.content.lower() == "!resetstats":
        await reset_stats(message.channel)
    elif message.content.lower() == "!kakstats":
        await show_kakera_stats(message.channel)
    elif message.content.lower().startswith("!setkakmin "):
        try:
            new_value = int(message.content.split(" ")[1])
            CONFIG["MIN_KAKERA"] = new_value
            await send(message.channel, f"✅ Minimum kakera threshold set to {new_value}")
        except:
            await send(message.channel, "❌ Invalid value. Use !setkakmin NUMBER")
            
async def show_stats(channel):
    try:
        with open(CONFIG["LOG_FILE"], "r") as f:
            data = json.load(f)

        total_claims = data["total"]
        total_kakera = data.get("kakera_total", 0)
        wish_claims = data.get("wish_claims", 0)
        
        top_names = sorted(data["by_name"].items(), key=lambda x: x[1], reverse=True)[:5]
        daily_data = sorted(data["by_day"].items(), reverse=True)[:7]

        stats_msg = f"\n📊 **Mudae Claim Stats**\n"
        stats_msg += f"Total Claims: {total_claims} characters\n"
        stats_msg += f"Total Kakera: {total_kakera:,} kakera\n"
        stats_msg += f"Wish Claims: {wish_claims} characters\n"
        stats_msg += f"Avg. Kakera/Claim: {total_kakera//total_claims if total_claims else 0}\n\n"
        
        stats_msg += f"**Top 5 Characters:**\n"
        for i, (name, count) in enumerate(top_names, 1):
            stats_msg += f"{i}. {name}: {count}\n"
        
        stats_msg += "\n**Last 7 Days:**\n"
        for day, values in daily_data:
            wish_str = f" ({values.get('wish_count', 0)} wished)" if values.get('wish_count', 0) > 0 else ""
            stats_msg += f"- {day}: {values['count']} claims{wish_str}, {values['kakera']:,} kakera\n"

        # Generate graph
        try:
            days = [d for d, _ in daily_data]
            days.reverse()  # Chronological order
            counts = [data["by_day"][d]["count"] for d in days]
            kakera = [data["by_day"][d]["kakera"] for d in days]
            wish_counts = [data["by_day"][d].get("wish_count", 0) for d in days]

            # Create figure with two subplots
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
            
            # Claims plot
            ax1.plot(days, counts, marker='o', linewidth=2, color='#4CAF50', label='Claims')
            ax1.plot(days, wish_counts, marker='*', linewidth=2, color='#FFC107', label='Wish Claims')
            ax1.set_title("Daily Claims")
            ax1.set_ylabel("Number of Claims")
            ax1.grid(True, alpha=0.3)
            ax1.legend()
            
            # Kakera plot
            ax2.plot(days, kakera, marker='s', linewidth=2, color='#2196F3', label='Kakera')
            ax2.set_title("Daily Kakera")
            ax2.set_xlabel("Date")
            ax2.set_ylabel("Kakera")
            ax2.grid(True, alpha=0.3)
            
            plt.tight_layout()
            plt.savefig("stats_graph.png")
            plt.close()

            await send(channel, stats_msg)
            await channel.send(file="stats_graph.png")
        except Exception as e:
            print(f"❌ Failed to generate graph: {e}")
            await send(channel, stats_msg + "\n(Unable to generate graph)")
    except Exception as e:
        print(f"❌ Failed to show stats: {e}")
        await send(channel, f"❌ Error: {e}")

async def show_kakera_stats(channel):
    try:
        with open(CONFIG["LOG_FILE"], "r") as f:
            data = json.load(f)

        # Sort claims by kakera value
        all_claims = data.get("claims", [])
        sorted_claims = sorted(all_claims, key=lambda x: x.get("value", 0), reverse=True)[:10]
        
        stats_msg = f"\n💎 **Top 10 Kakera Claims**\n"
        for i, claim in enumerate(sorted_claims, 1):
            claim_time = datetime.fromisoformat(claim["timestamp"]).strftime("%Y-%m-%d")
            wish_str = " ⭐" if claim.get("is_wished", False) else ""
            stats_msg += f"{i}. **{claim['name']}**{wish_str}: {claim['value']:,} kakera ({claim_time})\n"
        
        await send(channel, stats_msg)
    except Exception as e:
        print(f"❌ Failed to show kakera stats: {e}")
        await send(channel, f"❌ Error: {e}")

async def show_pokemon_stats(channel):
    try:
        with open(CONFIG["LOG_FILE"], "r") as f:
            data = json.load(f)

        # Filter for Pokemon claims only
        pokemon_claims = [claim for claim in data.get("claims", []) if claim.get("is_pokemon", False)]
        
        if not pokemon_claims:
            await send(channel, "🎮 No Pokemon have been claimed yet.")
            return
            
        # Count statistics
        total_pokemon = len(pokemon_claims)
        total_value = sum(claim.get("value", 0) for claim in pokemon_claims)
        avg_value = total_value // total_pokemon if total_pokemon else 0
        rare_pokemon = sum(1 for claim in pokemon_claims if claim.get("is_rare_pokemon", False))
        
        # Get top Pokemon by value
        top_pokemon = sorted(pokemon_claims, key=lambda x: x.get("value", 0), reverse=True)[:5]
        
        stats_msg = f"\n🎮 **Pokemon Claim Stats**\n"
        stats_msg += f"Total Pokemon: {total_pokemon}\n"
        stats_msg += f"Total Kakera: {total_value:,}\n"
        stats_msg += f"Avg. Kakera/Pokemon: {avg_value}\n"
        stats_msg += f"Rare Pokemon: {rare_pokemon}\n\n"
        
        stats_msg += f"**Top 5 Pokemon by Kakera:**\n"
        for i, claim in enumerate(top_pokemon, 1):
            rarity = f" ({claim.get('rarity', 'Common')})" if claim.get('rarity') else ""
            stats_msg += f"{i}. **{claim['name']}**{rarity}: {claim['value']:,} kakera\n"
            
        await send(channel, stats_msg)
    except Exception as e:
        print(f"❌ Failed to show Pokemon stats: {e}")
        await send(channel, f"❌ Error: {e}")

async def reset_stats(channel):
    try:
        # Backup old stats
        backup_file = CONFIG["LOG_FILE"].replace(".json", f"_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        if os.path.exists(CONFIG["LOG_FILE"]):
            with open(CONFIG["LOG_FILE"], "r") as src:
                with open(backup_file, "w") as dst:
                    dst.write(src.read())
        
        # Reset stats
        with open(CONFIG["LOG_FILE"], "w") as f:
            json.dump({
                "claims": [], 
                "total": 0, 
                "by_name": {}, 
                "by_day": {},
                "kakera_total": 0,
                "wish_claims": 0
            }, f, indent=2)
            
        await send(channel, f"🗑️ All stats have been reset. Backup saved to {backup_file}")
    except Exception as e:
        print(f"❌ Failed to reset stats: {e}")
        await send(channel, f"❌ Error: {e}")

# -------------------------------
# SMART DK TRACKING
# -------------------------------
@on_message()
async def track_dk(message):
    global last_dk_time

    # Check for DK claim command
    if message.author.name == "You" and f"{CONFIG['PREFIX']}dk" in message.content.lower():
        last_dk_time = datetime.now()
        await send(message.channel, "⏰ DK timer started. Will notify in 24h.")
        asyncio.create_task(dk_timer(message.channel))
    
    # Listen for Mudae's response to dk/daily commands
    if message.author.name == CONFIG["MUDAE_NAME"] and "claim" in message.content.lower():
        # Check if this is a response to a daily/dk command
        dk_keywords = ["daily", "kakera", "tower", "dk"]
        if any(kw in message.content.lower() for kw in dk_keywords):
            # Extract time until next claim if available
            time_match = re.search(r'(\d+)h\s*(\d+)m', message.content)
            if time_match:
                hours, mins = int(time_match.group(1)), int(time_match.group(2))
                seconds = (hours * 3600) + (mins * 60)
                
                if "daily" in message.content.lower():
                    print(f"✅ Daily claim detected. Next in {hours}h {mins}m")
                elif any(kw in message.content.lower() for kw in ["kakera", "tower", "dk"]):
                    print(f"✅ DK claim detected. Next in {hours}h {mins}m")
                    last_dk_time = datetime.now()
                    asyncio.create_task(dk_timer(message.channel, seconds))

async def dk_timer(channel, seconds=None):
    if seconds is None:
        seconds = CONFIG["DK_INTERVAL"]
        
    await sleep(seconds)
    
    if CONFIG["AUTO_DK"] and CONFIG["NOTIFICATIONS"]["DK_READY"]:
        await send(channel, f"{CONFIG['PREFIX']}dk")
        print("🔔 DK auto-claim executed")
    else:
        await send(channel, f"🔔 DK ready! Use `{CONFIG['PREFIX']}dk`.")

# -------------------------------
# AUTO ROLLER INIT & POKEMON ROLLING
# -------------------------------
@on_message()
async def set_auto_roll_channel(message):
    global auto_roll_channel, active_sessions

    if message.author.name != "You":
        return
        
    content = message.content.lower()
    
    if content == "!setrollhere":
        auto_roll_channel = message.channel
        await send(auto_roll_channel, f"✅ Auto-roll activated every {CONFIG['ROLL_INTERVAL']}s.")
        
        # Register this channel as an active session
        channel_id = str(message.channel.id)
        active_sessions[channel_id] = {
            "start_time": datetime.now(),
            "roll_count": 0,
            "claim_count": 0,
            "pokemon_rolls": 0,
            "pokemon_claims": 0,
            "last_pokemon_time": None,
            "daily_roll_count": 0,
            "roll_history": []
        }
        
        if CONFIG["ENABLE_AUTO_ROLL"]:
            asyncio.create_task(auto_roll_loop(channel_id))
            
            # Start Pokemon-specific roll loop if enabled
            if CONFIG["ENABLE_POKEMON_MODE"]:
                asyncio.create_task(pokemon_roll_loop(channel_id))
                print("🎮 Pokemon rolling activated")
            
    elif content == "!stoproll":
        if auto_roll_channel and auto_roll_channel.id == message.channel.id:
            channel_id = str(message.channel.id)
            if channel_id in active_sessions:
                session = active_sessions[channel_id]
                duration = (datetime.now() - session["start_time"]).total_seconds() / 60
                pokemon_stats = ""
                
                if CONFIG["ENABLE_POKEMON_MODE"] and session.get("pokemon_rolls", 0) > 0:
                    pokemon_stats = f"Pokemon rolls: {session.get('pokemon_rolls', 0)}\n"
                    pokemon_stats += f"Pokemon claimed: {session.get('pokemon_claims', 0)}\n"
                
                await send(message.channel, 
                    f"⏹️ Auto-roll stopped.\n" +
                    f"Session duration: {duration:.1f} minutes\n" +
                    f"Rolls performed: {session['roll_count']}\n" +
                    f"Characters claimed: {session['claim_count']}\n" +
                    pokemon_stats
                )
                del active_sessions[channel_id]
            
            auto_roll_channel = None
        else:
            await send(message.channel, "❌ Auto-roll was not active in this channel.")
    
    elif content == "!pokemonmode":
        if CONFIG["ENABLE_POKEMON_MODE"]:
            CONFIG["ENABLE_POKEMON_MODE"] = False
            await send(message.channel, "🎮 Pokemon mode disabled.")
        else:
            CONFIG["ENABLE_POKEMON_MODE"] = True
            await send(message.channel, f"🎮 Pokemon mode enabled! Will roll {CONFIG['POKEMON_ROLL_COMMAND']} every {CONFIG['POKEMON_INTERVAL']/3600} hours.")
            
            # If we have an active channel, start the pokemon loop
            if auto_roll_channel and str(auto_roll_channel.id) in active_sessions:
                asyncio.create_task(pokemon_roll_loop(str(auto_roll_channel.id)))
    
    elif content.startswith("!setpokemoninterval "):
        try:
            # Convert minutes to seconds
            minutes = int(content.split(" ")[1])
            CONFIG["POKEMON_INTERVAL"] = minutes * 60
            await send(message.channel, f"✅ Pokemon roll interval set to {minutes} minutes")
        except:
            await send(message.channel, "❌ Invalid value. Use !setpokemoninterval MINUTES")
            
    elif content == "!status":
        if auto_roll_channel and auto_roll_channel.id == message.channel.id:
            channel_id = str(message.channel.id)
            if channel_id in active_sessions:
                session = active_sessions[channel_id]
                duration = (datetime.now() - session["start_time"]).total_seconds() / 60
                
                # Calculate time until next Pokemon roll
                pokemon_status = ""
                if CONFIG["ENABLE_POKEMON_MODE"]:
                    last_poke_time = session.get("last_pokemon_time")
                    if last_poke_time:
                        time_since = (datetime.now() - last_poke_time).total_seconds()
                        time_until = max(0, CONFIG["POKEMON_INTERVAL"] - time_since)
                        pokemon_status = f"Pokemon mode: ✅ (Next in {time_until/60:.1f} min)\n"
                        pokemon_status += f"Pokemon rolls: {session.get('pokemon_rolls', 0)}\n"
                        pokemon_status += f"Pokemon claimed: {session.get('pokemon_claims', 0)}\n"
                    else:
                        pokemon_status = f"Pokemon mode: ✅ (Starting soon)\n"
                else:
                    pokemon_status = "Pokemon mode: ❌\n"
                
                await send(message.channel, 
                    f"🔄 Auto-roll active\n" +
                    f"Session duration: {duration:.1f} minutes\n" +
                    f"Rolls performed: {session['roll_count']}\n" +
                    f"Characters claimed: {session['claim_count']}\n" +
                    f"Min kakera: {CONFIG['MIN_KAKERA']}\n" +
                    f"Today's rolls: {session.get('daily_roll_count', 0)}/{CONFIG['MAX_DAILY_ROLLS']}\n" +
                    pokemon_status
                )
            else:
                await send(message.channel, "🔄 Auto-roll is active but no session data available.")
        else:
            await send(message.channel, "⏹️ Auto-roll is not active in this channel.")
            
    elif content.startswith("!wishlist"):
        if content == "!wishlist":
            # Show current wishlist
            if CONFIG["WISHED_CHARACTERS"]:
                wish_msg = "⭐ **Current Wishlist:**\n"
                for name in CONFIG["WISHED_CHARACTERS"][:10]:  # Show first 10
                    wish_msg += f"- {name}\n"
                    
                if len(CONFIG["WISHED_CHARACTERS"]) > 10:
                    wish_msg += f"...and {len(CONFIG['WISHED_CHARACTERS'])-10} more characters"
                    
                await send(message.channel, wish_msg)
            else:
                await send(message.channel, "⭐ Wishlist is empty. Add characters with !wishlist add CHARACTER")
        elif content.startswith("!wishlist add "):
            char_name = message.content[14:].strip()
            if char_name and char_name not in CONFIG["WISHED_CHARACTERS"]:
                CONFIG["WISHED_CHARACTERS"].append(char_name)
                await load_wishlist()  # Reload the wishlist
                await send(message.channel, f"✅ Added **{char_name}** to wishlist")
                
                # Save to file
                with open("wishlist.txt", "a") as f:
                    f.write(f"{char_name}\n")
            else:
                await send(message.channel, "❌ Character already in wishlist or invalid name")
    
    elif content.startswith("!pokemonlist"):
        if content == "!pokemonlist":
            # Show current rare Pokemon list
            if CONFIG["RARE_POKEMON"]:
                poke_msg = "🎮 **Rare Pokemon List:**\n"
                for name in CONFIG["RARE_POKEMON"][:15]:  # Show first 15
                    poke_msg += f"- {name}\n"
                    
                if len(CONFIG["RARE_POKEMON"]) > 15:
                    poke_msg += f"...and {len(CONFIG['RARE_POKEMON'])-15} more Pokemon"
                    
                await send(message.channel, poke_msg)
            else:
                await send(message.channel, "🎮 Rare Pokemon list is empty. Add Pokemon with !pokemonlist add POKEMON")
        elif content.startswith("!pokemonlist add "):
            poke_name = message.content[16:].strip()
            if poke_name and poke_name not in CONFIG["RARE_POKEMON"]:
                CONFIG["RARE_POKEMON"].append(poke_name)
                await send(message.channel, f"✅ Added **{poke_name}** to rare Pokemon list")
                
                # Save to file
                with open("rare_pokemon.txt", "a") as f:
                    f.write(f"{poke_name}\n")
            else:
                await send(message.channel, "❌ Pokemon already in list or invalid name")
    
    elif content == "!rollpokemon":
        if auto_roll_channel and auto_roll_channel.id == message.channel.id:
            await pokemon_roll_session(message.channel)
            await send(message.channel, "🎮 Pokemon roll session initiated")
        else:
            await send(message.channel, "❌ Please set a roll channel first with !setrollhere")
    
    elif content == "!pokestats":
        await show_pokemon_stats(message.channel)
    
    elif content.startswith("!setmaxrolls "):
        try:
            max_rolls = int(content.split(" ")[1])
            if max_rolls > 0:
                CONFIG["MAX_DAILY_ROLLS"] = max_rolls
                await send(message.channel, f"✅ Maximum daily rolls set to {max_rolls}")
            else:
                await send(message.channel, "❌ Value must be greater than 0")
        except:
            await send(message.channel, "❌ Invalid value. Use !setmaxrolls NUMBER")
            
    elif content == "!stealth":
        # Toggle enhanced stealth features
        if CONFIG["ACTIVITY_SIMULATION"]:
            CONFIG["ACTIVITY_SIMULATION"] = False
            CONFIG["ENABLE_RANDOM_DELAY"] = False
            await send(message.channel, "🕵️ Stealth features disabled")
        else:
            CONFIG["ACTIVITY_SIMULATION"] = True
            CONFIG["ENABLE_RANDOM_DELAY"] = True
            await send(message.channel, "🕵️ Enhanced stealth features enabled")
    
    elif content == "!help":
        help_msg = """
📋 **Mudae Bot Commands**

See commands_guide.txt for full list of commands and options.
        """
        await send(message.channel, help_msg)
        
        # Write the command guide file if it doesn't exist
        if not os.path.exists("commands_guide.txt"):
            with open("commands_guide.txt", "w") as f:
                f.write("# Mudae Bot Command Guide\n\n")
                f.write("## Auto Roll Commands\n")
                f.write("!setrollhere - Set current channel for auto-rolling\n")
                f.write("!stoproll - Stop auto-roll in current channel\n")
                f.write("!status - Check auto-roll status\n")
                f.write("!rollnow - Force an immediate roll batch\n")
                f.write("!rollpokemon - Force an immediate Pokemon roll session\n\n")
                f.write("## Stats Commands\n")
                f.write("!stats - View claim statistics\n")
                f.write("!kakstats - View top kakera claims\n")
                f.write("!pokestats - View Pokemon-specific statistics\n")
                f.write("!resetstats - Reset all statistics\n\n")
                f.write("## Configuration Commands\n")
                f.write("!setkakmin NUMBER - Set minimum kakera threshold\n")
                f.write("!wishlist - View your wishlist\n")
                f.write("!wishlist add CHARACTER - Add character to wishlist\n")
                f.write("!pokemonmode - Toggle Pokemon mode on/off\n")
                f.write("!pokemonlist - View rare Pokemon list\n")
                f.write("!pokemonlist add POKEMON - Add Pokemon to rare list\n")
                f.write("!setpokemoninterval MINUTES - Set Pokemon roll interval\n")
                f.write("!setmaxrolls NUMBER - Set maximum daily rolls limit\n\n")
                f.write("## Advanced Commands\n")
                f.write("!stealth - Toggle stealth features on/off\n")
                f.write("!exportstats - Export statistics to CSV file\n")
                f.write("!importwishlist FILENAME - Import wishlist from file\n")

# Dedicated Pokemon roll loop
async def pokemon_roll_loop(channel_id):
    while channel_id in active_sessions and CONFIG["ENABLE_POKEMON_MODE"] and auto_roll_channel:
        # Skip if we've hit the daily roll limit
        session = active_sessions[channel_id]
        if session.get("daily_roll_count", 0) >= CONFIG["MAX_DAILY_ROLLS"]:
            print(f"⚠️ Daily roll limit reached ({CONFIG['MAX_DAILY_ROLLS']}). Waiting until reset.")
            await sleep(3600)  # Check again in an hour
            continue
            
        # Record this roll session
        session["last_pokemon_time"] = datetime.now()
        
        # Execute a batch of Pokemon rolls
        await pokemon_roll_session(auto_roll_channel)
        
        # Wait until next Pokemon session with slight variation
        wait_time = CONFIG["POKEMON_INTERVAL"]
        if CONFIG["ENABLE_RANDOM_DELAY"]:
            # Add variation of ±10%
            variation = wait_time * 0.1
            wait_time += random.uniform(-variation, variation)
            
        print(f"🎮 Next Pokemon session in {wait_time/60:.1f} minutes")
        await sleep(wait_time)

# Execute a batch of Pokemon rolls
async def pokemon_roll_session(channel):
    channel_id = str(channel.id)
    if channel_id not in active_sessions:
        return
        
    session = active_sessions[channel_id]
    
    # Execute a batch of Pokemon rolls
    for _ in range(CONFIG["POKEMON_ROLLS"]):
        # Check if we've hit daily limits
        if session.get("daily_roll_count", 0) >= CONFIG["MAX_DAILY_ROLLS"]:
            print(f"⚠️ Daily roll limit reached during Pokemon session.")
            break
            
        await send(channel, CONFIG["POKEMON_ROLL_COMMAND"])
        print(f"🎮 Pokemon roll: {CONFIG['POKEMON_ROLL_COMMAND']}")
        
        # Update counters
        session["roll_count"] += 1
        session["pokemon_rolls"] = session.get("pokemon_rolls", 0) + 1
        session["daily_roll_count"] = session.get("daily_roll_count", 0) + 1
        
        # Random delay between rolls (0.8-1.5s) to seem natural
        await sleep(random.uniform(0.8, 1.5))
        
    print(f"🎮 Pokemon roll session complete ({CONFIG['POKEMON_ROLLS']} rolls)")

# -------------------------------
# ENHANCED AUTO ROLL LOOP WITH ACTIVITY SIMULATION
# -------------------------------
async def auto_roll_loop(channel_id):
    global current_roll_command_index, roll_counts
    
    while channel_id in active_sessions and auto_roll_channel:
        now = datetime.now()
        session = active_sessions[channel_id]
        
        # Reset daily roll count at midnight
        if session.get("last_day_checked", 0) != now.day:
            session["daily_roll_count"] = 0
            session["last_day_checked"] = now.day
            print(f"📅 Daily roll count reset")
        
        # Skip if we've hit the daily roll limit
        if session.get("daily_roll_count", 0) >= CONFIG["MAX_DAILY_ROLLS"]:
            print(f"⚠️ Daily roll limit reached ({CONFIG['MAX_DAILY_ROLLS']}). Waiting until reset.")
            await sleep(3600)  # Check again in an hour
            continue
        
        # Skip rolling during disabled hours
        if now.hour in CONFIG["DISABLE_DURING_HOURS"]:
            print(f"⏸️ Auto-roll paused during quiet hour: {now.hour}:00")
            await sleep(60)  # Check again in a minute
            continue
            
        # Activity simulation - randomly skip some rolls to appear more human-like
        if CONFIG["ACTIVITY_SIMULATION"] and random.random() < 0.05:  # 5% chance to skip
            print("🕵️ Activity simulation: Randomly skipping a roll")
            await sleep(random.randint(30, 120))  # Random pause between 30s-2m
            continue
            
        # Choose roll command with smart rotation
        if CONFIG["ENABLE_SMART_ROTATION"]:
            # Find command with least usage
            if sum(roll_counts.values()) > 10:
                least_used = min(CONFIG["ROLL_COMMANDS"], key=lambda cmd: roll_counts[cmd])
                roll_command = least_used
            else:
                roll_command = CONFIG["ROLL_COMMANDS"][current_roll_command_index]
                current_roll_command_index = (current_roll_command_index + 1) % len(CONFIG["ROLL_COMMANDS"])
        else:
            roll_command = CONFIG["ROLL_COMMANDS"][current_roll_command_index]
            current_roll_command_index = (current_roll_command_index + 1) % len(CONFIG["ROLL_COMMANDS"])
        
        # Skip Pokemon-specific command in regular rotation if Pokemon mode is enabled
        if CONFIG["ENABLE_POKEMON_MODE"] and roll_command == CONFIG["POKEMON_ROLL_COMMAND"]:
            roll_command = CONFIG["ROLL_COMMANDS"][0]  # Use first command instead
        
        # Execute batch rolls if enabled
        if CONFIG["ENABLE_BATCH_COMMANDS"]:
            batch_size = min(3, CONFIG["MAX_DAILY_ROLLS"] - session.get("daily_roll_count", 0))
            if batch_size > 0:
                for _ in range(batch_size):
                    await send(auto_roll_channel, roll_command)
                    print(f"🎲 Batch roll: {roll_command}")
                    
                    # Update session stats
                    session["roll_count"] += 1
                    session["daily_roll_count"] = session.get("daily_roll_count", 0) + 1
                    roll_counts[roll_command] += 1
                    
                    # Small delay between batch rolls
                    await sleep(random.uniform(0.8, 1.2))
            
                print(f"✅ Completed batch of {batch_size} rolls")
            else:
                print("⚠️ Cannot complete batch, daily limit reached")
        else:
            # Single roll
            await send(auto_roll_channel, roll_command)
            print(f"🎲 Rolled using {roll_command}")
            
            # Update session stats
            session["roll_count"] += 1
            session["daily_roll_count"] = session.get("daily_roll_count", 0) + 1
            roll_counts[roll_command] += 1
        
        # Advanced timing for more natural intervals
        if CONFIG["ADVANCED_TIMING"]:
            # Add variation based on time of day
            hour = now.hour
            
            # More frequent during peak hours, less frequent at odd hours
            base_interval = CONFIG["ROLL_INTERVAL"]
            if 8 <= hour <= 11 or 17 <= hour <= 22:  # Peak hours
                wait_time = base_interval * random.uniform(0.8, 1.1)
            elif 0 <= hour <= 6:  # Late night
                wait_time = base_interval * random.uniform(1.2, 1.5)
            else:  # Normal hours
                wait_time = base_interval * random.uniform(0.9, 1.2)
                
            # Add small random variation
            if CONFIG["ENABLE_RANDOM_DELAY"]:
                wait_time += random.uniform(-10, 10)
        else:
            # Standard timing with slight randomization
            wait_time = CONFIG["ROLL_INTERVAL"]
            if CONFIG["ENABLE_RANDOM_DELAY"]:
                wait_time += random.uniform(-5, 5)
            
        print(f"⏱️ Next roll in {wait_time:.1f} seconds")
        await sleep(wait_time)
        
        # If this channel is no longer active, exit loop
        if channel_id not in active_sessions or not auto_roll_channel:
            break
            
    print(f"🛑 Auto-roll loop ended for channel {channel_id}")

# -------------------------------
# ENHANCED CLAIM HANDLING
# -------------------------------
@on_message()
async def handle_claim_success(message):
    """Track successful claims for statistics"""
    if message.author.name != CONFIG["MUDAE_NAME"]:
        return
        
    # Look for claim confirmation messages
    if "claimed" in message.content.lower() and "successfully" in message.content.lower():
        # Extract character name if possible
        name_match = re.search(r"(?:You've? claimed|successfully claimed) \*\*([^*]+)\*\*", message.content)
        if name_match:
            character_name = name_match.group(1).strip()
            # Update session stats for the active channel
            if auto_roll_channel:
                channel_id = str(auto_roll_channel.id)
                if channel_id in active_sessions:
                    session = active_sessions[channel_id]
                    session["claim_count"] += 1
                    
                    # Check if this was a Pokemon
                    if any(pokemon.lower() in character_name.lower() for pokemon in CONFIG["RARE_POKEMON"]):
                        print(f"✅ Successfully claimed Pokemon: {character_name}")
                        session["pokemon_claims"] = session.get("pokemon_claims", 0) + 1

# -------------------------------
# DAILY COMMANDS AUTOMATION
# -------------------------------
@on_ready()
async def setup_daily_commands():
    if CONFIG["ENABLE_DAILY_COMMANDS"]:
        asyncio.create_task(daily_commands_loop())
        print("📆 Daily commands automation enabled")

async def daily_commands_loop():
    while True:
        # Run once every hour
        await sleep(3600)
        
        if not auto_roll_channel:
            continue
            
        now = datetime.now()
        
        # Run at specific hours (e.g., 8 AM)
        if now.hour == 8:
            for cmd in CONFIG["DAILY_COMMANDS"]:
                await send(auto_roll_channel, cmd)
                print(f"📆 Daily command sent: {cmd}")
                await sleep(2)  # Small delay between commands

# -------------------------------
# LOAD RARE POKEMON LIST
# -------------------------------
@on_ready()
async def load_rare_pokemon():
    try:
        if os.path.exists("rare_pokemon.txt"):
            with open("rare_pokemon.txt", "r") as f:
                custom_pokemon = [line.strip() for line in f if line.strip()]
                if custom_pokemon:
                    CONFIG["RARE_POKEMON"].extend(custom_pokemon)
                    # Remove duplicates
                    CONFIG["RARE_POKEMON"] = list(set(CONFIG["RARE_POKEMON"]))
                    print(f"🎮 Loaded {len(custom_pokemon)} custom Pokemon")
    except Exception as e:
        print(f"❌ Failed to load rare Pokemon list: {e}")

# -------------------------------
# ADDITIONAL UTILITY COMMANDS
# -------------------------------
@on_message()
async def handle_utility_commands(message):
    if message.author.name != "You":
        return
        
    content = message.content.lower()
    
    if content == "!exportstats":
        try:
            with open(CONFIG["LOG_FILE"], "r") as f:
                data = json.load(f)
                
            # Create CSV for claims
            with open("mudae_stats.csv", "w") as f:
                f.write("Name,Value,Date,Is Wished,Is Pokemon\n")
                for claim in data.get("claims", []):
                    timestamp = datetime.fromisoformat(claim["timestamp"]).strftime("%Y-%m-%d")
                    is_wished = "Yes" if claim.get("is_wished", False) else "No"
                    is_pokemon = "Yes" if claim.get("is_pokemon", False) else "No"
                    f.write(f"{claim['name']},{claim['value']},{timestamp},{is_wished},{is_pokemon}\n")
                    
            await send(message.channel, "📊 Statistics exported to mudae_stats.csv")
        except Exception as e:
            print(f"❌ Failed to export stats: {e}")
            await send(message.channel, f"❌ Error exporting stats: {e}")
            
    elif content.startswith("!importwishlist "):
        try:
            filename = content.split(" ")[1].strip()
            count = 0
            with open(filename, "r") as f:
                for line in f:
                    name = line.strip()
                    if name and name not in CONFIG["WISHED_CHARACTERS"]:
                        CONFIG["WISHED_CHARACTERS"].append(name)
                        count += 1
                        
            await load_wishlist()  # Reload wishlist with pattern matching
            await send(message.channel, f"✅ Imported {count} characters to wishlist")
        except Exception as e:
            await send(message.channel, f"❌ Error importing wishlist: {e}")
    
    elif content == "!rollnow":
        if auto_roll_channel and auto_roll_channel.id == message.channel.id:
            # Execute immediate roll batch
            for _ in range(5):  # Do 5 rolls
                roll_command = random.choice(CONFIG["ROLL_COMMANDS"])
                await send(auto_roll_channel, roll_command)
                await sleep(random.uniform(1.0, 1.5))
            await send(message.channel, "✅ Immediate roll batch completed")
        else:
            await send(message.channel, "❌ Please set a roll channel first with !setrollhere")
