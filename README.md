# Mudae AutoClaimer

<div align="center">
  <h2>Advanced Automation for Discord's Mudae Bot</h2>
  <p><i>Intelligent rolling and claiming system with Pokemon support</i></p>
  
  ![Version](https://img.shields.io/badge/Version-2.0-blue)
  ![Python](https://img.shields.io/badge/Python-3.7+-green)
  ![Framework](https://img.shields.io/badge/Framework-Nighty.one-purple)
</div>

## ⚠️ Disclaimer

This tool uses Nighty.one, a Discord self-bot framework. Self-bots violate Discord's Terms of Service. This script is provided for **educational purposes only**. Use at your own risk.

## 📖 Introduction

Mudae AutoClaimer is a sophisticated automation tool for Discord's Mudae bot. It handles character rolling, intelligent claiming based on kakera value, and provides comprehensive statistics tracking. The script includes specialized support for Pokemon rolls, wishlist prioritization, and advanced stealth features to mimic human behavior.

## ✨ Key Features

### 🤖 Core Automation System
- **Automatic Rolling**: Schedules and performs rolls at customizable intervals
- **Smart Claiming**: Evaluates characters based on kakera value and wishlist status
- **Command Rotation**: Intelligently rotates between `$wa`, `$wg`, `$mx`, and `$p` commands
- **Batch Processing**: Evaluates groups of characters before making optimal claim decisions
- **Anti-Snipe Protection**: Defensive protocol when others attempt to claim rare characters
- **Daily Command Automation**: Automatically executes `$daily`, `$dk`, and `$vote` commands

### 🎮 Pokemon Integration
- **Dedicated Pokemon Mode**: Specialized rolling with the `$p` command
- **Rare Pokemon Detection**: Automatically identifies and prioritizes legendary/mythical Pokemon
- **Pokemon-Specific Valuation**: Applies bonus values to rare Pokemon species
- **Separate Roll Sessions**: Independent Pokemon rolling schedule from regular characters
- **Pokemon Statistics Tracking**: Dedicated statistics for Pokemon collection

### 📊 Advanced Statistics
- **Claim Tracking**: Records all successful claims with timestamps and values
- **Visual Graphs**: Generates charts of daily claims and kakera earnings
- **Character Leaderboards**: Tracks most frequently claimed characters
- **Value Leaderboards**: Ranks characters by kakera value
- **Data Export**: Exports statistics to CSV format for external analysis
- **Session Statistics**: Tracks performance within active rolling sessions

### 🕵️ Stealth System
- **Human-Like Timing**: Randomized delays between actions to appear more natural
- **Activity Simulation**: Occasionally skips rolls to mimic human behavior patterns
- **Time-Based Adjustments**: Varies roll frequency based on time of day
- **Daily Limits**: Configurable maximum daily rolls to avoid detection
- **Quiet Hours**: Automatically pauses during specified hours
- **Tiered Protection**: 5 levels of stealth with increasing security measures

## 📥 Installation & Setup

1. **Install Requirements**:
   ```
   pip install nighty matplotlib
   ```

2. **Download the Script**:
   - Save `MudaeAutoClaimer.py` to your project directory

3. **Create Support Files** (Optional):
   - `wishlist.txt`: One character name per line to prioritize
   - `rare_pokemon.txt`: Additional rare Pokemon names to prioritize

4. **Set Claim Emoji**:
   - Verify the `CLAIM_EMOJI` in the config is set to the correct claim emoji (default is "❤️")
   - This must match the emoji your server uses for claiming characters
   - Common alternatives include "💖", "💝", "💞" or other heart variations

5. **Start the Script**:
   ```
   python MudaeAutoClaimer.py
   ```

6. **Initial Configuration**:
   - In Discord, navigate to your desired roll channel
   - Type `!setrollhere` to activate the auto-roller

## ⚙️ Configuration

The script uses a comprehensive configuration system at the top of the file:

```python
CONFIG = {
    # Basic Settings
    "MUDAE_NAME": "Mudae",          # Mudae bot's username
    "PREFIX": "$",                   # Command prefix
    "CLAIM_EMOJI": "❤️",             # Emoji used for claiming characters
                                     # IMPORTANT: Must match your server's claim emoji
                                     # Common alternatives: "💖", "💝", "💞", etc.
    
    # Roll Settings
    "ROLL_COMMANDS": ["$wa", "$wg", "$mx", "$p"],  # Commands to rotate
    "ROLL_INTERVAL": 120,            # Seconds between rolls
    "ROLL_WINDOW": 30,               # Seconds to evaluate batch
    "WAIT_TIME": 5,                  # Delay before claiming
    "ROLL_AMOUNT": 10,               # Characters to evaluate per batch
    "MAX_DAILY_ROLLS": 200,          # Maximum rolls per day
    
    # Value Settings
    "MIN_KAKERA": 400,               # Minimum kakera to claim
    "WISHED_BONUS": 300,             # Bonus value for wishlist characters
    
    # Pokemon Settings
    "ENABLE_POKEMON_MODE": True,     # Enable Pokemon rolling
    "POKEMON_INTERVAL": 3600,        # Seconds between Pokemon sessions
    "POKEMON_MIN_KAKERA": 350,       # Minimum kakera for Pokemon
    "POKEMON_ROLLS": 10,             # Rolls per Pokemon session
    "RARE_POKEMON_BONUS": 250,       # Bonus for rare Pokemon
    
    # Stealth Settings
    "ENABLE_RANDOM_DELAY": True,     # Add random timing variation
    "ACTIVITY_SIMULATION": True,     # Simulate human behavior patterns
    "ADVANCED_TIMING": True,         # Use time-of-day based timing
    "DISABLE_DURING_HOURS": [],      # Hours to disable rolling (e.g., [3,4,5])
    
    # Feature Toggles
    "ENABLE_ANTI_SNIPE": True,       # Enable anti-snipe protection
    "ENABLE_SMART_ROTATION": True,   # Smart command rotation
    "ENABLE_BATCH_COMMANDS": True,   # Batch roll execution
    "ENABLE_DAILY_COMMANDS": True,   # Daily command automation
    
    # Notification Settings
    "NOTIFICATIONS": {
        "DK_READY": True,            # Notify when DK is ready
        "CLAIM_SUCCESS": True,       # Notify on successful claims
        "ROLLS_COMPLETE": False      # Notify when roll batch completes
    }
}
```

## 💻 Command Reference

### Setup Commands
| Command | Description |
|---------|-------------|
| `!setrollhere` | Set current channel for auto-rolling |
| `!stoproll` | Stop auto-rolling in the current channel |
| `!status` | View current status and statistics |

### Rolling Commands
| Command | Description |
|---------|-------------|
| `!rollnow` | Execute an immediate roll batch |
| `!rollpokemon` | Execute a Pokemon roll session |
| `!pokemonmode` | Toggle Pokemon mode on/off |

### Statistics Commands
| Command | Description |
|---------|-------------|
| `!stats` | View comprehensive claim statistics and graph |
| `!kakstats` | View top kakera value characters |
| `!pokestats` | View Pokemon-specific statistics |
| `!resetstats` | Reset all statistics (with backup) |
| `!exportstats` | Export statistics to CSV file |

### Configuration Commands
| Command | Description |
|---------|-------------|
| `!setkakmin NUMBER` | Set minimum kakera threshold |
| `!setpokemoninterval MINUTES` | Set Pokemon roll interval |
| `!setmaxrolls NUMBER` | Set maximum daily rolls limit |
| `!stealth` | Toggle stealth features on/off |
| `!stealth NUMBER` | Set stealth level (1-5) |

### Wishlist Commands
| Command | Description |
|---------|-------------|
| `!wishlist` | View current wishlist |
| `!wishlist add CHARACTER` | Add character to wishlist |
| `!pokemonlist` | View rare Pokemon list |
| `!pokemonlist add POKEMON` | Add Pokemon to rare list |
| `!importwishlist FILENAME` | Import wishlist from file |

## 🕵️ Stealth System

The script includes a comprehensive stealth system with 5 configurable levels:

| Level | Features | Description |
|-------|----------|-------------|
| **1** | Basic Protection | Simple random delays between actions |
| **2** | Enhanced Timing | Random delays with activity simulation patterns |
| **3** | Advanced Algorithms | Smart timing with varied intervals based on time of day |
| **4** | High Security | Advanced timing plus automatic pausing during night hours |
| **5** | Maximum Protection | Complete suite of protection features with conservative limits |

Use `!stealth NUMBER` to set your desired stealth level.

## 📊 Statistics System

The statistics system tracks:

- **Total Claims**: Number of characters successfully claimed
- **Total Kakera**: Amount of kakera earned from all claims
- **Wish Claims**: Number of wishlist characters claimed
- **Daily Performance**: Claims and kakera per day
- **Character Frequency**: Most frequently claimed characters
- **Value Leaders**: Highest kakera value characters
- **Pokemon Stats**: Dedicated Pokemon claiming statistics

Statistics are saved to `claimed_characters.json` and automatically backed up.

## 📈 Performance Optimization

For best results:

- Set `MIN_KAKERA` appropriate to your server (400-500 recommended)
- Enable `ACTIVITY_SIMULATION` and `ADVANCED_TIMING` for better stealth
- Set reasonable daily limits with `MAX_DAILY_ROLLS` (150-200 recommended)
- Configure `DISABLE_DURING_HOURS` to pause during suspicious times
- Add your most wanted characters to the wishlist file
- Add valuable Pokemon to the rare Pokemon list

## 🔍 Troubleshooting

| Problem | Solution |
|---------|----------|
| Characters not being claimed | • Check `MIN_KAKERA` threshold<br>• **Verify `CLAIM_EMOJI` matches your server's claim emoji**<br>• Confirm the bot has permission to add reactions |
| Wrong emoji being used | • Change the `CLAIM_EMOJI` in CONFIG to match your server's claim emoji<br>• Common options: "❤️", "💖", "💝", "💞", "♥️" |
| No rolls happening | • Verify channel is set with `!setrollhere`<br>• Check `ROLL_INTERVAL` setting |
| Script crashes | • Check console for error messages<br>• Verify Mudae's embed format hasn't changed |
| Poor character selection | • Add important characters to wishlist.txt for higher priority |
| Pokemon not being recognized | • Ensure `ENABLE_POKEMON_MODE` is set to True |
| Detection concerns | • Increase stealth level with `!stealth 4` or `!stealth 5` |

## 🔄 Maintenance

- Back up your `claimed_characters.json` regularly
- Check for Mudae UI changes that might affect character detection
- Update your wishlist and rare Pokemon list as needed
- Use `!exportstats` periodically to back up your data
- Monitor console output for any warnings or errors

---

<div align="center">
  <p>Created for educational purposes only.</p>
  <p>Use responsibly and at your own risk.</p>
</div>
