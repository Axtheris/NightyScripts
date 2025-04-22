# 🎮 Mudae AutoClaimer v2.0

<p align="center">
Advanced automation script for Discord's Mudae bot with character and Pokemon claiming
</p>

## ⚠️ Disclaimer

This script uses Nighty.one, a Discord self-bot framework. Self-bots violate Discord's Terms of Service. Use at your own risk. This script is provided for educational purposes only.

## ✨ Features

The Mudae AutoClaimer includes the following features:

### Core Features
- Automatic character rolling with customizable intervals
- Smart character claiming based on kakera value
- Wishlist priority system for desired characters  
- Command rotation between $wa, $wg, $mx, and $p
- Anti-snipe protection to counter claim attempts
- DK/Daily command automation

### Pokemon Features
- Dedicated Pokemon rolling using $p command
- Rare Pokemon detection and priority claiming
- Separate Pokemon roll sessions and statistics

### Stealth & Security
- Human-like activity simulation
- Randomized timing between rolls
- Configurable daily roll limits
- Scheduled pausing during specific hours
- Multiple stealth levels (1-5)

### Statistics & Data
- Comprehensive claim statistics tracking
- Visual graphs for daily claims and kakera
- Exportable data in CSV format
- Character and Pokemon leaderboards

## 🔧 Configuration

The script uses the CONFIG section at the top of the file. Key settings include:

```python
CONFIG = {
    "MUDAE_NAME": "Mudae",          # Mudae bot's username
    "PREFIX": "$",                   # Command prefix
    "CLAIM_EMOJI": "❤️",             # Emoji used for claiming
    "ROLL_COMMANDS": ["$wa", "$wg", "$mx", "$p"], # Commands to use
    "ROLL_INTERVAL": 120,            # Seconds between rolls
    "MIN_KAKERA": 400,               # Minimum kakera to claim
    "ENABLE_POKEMON_MODE": True,     # Use Pokemon mode
    "POKEMON_INTERVAL": 3600,        # Pokemon roll interval (seconds)
    "POKEMON_MIN_KAKERA": 350,       # Minimum for Pokemon claims
    "MAX_DAILY_ROLLS": 200,          # Maximum rolls per day
    "DISABLE_DURING_HOURS": [],      # Hours to pause rolling
    "ACTIVITY_SIMULATION": True      # Simulate human behavior
}
```

## 📋 Usage

1. Install Nighty.one framework for Discord
2. Save the script as `MudaeAutoClaimer.py`
3. Create optional files:
   - `wishlist.txt` - One character name per line
   - `rare_pokemon.txt` - One Pokemon name per line
4. Start the script through Nighty.one
5. In Discord, use `!setrollhere` to begin auto-rolling

## 🤖 Commands

| Category | Commands |
|----------|----------|
| **Setup** | `!setrollhere` `!stoproll` `!status` |
| **Rolling** | `!rollnow` `!rollpokemon` `!pokemonmode` |
| **Stats** | `!stats` `!kakstats` `!pokestats` `!resetstats` |
| **Config** | `!setkakmin` `!wishlist` `!pokemonlist` `!setpokemoninterval` `!setmaxrolls` |
| **Wishlist** | `!wishlist add CHARACTER` `!pokemonlist add POKEMON` |
| **Advanced** | `!stealth` `!exportstats` `!importwishlist` |

## 🕵️ Stealth Levels

The script includes configurable stealth levels to reduce detection risk:

- **Level 1**: Basic random delays
- **Level 2**: Random delays + activity patterns
- **Level 3**: Advanced timing + varied intervals
- **Level 4**: Advanced timing + night pauses
- **Level 5**: Maximum protection with conservative limits

## 🔍 Troubleshooting

- If claims aren't working, verify your `MIN_KAKERA` setting
- If the bot isn't detecting characters, ensure Mudae's embed format hasn't changed
- Use `!status` to check if the bot is active and properly configured
- Review console output for any error messages

## 📊 Statistics

The script automatically tracks:
- Total claims and kakera earned
- Wish claims and Pokemon claims
- Daily performance metrics
- Top claimed characters
- Top kakera value characters

Use `!stats`, `!kakstats`, and `!pokestats` to view your statistics.
