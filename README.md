# Mudae AutoClaimer

<div align="center">
  <h2>Advanced Automation System for Discord's Mudae Bot</h2>
  <p><i>Intelligent character rolling, claiming, and analytics with Pokemon support</i></p>
  
  ![Version](https://img.shields.io/badge/Version-2.0-blue)
  ![Python](https://img.shields.io/badge/Python-3.7+-green)
  ![Framework](https://img.shields.io/badge/Framework-Nighty.one-purple)
  ![Status](https://img.shields.io/badge/Status-Active-success)
</div>

<hr>

<div align="center">
  <h3>📋 Table of Contents</h3>
</div>

- [⚠️ Disclaimer](#%EF%B8%8F-disclaimer)
- [📖 Introduction](#-introduction)
- [✨ Key Features](#-key-features)
- [🔧 Installation](#-installation)
- [⚙️ Configuration Guide](#%EF%B8%8F-configuration-guide)
- [🚀 Getting Started](#-getting-started)
- [💻 Command Reference](#-command-reference)
- [🎯 Character Evaluation System](#-character-evaluation-system)
- [🎮 Pokemon System](#-pokemon-system)
- [🕵️ Stealth System](#%EF%B8%8F-stealth-system)
- [📊 Statistics & Analytics](#-statistics--analytics)
- [🔍 Troubleshooting](#-troubleshooting)
- [🔄 Maintenance & Best Practices](#-maintenance--best-practices)
- [📝 Advanced Tips & Techniques](#-advanced-tips--techniques)
- [❓ Frequently Asked Questions](#-frequently-asked-questions)

<hr>

## ⚠️ Disclaimer

This tool uses Nighty.one, a Discord self-bot framework. Self-bots violate Discord's Terms of Service. This script is provided for **educational purposes only**. Use at your own risk.

The authors take no responsibility for any consequences resulting from the use of this tool, including but not limited to account suspensions or bans. By using this software, you acknowledge and accept all risks associated with automation tools that interact with Discord.

<hr>

## 📖 Introduction

Mudae AutoClaimer is a sophisticated automation tool designed to enhance your experience with Discord's Mudae bot. It provides a comprehensive system for character rolling, intelligent claiming based on kakera value and wishlist status, and detailed statistical tracking of your collection.

The script's core functionality includes:

- Automated character and Pokemon rolling at customizable intervals
- Intelligent character evaluation and claiming based on multiple factors
- Wishlist prioritization for characters you specifically want
- Anti-snipe protection to secure high-value characters
- Comprehensive statistics tracking with visual graphs
- Advanced stealth features to mimic human behavior patterns

This tool is perfect for dedicated Mudae collectors looking to optimize their claiming strategy and maximize their kakera efficiency while reducing the time investment needed for manual rolling and claiming.

<hr>

## ✨ Key Features

### 🤖 Core Automation System

- **Automated Rolling**: Schedule and automate character rolls at customizable intervals
- **Smart Command Rotation**: Intelligently rotate between `$wa`, `$wg`, `$mx`, and `$p` commands
- **Batch Processing**: Collect multiple characters before making claiming decisions
- **Optimal Claiming**: Automatically react to claim the most valuable character in each batch
- **Anti-Snipe Protection**: Detect and counter attempts by others to claim rare characters
- **Daily Command Automation**: Automatically execute `$daily`, `$dk`, and `$vote` commands
- **Customizable Roll Window**: Adjust the timeframe for evaluating characters before claiming

### 🎯 Character Evaluation Engine

- **Value-Based Assessment**: Evaluate characters based on their kakera value
- **Wishlist Prioritization**: Apply bonus values to characters on your wishlist
- **Series Recognition**: Identify and track character series information
- **Character Filtering**: Skip already claimed characters automatically
- **Context-Aware Claiming**: Make intelligent claiming decisions based on multiple factors
- **Customizable Thresholds**: Set minimum kakera values for claiming consideration

### 🎮 Pokemon Specialization

- **Dedicated Pokemon Mode**: Specialized rolling with the `$p` command
- **Rare Pokemon Detection**: Identify legendary and mythical Pokemon
- **Pokemon Value Boost**: Apply bonus values to rare and valuable Pokemon
- **Pokemon-Specific Scheduling**: Independent Pokemon rolling schedule
- **Pokemon Statistics**: Track Pokemon-specific claiming metrics
- **Custom Rare List**: Maintain a custom list of valuable Pokemon to prioritize

### 📊 Comprehensive Analytics

- **Claim Tracking**: Record all successful claims with timestamps
- **Value Metrics**: Track total and average kakera values
- **Visual Graphs**: Generate charts of daily claims and kakera earnings
- **Character Frequency**: Monitor most frequently claimed characters
- **Export Capabilities**: Export statistics to CSV for external analysis
- **Session Reporting**: Generate reports on active rolling sessions

### 🕵️ Stealth Technology

- **Human Simulation**: Random delays and timing variations to mimic human behavior
- **Time-Aware Activity**: Adjust roll frequency based on time of day
- **Daily Limits**: Configurable maximum daily rolls to avoid detection
- **Quiet Hours**: Automatically pause during specified hours
- **Multiple Stealth Levels**: 5 configurable levels of increasing protection
- **Activity Patterns**: Occasional random pauses to appear more natural

<hr>

## 🔧 Installation

### Prerequisites

- Python 3.7 or higher
- Nighty.one Discord self-bot framework
- Internet connection
- Discord account with access to Mudae servers

### Step 1: Install Required Packages

```bash
# Install Nighty.one (follow instructions from their website)
pip install nighty

# Install additional dependencies
pip install matplotlib
```

### Step 2: Download the Script

Download the `MudaeAutoClaimer.py` file and save it to your preferred directory.

### Step 3: Create Support Files (Optional)

Create the following text files in the same directory as the script:

**wishlist.txt** - Add character names you want to prioritize (one per line):
```
Rem
Megumin
Asuna
Zero Two
```

**rare_pokemon.txt** - Add additional rare Pokemon (one per line):
```
Charizard
Gardevoir
Greninja
Sylveon
```

### Step 4: Configure the Script

Open `MudaeAutoClaimer.py` in a text editor and modify the CONFIG section to match your preferences. Key settings to adjust include:

- `CLAIM_EMOJI`: Set to match your server's claim emoji
- `MIN_KAKERA`: Set your minimum kakera threshold for claiming
- `ROLL_INTERVAL`: Adjust how frequently rolls occur
- `MAX_DAILY_ROLLS`: Set a safe limit for daily activity

See the [Configuration Guide](#%EF%B8%8F-configuration-guide) section for detailed information on each setting.

<hr>

## ⚙️ Configuration Guide

The script uses a comprehensive configuration system located at the top of the file. Below is a detailed explanation of each setting:

### Basic Settings

```python
"MUDAE_NAME": "Mudae"        # The username of Mudae bot in your server
                             # Change if your Mudae bot has a different name

"PREFIX": "$"                # Command prefix used by Mudae
                             # Change if your server uses a different prefix

"CLAIM_EMOJI": "❤️"          # Emoji used for claiming characters
                             # CRITICAL: Must match your server's claim emoji
                             # Common alternatives: "💖", "💝", "💞", "♥️"
```

### Roll Settings

```python
"ROLL_COMMANDS": ["$wa", "$wg", "$mx", "$p"]  # Commands to rotate through
                                              # Add/remove commands as needed

"ROLL_INTERVAL": 120         # Seconds between automatic rolls
                             # Lower = more frequent rolls, higher = less frequent
                             # Recommended: 120-180 seconds

"ROLL_WINDOW": 30            # Seconds to collect characters before claiming
                             # Higher values collect more characters per batch
                             # Recommended: 30-60 seconds

"WAIT_TIME": 5               # Delay before claiming (in seconds)
                             # Adds natural delay to appear less automated
                             # Recommended: 3-7 seconds

"ROLL_AMOUNT": 10            # Number of characters to collect before evaluation
                             # Lower values claim faster, higher values find better characters
                             # Recommended: 8-12 characters

"MAX_DAILY_ROLLS": 200       # Maximum rolls per day to avoid detection
                             # Adjust based on your risk tolerance
                             # Recommended: 150-250 rolls
```

### Value Settings

```python
"MIN_KAKERA": 400            # Minimum kakera value to consider claiming
                             # Characters below this threshold won't be claimed
                             # Adjust based on your server's economy

"WISHED_BONUS": 300          # Extra "value" added to wishlist characters
                             # Higher values prioritize wishlist over kakera value
                             # Recommended: 250-450 bonus
```

### Pokemon Settings

```python
"ENABLE_POKEMON_MODE": True  # Enable/disable dedicated Pokemon rolling
                             # Set to False to disable Pokemon features

"POKEMON_INTERVAL": 3600     # Seconds between Pokemon roll sessions
                             # Default: 1 hour (3600 seconds)

"POKEMON_MIN_KAKERA": 350    # Minimum kakera for Pokemon claiming
                             # Can be different from regular MIN_KAKERA

"POKEMON_ROLLS": 10          # Number of Pokemon rolls per session
                             # Recommended: 8-12 rolls

"RARE_POKEMON_BONUS": 250    # Bonus value for rare Pokemon
                             # Higher values increase chances of claiming rare Pokemon
```

### Stealth Settings

```python
"ENABLE_RANDOM_DELAY": True  # Add random variations to timing
                             # Highly recommended for avoiding detection

"ACTIVITY_SIMULATION": True  # Mimic human behavior patterns
                             # Occasionally skips rolls, varies timing

"ADVANCED_TIMING": True      # Adjust roll frequency based on time of day
                             # More frequent during peak hours, less during off-hours

"DISABLE_DURING_HOURS": []   # Hours to disable rolling (24-hour format)
                             # Example: [3, 4, 5] disables rolls from 3-5 AM
                             # Empty list = active all hours
```

### Feature Toggles

```python
"ENABLE_ANTI_SNIPE": True    # Enable protection against other users claiming
                             # Recommended: True

"ENABLE_SMART_ROTATION": True  # Intelligently rotate commands based on results
                               # Recommended: True

"ENABLE_BATCH_COMMANDS": True  # Execute multiple rolls in quick succession
                               # More efficient but slightly more detectable

"ENABLE_DAILY_COMMANDS": True  # Automatically use daily commands
                               # Executes $daily, $dk, and $vote automatically
```

### Notification Settings

```python
"NOTIFICATIONS": {
    "DK_READY": True,        # Notify when DK timer is ready
    "CLAIM_SUCCESS": True,   # Notify on successful claims
    "ROLLS_COMPLETE": False  # Notify when roll batch completes
}
```

<hr>

## 🚀 Getting Started

Follow these steps to start using the Mudae AutoClaimer:

### 1. Start the Script

Run the script through the Nighty.one framework:

```bash
python MudaeAutoClaimer.py
```

You should see the startup banner with your current configuration:

```
╔══════════════════════════════════════════════╗
║  MUDAE AUTO-CLAIMER v2.0 - NIGHTY.ONE READY  ║
╚══════════════════════════════════════════════╝

🔄 Roll interval: 120s | Min kakera: 400
🎮 Auto-roll: ✅ | Auto-DK: ✅
```

### 2. Set Up Your Roll Channel

In Discord, navigate to the channel where you want to roll characters. Type:

```
!setrollhere
```

You should receive a confirmation message:

```
✅ Auto-roll activated every 120s.
```

### 3. Check Status and Start Monitoring

Use the status command to verify everything is working correctly:

```
!status
```

This will show your current session statistics:

```
🔄 Auto-roll active
Session duration: 5.2 minutes
Rolls performed: 3
Characters claimed: 0
Min kakera: 400
Today's rolls: 3/200
Pokemon mode: ✅ (Next in 45.3 min)
```

### 4. Let It Run

The bot will now automatically:
- Roll characters at the configured interval
- Evaluate characters based on kakera value and wishlist status
- Claim characters that meet your criteria
- Track statistics for your review

### 5. Configure As Needed

As you use the system, you can adjust various settings with commands:

```
!setkakmin 450       # Adjust minimum kakera threshold
!pokemonmode         # Toggle Pokemon mode on/off
!stealth 3           # Set stealth level to 3
```

### 6. Monitor Progress

Periodically check your statistics to see how the system is performing:

```
!stats               # View overall statistics
!kakstats            # View top kakera claims
!pokestats           # View Pokemon statistics
```

<hr>

## 💻 Command Reference

### Setup & Control Commands

| Command | Description | Example |
|---------|-------------|---------|
| `!setrollhere` | Set current channel for auto-rolling | `!setrollhere` |
| `!stoproll` | Stop auto-rolling in the current channel | `!stoproll` |
| `!status` | View current status and statistics | `!status` |
| `!rollnow` | Execute an immediate roll batch | `!rollnow` |
| `!help` | Display available commands | `!help` |

### Statistics Commands

| Command | Description | Example |
|---------|-------------|---------|
| `!stats` | View comprehensive claim statistics and graph | `!stats` |
| `!kakstats` | View top kakera value characters | `!kakstats` |
| `!pokestats` | View Pokemon-specific statistics | `!pokestats` |
| `!resetstats` | Reset all statistics (with backup) | `!resetstats` |
| `!exportstats` | Export statistics to CSV file | `!exportstats` |

### Configuration Commands

| Command | Description | Example |
|---------|-------------|---------|
| `!setkakmin NUMBER` | Set minimum kakera threshold | `!setkakmin 450` |
| `!setpokemoninterval MINUTES` | Set Pokemon roll interval | `!setpokemoninterval 60` |
| `!setmaxrolls NUMBER` | Set maximum daily rolls limit | `!setmaxrolls 180` |
| `!stealth` | Toggle stealth features on/off | `!stealth` |
| `!stealth NUMBER` | Set stealth level (1-5) | `!stealth 3` |

### Pokemon Commands

| Command | Description | Example |
|---------|-------------|---------|
| `!pokemonmode` | Toggle Pokemon mode on/off | `!pokemonmode` |
| `!rollpokemon` | Execute a Pokemon roll session | `!rollpokemon` |
| `!pokemonlist` | View rare Pokemon list | `!pokemonlist` |
| `!pokemonlist add POKEMON` | Add Pokemon to rare list | `!pokemonlist add Greninja` |

### Wishlist Commands

| Command | Description | Example |
|---------|-------------|---------|
| `!wishlist` | View current wishlist | `!wishlist` |
| `!wishlist add CHARACTER` | Add character to wishlist | `!wishlist add Rem` |
| `!importwishlist FILENAME` | Import wishlist from file | `!importwishlist wishes.txt` |

<hr>

## 🎯 Character Evaluation System

The character evaluation system is the core of Mudae AutoClaimer's intelligence. It analyzes characters based on multiple factors to determine which ones are worth claiming.

### Evaluation Process

1. **Character Detection**:
   - Monitors Mudae embeds for character information
   - Extracts name, series, and kakera value
   - Identifies whether the character is already claimed

2. **Value Assessment**:
   - Base value from kakera amount in footer
   - Wishlist bonus applied to desired characters
   - Special bonuses for rare Pokemon
   - Rarity detection for legendary/mythical Pokemon

3. **Decision Making**:
   - Compares character value against minimum threshold
   - Prioritizes characters based on total calculated value
   - Considers wishlist status as a priority factor
   - Makes claiming decisions based on the highest value character

### Customizing Evaluation

You can customize how characters are evaluated by adjusting:

- `MIN_KAKERA`: Base threshold for consideration
- `WISHED_BONUS`: Extra value for wishlist characters
- `RARE_POKEMON_BONUS`: Extra value for rare Pokemon
- `wishlist.txt`: Characters to prioritize
- `rare_pokemon.txt`: Pokemon to prioritize

### Anti-Snipe Protection

The anti-snipe system protects valuable characters from being claimed by others:

1. Monitors chat for claiming attempts by other users
2. Immediately triggers emergency claim protocol when detected
3. Claims the best available character before it can be sniped
4. Bypasses normal waiting periods in emergency situations

<hr>

## 🎮 Pokemon System

The Pokemon system provides specialized handling for Pokemon characters rolled with the `$p` command.

### Pokemon Mode Features

- **Dedicated Rolling**: Separate roll command and schedule for Pokemon
- **Enhanced Recognition**: Detects Pokemon series and rarity levels
- **Special Valuation**: Applies bonus values to rare and legendary Pokemon
- **Optimized Timing**: Configurable intervals for Pokemon-specific rolling
- **Collection Tracking**: Specialized statistics for Pokemon collection

### Pokemon Detection Logic

The script detects Pokemon using multiple methods:

1. **Series Detection**:
   - Identifies "Pokemon" in the series name
   - Recognizes Pokemon-specific formatting in embeds

2. **Rarity Classification**:
   - Identifies legendary Pokemon from description
   - Detects mythical Pokemon from description
   - Matches against custom rare Pokemon list

3. **Value Calculation**:
   - Base kakera value from the embed
   - Bonus value for rare Pokemon list matches
   - Rarity bonuses for legendary/mythical status

### Pokemon Configuration

Customize the Pokemon system with these settings:

- `ENABLE_POKEMON_MODE`: Toggle the entire Pokemon system
- `POKEMON_INTERVAL`: How often to run Pokemon roll sessions
- `POKEMON_MIN_KAKERA`: Threshold for claiming Pokemon
- `POKEMON_ROLLS`: Number of rolls per Pokemon session
- `RARE_POKEMON_BONUS`: Value bonus for rare Pokemon
- `RARE_POKEMON`: List of valuable Pokemon to prioritize

### Pokemon Commands

- `!pokemonmode`: Toggle Pokemon mode on/off
- `!rollpokemon`: Execute an immediate Pokemon roll session
- `!pokemonlist`: View your rare Pokemon list
- `!pokemonlist add POKEMON`: Add a Pokemon to your rare list
- `!pokestats`: View Pokemon-specific statistics

<hr>

## 🕵️ Stealth System

The stealth system is designed to make the bot's behavior appear more human-like and reduce the risk of detection.

### Stealth Features

- **Random Timing**: Variable delays between actions
- **Activity Simulation**: Occasional skipped rolls and varied patterns
- **Time-Based Adjustments**: Different behavior based on time of day
- **Daily Limits**: Maximum daily roll caps to avoid suspicious activity
- **Quiet Hours**: Automatic pausing during specified hours
- **Tiered Protection**: 5 configurable levels of increasing security

### Stealth Levels

| Level | Features | Description | Detection Risk |
|-------|----------|-------------|----------------|
| **1** | Basic | Simple random delays between rolls | Moderate |
| **2** | Enhanced | Random delays + activity patterns | Low-Moderate |
| **3** | Advanced | Smart timing based on time of day | Low |
| **4** | High Security | Advanced timing + night pauses | Very Low |
| **5** | Maximum | Complete protection suite with conservative limits | Minimal |

### Configuring Stealth

You can configure the stealth system through:

1. **Static Configuration**:
   - `ENABLE_RANDOM_DELAY`: Adds variation to timing
   - `ACTIVITY_SIMULATION`: Makes behavior more human-like
   - `ADVANCED_TIMING`: Adjusts behavior based on time of day
   - `DISABLE_DURING_HOURS`: Hours to pause activity
   - `MAX_DAILY_ROLLS`: Daily roll limit to avoid detection

2. **Dynamic Configuration**:
   - `!stealth`: Toggle stealth features on/off
   - `!stealth NUMBER`: Set stealth level (1-5)

### Stealth Level Details

**Level 1: Basic Protection**
- Random delays between rolls
- Basic claim timing variation

**Level 2: Enhanced Protection**
- Random delays between rolls
- Activity simulation patterns
- Occasional skipped rolls

**Level 3: Advanced Protection**
- Smart timing based on time of day
- Variable intervals between roll sessions
- Human-like claiming behavior
- Activity patterns and simulated breaks

**Level 4: High Security**
- All Level 3 protections
- Automatic pausing during night hours (1-5 AM)
- More conservative timing patterns
- Higher variation in behavior

**Level 5: Maximum Protection**
- All Level 4 protections
- Extended night hour pausing (1-6 AM)
- Very conservative daily limits
- Maximum randomization of timing
- Extensive activity simulation

<hr>

## 📊 Statistics & Analytics

The statistics system tracks your Mudae collection progress and provides detailed analytics.

### Tracked Metrics

- **Total Claims**: Number of characters successfully claimed
- **Total Kakera**: Amount of kakera earned from claims
- **Wish Claims**: Number of wishlist characters claimed
- **Daily Metrics**: Claims and kakera per day
- **Character Frequency**: Most frequently claimed characters
- **Value Leaders**: Highest kakera value characters
- **Pokemon Stats**: Dedicated Pokemon claiming statistics
- **Session Data**: Performance within active rolling sessions

### Statistics Commands

- `!stats`: View comprehensive claim statistics and graph
- `!kakstats`: View top kakera value characters
- `!pokestats`: View Pokemon-specific statistics
- `!resetstats`: Reset all statistics (with backup)
- `!exportstats`: Export statistics to CSV file

### Data Storage

Statistics are stored in the `claimed_characters.json` file with the following structure:

```json
{
  "claims": [
    {
      "name": "Character Name",
      "value": 1250,
      "timestamp": "2023-10-25T15:30:45.123456",
      "is_wished": true,
      "series": "Series Name"
    },
    ...
  ],
  "total": 42,
  "by_name": {
    "Character Name": 3,
    ...
  },
  "by_day": {
    "2023-10-25": {
      "count": 15,
      "kakera": 12500,
      "wish_count": 3
    },
    ...
  },
  "kakera_total": 45000,
  "wish_claims": 8
}
```

### Visual Analytics

The `!stats` command generates visual graphs showing:

1. Daily claims over time (including wish claims)
2. Daily kakera earnings over time

These graphs help visualize your collection progress and identify trends in your claiming patterns.

### Data Export

The `!exportstats` command exports your statistics to a CSV file (`mudae_stats.csv`) with the following columns:

- Character Name
- Kakera Value
- Claim Date
- Wishlist Status
- Pokemon Status

This allows for external analysis in spreadsheet applications.

<hr>

## 🔍 Troubleshooting

### Common Issues

| Problem | Possible Causes | Solutions |
|---------|----------------|-----------|
| **Characters not being claimed** | • Incorrect claim emoji<br>• Kakera threshold too high<br>• Permission issues | • Check and update `CLAIM_EMOJI` to match your server<br>• Lower `MIN_KAKERA` value<br>• Verify the bot has permission to add reactions |
| **Wrong emoji being used** | • Incorrect emoji in configuration<br>• Server using custom emoji | • Update `CLAIM_EMOJI` to match server's claim emoji<br>• Try common alternatives: "❤️", "💖", "💝", "💞", "♥️" |
| **No rolls happening** | • Channel not set properly<br>• Roll interval too long<br>• Script not running | • Use `!setrollhere` in the correct channel<br>• Check `ROLL_INTERVAL` setting<br>• Verify the script is running without errors |
| **Script crashes** | • API changes in Mudae<br>• Discord rate limiting<br>• Python errors | • Check console for error messages<br>• Verify Mudae's embed format hasn't changed<br>• Use stealth settings to avoid rate limits |
| **Poor character selection** | • Low MIN_KAKERA threshold<br>• Empty wishlist<br>• Small roll window | • Increase `MIN_KAKERA` to skip low-value characters<br>• Add important characters to wishlist.txt<br>• Increase `ROLL_WINDOW` to evaluate more characters |
| **Pokemon not being recognized** | • Pokemon mode disabled<br>• Detection issues | • Enable `POKEMON_MODE` in config<br>• Verify Pokemon embeds are being detected properly |
| **Detection concerns** | • Too many rolls<br>• Predictable patterns<br>• No stealth features | • Increase stealth level with `!stealth 4` or `!stealth 5`<br>• Enable `ACTIVITY_SIMULATION`<br>• Reduce `MAX_DAILY_ROLLS` |
| **Statistics not updating** | • JSON file issues<br>• Permission problems | • Check if `claimed_characters.json` exists and is writable<br>• Verify the script has write permissions |

### Debugging Tips

1. **Check Console Output**:
   - Look for error messages in the console
   - Note any warning messages about configuration
   - Verify that rolls and claims are being logged

2. **Verify Configurations**:
   - Double-check emoji settings match your server
   - Confirm roll intervals are appropriate
   - Ensure thresholds match your server's economy

3. **Test Manually**:
   - Use `!rollnow` to test immediate rolls
   - Use `!status` to check if the channel is active
   - Watch the bot's reactions to see if claiming works

4. **Reset if Necessary**:
   - Stop the bot with `!stoproll`
   - Restart the script
   - Set up the channel again with `!setrollhere`

<hr>

## 🔄 Maintenance & Best Practices

### Regular Maintenance

- **Backup Statistics**: Regularly back up your `claimed_characters.json` file
- **Update Wishlist**: Keep your wishlist updated with desired characters
- **Monitor Performance**: Check statistics periodically to ensure optimal claiming
- **Adjust Settings**: Fine-tune configuration based on results
- **Update Script**: Check for script updates to address any Mudae changes

### Optimal Settings

- **Roll Interval**: 120-180 seconds is a good balance
- **Min Kakera**: Set based on your server's average (typically 400-600)
- **Wishlist Bonus**: 250-400 provides good prioritization
- **Roll Amount**: 8-12 characters per batch is optimal
- **Stealth Level**: 3-4 for regular use, 5 for high-security needs

### Best Practices

1. **Stay Under the Radar**:
   - Use stealth features consistently
   - Don't run 24/7 without breaks
   - Set reasonable daily limits
   - Vary your activity patterns

2. **Optimize Your Wishlist**:
   - Add high-value characters you want
   - Keep wishlist focused (50-200 characters)
   - Update as you claim wished characters

3. **Server Consideration**:
   - Be aware of server rules about automation
   - Consider using lower roll frequency in active servers
   - Avoid using in servers that actively monitor for bots

4. **Performance Optimization**:
   - Regular exports of statistics
   - Periodic script restarts
   - Adjust thresholds based on server economy
   - Monitor system resource usage

<hr>

## 📝 Advanced Tips & Techniques

### Optimizing Claim Efficiency

- Set `MIN_KAKERA` slightly above the server's average character value
- Use `WISHED_BONUS` to prioritize specific characters without losing overall value
- Adjust `ROLL_WINDOW` based on server activity (higher in active servers)
- Configure Pokemon settings separately from main settings for better specialization

### Custom Wishlists Strategy

- Focus wishlist on high-value characters first
- Add rare characters with personal value
- Group wishlist by series for better collection building
- Update wishlist regularly based on claiming patterns

### Stealth Optimization

- Use `ADVANCED_TIMING` with custom hour-based patterns
- Implement varied `DISABLE_DURING_HOURS` for different days
- Adjust stealth levels based on server activity patterns
- Use different stealth profiles for different servers

### Multi-Server Strategy

- Create separate configuration files for different servers
- Adjust thresholds based on each server's economy
- Use different wishlist priorities per server
- Customize Pokemon settings based on server collection focus

### Analytics Utilization

- Export and analyze trends in claiming patterns
- Identify optimal rolling times based on value patterns
- Adjust thresholds based on statistical analysis
- Track success rates for different configuration settings

<hr>

## ❓ Frequently Asked Questions

### General Questions

**Q: Is this against Discord's Terms of Service?**  
A: Yes, self-bots violate Discord's ToS. This script is provided for educational purposes only, and usage is at your own risk.

**Q: How many characters can I expect to claim per day?**  
A: With default settings and average luck, approximately 5-15 characters per day depending on server activity and kakera values.

**Q: Will this get my account banned?**  
A: There is always a risk when using automation tools. Using stealth features reduces risk, but cannot eliminate it entirely.

**Q: Can I run this 24/7?**  
A: While technically possible, it's not recommended. Using scheduled breaks and quiet hours creates more natural patterns.

### Technical Questions

**Q: Which claim emoji should I use?**  
A: Check your server's Mudae settings with `$setautomark`. Common options are "❤️", "💖", "💝", "💞", and "♥️".

**Q: How do I find the right MIN_KAKERA value?**  
A: Monitor characters in your server for a day, noting their kakera values. Set the threshold slightly below the average of characters you want.

**Q: Can I use this on multiple servers?**  
A: Yes, but you should run separate instances with configurations tailored to each server.

**Q: Does this work with custom Mudae prefixes?**  
A: Yes, update the `PREFIX` setting in the configuration to match your server's prefix.

### Feature Questions

**Q: Can I prioritize certain series over others?**  
A: Not directly, but you can add all characters from your favorite series to the wishlist.

**Q: Will this claim characters I already own?**  
A: No, the script detects and skips already claimed characters.

**Q: Can I use custom reaction emojis for claiming?**  
A: Yes, update the `CLAIM_EMOJI` setting to match your server's custom emoji.

**Q: How does the anti-snipe system work?**  
A: It monitors chat for claim attempts by others and triggers immediate claiming of the best available character.

<hr>

<div align="center">
  <p>Created for educational purposes only.</p>
  <p>Use responsibly and at your own risk.</p>
</div>
